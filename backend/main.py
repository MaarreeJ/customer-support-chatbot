from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="Customer Support AI",
    version="1.0.0",
    description="AI-powered Customer Support Assistant using a Hugging Face DPO model",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Customer Support AI Backend Running 🚀",
        "version": "1.0.0",
    }