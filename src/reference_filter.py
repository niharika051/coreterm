import re

REFERENCE_HEADERS = [
    r"\nreferences\n",
    r"\nreference\n",
    r"\nbibliography\n",
    r"\nliterature cited\n",
    r"\nacknowledgments\n",
    r"\nacknowledgements\n",
    r"\nappendix\n",
    r"\nappendix a\n",
    r"\nappendices\n"
]

def remove_references_section(text: str) -> str:
    lowered = text.lower()
    cut_positions = []

    for pattern in REFERENCE_HEADERS:
        match = re.search(pattern, lowered)
        if match:
            cut_positions.append(match.start())

    if not cut_positions:
        return text

    cut_point = min(cut_positions)
    return text[:cut_point]