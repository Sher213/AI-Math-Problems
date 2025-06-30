import os
import io
import logging
from PIL import Image
from google.genai import Client, types
import dotenv

from modules.rag_utils import RAGRetriever

# Load environment vars from a .env file
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MathProblemSummarizer:
    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        api_key_env: str = "GEMINI_API_KEY"
    ):
        # Initialize Gemini client
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise ValueError(f"Environment variable {api_key_env} not set")
        self.client = Client(api_key=api_key)
        self.model = model
        logger.info(f"Initialized Google GenAI client with model '{self.model}'")
        # Initialize RAG retriever with your rubric text
        rubric_path = os.getenv("RUBRIC_PATH", "math_difficulty_rubric.txt")
        self.retriever = RAGRetriever(doc_path=rubric_path)

    def summarize(self, image: Image.Image) -> str:
        # Convert PIL image to JPEG bytes
        with io.BytesIO() as buf:
            image.save(buf, format="JPEG")
            img_bytes = buf.getvalue()

        instruction = (
            "Read and analyze the math problem shown in the image. "
            "Summarize it in detail: problem type, key values, question, "
            "and any implicit concepts or steps."
        )

        contents = [
            types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
            instruction
        ]
        logger.info("Sending summarization request to Gemini...")
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents
        )
        summary = response.text.strip()
        logger.info("Received summary from Gemini.")
        return summary

    def predict_difficulty(self, summary: str) -> str:
        # Retrieve top‐5 rubric chunks
        chunks = self.retriever.retrieve(summary, k=5)
        context = "\n\n".join(chunks)

        prompt = (
            f"You are an AI math expert using the following rubric information:\n\n"
            f"{context}\n\n"
            f"Problem Summary: {summary}\n\n"
            "Based on the rubric, predict:\n"
            "1. Difficulty Level (Novice, Beginner, Intermediate, Advanced, Expert)\n"
            "2. Predicted Grade Level (G1–G12)\n"
            "Provide your answer clearly."
        )

        logger.info("Sending difficulty prediction request to Gemini...")
        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt]
        )
        result = response.text.strip()
        logger.info("Received difficulty prediction from Gemini.")
        return result