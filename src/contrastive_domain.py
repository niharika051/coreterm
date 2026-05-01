import math
import re
from collections import Counter

GENERAL_ENGLISH_FREQ = {
    "the": 60000, "of": 30000, "and": 27000, "to": 25000,
    "a": 22000, "in": 21000, "is": 10000, "it": 9000,
    "that": 9000, "was": 8000, "for": 8000, "on": 7000,
    "are": 6000, "with": 6000, "as": 6000, "be": 5000,
    "at": 5000, "by": 5000, "from": 5000, "this": 5000,
    "or": 4000, "an": 4000, "which": 4000, "but": 3500,
    "not": 3500, "have": 3500, "has": 3000, "been": 3000,
    "can": 3000, "more": 2500, "their": 2500, "they": 2500,
    "we": 2000, "new": 2000, "also": 2000, "into": 2000,
    "time": 2000, "way": 1800, "use": 1800, "used": 1800,
    "two": 1500, "how": 1500, "its": 1500, "may": 1500,
    "such": 1400, "each": 1400, "both": 1200, "between": 1200,
    "many": 1200, "data": 1100, "value": 1000, "values": 1000,
    "number": 1000, "same": 900, "result": 900, "results": 900,
    "example": 900, "first": 850, "set": 850, "problem": 800,
    "point": 800, "case": 800, "order": 750, "given": 750,
    "term": 700, "terms": 700, "system": 700, "function": 650,
    "process": 650, "method": 650, "approach": 600, "model": 600,
    "information": 600, "large": 550, "different": 550,
    "general": 500, "good": 500, "important": 500, "work": 500,
    "analysis": 400, "based": 400, "error": 400, "output": 380,
    "input": 380, "high": 350, "low": 350, "form": 350,
    "matrix": 300, "vector": 300, "parameter": 280, "algorithm": 270,
    "solution": 260, "equation": 250, "variables": 240, "variable": 240,
    "probability": 230, "distribution": 220, "network": 210,
    "learning": 200, "training": 190, "image": 180, "feature": 175,
    "classification": 160, "regression": 140, "clustering": 100,
    "optimization": 120, "gradient": 110, "convergence": 90,
    "constraint": 90, "objective": 85, "kernel": 80,
}

def _tokenize(text: str) -> list:
    return re.findall(r"[a-z]+", text.lower())

def build_doc_frequencies(text: str) -> Counter:
    tokens = _tokenize(text)
    freq = Counter(tokens)

    for i in range(len(tokens) - 1):
        bigram = tokens[i] + " " + tokens[i + 1]
        freq[bigram] += 1

    return freq

def domain_specificity_score(term: str, doc_freq: Counter) -> float:
    words = term.lower().split()

    phrase_doc_freq = doc_freq.get(term.lower(), 0)
    phrase_ref_freq = GENERAL_ENGLISH_FREQ.get(term.lower(), 1)
    phrase_score = math.log2((phrase_doc_freq + 1) / (phrase_ref_freq + 1))

    word_scores = []
    for w in words:
        wdf = doc_freq.get(w, 0)
        wrf = GENERAL_ENGLISH_FREQ.get(w, 1)
        word_scores.append(math.log2((wdf + 1) / (wrf + 1)))

    if word_scores:
        constituent_score = min(word_scores)
    else:
        constituent_score = 0.0

    return round((phrase_score + constituent_score) / 2, 4)

def filter_by_domain_specificity(
    ranked_terms: list,
    doc_freq: Counter,
    threshold: float = 0.0
) -> list:
    filtered = []
    for term, score in ranked_terms:
        ds = domain_specificity_score(term, doc_freq)
        if ds > threshold:
            filtered.append((term, score))
    return filtered

def score_all_terms(
    ranked_terms: list,
    doc_freq: Counter
) -> list:
    return [
        (term, score, domain_specificity_score(term, doc_freq))
        for term, score in ranked_terms
    ]