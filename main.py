from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from googletrans import Translator
import openai
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"]
  # For production, set this to your domain only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Translator instance
translator = Translator()

# Business context for GPT
BUSINESS_CONTEXT = """
You are an AI assistant for a local coaching center in India.
You answer in simple, friendly language.

Sample FAQs:
Q: क्या क्लासेस ऑनलाइन हैं?
A: हां, हमारी क्लासेस ऑनलाइन और ऑफलाइन दोनों होती हैं।
Q: फीस कितनी है?
A: कोर्स के अनुसार फीस अलग-अलग होती है। कृपया कोर्स बताएं।
Q: डेमो क्लास मिलता है क्या?
A: हां, एक फ्री डेमो क्लास उपलब्ध है।
"""

# Request model from frontend
class UserInput(BaseModel):
    user_input: str

# POST route to handle chat
@app.post("/")
async def chat(data: UserInput):
    translated = translator.translate(data.user_input, src="hi", dest="en")
    english_input = translated.text

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": BUSINESS_CONTEXT},
            {"role": "user", "content": english_input}
        ]
    )

    english_reply = response['choices'][0]['message']['content']
    final_reply = translator.translate(english_reply, src="en", dest="hi").text

    return JSONResponse(content={"reply": final_reply})
