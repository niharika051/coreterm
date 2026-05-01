GENERIC_HEADS = {
    "number", "range", "type", "kind", "form", "way", "case",
    "example", "result", "problem", "approach", "method",
    "system", "process", "thing", "part", "set", "group",
    "deal", "point", "points", "image", "images", "data",
    "value", "values", "level", "levels", "rate", "figure"
}

WEAK_SINGLE_WORDS = {
    "model", "method", "approach", "system",
    "which", "detection", "classification",
    "clustering", "probabilistic", "dynamical",
    "compositional", "tree-structured"
}

WEAK_PREFIXES = {
    "good", "better", "best", "current", "more",
    "other", "various", "different"
}

def is_valid_term_candidate(phrase: str) -> bool:
    words = phrase.strip().lower().split()

    if len(words) < 2:
        return False

    head = words[-1]

    if head in GENERIC_HEADS:
        return False

    if words[0] in WEAK_PREFIXES:
        return False

    if words[0].endswith("ing") and not head.endswith("ing"):
        return False

    if head.endswith("al") and len(words) == 2:
        return False

    return True

def filter_linguistic_candidates(candidates):
    filtered = []

    for c in candidates:
        if not is_valid_term_candidate(c):
            continue

        words = c.strip().lower().split()

        if len(words) == 1 and words[0] in WEAK_SINGLE_WORDS:
            continue

        filtered.append(c)

    return filtered