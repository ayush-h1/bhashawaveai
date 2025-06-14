from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Set your frontend domain here (e.g., from Render)
frontend_url = "https://frontend4-5y6k.onrender.com"

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # ✅ Use exact frontend URL, not "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Translator instance
translator = Translator()

# Business context for OpenAI
BUSINESS_CONTEXT = """
You are an AI assistant for a local coaching center in India.
You answer in simple, friendly Hindi.

Sample FAQs:
Q: क्या क्लासेस ऑनलाइन हैं?
A: हां, हमारी क्लासेस ऑनलाइन और ऑफलाइन दोनों होती हैं।
Q: फीस कितनी है?
A: कोर्स के अनुसार फीस अलग-अलग होती है। कृपया कोर्स बताएं।
Q: डेमो क्लास मिलता है क्या?
A: हां, एक फ्री डेमो क्लास उपलब्ध है।
"""

# Request model
class UserInput(BaseModel):
    user_input: str

# POST endpoint
@app.post("/")
async def chat_api(data: UserInput):
    try:
        # Translate Hindi to English
     from deep_translator import GoogleTranslator

# Hindi to English


# ... AI processing ...

# English to Hindi
from deep_translator import GoogleTranslator

# Hindi to English
english_input = GoogleTranslator(source='hi', target='en').translate(data.user_input)

# ... AI processing ...

# English to Hindi
final_reply = GoogleTranslator(source='en', target='hi').translate(english_reply)

        # Get OpenAI response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": BUSINESS_CONTEXT},
                {"role": "user", "content": english_input}
            ]
        )

        english_reply = response['choices'][0]['message']['content']

        # Translate back to Hindi
        final_reply = translator.translate(english_reply, src='en', dest='hi').text

        return JSONResponse(content={"reply": final_reply})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

