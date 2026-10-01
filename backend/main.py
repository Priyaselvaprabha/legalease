import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router

# Load environment variables from .env
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="LegalEase API",
    description="AI-Powered Legal Document Generator",
    version="1.0.0",
)

# Read allowed frontend origins from .env
origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501",
    ).split(",")
    if origin.strip()
]

# Enable CORS so Streamlit frontend can communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


# Home / root endpoint
@app.get("/")
def root():
    return {
        "service": "LegalEase API",
        "status": "running",
        "message": "LegalEase backend is working",
        "docs": "/docs",
    }


# Health-check endpoint
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "LegalEase API",
    }