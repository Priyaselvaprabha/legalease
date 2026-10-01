from services.document_service import (
    save_text_file,
    create_docx,
    create_pdf,
)


def test_save_text_file():

    path = save_text_file(
        "test.txt",
        "LegalEase test document"
    )

    assert path.endswith(
        "test.txt"
    )


def test_create_docx():

    path = create_docx(
        "test.docx",
        "Test Document",
        "This is a test."
    )

    assert path.endswith(
        "test.docx"
    )


def test_create_pdf():

    path = create_pdf(
        "test.pdf",
        "Test Document",
        "This is a test."
    )

    assert path.endswith(
        "test.pdf"
    )