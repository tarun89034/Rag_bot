from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a retrieval-based document analysis assistant.

Answer questions strictly using the retrieved document context.
If the answer is not present in the context, clearly state that it is not found.
Never hallucinate or fabricate information.

---

Context:
{context}

Question:
{question}

---

Answer:
"""
)

def get_llm_chain(retriever):
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant"
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever
