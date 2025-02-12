# main.py

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Medical Chatbot",
    description="A simple chatbot that uses OpenAI's GPT-3 to answer medical questions.",
    version="1.0.0"
)

app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

