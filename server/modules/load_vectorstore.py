import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "medical-index"

UPLOAD_DIR = "./uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)

# Only create if the index doesn't already exist (never delete existing data)
existing_indexes = [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,
        metric="dotproduct",
        spec=spec
    )

    while True:
        idx = pc.describe_index(PINECONE_INDEX_NAME)
        if idx and idx.status.get("ready"):
            break
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)

def load_vectorstore(uploaded_files):
    embed_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    file_paths = []

    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadatas = [
            {
                "text": chunk.page_content,
                **chunk.metadata
            }
            for chunk in chunks
        ]

        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        print(f"Embedding {len(texts)} chunks...")
        embeddings = embed_model.embed_documents(texts)

        print("Uploading to Pinecone...")
        with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
            vectors = list(zip(ids, embeddings, metadatas))
            index.upsert(vectors=vectors)
            progress.update(len(embeddings))

        print(f"Upload complete for {file_path}")
