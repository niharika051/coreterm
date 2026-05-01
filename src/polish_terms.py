JUNK_PHRASES = [
    "website",
    "chapter",
    "edition",
    "reader",
    "textbook",
    "companion",
    "support package",
    "login",
    "global edition",
    "exercise",
    "new material",
    "new chapter",
    "new edition",
    "expanded coverage",
    "book website",
    "digital resource",
    "entitled",
    "their use",
    "our reader",
    "your textbook"
]


def polish_terms(terms):

    clean = []

    for term in terms:
        t = term.lower()

        # Remove junk phrases
        if any(junk in t for junk in JUNK_PHRASES):
            continue

        # Remove single generic words
        if len(t.split()) == 1 and t in {
            "chapter", "image", "book", "figure", "section"
        }:
            continue

        clean.append(term)

    return clean