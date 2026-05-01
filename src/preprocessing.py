import re
import math
import nltk
import unicodedata
from collections import Counter

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

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
    cleaned_lines = [line for line in normalized_lines if line_counts[line] < 12]
    text = " ".join(cleaned_lines)
    text = re.sub(r"-\s+", "", text)
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"\[\d+\]", " ", text)
    text = re.sub(r"\(\d+\)", " ", text)
    text = re.sub(r"\s*-\s*", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_noun_phrases(text: str, chunk_size: int = 50000):
    candidates = []
    junk_tokens = {"figure","part","ed","appendix","problem","section","page","chapter"}
    weak_prefixes = {"this","these","that"}

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        try:
            tokens = nltk.word_tokenize(chunk)
            tagged = nltk.pos_tag(tokens)
        except:
            continue

        phrase = []
        for word, tag in tagged:
            if tag in ("NN","NNS","NNP","NNPS","JJ"):
                phrase.append(word.lower())
            else:
                if 2 <= len(phrase) <= 4:
                    p = " ".join(phrase)
                    p = re.sub(r"[^a-z0-9\s-]", "", p)
                    words = p.split()
                    if (len(words) >= 2
                        and words[0] not in weak_prefixes
                        and not any(t in junk_tokens for t in words)
                        and not any(len(t)==1 for t in words)
                        and not any(t.isdigit() for t in words)
                        and "and" not in words
                        and len(p) >= 5):
                        candidates.append(p)
                phrase = []

    return candidates
