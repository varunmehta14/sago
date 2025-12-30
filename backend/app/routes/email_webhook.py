"""
Email Webhook Endpoint for receiving pitch decks via email
"""
from fastapi import APIRouter, Form, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from app.services.pdf_parser import PDFParser
from app.services.langgraph_agents import PitchDeckVerificationGraph
from app.services.email_service import EmailService
from email import message_from_string
from email.policy import default
import os
import uuid
import tempfile
from typing import Optional

router = APIRouter(prefix="/api/email", tags=["email"])

pdf_parser = PDFParser()
langgraph_agent = PitchDeckVerificationGraph()
email_service = EmailService()


@router.post("/webhook")
async def email_webhook(
    request: Request,
    sender: str = Form(...),
    subject: str = Form(...),
    recipient: str = Form(None),
    body_plain: str = Form(None),
    body_html: str = Form(None),
    attachment_count: int = Form(0)
):
    """
    Mailgun email webhook endpoint
    Receives emails with pitch deck PDFs and sends analysis results
    """
    print(f"📧 Received email from {sender}")
    print(f"   Subject: {subject}")
    print(f"   Attachments: {attachment_count}")
    
    try:
        # Get all form data
        form_data = await request.form()
        
        # Find PDF attachment
        pdf_file = None
        for key in form_data:
            if key.startswith('attachment-'):
                file = form_data[key]
                if isinstance(file, UploadFile) and file.filename.endswith('.pdf'):
                    pdf_file = file
                    break
        
        if not pdf_file:
            return JSONResponse({
                "status": "error",
                "message": "No PDF attachment found"
            }, status_code=400)
        
        # Save PDF temporarily
        temp_file_path = f"/tmp/{uuid.uuid4()}.pdf"
        with open(temp_file_path, "wb") as f:
            content = await pdf_file.read()
            f.write(content)
        
        # Extract text from PDF
        text = pdf_parser.extract_text(temp_file_path)
        
        print(f"📄 Extracted {len(text)} characters from PDF")
        
        # Run analysis
        print("🚀 Running multi-agent analysis...")
        result = await langgraph_agent.analyze_pitch_deck(text)
        
        # Send results via email
        print(f"📤 Sending results to {sender}")
        email_sent = email_service.send_analysis_results(
            to_email=sender,
            company_name=result.get('company_name', 'Unknown'),
            verification_results=result.get('verification_results', []),
            questions=result.get('questions', []),
            summary=result.get('summary', {})
        )
        
        # Clean up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        if email_sent:
            print(f"✅ Analysis sent to {sender}")
            return JSONResponse({
                "status": "success",
                "message": f"Analysis sent to {sender}"
            })
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def email_health():
    """Health check for email webhook"""
    return {"status": "healthy", "service": "email-webhook"}
