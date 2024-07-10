from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
import openai
import getpass

# Key to use OpenAI APIs
openai.api_key = getpass.getpass("OpenAI API Key:")

# Add data to user profile
def add_data(index, storage_context, dir = ""):
    
    documents = None
    # If directory provided read data from directory
    if dir != "":
        documents = SimpleDirectoryReader(dir).load_data();
    else:
        print("\nChoose the type of data you want to add:")
        print("1. WebPage")
        print("2. Local Document")
        
        choice = input("Enter your choice (1-2): ").strip()
        
        if choice == '1':
            # Read data from web page
            url = input("\nEnter the URL for the webpage: ")
            documents = SimpleWebPageReader(html_to_text=True).load_data([url])
        elif choice == '2':
            # Read data from directory
            dir = input("\nEnter the directory address: ")
            documents = SimpleDirectoryReader(dir).load_data();
        else:
            print("Invalid choice. Please enter either 1 or 2.")
        
    # Split data into chunks and create nodes from them
    text_splitter = SentenceSplitter(chunk_size=200, chunk_overlap=10)
    nodes = text_splitter.get_nodes_from_documents(documents=documents)
    
    # If index hasn't been created yet, create it with given nodes, storage_context and OpenAIEmbedding. If already created, insert nodes into the VectorStoreIndex.
    if index is None:
        index = VectorStoreIndex(nodes=nodes, storage_context=storage_context, embed_model=OpenAIEmbedding())
    else:
        index.insert_nodes(nodes)
    print("\nThe data was added.")
    return index


def update_data(chroma_collection):
    # Data to be updated
    old_data = input("\nEnter a part of the data that needs to be updated: ")
    new_data = ""
    
    print("\nChoose method of entering new data:")
    print("1. Type manually")
    print("2. Local Document")
    choice = input("Enter your choice (1-2): ").strip()
        
    if choice == '1':
        new_data = input("\nEnter the new data: ")
    elif choice == '2':
        dir = input("\nEnter the document address: ")
        file = open(dir, "r")
        new_data = file.read()
    else:
        print("Invalid choice. Please enter either 1 or 2.")
       
    # Query for the document that needs to be updated
    doc_to_update = chroma_collection.get(where_document = { "$contains": old_data })
    # Get embeddings for the new data
    embed_model = OpenAIEmbedding()
    new_embed = embed_model.get_text_embedding(new_data)
    # Update data in the user's collection
    chroma_collection.update(ids=[doc_to_update["ids"][0]], embeddings=[new_embed], documents=[new_data])
    print("\nThe data was updated.")
    
def delete_data(chroma_collection):
    # Data to be deleted
    data = input("\nEnter a part of the data that needs to be delete: ")
    # Dlete data from the user's collection
    chroma_collection.delete(where_document = { "$contains": data })
    print("\nThe data was deleted.")

def talk_to_perch(user, index, vector_store, storage_context):
    # If index doesn't exist, create it.
    if index is None:
        index = VectorStoreIndex.from_vector_store(vector_store, embed_model=OpenAIEmbedding())
    # Create chat engine from the index
    chat_engine = index.as_chat_engine(chat_mode="condense_question")
    
    print(f"\nHi {user}, I am Perch! Your personalized chat assistant. Enter your question to chat or type Bye to go to the previous menu:\n")
    # Store current chat history
    cur_chat_history = ""
    while True:
        question = input("Q: ")
        if question == "Bye":
            break
        cur_chat_history += "Q: " + question + "\n"
        # Query the chat engine
        response = chat_engine.chat(question)
        print("A: " + response.response)
        cur_chat_history += "A: " + response.response + "\n"
    
    dir = "data/chat_history"
    with open(dir + "/cur_chat_history.txt", "w", encoding='utf-8') as text_file:
        text_file.write(cur_chat_history)
    # Add curent chat history to the user's collection
    idx = add_data(index, storage_context, dir)
    
def chatbot(user, chroma_collection, vector_store, storage_context):
    Settings.llm = OpenAI(model="gpt-3.5-turbo")
    index = None
    print(f"\nHello {user}!")
    while True:
        print("\nWelcome to your personalized chatbot. Enter your choice:")
        print("1. Talk to Perch")
        print("2. Upload data")
        print("3. Update data")
        print("4. Delete data")
        print("5. Log out")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            talk_to_perch(user, index, vector_store, storage_context)
        elif choice == '2':
            index = add_data(index, storage_context)
        elif choice == '3':
            update_data(chroma_collection)
        elif choice == '4':
            delete_data(chroma_collection)
        elif choice == '5':
            print(f"Logging out. Bye {user}!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")