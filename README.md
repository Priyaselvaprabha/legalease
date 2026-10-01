# LegalEase

LegalEase is an AI-powered legal information assistant.

## Features

- Ask legal questions
- Explain legal text
- Summarize documents
- Generate legal document drafts
- FastAPI backend
- Streamlit frontend
- Gemini AI integration

## Project Structure

LegalEase/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
│
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
│
├── services/
│   ├── __init__.py
│   └── document_service.py
│
├── utils/
│   ├── __init__.py
│   └── sanitize.py
│
├── frontend/
│   └── app.py
│
├── assets/
│   └── logo.png
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_documents.py
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── requirements.txt
└── README.md

## Installation

Create virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install packages:

pip install -r requirements.txt

Add Gemini API key to `.env`.

## Run Backend

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## Run Frontend

Open another terminal:

.venv\Scripts\activate

streamlit run frontend/app.py

Frontend:

http://localhost:8501

## Run Tests

pytest