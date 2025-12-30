from google import genai
from google.genai import types
from typing import Dict, List
from app.config import get_settings


class GeminiService:
    def __init__(self):
        settings = get_settings()
        self.client = genai.Client(api_key=settings.google_api_key)

    async def extract_claims(self, pitch_deck_text: str) -> List[Dict]:
        """Extract key claims from pitch deck"""
        prompt = f"""
        Analyze this pitch deck and extract all the key claims, facts, and statements that should be verified.
        Focus on:
        - Market size claims
        - Revenue/growth numbers
        - Customer numbers
        - Technology claims
        - Competitive advantages
        - Team credentials

        Pitch Deck Text:
        {pitch_deck_text}

        Return a JSON list of claims with the following structure:
        [
            {{
                "claim": "the actual claim text",
                "category": "market/revenue/technology/team/other",
                "importance": "high/medium/low"
            }}
        ]
        """

        response = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )
        return self._parse_claims_response(response.text)

    async def verify_claim(self, claim: str) -> Dict:
        """Verify a specific claim using Gemini's knowledge"""
        prompt = f"""
        You are a fact-checker for investor due diligence. Analyze this claim from a startup pitch deck:

        Claim: "{claim}"

        Provide:
        1. Verification status (Verified/Partially Verified/Cannot Verify/Potentially Misleading)
        2. Supporting evidence or reasoning
        3. Red flags or concerns (if any)
        4. Recommended verification steps

        Be thorough but concise.
        """

        response = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )
        return {
            "claim": claim,
            "verification_result": response.text
        }

    async def generate_questions(self, pitch_deck_text: str, verification_results: List[Dict]) -> List[str]:
        """Generate personalized questions based on verification results"""
        verification_summary = "\n".join([
            f"- {v['claim']}: {v.get('verification_result', 'Not verified')}"
            for v in verification_results
        ])

        prompt = f"""
        You are helping an investor prepare for a meeting with a startup founder.

        Based on the pitch deck and verification results below, generate 8-12 insightful questions
        the investor should ask the founder. Focus on:
        - Unverified or questionable claims
        - Gaps in the pitch
        - Critical assumptions
        - Market and competitive positioning
        - Business model sustainability
        - Team capabilities

        Pitch Deck Summary:
        {pitch_deck_text[:2000]}...

        Verification Results:
        {verification_summary}

        Generate questions that demonstrate the investor has done their homework and is serious about the opportunity.
        Return as a numbered list.
        """

        response = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )
        return self._parse_questions_response(response.text)

    def _parse_claims_response(self, response_text: str) -> List[Dict]:
        """Parse the claims from Gemini's response"""
        # Simple parsing - in production, you'd use more robust JSON parsing
        import json
        import re

        # Try to extract JSON from response
        json_match = re.search(r'\[[\s\S]*\]', response_text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass

        # Fallback: return raw text as single claim
        return [{
            "claim": response_text,
            "category": "general",
            "importance": "medium"
        }]

    def _parse_questions_response(self, response_text: str) -> List[str]:
        """Parse questions from Gemini's response"""
        # Extract numbered list items
        import re
        lines = response_text.split('\n')
        questions = []

        for line in lines:
            # Match numbered items like "1. Question text" or "1) Question text"
            match = re.match(r'^\d+[\.\)]\s*(.+)$', line.strip())
            if match:
                questions.append(match.group(1))

        return questions if questions else [response_text]
