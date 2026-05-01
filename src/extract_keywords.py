import re 

from coreterm.src.linguistic_filter import filter_linguistic_candidates
from coreterm.src.domain_filter import filter_domain_terms
from coreterm.src.layout_filter import filter_layout_artifacts
from coreterm.src.term_normalizer import normalize_ranked_terms
from coreterm.src.termhood_filter import filter_termhood
from coreterm.src.polish_terms import polish_terms
from coreterm.src.preprocessing import clean_text, extract_noun_phrases
from coreterm.src.generate_keywords import (
    compute_term_frequencies,
    compute_c_value,
    compute_dispersion_score,
    combine_scores
)
from coreterm.src.reference_filter import remove_references_section
from coreterm.src.citation_filter import remove_citation_phrases

def remove_front_matter(text):
    lower = text.lower()
    chapter_match = re.search(r"\bchapter\s+1\b", lower)
    if chapter_match:
        return text[chapter_match.start():]
    intro_match = re.search(r"\bintroduction\b", lower)
    if intro_match:
        return text[intro_match.start():]
    return text

def extract_keywords(text: str, top_k: int = 20):
    text = remove_references_section(text)
    text = remove_citation_phrases(text)
    text = remove_front_matter(text)
    text = clean_text(text)
    if not text.strip():
        return []
    candidates = []
    MAX_CHARS = 200_000
    for i in range(0, len(text), MAX_CHARS):
        chunk = text[i:i + MAX_CHARS]
        candidates.extend(extract_noun_phrases(chunk))
    if not candidates:
        return []
    candidates = filter_linguistic_candidates(candidates)
    if not candidates:
        return []
    term_freq = compute_term_frequencies(candidates)
    if not term_freq:
        return []
    c_values = compute_c_value(term_freq)
    dispersion_scores = compute_dispersion_score(text, candidates)
    final_scores = combine_scores(c_values, dispersion_scores)
    ranked_terms = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    ranked_terms = filter_domain_terms(ranked_terms)
    ranked_terms = filter_layout_artifacts(ranked_terms)
    ranked_terms = normalize_ranked_terms(ranked_terms)
    ranked_terms = filter_termhood(ranked_terms)
    final_terms = [term for term, score in ranked_terms]
    final_terms = polish_terms(final_terms)
    return final_terms[:top_k]