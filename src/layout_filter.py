import re

ROMAN = r'\b(i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii|xiii|xiv|xv)\b'

def looks_like_toc(term: str) -> bool:
    t = term.lower()

    if len(re.findall(r'\d+', t)) >= 2:
        return True

    if re.search(ROMAN, t):
        return True

    if re.search(r'\d+\s+\d+', t):
        return True

    if re.match(r'^\d+', t):
        return True

    if re.search(r'\d+\.\d+', t):
        return True

    if re.search(r'\b[23]d\b', t):
        return True

    return False

def filter_layout_artifacts(ranked_terms):
    cleaned = []

    for term, score in ranked_terms:
        if not looks_like_toc(term):
            cleaned.append((term, score))

    return cleaned