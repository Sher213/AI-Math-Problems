import os
import io
import logging
from PIL import Image
from google.genai import Client, types
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MathProblemSummarizer:
    def __init__(self,
                 model: str = "gemini-2.5-flash",
                 api_key_env: str = "GEMINI_API_KEY"):
        """
        Summarizer backed by Google GenAI Gemini.
        Expects your API key in the environment variable named by `api_key_env`.
        """
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise ValueError(f"Environment variable {api_key_env} not set")
        self.client = Client(api_key=api_key)
        self.model = model
        logger.info(f"Initialized Google GenAI client with model '{self.model}'")

    def summarize(self, image: Image.Image) -> str:
        """
        Sends the image and a prompt to Gemini to get a detailed math-problem summary.
        """
        # 1. Encode image as JPEG bytes
        with io.BytesIO() as buf:
            image.save(buf, format="JPEG")
            image_bytes = buf.getvalue()

        # 2. Build contents: first the image, then the instruction
        instruction = (
            "Read and analyze the math problem shown in the image. Summarize it in detail, including:\n"
            "1. The type of problem (e.g., arithmetic, geometry, algebra)\n"
            "2. The important given values and variables\n"
            "3. The question being asked\n"
            "4. Any implicit concepts or steps needed to solve it\n\n"
            "Provide the summary in clear, complete sentences understandable by a student or teacher."
        )

        contents = [
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            instruction
        ]

        # 3. Call the Gemini model
        logger.info("Sending request to Gemini...")
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents
        )

        # 4. Return the text
        summary = response.text.strip()
        logger.info("Received summary from Gemini.")
        return summary