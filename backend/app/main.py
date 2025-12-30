from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import pitch_deck, email_webhook

app = FastAPI(
    title="Sago Pitch Deck Analyzer",
    description="AI-powered pitch deck verification and question generation",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pitch_deck.router)
app.include_router(email_webhook.router)


@app.get("/")
async def root():
    return {
        "message": "Sago Pitch Deck Analyzer API",
        "docs": "/docs",
        "version": "1.0.0"
    }
