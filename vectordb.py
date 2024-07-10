from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core import StorageContext


# Chroma DB database file path
DATABASE_PATH = "./chroma_db"
# Database client
db_client = chromadb.PersistentClient(path=DATABASE_PATH)

# Get (if exists) or create (if doesn't exist) user's personalized chat chistory from chroma db
def get_or_create_chat_histry(collection_name):
    chroma_collection = db_client.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return chroma_collection, vector_store, storage_context