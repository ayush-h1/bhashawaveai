from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # ✅ Define app FIRST

# ✅ Then add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... your routes below ...


from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi import Request
from pydantic import BaseModel

import openai
from googletrans import Translator
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class UserInput(BaseModel):
    user_input: str

@app.post("/")
async def post_chat(data: UserInput, request: Request):
    translated = translator.translate(data.user_input, src="hi", dest="en")
    ...


translator = Translator()



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



@app.post("/", response_class=HTMLResponse)
async def post_chat(request: Request, message: str = Form(...)):
    translated = translator.translate(message, src="hi", dest="en")
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

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "messages": [{"role": "user", "content": message}, {"role": "bot", "content": final_reply}]
    })
