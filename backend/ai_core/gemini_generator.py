import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


if not GEMINI_API_KEY:
    client = None
else:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


def generate_response(prompt: str) -> str:

    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to the .env file."
        )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text


def ask_gemini(question: str) -> str:

    prompt = f"""
You are LegalEase, an AI legal information assistant.

User question:
{question}

Give a clear and simple answer.

Rules:
- Explain legal concepts in simple language.
- Do not pretend to be a lawyer.
- Do not guarantee a legal outcome.
- Mention that laws can vary by country/state when relevant.
- Suggest consulting a qualified lawyer for important legal decisions.
"""

    return generate_response(prompt)


def explain_legal_text(text: str) -> str:

    prompt = f"""
You are LegalEase.

Explain the following legal text in simple language.

Legal text:
{text}

Provide:
1. Simple meaning
2. Important points
3. Possible responsibilities
4. Important things the user should check

Do not provide guaranteed legal conclusions.
"""

    return generate_response(prompt)


def summarize_text(text: str) -> str:

    prompt = f"""
You are LegalEase.

Summarize the following legal document.

Document:
{text}

Give:
- Short summary
- Main parties
- Important obligations
- Important dates
- Important conditions
- Potential concerns

Use simple language.
"""

    return generate_response(prompt)


def generate_legal_document(
    document_type: str,
    details: str
) -> str:

    prompt = f"""
You are LegalEase, an AI legal document drafting assistant.

Create a professional draft for:

Document type:
{document_type}

User details:
{details}

Requirements:
- Use a professional format.
- Keep placeholders where information is missing.
- Do not invent personal information.
- Make it clear that this is an AI-generated draft.
- Recommend legal review before official use.
"""

    return generate_response(prompt)