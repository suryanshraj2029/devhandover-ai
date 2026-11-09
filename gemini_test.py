
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: API key not found. Check your .env file.")

else:
    try:
        print("Connecting to Gemini...")

        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=120000)
        )

        print("Sending test request...")

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents="Reply with: Gemini connected!",
            config=types.GenerateContentConfig(
                max_output_tokens=20
            )
        )

        print("\nSUCCESS!")
        print(response.text)

    except Exception as e:
        print("\nCONNECTION FAILED")
        print("Error:", str(e))
