import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def create_client():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY not found. Check your .env file.")
    return Groq(api_key=key)

client = create_client()

def prompting(mood: str) -> str:
    system_prompt = """You must assume the role of an English writing professor.
The user enters a specific mood or emotion.
Your job is to create an evocative and interesting writing prompt solely
in accordance with that specific mood without driving the user towards
a specific plot or idea. Do not end on an instructional note.
Only output the prompt, nothing else. Keep it to 2-3 sentences, do not exceed 30 words total.
Generate a new prompt each time, no repetition of same prompt allowed."""

    user_message = f"I'm currently feeling {mood}. Give me a writing prompt"

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            max_tokens=300,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
    except Exception as e:
        raise RuntimeError(f"Groq API call failed: {e}")

    return response.choices[0].message.content.strip()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MoodRequest(BaseModel):
    mood: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/generate-prompt")
def generate_prompt(data: MoodRequest):
    mood = data.mood.strip()
    if not mood:
        raise HTTPException(status_code=400, detail="Mood cannot be empty")

    try:
        prompt_text = prompting(mood)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "success",
        "mood": mood,
        "prompt": prompt_text
    }