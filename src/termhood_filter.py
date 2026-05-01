GENERIC_HEADS = {
    "model",
    "models",
    "method",
    "methods",
    "approach",
    "approaches",
    "strategy",
    "strategies",
    "technique",
    "techniques",
    "process",
    "processes",
    "system",
    "systems",
    "feature",
    "features",
    "output",
    "outputs",
    "representation",
    "representations"
}

ALLOWED_COMPOUNDS = {
    "support vector machine",
    "mixture model",
    "active appearance model",
    "visual hull model",
    "pictorial structure model",
    "interreflection model",
    "geometric camera model",
    "probabilistic model",
    "tree-structured model",
    "compositional model",
    "dynamical model",
    "particle filter",
    "kalman filter",
    "model selection"
}

def is_strong_term(term: str) -> bool:
    words = term.lower().split()

    if len(words) < 2:
        return False

    head = words[-1]

    if term.lower() in ALLOWED_COMPOUNDS:
        return True

    if head in GENERIC_HEADS:
        return False

    return True

def filter_termhood(ranked_terms):
    filtered = []

    for term, score in ranked_terms:
        if is_strong_term(term):
            filtered.append((term, score))

    return filtered