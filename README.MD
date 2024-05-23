# Chat-Bot Project

This project is a chat-bot built using Django, Pinecone vector database, OpenAI, and LangChain. The user interface is implemented using Streamlit. The chat-bot leverages a custom knowledge base to provide responses.

## Features

- **Django**: Backend framework to manage the application.
- **Django REST framework**: For building robust APIs.
- **Pinecone**: Vector database to manage and search through embeddings.
- **OpenAI**: For natural language understanding and response generation.
- **LangChain**: To facilitate the interaction between the language model and the knowledge base.
- **Streamlit**: For creating an interactive and user-friendly UI.
- **Flask**: For handling API requests to store and retrieve data.
- **PostgreSQL**: Database to store responses and feedback.

## Prerequisites

- Python 3.11.5
- Django REST framework
- Flask
- psycopg2
- Pinecone API Key
- OpenAI API Key
- Streamlit
- PostgreSQL

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/chat-bot-project.git
    cd chat-bot-project
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up configuration file:**
    Create a `config-dev.json` file in the root directory and add your API keys and other necessary configurations:
    ```json
    {
      "DIRECTORY_TO_SCAN": "C:/Users/User/Downloads/Project/Source/",
      "PROCESSED_FILES": "C:/Users/User/Downloads/Project/Processed/",
      "ERROR_FILES": "C:/Users/User/Downloads/Project/Error/",
      "PINECONE_API_KEY": "your_pinecone_api_key",
      "PINECONE_INDEX": "langchain-app",
      "OPENAI_API_KEY": "your_openai_api_key",
      "PDF_MODEL": "OPENAI",
      "TXT_MODEL": "OPENAI",
      "OPEN_AI_PDF_EMBEDDING_MODEL": "text-embedding-ada-002",
      "OPEN_AI_PDF_EMBEDDING_CTX_LENGTH": 8191,
      "OPEN_AI_PDF_EMBEDDING_ENCODING": "cl100k_base",
      "EMBEDDING_CHUNK_SIZE": 300,
      "NUM_RELATED_QUESTIONS": 3
    }
    ```

5. **Set up PostgreSQL database:**
    Ensure you have PostgreSQL installed and running. Create a database named `PANNADB` and a table named `prompt_audit` with the following schema:
    ```sql
    CREATE TABLE prompt_audit (
        time TIMESTAMP,
        prompt TEXT,
        refined_prompt TEXT,
        response TEXT,
        feedback TEXT,
        feedback_comment TEXT,
        channel TEXT
    );
    ```

6. **Start the Django server:**
    ```bash
    python manage.py runserver
    ```
7. **Open a new terminal and run the Flask backend:**
    ```bash
    python backend.py
    ```
8. **Run the Streamlit app:**
    ```bash
    streamlit run trainingFE.py
    ```

## Usage

1. **Start the Django server:**
    ```bash
    python manage.py runserver
    ```

2. **Open a new terminal and run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

3. **Interact with the chat-bot:**
    Open your web browser and go to `http://localhost:8501` to access the Streamlit UI and start interacting with the chat-bot.

## Project Structure

TrainingModule/
├── Training/                # Django app for the chat-bot backend
│   ├── migrations/          # Database migrations
│   ├── models.py            # Database models
│   ├── views.py             # Django views
│   ├── urls.py              # URL configurations
│   ├── process/             # Folder containing processing files
│   └── ...
├── TrainingModule/          # Django project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── backend.py               # Flask backend script
├── trainingFE.py            # Streamlit frontend script
├── config-dev.json          # Configuration file for API keys
├── requirements.txt         # Python dependencies
└── manage.py                # Django management script

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.




