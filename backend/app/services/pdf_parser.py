import PyPDF2
from typing import Dict, List


class PDFParser:
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    @staticmethod
    def extract_structured_info(text: str) -> Dict:
        """Extract key information from pitch deck text"""
        # This is a simplified version - in production, you'd use more sophisticated parsing
        return {
            "full_text": text,
            "length": len(text),
            "word_count": len(text.split())
        }
