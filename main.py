from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os

# Load environment variables (includes OPENAI_API_KEY)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# ✅ Set the exact origin of your frontend (Render deploy URL)
origins = [
    "https://frontend4-5y6k.onrender.com"
]

# ✅ Add CORS middleware immediately after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ✅ React dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body
class UserInput(BaseModel):
    user_input: str

# POST route to handle chat
@app.post("/")
async def chat_endpoint(data: UserInput):
    user_message = data.user_input

    # Example GPT-style reply (replace with real OpenAI call later)
    reply = f"आपने कहा: {user_message}"

    return {"reply": reply}
