# 🚀 Sago Pitch Deck Analyzer

AI-powered pitch deck verification and question generation system for investors.

> **"Seamless Integration, Hyper-Personalization, True Agency"**

## 📺 Demo Videos

### Web Interface Demo
https://github.com/varunmehta14/sago/blob/main/Sago-website.mov

Watch the web interface in action: Upload a pitch deck PDF, run multi-agent analysis, and get instant verification results with personalized questions.

### Gmail Integration Demo
https://github.com/varunmehta14/sago/blob/main/Sago-email.mov

See the Gmail integration: Send "Hey Sago, analyze this pitch deck" with a PDF attachment, and receive a beautifully formatted analysis email automatically.

## 📐 System Architecture

### High-Level Architecture
![System Architecture](https://raw.githubusercontent.com/varunmehta14/sago/main/docs/architecture.png)

The system consists of three main layers:
- **User Interfaces** (Web + Gmail)
- **Backend API** (FastAPI + Multi-Agent System)
- **External Services** (Gemini AI + DuckDuckGo Search)

### Multi-Agent Workflow
![Multi-Agent Workflow](https://raw.githubusercontent.com/varunmehta14/sago/main/docs/multi-agent-workflow.png)

The LangGraph orchestrator coordinates 4 specialized AI agents:
1. **Claim Extractor** - Extracts 27 claims from pitch deck
2. **Research Agent** - Searches web for top 3 claims
3. **Verification Agent** - Verifies claims with research data
4. **Question Generator** - Generates 12 investor questions

**Processing Time:** ~60 seconds | **Cost:** $0 (free tier)

## Overview

This application implements **Use Case 2** from the Sago assignment: An investor receives a pitch deck in PDF and wants to verify the information and generate personalized questions to ask the founder.

### ✨ Key Features

✅ **Two Analysis Interfaces:**
- **Web App** (Next.js + React) - Manual upload and analysis
- **Gmail Integration** (Google Apps Script) - Automatic email-based analysis

✅ **Multi-Agent AI System:**
- 4 specialized agents working together (LangGraph)
- Real-time web search for claim verification
- Evidence-based verification with sources

✅ **Seamless Workflow:**
- No new apps to download
- Works with existing Gmail workflow
- Trigger-based analysis ("hey sago" activates the system)

✅ **Beautiful Results:**
- Professional HTML email formatting
- Detailed verification results
- Personalized investor questions

### Design Principles

#### 1. Seamless Integration
- **Web-based interface** accessible from any browser
- **Gmail integration** - Email "hey sago" with PDF attachment → get automated analysis
- **Google Apps Script** - Runs every 5 minutes, monitors Gmail automatically
- **No new apps to download** - Works with existing workflow

#### 2. Hyper-Personalization
- Analyzes specific claims from each unique pitch deck
- Generates customized questions based on verification results
- Adapts analysis focus based on claim categories (market, revenue, technology, team)

#### 3. True Agency
- Automatically extracts and categorizes claims from pitch decks
- Proactively verifies information using AI
- Generates actionable questions for investor-founder meetings

## 🚀 Advanced Feature: LangGraph Multi-Agent System

This application includes **two analysis modes**:

### 1. Simple AI Analysis (Gemini)
- Fast analysis using Google Gemini
- Knowledge-based verification
- ~30 seconds processing time

### 2. Advanced Multi-Agent Analysis (LangGraph) ⭐
- **4 specialized AI agents** working together
- **Real-time web search** for claim verification
- **6+ research tools** (market data, company lookup, team credentials)
- **Deep verification** with evidence sources
- ~60-90 seconds processing time

**Agent Workflow:**
```
Agent 1: Claim Extractor → Agent 2: Research Agent (web search) →
Agent 3: Verification Agent → Agent 4: Question Generator
```

For details, see **[LANGGRAPH_AGENTS.md](LANGGRAPH_AGENTS.md)**

## 📧 Gmail Integration (Seamless Integration)

Sago integrates directly with your Gmail inbox - **no new apps needed!**

### How It Works

1. **Send email** to your Gmail account
2. **Write trigger phrase** in email body: "Hey Sago, analyze this pitch deck"
3. **Attach** pitch deck PDF
4. **Wait ~5 minutes** - Google Apps Script runs automatically
5. **Receive analysis** as a reply email with beautiful formatting

### Features

- ✅ **Automatic monitoring** - Script checks Gmail every 5 minutes
- ✅ **Trigger-based** - Only processes emails with "hey sago" phrases
- ✅ **Auto-labeling** - Processed emails labeled as "Sago/Analyzed"
- ✅ **No duplicates** - Each email analyzed only once
- ✅ **Beautiful emails** - Professional HTML formatting with colored summaries

### Setup

See **[GOOGLE_APPS_SCRIPT_SETUP.md](GOOGLE_APPS_SCRIPT_SETUP.md)** for complete instructions.

**Quick Start:**
1. Go to https://script.google.com
2. Copy code from `google-apps-script/Code.gs`
3. Set up 5-minute trigger
4. Done! 🎉

## Architecture

### Tech Stack

**Backend:**
- FastAPI (Python 3.11)
- Google Gemini API (Free tier - gemini-2.5-flash-lite)
- **LangGraph** for multi-agent orchestration
- **LangChain** for agent tools and utilities
- PyPDF2 for PDF parsing
- Pydantic for data validation
- DuckDuckGo Search (no API key needed)
- **Gmail SMTP** for sending analysis emails

**Frontend:**
- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS

**Integration Layer:**
- **Google Apps Script** - Gmail monitoring
- **Localtunnel** - Public URL for local development
- Gmail API - Email reading and labeling

### System Flow

```
1. User uploads pitch deck PDF
   ↓
2. Backend extracts text from PDF
   ↓
3. Gemini AI extracts key claims (market size, revenue, tech, team)
   ↓
4. Gemini AI verifies each claim and provides evidence/concerns
   ↓
5. Gemini AI generates personalized questions based on gaps
   ↓
6. Frontend displays verification results and questions
```

## Setup Instructions

### Prerequisites

- Python 3.11
- Node.js 18+ and npm
- Google Gemini API key (free from https://makersuite.google.com/app/apikey)

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create Python 3.11 virtual environment:**
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your Google API key:
# GOOGLE_API_KEY=your_actual_api_key_here
```

5. **Run the backend server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment variables:**
```bash
cp .env.local.example .env.local
# Default API URL is http://localhost:8000
```

4. **Run the development server:**
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Usage

1. Open `http://localhost:3000` in your browser
2. Click "Choose PDF File" and select a pitch deck
3. Click "Analyze Pitch Deck"
4. Wait for AI analysis (typically 30-60 seconds)
5. Review:
   - Extracted claims
   - Verification results for each claim
   - Personalized questions to ask the founder

## Sample Inputs and Outputs

### Sample Input
A typical pitch deck PDF containing:
- Market size claims (e.g., "$50B TAM")
- Growth metrics (e.g., "300% YoY growth")
- Customer numbers (e.g., "10,000 active users")
- Team credentials (e.g., "Ex-Google engineers")

### Sample Output

**Claims Extracted:** 8
**Verified Claims:** 5
**Questions Generated:** 10

**Example Verification Result:**
```
Claim: "The global SaaS market is worth $200B and growing at 25% annually"

Verification: Verified
Supporting Evidence: Multiple industry reports (Gartner, IDC) confirm the global
SaaS market was approximately $197B in 2023 with projected CAGR of 22-27% through 2030.

Concerns: None major. The numbers align with industry estimates.

Recommended Verification Steps:
- Ask which specific market segment they're targeting
- Verify their serviceable addressable market (SAM)
```

**Example Generated Questions:**
1. Can you break down your $50M revenue projection by customer segment and pricing tier?
2. What are the key assumptions behind your 300% growth rate, and what's your unit economics?
3. How do you plan to differentiate from [Competitor X] who has similar features?
4. Can you walk me through your customer acquisition cost and payback period?

## API Endpoints

### POST /api/pitch-deck/upload
Upload a pitch deck PDF

**Request:** multipart/form-data with PDF file
**Response:**
```json
{
  "file_id": "uuid",
  "filename": "pitch.pdf",
  "text_preview": "...",
  "word_count": 1234,
  "message": "Pitch deck uploaded successfully"
}
```

### POST /api/pitch-deck/analyze/{file_id}
Analyze uploaded pitch deck using **simple AI** (Gemini only)

**Response:**
```json
{
  "file_id": "uuid",
  "claims": [...],
  "verification_results": [...],
  "questions": [...],
  "summary": {...}
}
```

### POST /api/pitch-deck/analyze-with-agents/{file_id} 🚀
Analyze uploaded pitch deck using **advanced multi-agent system** (LangGraph)

**Features:**
- 4 specialized agents
- Real-time web search
- Tool-based verification
- Evidence-backed results

**Response:**
```json
{
  "file_id": "uuid",
  "company_name": "extracted company name",
  "method": "langgraph_multi_agent",
  "claims": [
    {
      "claim": "Market size is $200B",
      "category": "market",
      "importance": "high",
      "needs_verification": true
    }
  ],
  "verification_results": [
    {
      "claim": "...",
      "verification_result": "Verification Status: Verified\nEvidence: ...",
      "research_summary": "Web search results: ..."
    }
  ],
  "questions": ["Question 1", "Question 2", ...],
  "summary": {
    "total_claims": 12,
    "verified_claims": 5,
    "questions_generated": 10
  }
}
```

## Design Choices

### Why Gemini API?
- Free tier with generous limits
- Excellent reasoning capabilities for claim verification
- Good at generating contextual questions
- Easy to integrate with minimal code

### Why FastAPI?
- Fast, modern Python framework
- Automatic API documentation
- Built-in async support for AI API calls
- Type safety with Pydantic

### Why Next.js?
- Server and client components for optimal performance
- TypeScript support out of the box
- Excellent developer experience
- Easy deployment

### Why LangGraph?
- **Multi-agent orchestration** - Coordinate specialized agents
- **Tool integration** - Agents can use web search, APIs, databases
- **State management** - Complex workflows with state persistence
- **Real-time verification** - Access current data, not just training data
- **Transparency** - See what each agent researched and why
- **Extensible** - Easy to add new agents and tools

### Scalability Considerations

**Current Implementation:**
- Analyzes top 5 claims to avoid rate limits
- Synchronous processing

**Production Enhancements:**
- Queue system (Celery/Redis) for background processing
- Database (PostgreSQL) for storing analysis history
- Caching layer for common claims
- Webhook system for integration with Gmail/Slack
- User authentication and personalization
- Multiple AI providers for redundancy

## Future Enhancements

1. **Integration Layer:**
   - Gmail plugin to auto-analyze pitch decks from emails
   - Slack bot for team collaboration
   - Chrome extension for seamless workflow

2. **Personalization:**
   - User investment preferences and thesis
   - Historical interaction tracking
   - Custom question templates

3. **Agency:**
   - Automated follow-up scheduling
   - Market signal monitoring for re-engagement (Use Case 1)
   - Auto-generate meeting notes and action items

## License

MIT

## Contact

For questions about this implementation, please contact the developer.
