import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

CHROMA_PATH = "rag_store"
DOCS_PATH = "documents"


def load_all_documents():
    docs = []
    for filename in os.listdir(DOCS_PATH):
        if filename.endswith(".txt"):  # Only support .txt for now
            filepath = os.path.join(DOCS_PATH, filename)
            print(f"📄 Loading: {filename}")
            loader = TextLoader(filepath)
            docs.extend(loader.load())
    return docs


def embed_documents(docs):
    print("🔪 Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    split_docs = splitter.split_documents(docs)

    print("🧠 Embedding and saving to Chroma...")
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(
        split_docs, embedding, persist_directory=CHROMA_PATH)
    db.persist()
    print("✅ RAG store built and saved.")


def get_vectorstore():
    if not os.path.exists(CHROMA_PATH):
        print("❌ No RAG store found.")
        return None
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)


def retrieve_context(query, k=3):
    db = get_vectorstore()
    if not db:
        return ""
    results = db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in results])
