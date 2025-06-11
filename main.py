from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from googletrans import Translator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize app and translator
app = FastAPI()
translator = Translator()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] for strict mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input schema
class UserInput(BaseModel):
    user_input: str

# Business context (Hindi FAQs)
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

# POST endpoint for chat
@app.post("/")
async def post_chat(data: UserInput, request: Request):
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
    final_reply = translator.translate(english_reply, src='en', dest="hi").text

    return {"response": final_reply}
