import re
import spacy
import unicodedata
from collections import Counter

nlp = spacy.load("en_core_web_sm")
STOPWORDS = nlp.Defaults.stop_words

def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)

    lines = text.split("\n")

    normalized_lines = []

    for line in lines:
        line = line.strip().lower()
        line = re.sub(r"\s+", " ", line)
        if line:
            normalized_lines.append(line)

    line_counts = Counter(normalized_lines)

    cleaned_lines = []

    for line in normalized_lines:
        if line_counts[line] < 12:
            cleaned_lines.append(line)

    text = " ".join(cleaned_lines)

    text = re.sub(r"-\s+", "", text)
    text = re.sub(r"\b\d+\b", " ", text)

    text = text.replace("fourierer", "fourier")
    text = text.replace("fouri", "fourier")
    text = text.replace("sery", "series")
    text = text.replace("low-pas", "low-pass")
    text = text.replace("gaus", "gauss")
    text = text.replace("unambiguou", "unambiguous")
    text = text.replace("thi ", "")
    text = text.replace("netvvork", "network")
    text = text.replace("wirelesss", "wireless")

    text = re.sub(r"\[\d+\]", " ", text)
    text = re.sub(r"\(\d+\)", " ", text)

    text = re.sub(r"\s*-\s*", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def extract_noun_phrases(text: str, chunk_size: int = 50000):

    candidates = []

    junk_tokens = {
        "figure", "part", "ed", "appendix",
        "problem", "repeat", "section",
        "page", "chapter"
    }

    weak_prefixes = {
        "this", "these", "that"
    }

    for i in range(0, len(text), chunk_size):

        chunk_text = text[i:i + chunk_size]

        try:
            doc = nlp(chunk_text)
        except:
            continue

        for chunk in doc.noun_chunks:

            if chunk.root.pos_ != "NOUN":
                continue

            phrase = chunk.text.strip().lower()
            phrase = re.sub(r"[^a-z0-9\s-]", "", phrase)

            tokens = phrase.split()

            if len(tokens) < 2 or len(tokens) > 4:
                continue

            if tokens[0] in weak_prefixes:
                continue

            if any(t in junk_tokens for t in tokens):
                continue

            if any(len(t) == 1 for t in tokens):
                continue

            if any(t.isdigit() for t in tokens):
                continue

            if "and" in tokens:
                continue

            if len(phrase) < 5:
                continue

            candidates.append(phrase)

    return candidates