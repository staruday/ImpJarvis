# from modules.rag_engine import load_all_documents, embed_documents

# docs = load_all_documents()
# embed_documents(docs)
from modules.rag_engine import retrieve_context

while True:

    query = input("\n❓ Ask something (or type 'exit'): ")
    if query.lower() == "exit":
        break

    context = retrieve_context(query, k=3)
    print("\n📚 Retrieved Context:")
    print("-" * 60)
    print(context if context else "⚠️ No relevant content found.")
