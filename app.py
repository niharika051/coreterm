import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.extract_keywords import extract_keywords
from src.extract_text import (
    pdf_to_text,
    pptx_to_text,
    docx_to_text
)

st.set_page_config(
    page_title="CoreTerms Terminology Miner",
    layout="wide"
)

st.title("CoreTerms: Terminology Mining System")

st.markdown(
    """
Extract domain terminology from **technical documents** using a linguistic
and statistical pipeline (C-Value + domain filtering).

Supported formats:
- PDF
- PPTX
- DOCX
"""
)

st.divider()

top_k = st.selectbox(
    "Number of terms to extract",
    options=[10, 20, 30, 40, 50, 75, 100],
    index=2
)

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "pptx", "docx"]
)

if uploaded_file:

    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    text = ""

    try:
        with st.spinner("Reading document..."):

            if file_path.lower().endswith(".pdf"):
                text = pdf_to_text(file_path)

            elif file_path.lower().endswith(".pptx"):
                text = pptx_to_text(file_path)

            elif file_path.lower().endswith(".docx"):
                text = docx_to_text(file_path)

    except Exception as e:
        st.error(f"Failed to read file: {e}")

    if text and text.strip():

        try:
            with st.spinner("Mining terminology (running NLP pipeline)..."):
                keywords = extract_keywords(text, top_k)

            st.success(f"Extraction complete! Found {len(keywords)} terms.")

            if len(keywords) < top_k:
                st.info(
                    f" Only {len(keywords)} high-quality domain-specific terms were found. "
                    "Lower-ranked candidates were filtered out to preserve terminology quality."
                )

            st.subheader(" Extracted Terminology")

            for i, kw in enumerate(keywords, 1):
                st.markdown(f"**{i}.** {kw}")

            keyword_text = "\n".join(keywords)

            st.download_button(
                label="⬇ Download terms as .txt",
                data=keyword_text,
                file_name="coreterms_keywords.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"NLP pipeline crashed: {e}")

    else:
        st.warning("No readable text detected in the document.")

    try:
        os.remove(file_path)
    except Exception:
        pass