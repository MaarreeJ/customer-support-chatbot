from fastapi import APIRouter
from pydantic import BaseModel

from inference import generate_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    answer = generate_answer(request.question)

    return ChatResponse(answer=answer)


@router.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "Customer Support AI Backend is running 🚀",
    }