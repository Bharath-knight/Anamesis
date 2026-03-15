from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json, os
from dotenv import load_dotenv

from prompts import SYSTEM_PROMPT
from models import MedicationTimeline

load_dotenv()

app = FastAPI(title="Medication Timeline API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoteRequest(BaseModel):
    note: str

@app.post("/extract", response_model=MedicationTimeline)
async def extract_timeline(req: NoteRequest):
    if not req.note.strip():
        raise HTTPException(status_code=400, detail="Note cannot be empty.")
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": SYSTEM_PROMPT + "\n\nNote:\n" + req.note,
                "stream": False,
                "options": { "temperature": 0.1 }
            }
        )
        raw = response.json()["response"]
        raw = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)
        return MedicationTimeline(**data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Model returned invalid JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}