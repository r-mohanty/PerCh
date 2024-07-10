# Perch
Perch is a RAG pipeline to personalized language models based on user data. It allows users to create an account and upload personal informtion as unstructured data. It then uses this information along with the chat history to generate personalized responses for each user account.


## Technology Used
* [<b>LlamaIndex</b>](https://www.llamaindex.ai/) - To build the RAG pipeline for connecting user data to LLM.
* [<b>GPT-3.5-turbo</b>](https://platform.openai.com/docs/models/gpt-3-5-turbo) - LLM used to gennerate responses.
* [<b>Chroma DB</b>](https://www.trychroma.com/) - Vector Database used to store and retrieve embeddings.
* [<b>SQLAlchemy</b>](https://www.sqlalchemy.org/) - Database used to store user account detais.

## Technical Details

To run the application on your teminal use the command `python app.py` and follow the menu instrctions to use the application.

The home menu of the application allows users to create pofile or login to chat with their personal chatbot. User can login after creating a profile and access their personal chatbot menu. The chatbot gives responses based on the updated data provided by the user and the chat history with the user.

Each user's chat profile is saved in a separate collection in Chroma DB and user can manage the data in their chat profile from the chatbot menu. Users can make the following modifications to their data:
* Upload New Unstructured Data
* Update Existing Data
* Delete Existing Data

The data is divided into chunks and stored as nodes in the Vector Store which is later used by the LLM to generate personalized responses.


## Contributing
#### Step 1

- **Option 1**
    - 🍴 Fork this repo!

- **Option 2**
    - 👯 Clone this repo to your local machine.


#### Step 2

- **Build your code**

#### Step 3

- 🔃 Create a new pull request.

## License
This project is licensed under the [MIT License](./LICENSE).