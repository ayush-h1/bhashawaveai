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

# Create app FIRST
app = FastAPI()

# Add CORS Middleware IMMEDIATELY after creating app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init translator
translator = Translator()

# Pydantic model
class UserInput(BaseModel):
    user_input: str

# GPT system prompt
BUSINESS_CONTEXT = """
You are an AI assistant for a local coaching center in India.
Answer questions in friendly, simple Hindi.
"""

# POST route
@app.post("/")
async def post_chat(data: UserInput, request: Request):
    # Translate input
    english_input = translator.translate(data.user_input, src="hi", dest="en").text

    # Ask GPT
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
