def sanitize_text(text: str) -> str:
    """
    Basic text cleaning.
    """

    if not text:
        return ""

    text = text.strip()

    while "  " in text:
        text = text.replace(
            "  ",
            " "
        )

    return text


def limit_text(
    text: str,
    max_length: int = 10000
) -> str:

    text = sanitize_text(text)

    return text[:max_length]