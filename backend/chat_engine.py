import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# backend -> clinic-ai-agent -> rag -> faiss_index
PROJECT_ROOT = Path(__file__).resolve().parent.parent
VECTOR_DB_PATH = PROJECT_ROOT / "rag" / "faiss_index"

vector_db = FAISS.load_local(
    str(VECTOR_DB_PATH),
    embeddings,
    allow_dangerous_deserialization=True
)

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


def retrieve_context(question: str):

    docs = vector_db.similarity_search(
        question,
        k=4
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return context


def generate_answer(question: str):

    context = retrieve_context(question)

    prompt = f"""
You are an AI assistant for Clinikk Healthcare.

Answer Only using the supplied context.

If the answer is unavailable,
say:

"I couldn't find that information on the clinic website."

Never invent facts.

Context:

{context}

Question:

{question}
"""

    response = llm.invoke(prompt)

    return response.content