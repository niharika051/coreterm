import re

CITATION_TEXT_PATTERNS = [
    r"ieee\s+transactions\s+on\s+pattern\s+analysis\s+and\s+machine\s+intelligence",
    r"ieee\s+transactions",
    r"ieee\s+cvpr",
    r"ieee\s+conference",
    r"proc\.?\s+int\.?\s+conf\.?",
    r"international\s+journal",
    r"optical\s+society",
    r"ieee",
    r"proceedings\s+of\s+the",
]

def remove_citation_phrases(text: str) -> str:
    cleaned = text.lower()

    for pattern in CITATION_TEXT_PATTERNS:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)

    return cleaned