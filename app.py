from models import User, Session, engine
from vectordb import get_or_create_chat_histry
from perch import chatbot
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

def create_profile():
    # Create a db session
    session = Session()

    # Getting user data
    print("Creating a new user account...")
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    email = input("Enter your email address: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    collection_name = username + "_chat_history"
    
    # Hashing the password before storing
    hashed_pwd = generate_password_hash(password)
    
    # Creating user object with given data
    user = User(name=name, age=age, email=email, username=username, password=hashed_pwd, collection_name=collection_name)
    # Verifying credentials and creating account
    try:
        session.add(user)
        session.commit()
        print(f"Account created successfully for {name}.")
    except IntegrityError:
        session.rollback()
        print("Email / Username already exists. Please try with different credentials.")


def login_user():
    # Create a db session
    session = Session()
    try:
        # Getting user credentials
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        # Querying user data
        user = session.query(User).filter_by(username=username).first()
        
        # verifying hashed password
        if check_password_hash(user.password, password):
            print("Login successful!")
            # Creating or retrieving user personalized chat history from chromadb
            chroma_collection, vector_store, storage_context = get_or_create_chat_histry(user.collection_name)
            # Starting user's personaized chatbot
            chatbot(user.name, chroma_collection, vector_store, storage_context)
        else:
            print("Incorrect password. Please try again.")
    
    except NoResultFound:
        print("Username does not exist. Please register.")

def main():
    while True:
        print("\nHi! Please Login / Create Account to talk to Perch.")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            create_profile()
        elif choice == '2':
            login_user()
        elif choice == '3':
            print("Exiting program. Bye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 3.")

if __name__ == "__main__":
    main()
