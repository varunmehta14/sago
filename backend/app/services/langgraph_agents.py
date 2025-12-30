"""
LangGraph Multi-Agent Workflow for Pitch Deck Verification
"""
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from google import genai
from app.services.agent_tools import VerificationTools
from app.config import get_settings
import json
import re


# Define the state that flows through the graph
class AgentState(TypedDict):
    pitch_deck_text: str
    company_name: str
    claims: List[Dict[str, Any]]
    research_results: List[Dict[str, Any]]
    verification_results: List[Dict[str, Any]]
    questions: List[str]
    current_step: str


class PitchDeckVerificationGraph:
    """LangGraph workflow for multi-agent pitch deck verification"""

    def __init__(self):
        settings = get_settings()
        self.client = genai.Client(api_key=settings.google_api_key)
        self.model_name = "gemini-2.5-flash-lite"
        self.tools = VerificationTools()
        self.workflow = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)

        # Add nodes for each agent
        workflow.add_node("extract_claims", self.extract_claims_node)
        workflow.add_node("research_claims", self.research_claims_node)
        workflow.add_node("verify_claims", self.verify_claims_node)
        workflow.add_node("generate_questions", self.generate_questions_node)

        # Define the flow
        workflow.set_entry_point("extract_claims")
        workflow.add_edge("extract_claims", "research_claims")
        workflow.add_edge("research_claims", "verify_claims")
        workflow.add_edge("verify_claims", "generate_questions")
        workflow.add_edge("generate_questions", END)

        return workflow.compile()

    def extract_claims_node(self, state: AgentState) -> AgentState:
        """
        Agent 1: Claim Extractor
        Extracts verifiable claims from the pitch deck
        """
        print("🔍 Agent 1: Extracting claims...")

        prompt = f"""
        You are a senior investment analyst. Analyze this pitch deck and extract ALL verifiable claims.

        Focus on:
        1. Market size and growth claims (TAM, SAM, SOM, CAGR)
        2. Company metrics (revenue, users, growth rate, MRR, ARR)
        3. Technology performance claims (speed, accuracy, efficiency)
        4. Team credentials (previous companies, roles, years of experience)
        5. Competitive advantages and differentiators
        6. Customer/traction metrics

        Pitch Deck:
        {state['pitch_deck_text'][:3000]}

        Also identify the company name if mentioned.

        Return a JSON object with:
        {{
            "company_name": "company name or 'Unknown'",
            "claims": [
                {{
                    "claim": "exact claim text",
                    "category": "market|revenue|technology|team|competitive|traction",
                    "importance": "high|medium|low",
                    "needs_verification": true|false
                }}
            ]
        }}

        Return ONLY valid JSON, no other text.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
        except Exception as e:
            print(f"❌ Error calling Gemini API in extract_claims_node: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            state['claims'] = []
            state['company_name'] = 'Unknown'
            state['current_step'] = 'claims_extraction_failed'
            return state

        try:
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response.text)
            if json_match:
                result = json.loads(json_match.group())
                state['claims'] = result.get('claims', [])
                state['company_name'] = result.get('company_name', 'Unknown')
            else:
                # Fallback if JSON parsing fails
                state['claims'] = [{
                    "claim": "Unable to extract structured claims",
                    "category": "general",
                    "importance": "low",
                    "needs_verification": False
                }]
                state['company_name'] = 'Unknown'
        except Exception as e:
            print(f"❌ Error in extract_claims_node: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            state['claims'] = []
            state['company_name'] = 'Unknown'

        state['current_step'] = 'claims_extracted'
        print(f"✅ Extracted {len(state['claims'])} claims")
        return state

    def research_claims_node(self, state: AgentState) -> AgentState:
        """
        Agent 2: Research Agent
        Uses tools to gather data for verifying claims
        """
        print("🔎 Agent 2: Researching claims...")

        research_results = []

        # Research top 3 high-importance claims to avoid rate limits
        high_priority_claims = [
            c for c in state['claims']
            if c.get('importance') == 'high' and c.get('needs_verification', True)
        ][:3]

        for claim_obj in high_priority_claims:
            claim = claim_obj['claim']
            category = claim_obj['category']

            print(f"  Researching: {claim[:60]}...")

            # Use appropriate tool based on claim category
            research_data = ""

            if category == "market":
                research_data = self.tools.search_market_data(claim)
            elif category == "team":
                # Extract person name from claim
                research_data = self.tools.search_person(claim, state['company_name'])
            elif category == "technology":
                research_data = self.tools.search_technology(claim)
            elif category == "competitive":
                research_data = self.tools.analyze_competitor(claim, "")
            elif category in ["revenue", "traction"]:
                research_data = self.tools.search_company_info(state['company_name'])
            else:
                research_data = self.tools.web_search(claim)

            research_results.append({
                "claim": claim,
                "category": category,
                "research_data": research_data[:1000]  # Limit to avoid token overload
            })

        state['research_results'] = research_results
        state['current_step'] = 'research_complete'
        print(f"✅ Researched {len(research_results)} claims")
        return state

    def verify_claims_node(self, state: AgentState) -> AgentState:
        """
        Agent 3: Verification Agent
        Analyzes claims against research data
        """
        print("✓ Agent 3: Verifying claims...")

        verification_results = []

        for research in state['research_results']:
            claim = research['claim']
            research_data = research['research_data']

            prompt = f"""
            You are a fact-checker for investor due diligence.

            Claim to verify: "{claim}"

            Research data found:
            {research_data}

            Provide:
            1. Verification Status: [Verified / Partially Verified / Cannot Verify / Red Flag]
            2. Evidence: What supports or contradicts this claim?
            3. Confidence Level: [High / Medium / Low]
            4. Red Flags: Any concerns or inconsistencies?
            5. Next Steps: How should the investor verify this further?

            Be thorough but concise. Focus on facts.
            """

            response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

            verification_results.append({
                "claim": claim,
                "verification_result": response.text,
                "research_summary": research_data[:300]
            })

        state['verification_results'] = verification_results
        state['current_step'] = 'verification_complete'
        print(f"✅ Verified {len(verification_results)} claims")
        return state

    def generate_questions_node(self, state: AgentState) -> AgentState:
        """
        Agent 4: Question Generator
        Generates personalized questions based on verification
        """
        print("❓ Agent 4: Generating questions...")

        # Summarize verification results
        verification_summary = "\n\n".join([
            f"Claim: {v['claim']}\nVerification: {v['verification_result'][:200]}..."
            for v in state['verification_results']
        ])

        prompt = f"""
        You are helping an investor prepare for a meeting with the {state['company_name']} founder.

        Based on the verification results below, generate 10-12 specific, insightful questions.

        Focus on:
        - Unverified or questionable claims
        - Red flags or inconsistencies
        - Missing information or gaps
        - Critical assumptions that need validation
        - Market positioning and competitive dynamics

        Verification Summary:
        {verification_summary}

        Generate questions that:
        1. Show you've done your homework
        2. Get to the heart of the business model
        3. Reveal risks and assumptions
        4. Help assess founder credibility

        Return as a numbered list (1., 2., 3., etc.)
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        # Parse questions
        questions = []
        for line in response.text.split('\n'):
            match = re.match(r'^\d+[\.\)]\s*(.+)$', line.strip())
            if match:
                questions.append(match.group(1))

        state['questions'] = questions
        state['current_step'] = 'complete'
        print(f"✅ Generated {len(questions)} questions")
        return state

    async def analyze_pitch_deck(self, pitch_deck_text: str) -> Dict[str, Any]:
        """
        Run the full multi-agent workflow
        """
        print("\n🚀 Starting LangGraph Multi-Agent Verification Workflow\n")

        # Initialize state
        initial_state = AgentState(
            pitch_deck_text=pitch_deck_text,
            company_name="Unknown",
            claims=[],
            research_results=[],
            verification_results=[],
            questions=[],
            current_step="initialized"
        )

        # Run the workflow
        final_state = self.workflow.invoke(initial_state)

        print("\n✅ Workflow Complete!\n")

        # Format response
        return {
            "company_name": final_state['company_name'],
            "claims": final_state['claims'],
            "verification_results": final_state['verification_results'],
            "questions": final_state['questions'],
            "summary": {
                "total_claims": len(final_state['claims']),
                "verified_claims": len(final_state['verification_results']),
                "questions_generated": len(final_state['questions'])
            }
        }
