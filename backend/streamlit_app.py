import streamlit as st
from PIL import Image
from modules.summarizer import MathProblemSummarizer

@st.cache_resource
def load_summarizer():
    return MathProblemSummarizer()

summarizer = load_summarizer()

st.title("🧮 Math Problem Assistant")

uploaded = st.file_uploader(
    "Upload a math problem image", type=["jpg", "jpeg", "png"]
)
if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_column_width=True)

    if st.button("🔍 Summarize and Predict Difficulty"):
        with st.spinner("Processing..."):
            # Step 1: Summarize the problem
            summary = summarizer.summarize(img)
            # Step 2: Predict difficulty & grade
            prediction = summarizer.predict_difficulty(summary)
        st.subheader("Summary")
        st.write(summary)
        st.subheader("Difficulty & Grade Prediction")
        st.write(prediction)