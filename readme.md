# PDF Chat App

This is a Streamlit-based web application that allows users to chat with multiple PDF documents. The application uses LangChain and OpenAI's GPT-4 to provide intelligent responses based on the content of uploaded PDFs.

## Features

- Upload and process multiple PDF documents simultaneously
- Interactive chat interface to ask questions about your documents
- Powered by OpenAI's GPT-4 for accurate and contextual responses
- Built with Streamlit for a clean, user-friendly interface
- Docker support for easy deployment and scalability

## Usage

1. Launch the application using one of the installation methods below
2. Upload one or more PDF documents using the file upload interface
3. Wait for the documents to be processed
4. Type your questions in the chat interface
5. Receive AI-powered responses based on the content of your PDFs

## Requirements

- **Python Version**: 3.9 or later
- **OpenAI API Key**: Required for GPT-4 and embeddings
- **Docker**: Required for containerized deployment
    - [Install Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
    - After installation, restart your computer
    - Verify installation by opening a new terminal and running: `docker --version`

## Local Setup Instructions

Follow the steps below to set up and run the application locally.

### Step 1: Create and Activate Virtual Environment

**Windows**:
```bash
python -m venv PDFChat
.\PDFChat\Scripts\activate
```

**Linux/MacOS**:
```bash
python3 -m venv PDFChat
source PDFChat/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key (https://platform.openai.com/api-keys):
```
OPENAI_API_KEY=your_api_key_here
```

### Step 4: Run Application
```bash
streamlit run app.py
```

## Docker Deployment

You can also run the application using Docker, which ensures consistent behavior across different platforms.

### Step 1: Build Docker Image
```bash
docker build -t pdf-chat-app .
```

### Step 2: Run Docker Container
```bash
docker run -p 8501:8501 --env-file .env pdf-chat-app
```

The application will be available at `http://localhost:8501`

### Docker Compose (Recommended)
With the provided `docker-compose.yml` file, run:
```bash
docker compose up
```

## Troubleshooting

### Docker Issues

1. **EOF Error During Build**
   If you encounter an EOF error while building or running the Docker container:
   ```bash
   # Try these steps:
   
   # 1. Stop all running containers
   docker compose down
   
   # 2. Clear Docker cache
   docker builder prune -f
   
   # 3. Restart Docker Desktop
   
   # 4. Rebuild and run
   docker compose up --build
   ```

2. **Memory Issues**
   - Ensure Docker Desktop has sufficient resources allocated (recommended: at least 4GB RAM)
   - You can adjust this in Docker Desktop Settings > Resources

## Important Notes

- Ensure your `.env` file is properly configured with the OpenAI API key
- The application uses port 8501 by default (localhost:8501)
- When using Docker, make sure to properly handle environment variables
