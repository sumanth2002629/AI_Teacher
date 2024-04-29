# Getting started
To get started with this project, follow these steps:
1. Fork this repository

2. Clone this repository to your local machine:

   
```bash 
git clone https://github.com/sumanth2002629/AI_Teacher.git
```

3. Install the required dependencies for python backend:

```bash
cd AI_Teacher
cd ./backend && pip install Flask flask-cors reportlab transformers langchain chromadb pypdf openai-whisper
```
- Install ollama from [https://ollama.com/download](https://ollama.com/download).
```bash
ollama pull llama3
```

4. Install the required dependencies for react frontend:

```bash
cd ./frontend && npm install
```

5. Start the backend server:

```bash
cd backend && python3 backend.py
```

6. Start the frontend server:

```bash
cd frontend && npm start
```

7. Access the application in your web browser at [http://localhost:3000](http://localhost:3000)
