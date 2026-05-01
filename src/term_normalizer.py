import re

WEAK_PREFIXES = {
    "linear", "analytical", "basic", "simple",
    "simplest", "workable", "local", "current",
    "more", "other", "various"
}

GENERIC_HEADS = {
    "model", "models",
    "method", "methods",
    "approach", "approaches",
    "strategy", "strategies"
}

CANONICAL_REPLACEMENTS = {
    "svms": "support vector machine",
    "kernel machines": "support vector machine",
    "svms and kernel machines": "support vector machine",
    "weak-perspective projection matrices": "weak perspective projection",
    "perspective projection matrices": "perspective projection",
    "pictorial structure models": "pictorial structure model",
    "active appearance models": "active appearance model",
    "mixture models": "mixture model",
    "probabilistic models": "probabilistic model",
}

def singularize(word):
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith("s") and len(word) > 3:
        return word[:-1]
    return word

def normalize_term(term):
    term = term.lower().strip()

    if term in CANONICAL_REPLACEMENTS:
        return CANONICAL_REPLACEMENTS[term]

    words = term.split()

    if words[0] in WEAK_PREFIXES:
        words = words[1:]

    words = [singularize(w) for w in words]

    normalized = " ".join(words)

    if normalized in CANONICAL_REPLACEMENTS:
        return CANONICAL_REPLACEMENTS[normalized]

    return normalized

def normalize_ranked_terms(ranked_terms):
    merged = {}

    for term, score in ranked_terms:
        norm = normalize_term(term)

        if norm in merged:
            merged[norm] += score
        else:
            merged[norm] = score

    return sorted(merged.items(), key=lambda x: x[1], reverse=True)