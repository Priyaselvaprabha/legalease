import sys
from pathlib import Path
import requests
import streamlit as st

# ============================================================
# IMPORT DOCUMENT GENERATORS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.document_generator import (
    create_pdf,
    create_docx,
)

# ============================================================
# CONFIGURATION
# ============================================================

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered"
)

# ============================================================
# DARK BACKGROUND + STYLING
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0e0e14 !important;
        color: white !important;
    }

    .main .block-container {
        max-width: 760px;
        padding-top: 35px;
        padding-bottom: 50px;
    }

    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }

    p {
        color: white !important;
    }

    label {
        color: white !important;
    }

    input {
        background-color: #262530 !important;
        color: white !important;
        border: 1px solid #555463 !important;
        border-radius: 5px !important;
    }

    textarea {
        background-color: #262530 !important;
        color: white !important;
        border: 1px solid #555463 !important;
        border-radius: 5px !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #aaaaaa !important;
    }

    .stButton > button {
        background-color: #262530 !important;
        color: white !important;
        border: 1px solid #555463 !important;
        border-radius: 5px !important;
    }

    .stButton > button:hover {
        background-color: #353442 !important;
        color: white !important;
    }

    .stDownloadButton > button {
        background-color: #262530 !important;
        color: white !important;
        border: 1px solid #555463 !important;
        border-radius: 5px !important;
    }

    .stDownloadButton > button:hover {
        background-color: #353442 !important;
        color: white !important;
    }

    div[data-testid="stAlert"] {
        background-color: #17202b !important;
        color: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# LEGALEASE HEADER
# ============================================================

st.title("⚖️ LegalEase")

st.subheader("AI Legal Document Generator")

# ============================================================
# INFORMATION
# ============================================================

st.info(
    "LegalEase provides general legal information and "
    "AI-generated drafts for educational and informational "
    "purposes only."
)

# ============================================================
# GENERATE LEGAL DOCUMENT
# ============================================================

st.header("Generate Legal Document")

st.write(
    "Enter the details below to generate your legal document."
)

# ============================================================
# DOCUMENT TYPE
# ============================================================

document_type = st.text_input(
    "Document Type",
    value="Web Development Agreement"
)

# ============================================================
# PARTIES INVOLVED
# ============================================================

parties = st.text_area(
    "Parties Involved",
    value=(
        "Priya (Developer)\n"
        "ABC Tech Solutions (Client)"
    ),
    height=100
)

# ============================================================
# TERMS & CONDITIONS
# ============================================================

terms = st.text_area(
    "Terms & Conditions",
    value=(
        "The website must be completed within 30 days\n"
        "Full payment should be transferred upon project delivery\n"
        "All source code belongs to the client"
    ),
    height=160
)

# ============================================================
# EFFECTIVE DATE
# ============================================================

dates = st.text_input(
    "Effective Date",
    value="September 28, 2026"
)

# ============================================================
# BACKEND FUNCTION
# ============================================================

def call_backend(endpoint, payload):

    try:

        response = requests.post(
            f"{BACKEND_URL}{endpoint}",
            json=payload,
            timeout=120
        )

        if response.status_code != 200:

            try:

                error_data = response.json()

                detail = error_data.get(
                    "detail",
                    "Backend error"
                )

            except Exception:

                detail = response.text

            st.error(
                f"Backend error: {detail}"
            )

            return None

        return response.json()

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to the backend. "
            "Please make sure Uvicorn is running "
            "on port 8000."
        )

        return None

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )

        return None

# ============================================================
# GENERATE BUTTON
# ============================================================

if st.button("Generate Document"):

    if not document_type.strip():

        st.warning(
            "Please enter the document type."
        )

    elif not parties.strip():

        st.warning(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.warning(
            "Please enter the terms and conditions."
        )

    elif not dates.strip():

        st.warning(
            "Please enter the effective date."
        )

    else:

        result = call_backend(
            "/api/generate",
            {
                "document_type": document_type,
                "parties": parties,
                "terms": terms,
                "dates": dates
            }
        )

        if result:

            content = result.get(
                "content",
                ""
            )

            # Save content in session
            st.session_state["content"] = content
            st.session_state["title"] = document_type


# ============================================================
# SHOW GENERATED DOCUMENT
# ============================================================

if "content" in st.session_state:

    content = st.session_state["content"]

    title = st.session_state.get(
        "title",
        "LegalEase Document"
    )

    st.subheader(
        "Generated Document"
    )

    st.text_area(
        "Document",
        content,
        height=600
    )

    # ========================================================
    # CREATE PDF
    # ========================================================

    try:

        pdf_path = create_pdf(
            "legalease_document.pdf",
            title,
            content
        )

        # ====================================================
        # CREATE DOCX
        # ====================================================

        docx_path = create_docx(
            "legalease_document.docx",
            title,
            content
        )

        # Read files
        with open(
            pdf_path,
            "rb"
        ) as pdf_file:

            pdf_data = pdf_file.read()

        with open(
            docx_path,
            "rb"
        ) as docx_file:

            docx_data = docx_file.read()

        # ====================================================
        # DOWNLOAD SECTION
        # ====================================================

        st.markdown(
            "### Download Document"
        )

        col1, col2, col3 = st.columns(3)

        # ----------------------------------------------------
        # TXT
        # ----------------------------------------------------

        with col1:

            st.download_button(
                label="Download TXT",
                data=content,
                file_name="legalease_document.txt",
                mime="text/plain",
                use_container_width=True
            )

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        with col2:

            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="legalease_document.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # ----------------------------------------------------
        # DOCX
        # ----------------------------------------------------

        with col3:

            st.download_button(
                label="Download DOCX",
                data=docx_data,
                file_name="legalease_document.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True
            )

    except Exception as e:

        st.error(
            f"Document generation error: {str(e)}"
        )