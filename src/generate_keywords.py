from collections import Counter, defaultdict
import math

def compute_term_frequencies(candidates):
    return Counter(candidates)

def compute_c_value(term_freq):
    c_values = {}
    terms = list(term_freq.keys())
    terms_sorted = sorted(terms, key=lambda t: len(t.split()), reverse=True)
    for term in terms_sorted:
        freq = term_freq[term]
        length = len(term.split())
        if length == 1:
            c_values[term] = math.log2(2) * freq
            continue
        longer_terms = [
            t for t in terms
            if term != t and term in t and len(t.split()) > length
        ]
        if longer_terms:
            sum_freq = sum(term_freq[t] for t in longer_terms)
            adjusted_freq = freq - (sum_freq / len(longer_terms))
            c_values[term] = math.log2(length + 1) * max(adjusted_freq, 1)
        else:
            c_values[term] = math.log2(length + 1) * freq
    return c_values

def compute_dispersion_score(text, candidates, block_size=4000):
    blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]
    term_blocks = defaultdict(set)
    for idx, block in enumerate(blocks):
        block_lower = block.lower()
        for term in candidates:
            if term in block_lower:
                term_blocks[term].add(idx)
    dispersion_scores = {}
    total_blocks = max(len(blocks), 1)
    for term, bset in term_blocks.items():
        dispersion_scores[term] = 1 + math.log2(1 + len(bset))
    return dispersion_scores

def combine_scores(c_values, dispersion_scores):
    final_scores = {}
    for term in c_values:
        c = c_values.get(term, 0)
        d = dispersion_scores.get(term, 1)
        final_scores[term] = c * d
    return final_scores