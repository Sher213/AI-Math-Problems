import streamlit as st
from PIL import Image
from summarizer import MathProblemSummarizer

@st.cache_resource
def load_summarizer():
    return MathProblemSummarizer()

summarizer = load_summarizer()

st.title("🧮 Math Problem Summarizer (Gemini)")
uploaded = st.file_uploader("Upload a math problem image", type=["jpg","jpeg","png"])
if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_column_width=True)

    if st.button("🔍 Summarize"):
        with st.spinner("Calling Gemini..."):
            text = summarizer.summarize(img)
        st.subheader("Summary")
        st.write(text)