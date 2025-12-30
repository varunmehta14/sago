"""
Email Service for sending analysis results via Gmail SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
from app.config import get_settings


class EmailService:
    """Service for sending emails via Gmail SMTP"""
    
    def __init__(self):
        settings = get_settings()
        self.gmail_address = settings.gmail_address
        self.gmail_app_password = settings.gmail_app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_analysis_results(
        self, 
        to_email: str, 
        company_name: str,
        verification_results: List[Dict],
        questions: List[str],
        summary: Dict
    ) -> bool:
        """Send pitch deck analysis results via email"""
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"✅ Pitch Deck Analysis: {company_name}"
        msg['From'] = f"Sago Analysis <{self.gmail_address}>"
        msg['To'] = to_email
        
        # Format results as HTML email
        html_body = self._format_html_email(
            company_name, verification_results, questions, summary
        )
        
        # Attach HTML body
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Send via Gmail SMTP
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.gmail_address, self.gmail_app_password)
                server.send_message(msg)
            print(f"✅ Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _format_html_email(
        self, 
        company_name: str,
        verification_results: List[Dict],
        questions: List[str],
        summary: Dict
    ) -> str:
        """Format analysis results as HTML email"""
        
        # Build verification results HTML
        verifications_html = ""
        for i, result in enumerate(verification_results, 1):
            verifications_html += f"""
            <div style="margin-bottom: 20px; padding: 15px; background: #f9fafb; border-left: 4px solid #4f46e5; border-radius: 4px;">
                <h3 style="margin-top: 0; color: #1f2937; font-size: 16px;">
                    {i}. {result['claim']}
                </h3>
                <div style="color: #4b5563; font-size: 14px; white-space: pre-wrap;">
                    {result['verification_result']}
                </div>
            </div>
            """
        
        # Build questions HTML
        questions_html = ""
        for i, question in enumerate(questions, 1):
            questions_html += f"""
            <li style="margin-bottom: 10px; color: #374151; font-size: 14px;">
                {question}
            </li>
            """
        
        # Complete HTML template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px 20px; border-radius: 8px; margin-bottom: 30px; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 28px;">🚀 Sago Analysis</h1>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">
                    Pitch Deck Verification Report
                </p>
            </div>
            
            <!-- Summary Cards -->
            <table style="width: 100%; margin-bottom: 30px;" cellpadding="0" cellspacing="0">
                <tr>
                    <td style="width: 33%; padding: 5px;">
                        <div style="background: #dbeafe; padding: 15px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #1e40af;">
                                {summary['total_claims']}
                            </div>
                            <div style="font-size: 12px; color: #1e3a8a; margin-top: 5px;">
                                Claims Extracted
                            </div>
                        </div>
                    </td>
                    <td style="width: 33%; padding: 5px;">
                        <div style="background: #d1fae5; padding: 15px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #047857;">
                                {summary['verified_claims']}
                            </div>
                            <div style="font-size: 12px; color: #065f46; margin-top: 5px;">
                                Verified Claims
                            </div>
                        </div>
                    </td>
                    <td style="width: 33%; padding: 5px;">
                        <div style="background: #e9d5ff; padding: 15px; border-radius: 8px; text-align: center;">
                            <div style="font-size: 24px; font-weight: bold; color: #7c3aed;">
                                {summary['questions_generated']}
                            </div>
                            <div style="font-size: 12px; color: #6b21a8; margin-top: 5px;">
                                Questions
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
            
            <!-- Company Name -->
            <h2 style="color: #1f2937; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px;">
                Company: {company_name}
            </h2>
            
            <!-- Verification Results -->
            <div style="margin-bottom: 30px;">
                <h2 style="color: #1f2937; margin-bottom: 20px;">
                    ✓ Verification Results
                </h2>
                {verifications_html}
            </div>
            
            <!-- Questions -->
            <div style="margin-bottom: 30px;">
                <h2 style="color: #1f2937; margin-bottom: 20px;">
                    ❓ Questions for the Founder
                </h2>
                <ol style="padding-left: 20px;">
                    {questions_html}
                </ol>
            </div>
            
            <!-- Footer -->
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280; font-size: 12px;">
                <p>🤖 Generated by Sago - AI-Powered Pitch Deck Analyzer</p>
                <p style="margin-top: 10px;">
                    <a href="https://github.com/varunmehta14/sago" style="color: #4f46e5; text-decoration: none;">
                        View on GitHub
                    </a>
                </p>
            </div>
            
        </body>
        </html>
        """
        
        return html
