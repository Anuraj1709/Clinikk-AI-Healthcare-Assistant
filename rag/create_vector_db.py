from pathlib import Path
import os

from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found!")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_PATH = PROJECT_ROOT / "knowledge"

VECTOR_DB_PATH = Path(__file__).parent / "faiss_index"


print("\nLoading documents...\n")

loader = DirectoryLoader(
    str(KNOWLEDGE_PATH),
    glob="*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)

documents = loader.load()

print(f"Loaded {len(documents)} files")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")


print("\nGenerating embeddings...\n")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


print("\nCreating FAISS Vector Store...\n")

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

VECTOR_DB_PATH.mkdir(exist_ok=True)

vectorstore.save_local(str(VECTOR_DB_PATH))

print("\nDone!\n")

print(f"Vector DB saved to:\n{VECTOR_DB_PATH}")