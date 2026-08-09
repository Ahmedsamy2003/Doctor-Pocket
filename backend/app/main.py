from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.models.model_loader import (
    get_model_and_tokenizer,
    generate_answer,
)



app = FastAPI(
    title="Doctor Pocket API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    question: str


class GenerateResponse(BaseModel):
    answer: str


@app.on_event("startup")
def load_model_on_startup():
    print("\nStarting Doctor Pocket API...")
    get_model_and_tokenizer()
    print("Doctor Pocket API is ready!")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "Doctor Pocket API",
    }


@app.post("/api/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question must not be empty.",
        )

    try:
        answer = generate_answer(question)

        return GenerateResponse(
            answer=answer
        )

    except Exception as e:
        print(f"Generation error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer.",
        )