from fastapi import FastAPI,UploadFile,File,Form,Request,HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from modules.load_vectorstore import load_vectorstore, index as pinecone_index
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from logger import logger
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import Field
import os
import shutil

app=FastAPI(title="RagBot2.0")

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize embedding model once at startup (not per request)
embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

class SimpleRetriever(BaseRetriever):
    """A simple retriever that returns pre-fetched documents."""
    docs: List[Document] = Field(default_factory=list)

    def _get_relevant_documents(self, query: str, run_manager=None) -> List[Document]:
        return self.docs

@app.middleware("http")
async def catch_exception_middleware(request:Request,call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION")
        return JSONResponse(status_code=500,content={"error":str(e)})

# Upload single file to server (bypasses Streamlit's _stcore)
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        filename = file.filename or "unknown.pdf"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": "File uploaded", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload_pdfs/")
async def upload_pdfs(files:List[UploadFile]=File(...)):
    try:
        logger.info(f"recieved {len(files)} files")
        load_vectorstore(files)
        logger.info("documents added to pinecone")
        return {"message":"Files processed and vectorstore updated"}
    except Exception as e:
        logger.exception("Error during pdf upload")
        return JSONResponse(status_code=500,content={"error":str(e)})

# Upload from URL (bypasses Streamlit's _stcore entirely)
@app.post("/upload_from_url/")
async def upload_from_url(request: Request):
    try:
        body = await request.json()
        url = body.get("url")
        if not url:
            return JSONResponse(status_code=400, content={"error": "No URL provided"})
        
        # Download file from URL
        import httpx
        response = httpx.get(url, timeout=30)
        if response.status_code != 200:
            return JSONResponse(status_code=400, content={"error": f"Failed to download: {response.status_code}"})
        
        # Extract filename from URL
        filename = url.split("/")[-1] or "document.pdf"
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(response.content)
        
        # Process the file
        from pathlib import Path
        from modules.pdf_handlers import process_pdf
        
        # Create a simple file-like object
        class FileObj:
            def __init__(self, name, content):
                self.filename = name
                self.file = __import__('io').BytesIO(content)
        
        files = [FileObj(filename, response.content)]
        load_vectorstore(files)
        
        return {"message": f"File {filename} processed successfully"}
    except Exception as e:
        logger.exception("Error during URL upload")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"user query: {question}")

        embedded_query = embed_model.embed_query(question)
        res = pinecone_index.query(vector=embedded_query, top_k=3, include_metadata=True)

        docs = [
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
            ) for match in res["matches"]
        ]

        retriever = SimpleRetriever(docs=docs)
        chain, retriever_obj = get_llm_chain(retriever)
        result = query_chain(chain, retriever_obj, question)

        logger.info("query successful")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/test")
async def test():
    return {"message":"Testing successfull..."}
