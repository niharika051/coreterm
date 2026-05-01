import re

def strip_leading_numbers(term: str) -> str:
    return re.sub(r"^(\d+\s+)+", "", term).strip()

HARD_JUNK = {
    "website", "chapter", "edition", "reader",
    "textbook", "companion", "support", "package",
    "login", "global", "exercise", "expanded",
    "coverage", "digital resource", "new material",
    "new chapter", "new edition", "copyright",
    "permission", "publisher", "director",
    "family", "assistant", "student"
}

BIBLIOGRAPHIC_KEYWORDS = {
    "ieee", "conference", "conf", "transactions",
    "journal", "proceedings", "proc", "society",
    "international", "vol", "no", "pp", "press",
    "isbn"
}

CITATION_PATTERNS = [
    r"^et al",
    r"^\d{4}$",
    r"^\d{1,3}-\d{1,3}$",
    r"^vol",
    r"^pp",
]

def is_bibliographic_term(term: str) -> bool:
    t = term.lower().strip()
    words = t.split()

    if any(w in BIBLIOGRAPHIC_KEYWORDS for w in words):
        return True

    for pattern in CITATION_PATTERNS:
        if re.search(pattern, t):
            return True

    digits = sum(c.isdigit() for c in t)
    if digits > len(t) * 0.4:
        return True

    return False

GENERIC_BAD = {
    "thing", "things", "paper", "approach",
    "result", "example", "problem", "method",
    "detail", "impact", "development"
}

GENERIC_ADJECTIVES = {
    "important", "significant", "practical",
    "advanced", "general", "basic",
    "original", "new", "several",
    "various", "certain", "other",
    "different", "similar"
}

TECHNICAL_STEMS = {
    "model", "optim", "learn", "probab",
    "distribut", "infer", "classif",
    "regress", "variat", "dual",
    "matrix", "vector", "filter",
    "transform", "segment", "compress",
    "stabil", "control", "estim",
    "function", "equation", "constraint",
    "system", "network", "likelihood",
    "density", "kernel"
}

def has_technical_anchor(words):
    for w in words:
        for stem in TECHNICAL_STEMS:
            if stem in w:
                return True
    return False

def is_valid_concept(term: str) -> bool:
    term = strip_leading_numbers(term)
    term = re.sub(r"^(the|a|an)\s+", "", term, flags=re.IGNORECASE)
    term = term.lower().strip()

    words = term.split()

    if len(words) < 2:
        return False

    if any(junk in term for junk in HARD_JUNK):
        return False

    if any(w in GENERIC_BAD for w in words):
        return False

    if words[0] in GENERIC_ADJECTIVES:
        return False

    if is_bibliographic_term(term):
        return False

    if not has_technical_anchor(words):
        return False

    return True

def filter_domain_terms(ranked_terms):
    filtered = []

    for term, score in ranked_terms:

        clean_term = strip_leading_numbers(term)
        clean_term = re.sub(
            r"^(the|a|an)\s+", "",
            clean_term,
            flags=re.IGNORECASE
        )

        if is_valid_concept(clean_term):
            filtered.append((clean_term.lower(), score))

    return filtered