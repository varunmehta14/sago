from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.pdf_parser import PDFParser
from app.services.gemini_service import GeminiService
from app.services.langgraph_agents import PitchDeckVerificationGraph
from app.config import get_settings
import os
import uuid
from typing import Dict, List

router = APIRouter(prefix="/api/pitch-deck", tags=["pitch-deck"])

pdf_parser = PDFParser()
gemini_service = GeminiService()
langgraph_agent = PitchDeckVerificationGraph()


@router.post("/upload")
async def upload_pitch_deck(file: UploadFile = File(...)) -> Dict:
    """Upload a pitch deck PDF for analysis"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    settings = get_settings()
    os.makedirs(settings.upload_dir, exist_ok=True)

    # Save file with unique ID
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Extract text from PDF
    try:
        text = pdf_parser.extract_text(file_path)
        structured_info = pdf_parser.extract_structured_info(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing PDF: {str(e)}")

    return {
        "file_id": file_id,
        "filename": file.filename,
        "text_preview": text[:500] + "..." if len(text) > 500 else text,
        "word_count": structured_info["word_count"],
        "message": "Pitch deck uploaded successfully"
    }


@router.post("/analyze/{file_id}")
async def analyze_pitch_deck(file_id: str) -> Dict:
    """Analyze pitch deck: extract claims, verify them, and generate questions"""
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Pitch deck not found")

    # Extract text
    text = pdf_parser.extract_text(file_path)

    # Step 1: Extract claims
    claims = await gemini_service.extract_claims(text)

    # Step 2: Verify top claims (limit to avoid rate limits)
    verification_results = []
    for claim in claims[:3]:  # Verify top 3 claims
        result = await gemini_service.verify_claim(claim.get("claim", str(claim)))
        verification_results.append(result)

    # Step 3: Generate questions
    questions = await gemini_service.generate_questions(text, verification_results)

    return {
        "file_id": file_id,
        "claims": claims,
        "verification_results": verification_results,
        "questions": questions,
        "summary": {
            "total_claims": len(claims),
            "verified_claims": len(verification_results),
            "questions_generated": len(questions)
        }
    }


@router.post("/analyze-with-agents/{file_id}")
async def analyze_with_agents(file_id: str) -> Dict:
    """
    🚀 ADVANCED: Analyze pitch deck using LangGraph Multi-Agent Workflow

    This endpoint uses a sophisticated multi-agent system:
    - Agent 1: Claim Extractor - Extracts all verifiable claims
    - Agent 2: Research Agent - Uses web search tools to gather verification data
    - Agent 3: Verification Agent - Analyzes claims against research
    - Agent 4: Question Generator - Creates personalized questions

    Agents have access to tools:
    - Web search (DuckDuckGo)
    - Company research
    - Market data lookup
    - Team credential verification
    - Competitor analysis
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Pitch deck not found")

    # Extract text
    text = pdf_parser.extract_text(file_path)

    # Run LangGraph multi-agent workflow
    try:
        result = await langgraph_agent.analyze_pitch_deck(text)
        result['file_id'] = file_id
        result['method'] = 'langgraph_multi_agent'
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent workflow failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "pitch-deck-analyzer"}
