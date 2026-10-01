import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api",
    tags=["LegalEase"]
)


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash-lite"
)

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )
else:
    client = None


# ============================================================
# REQUEST MODELS
# ============================================================

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)


class ExplainRequest(BaseModel):
    text: str = Field(..., min_length=1)


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1)


class GenerateRequest(BaseModel):
    document_type: str = Field(..., min_length=1)
    parties: str = Field(..., min_length=1)
    terms: str = Field(..., min_length=1)
    dates: str = Field(..., min_length=1)


# ============================================================
# GEMINI FUNCTION
# ============================================================

def generate_ai_response(prompt: str) -> str:

    if client is None:

        raise HTTPException(
            status_code=500,
            detail=(
                "GEMINI_API_KEY is not configured "
                "in the .env file."
            )
        )

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        text = getattr(
            response,
            "text",
            None
        )

        if not text:

            raise HTTPException(
                status_code=500,
                detail="Gemini returned an empty response."
            )

        return text.strip()

    except HTTPException:

        raise

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=f"Gemini API error: {str(exc)}"
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
def health():

    return {
        "status": "ok",
        "service": "LegalEase API",
        "gemini_configured": bool(
            GEMINI_API_KEY
        ),
        "model": GEMINI_MODEL
    }


# ============================================================
# ASK LEGAL QUESTION
# ============================================================

@router.post("/ask")
def ask_legal_question(
    request: AskRequest
):

    prompt = f"""
You are LegalEase, an AI legal information assistant.

The user asked:

{request.question}

Give a clear and easy-to-understand answer.

Important rules:

1. Provide general legal information, not a substitute
   for a qualified lawyer.

2. Do not claim certainty when laws may differ
   by location or situation.

3. If the user's country or jurisdiction is missing
   and it matters, clearly mention that.

4. Explain important legal terms in simple language.

5. Use headings and bullet points when useful.

6. Do not invent laws, sections, cases, or citations.

7. If the question involves an emergency, advise the
   user to contact the appropriate local authority
   or qualified professional.

Answer in a helpful and concise manner.
"""

    answer = generate_ai_response(
        prompt
    )

    return {
        "success": True,
        "question": request.question,
        "answer": answer
    }


# ============================================================
# EXPLAIN LEGAL TEXT
# ============================================================

@router.post("/explain")
def explain_legal_text(
    request: ExplainRequest
):

    prompt = f"""
You are LegalEase, an AI assistant that explains
legal documents in simple language.

Explain the following legal text:

{request.text}

Give the response using these sections:

1. Simple Explanation
2. Important Points
3. What the User Should Understand
4. Important Caution

Do not change the legal meaning.
Do not invent information.
Explain difficult legal words in simple English.

This is educational information and not legal advice.
"""

    answer = generate_ai_response(
        prompt
    )

    return {
        "success": True,
        "answer": answer
    }


# ============================================================
# SUMMARIZE LEGAL TEXT
# ============================================================

@router.post("/summarize")
def summarize_legal_text(
    request: SummarizeRequest
):

    prompt = f"""
You are LegalEase.

Summarize the following legal text:

{request.text}

Create a clear summary containing:

- Main purpose
- Important facts
- Rights or responsibilities mentioned
- Important dates or deadlines if present
- Important conditions
- Possible concerns

Only use information contained in the provided text.
Do not invent missing information.

Use simple English.
"""

    answer = generate_ai_response(
        prompt
    )

    return {
        "success": True,
        "summary": answer
    }


# ============================================================
# GENERATE LEGAL DOCUMENT
# ============================================================

@router.post("/generate")
def generate_legal_document(
    request: GenerateRequest
):

    # --------------------------------------------------------
    # FIXED VALUES
    # --------------------------------------------------------

    developer = "Priya (Developer)"

    client_name = "ABC Tech Solutions (Client)"

    effective_date = request.dates.strip()

    terms = request.terms.strip()


    # --------------------------------------------------------
    # READ TERMS
    # --------------------------------------------------------

    term_lines = []

    for line in terms.replace(
        ";",
        "\n"
    ).splitlines():

        line = line.strip()

        if line:

            term_lines.append(
                f"- {line}"
            )


    # --------------------------------------------------------
    # DEFAULT TERMS
    # --------------------------------------------------------

    if not term_lines:

        term_lines = [

            "- The website must be completed within 30 days",

            "- Full payment should be transferred upon project delivery",

            "- All source code belongs to the client"

        ]


    services_text = "\n".join(
        term_lines
    )


    # ========================================================
    # WEB DEVELOPMENT AGREEMENT
    # ========================================================

    content = f"""
Agreement made this {effective_date}

Between:

{developer}

And:

{client_name}

WITNESSETH:

WHEREAS, the Client desires to engage the Service Provider to perform certain services as described herein; and

WHEREAS, the Service Provider is willing to perform such services for the Client on the terms and conditions set forth in this Agreement;

NOW, THEREFORE, in consideration of the mutual covenants and promises contained herein, the parties agree as follows:

1. Services:

The Service Provider agrees to provide the following services:

{services_text}

2. Term and Termination:

This Agreement shall commence on the Effective Date and shall terminate upon completion of the Services, or upon occurrence of breach by either party.

3. Payment:

The Client agrees to pay the Service Provider for the complete and satisfactory performance of the Services. Payment shall be made within seven (7) days of receipt of invoice.

4. Intellectual Property Rights:

All intellectual property rights developed in connection with this Agreement shall belong exclusively to the Client.

5. Confidentiality:

The Service Provider agrees not to disclose any confidential information of the Client to any third party.

6. Governing Law:

This Agreement shall be governed by and construed in accordance with the applicable laws of the State.

7. Signatures:


____________________________

{developer}


____________________________

{client_name}
""".strip()


    # ========================================================
    # RETURN
    # ========================================================

    return {
        "success": True,
        "document_type": request.document_type,
        "content": content
    }