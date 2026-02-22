from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_router

app = FastAPI()

# Enable CORS so the C# backend and frontend can talk to the AI_Sevice
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, tags=["Chatbot"])

@app.get("/")
async def root():
    return {"message": "Good day, how have you been today?"}