# Sago Pitch Deck Analyzer - System Architecture

**Version:** 1.0
**Date:** December 30, 2024
**Author:** Varun Mehta

---

## Executive Summary

Sago is an AI-powered pitch deck analyzer that implements **Use Case 2** from the Sago assignment: helping investors verify pitch deck claims and generate personalized due diligence questions. The system embodies three core design principles:

1. **Seamless Integration** - Works within existing workflow (Gmail) without requiring new apps
2. **Hyper-Personalization** - Analyzes each pitch deck uniquely and generates custom questions
3. **True Agency** - Automatically extracts, verifies, and generates insights without manual intervention

This document describes the system architecture, design choices, and technical considerations for a production-ready implementation.

---

## 1. High-Level Architecture

### 1.1 System Components

The system consists of three main layers:

**1. User Interface Layer**
- Web application (Next.js + React)
- Gmail integration (Google Apps Script)

**2. Backend API Layer**
- FastAPI server (Python 3.11)
- PDF parsing service
- Multi-agent orchestration (LangGraph)
- Email service (Gmail SMTP)

**3. AI & External Services Layer**
- Google Gemini API (gemini-2.5-flash-lite)
- DuckDuckGo Search API
- Gmail API

### 1.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACES                               │
│  ┌─────────────────┐              ┌───────────────────┐         │
│  │  Web Interface  │              │ Gmail Integration │         │
│  │ (Next.js/React) │              │  (Apps Script)    │         │
│  └────────┬────────┘              └─────────┬─────────┘         │
└───────────┼───────────────────────────────────┼─────────────────┘
            │                                   │
            ▼                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                  BACKEND API (FastAPI)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │Upload Endpoint│  │    Analysis  │  │  Email Webhook   │      │
│  │  /upload      │  │   /analyze   │  │   /webhook       │      │
│  └──────┬────────┘  └──────┬───────┘  └─────────┬────────┘      │
│         │                  │                     │               │
│         └──────────────────┼─────────────────────┘               │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │           CORE SERVICES                                     │ │
│  │  ┌───────────┐  ┌────────────────┐  ┌─────────────┐       │ │
│  │  │PDF Parser │  │   LangGraph    │  │Email Service│       │ │
│  │  │ (PyPDF2)  │  │  Multi-Agent   │  │(Gmail SMTP) │       │ │
│  │  └───────────┘  └────────────────┘  └─────────────┘       │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────┼─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              AI AGENT WORKFLOW (LangGraph)                       │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌────────────┐   │
│  │  Agent1 ├──►│ Agent 2  ├──►│ Agent 3  ├──►│  Agent 4   │   │
│  │ Claim   │   │ Research │   │Verification│  │ Question   │   │
│  │Extractor│   │  (Web)   │   │            │  │ Generator  │   │
│  └────┬────┘   └────┬─────┘   └────┬─────┘   └─────┬──────┘   │
└───────┼─────────────┼──────────────┼───────────────┼───────────┘
        │             │              │               │
        ▼             ▼              ▼               ▼
┌─────────────────────────────────────────────────────────────────┐
│               EXTERNAL SERVICES                                  │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐      │
│  │ Google Gemini │  │  DuckDuckGo  │  │  Gmail SMTP     │      │
│  │      API      │  │  Search API  │  │    Server       │      │
│  └───────────────┘  └──────────────┘  └─────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Agent Workflow (LangGraph)

### 2.1 Agent Architecture

The system uses LangGraph to orchestrate four specialized AI agents that work sequentially:

**Agent 1: Claim Extractor**
- **Input:** Extracted PDF text
- **Task:** Identify quantifiable claims with importance scores
- **Output:** List of 20-30 claims with categories (market, revenue, growth, team, technology)
- **LLM Calls:** ~1 call

**Agent 2: Research Agent**
- **Input:** Top 3-5 high-importance claims
- **Task:** Conduct web searches to find verification data
- **Tools:** DuckDuckGo Search API
- **Output:** Research summaries with source URLs
- **LLM Calls:** 0 (search-only)

**Agent 3: Verification Agent**
- **Input:** Claims + Research data
- **Task:** Cross-reference claims against research to verify accuracy
- **Output:** Verification results with confidence scores
- **LLM Calls:** ~3-5 calls (one per researched claim)

**Agent 4: Question Generator**
- **Input:** All claims + Verification results
- **Task:** Generate personalized due diligence questions
- **Output:** 10-15 investor questions
- **LLM Calls:** ~1 call

### 2.2 Workflow State Management

LangGraph manages the workflow state as a typed dictionary:

```python
class PitchDeckState(TypedDict):
    text: str                        # Original PDF text
    claims: List[Dict]                # Extracted claims
    research_results: Dict            # Web search results
    verification_results: List[Dict]  # Verified claims
    questions: List[str]              # Generated questions
    company_name: str                 # Detected company
```

### 2.3 Performance Optimizations

**Selective Research**
- Only research top 3-5 claims (based on importance scores)
- Reduces API calls from 30+ to ~5
- Saves ~40 seconds in processing time

**Rate Limit Management**
- Uses free tier model (gemini-2.5-flash-lite)
- Implements exponential backoff for rate limit errors
- Caches verification results (future enhancement)

**Parallel Processing**
- Web searches executed concurrently
- Multiple LLM calls batched when possible

---

## 3. Design Choices & Rationale

### 3.1 Why LangGraph Over Simple LLM Calls?

**Problem:** Single LLM call cannot verify claims against real-time data.

**Solution:** Multi-agent system with web search capabilities.

**Benefits:**
- **Real-time verification** using current web data (not just training data)
- **Specialized agents** with focused responsibilities
- **Tool integration** (web search, APIs, databases)
- **Transparency** - See what each agent researched
- **Extensibility** - Easy to add new agents/tools

**Trade-offs:**
- Increased complexity (4 agents vs 1 LLM call)
- Longer processing time (60s vs 30s)
- More API calls (~32 vs ~3)
- Worth it for production-grade verification

### 3.2 Why Google Gemini API?

**Evaluation Criteria:**
- Cost (free tier)
- Reasoning capability
- API reliability
- Rate limits

**Comparison:**

| Provider | Cost (Free Tier) | Reasoning Quality | Rate Limits | Decision |
|----------|------------------|-------------------|-------------|----------|
| OpenAI GPT-4 | $0 trial, then $0.01/1K tokens | Excellent | 3 RPM | ❌ Expensive |
| Anthropic Claude | $0 trial only | Excellent | Limited | ❌ No free tier |
| Google Gemini | 15 RPM free tier | Very Good | 60 RPM | ✅ **Selected** |
| Llama 3 (Local) | Free | Good | Unlimited | ❌ Complex setup |

**Winner:** Google Gemini (gemini-2.5-flash-lite)
- Free 15 RPM permanently
- Sufficient reasoning for claim extraction & verification
- Reliable API with good documentation

### 3.3 Why DuckDuckGo Search?

**Requirements:**
- No API key required
- No cost
- Sufficient search quality

**Comparison:**

| Provider | Cost | API Key? | Search Quality | Decision |
|----------|------|----------|----------------|----------|
| Google Search API | $5/1000 queries | Yes | Excellent | ❌ Expensive |
| Bing Search API | $3/1000 queries | Yes | Very Good | ❌ Requires key |
| DuckDuckGo | Free | No | Good | ✅ **Selected** |
| SerpAPI | $50/month | Yes | Excellent | ❌ Expensive |

**Winner:** DuckDuckGo
- No API key or signup
- Instant searches via `ddgs` Python package
- Good enough for claim verification

### 3.4 Why Gmail Integration (Google Apps Script)?

**Design Principle:** Seamless Integration

**Rationale:**
- Investors already use Gmail for pitch deck emails
- No need to download new apps
- Works with existing workflow
- Trigger-based activation ("hey sago")

**Alternatives Considered:**

1. **Browser Extension**
   - ❌ Requires Chrome/Firefox download
   - ❌ Needs manual clicking
   - ✅ Real-time integration

2. **Gmail Add-on**
   - ❌ Complex Google Workspace approval process
   - ❌ Requires admin permissions
   - ✅ Native Gmail UI

3. **Google Apps Script** (Selected)
   - ✅ No downloads required
   - ✅ Runs on Google servers (always on)
   - ✅ Simple OAuth authorization
   - ✅ 5-minute automatic checking

### 3.5 Tech Stack Decisions

**Backend: FastAPI**
- Modern async Python framework
- Automatic API documentation (OpenAPI)
- Type safety with Pydantic
- Easy deployment to cloud services
- **Alternative:** Flask (older, less features)

**Frontend: Next.js 16**
- Server-side rendering for SEO
- TypeScript for type safety
- App Router for modern routing
- Easy Vercel deployment
- **Alternative:** Create React App (no SSR)

**PDF Parsing: PyPDF2**
- Simple text extraction
- No dependencies
- Works with most PDFs
- **Alternative:** pdfplumber (more features, heavier)

**Email: Gmail SMTP**
- Free (no SendGrid/Mailgun costs)
- HTML email support
- Built into Python (smtplib)
- **Alternative:** Mailgun (requires payment info)

---

## 4. System Workflows

### 4.1 Web Interface Workflow

```
1. User uploads PDF → Frontend
2. Frontend calls POST /api/pitch-deck/upload
3. Backend extracts text with PyPDF2
4. Backend returns file_id
5. Frontend calls POST /api/pitch-deck/analyze-with-agents/{file_id}
6. Backend triggers LangGraph workflow:
   a. Agent 1 extracts 27 claims
   b. Agent 2 researches top 3 claims (web search)
   c. Agent 3 verifies claims with research data
   d. Agent 4 generates 12 questions
7. Backend returns JSON results
8. Frontend displays:
   - Claims extracted (27)
   - Verified claims (3)
   - Generated questions (12)
```

**Total Time:** ~60 seconds

### 4.2 Gmail Integration Workflow

```
1. User sends email with "hey sago" + PDF attachment
2. Google Apps Script runs every 5 minutes
3. Script checks for:
   - Unprocessed emails (no "Sago/Analyzed" label)
   - PDF attachments
   - Trigger phrase ("hey sago", "sago analyze", etc.)
4. If found:
   a. Extract PDF from email
   b. Call POST /api/pitch-deck/upload
   c. Call POST /api/pitch-deck/analyze-with-agents/{file_id}
   d. Receive analysis results
   e. Format as beautiful HTML email
   f. Send reply via Gmail SMTP
   g. Add "Sago/Analyzed" label to original email
5. User receives analysis email in ~5-7 minutes
```

**Total Time:** Up to 5 minutes (trigger) + 60 seconds (analysis) = ~6 minutes

### 4.3 Error Handling & Edge Cases

**Scenario 1: PDF with no text (images only)**
- PyPDF2 returns empty string
- Agent 1 returns error: "No extractable text"
- System returns helpful message to user

**Scenario 2: Rate limit exceeded**
- Gemini API returns 429 error
- System implements exponential backoff
- Retries after 60 seconds
- If still failing, returns error to user

**Scenario 3: Invalid trigger phrase**
- Google Apps Script logs: "Skipped - no trigger phrase"
- No email sent, no label added
- Silent failure (by design)

**Scenario 4: Network timeout during research**
- DuckDuckGo search fails
- Agent 2 returns empty research results
- Agent 3 marks claims as "Unable to verify (no web data)"
- Continues with question generation

---

## 5. Scalability & Production Considerations

### 5.1 Current Limitations

1. **Synchronous Processing**
   - Blocks API request for 60 seconds
   - Cannot handle concurrent users efficiently

2. **No Database**
   - Analysis results not stored
   - Cannot track historical analyses

3. **Local File Storage**
   - PDFs saved to `/uploads` directory
   - Not suitable for cloud deployment

4. **Single AI Provider**
   - Gemini API outage = system failure
   - No fallback options

### 5.2 Production Enhancements

**1. Asynchronous Processing**
```
User uploads PDF → Returns job_id immediately
Backend processes in background (Celery + Redis)
User polls /api/status/{job_id} for results
```

**2. Database Integration**
```
PostgreSQL:
- Store analysis results
- Track user history
- Cache common claims

Tables:
- users (id, email, created_at)
- analyses (id, user_id, file_id, status, results, created_at)
- claims_cache (claim_text, verification_result, last_verified)
```

**3. Cloud Storage**
```
AWS S3 or Google Cloud Storage:
- Store PDFs permanently
- Enable re-analysis without re-upload
- Share results via signed URLs
```

**4. Multi-Provider Fallback**
```
Primary: Google Gemini
Fallback 1: OpenAI GPT-4
Fallback 2: Anthropic Claude

If Gemini fails → Try OpenAI → Try Claude
```

**5. Rate Limiting & Caching**
```
Redis Cache:
- Cache claim verification results for 7 days
- If claim seen before → Return cached result

Rate Limiting:
- Limit to 10 analyses per user per day
- Prevent abuse
```

**6. Monitoring & Observability**
```
Datadog / NewRelic:
- Track API latency
- Monitor error rates
- Alert on failures

Logging:
- Structured JSON logs
- Track each agent's output
- Searchable in CloudWatch
```

### 5.3 Deployment Architecture (Production)

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS                                    │
│         (Web UI)              (Gmail)              (API)         │
└──────────────────┬──────────────┬───────────────────┬───────────┘
                   │              │                   │
                   ▼              ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│              CLOUDFLARE (CDN + DDoS Protection)                  │
└──────────────────┬──────────────┬───────────────────┬───────────┘
                   │              │                   │
          ┌────────▼────────┐  ┌──▼────────┐  ┌──────▼───────┐
          │  Vercel (Next.js │  │  Ngrok/   │  │   API Gateway│
          │    Frontend)     │  │ Localtunnel│  │   (AWS/GCP) │
          └─────────┬────────┘  └──┬────────┘  └──────┬───────┘
                    │              │                   │
                    └──────────────┴───────────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  Load Balancer (AWS ELB)     │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  FastAPI Servers (ECS/GKE)   │
                    │  - Auto-scaling (2-10 instances)
                    │  - Health checks             │
                    └──────────┬────────┬───────────┘
                               │        │
                 ┌─────────────▼───┐  ┌▼─────────────┐
                 │  Celery Workers │  │  PostgreSQL  │
                 │  (Background    │  │  (RDS/Cloud  │
                 │   Analysis)     │  │   SQL)       │
                 └─────────┬───────┘  └──────────────┘
                           │
                    ┌──────▼──────┐
                    │Redis (Cache)│
                    └─────────────┘
```

**Estimated Cost (AWS):**
- EC2 t3.medium (2 instances): $60/month
- RDS PostgreSQL: $30/month
- S3 Storage: $5/month
- CloudFront CDN: $10/month
- **Total: ~$105/month** (supports 1000+ analyses/day)

---

## 6. Security & Privacy

### 6.1 Security Measures Implemented

1. **Environment Variables**
   - API keys in `.env` (not committed to git)
   - `.env.example` with placeholders only

2. **Input Validation**
   - File type validation (PDF only)
   - File size limits (10 MB max)
   - Pydantic schema validation

3. **CORS Configuration**
   - Restrict origins to localhost (dev) / domain (prod)

4. **Gmail App Passwords**
   - Not using real Gmail password
   - 16-character app-specific passwords
   - Can be revoked anytime

### 6.2 Privacy Considerations

1. **Data Storage**
   - PDFs stored temporarily (deleted after analysis)
   - No long-term storage of user data

2. **Email Privacy**
   - Analysis sent only to original sender
   - No CC/BCC to third parties
   - Emails not logged or stored

3. **API Usage**
   - Gemini API: Data not used for model training (per Google policy)
   - DuckDuckGo: Anonymous searches (no tracking)

### 6.3 Production Security Enhancements

1. **Authentication**
   - OAuth 2.0 for web users
   - API keys for programmatic access
   - Rate limiting per user

2. **Data Encryption**
   - HTTPS/TLS for all API calls
   - Encrypt PDFs at rest (S3 encryption)
   - Encrypt database (RDS encryption)

3. **Compliance**
   - GDPR: Right to deletion
   - SOC 2: Audit logging
   - Data retention policies (30 days)

---

## 7. Future Enhancements

### 7.1 Additional Integrations

1. **Slack Bot**
   - `/sago analyze <url>` command
   - Post results to channel
   - Thread-based discussions

2. **Chrome Extension**
   - Right-click → "Analyze with Sago"
   - Works on Google Drive, Dropbox
   - Inline results overlay

3. **API Webhooks**
   - POST to custom URL when analysis complete
   - Integrate with CRM (Salesforce, HubSpot)
   - Zapier integration

### 7.2 Advanced AI Features

1. **Competitive Analysis**
   - Compare pitch deck against known competitors
   - Identify differentiation gaps
   - Market positioning insights

2. **Historical Tracking**
   - Track claim changes over time (seed → Series A)
   - Detect inconsistencies in storytelling
   - Flag unusual metric trajectories

3. **Custom Agent Tools**
   - Crunchbase API (funding data)
   - LinkedIn API (team credentials)
   - SEC EDGAR (financial filings)
   - PitchBook (market data)

### 7.3 Personalization Features

1. **Investment Thesis Matching**
   - User defines investment criteria
   - System scores pitch deck fit
   - Recommends pass/consider/deep dive

2. **Custom Question Templates**
   - User saves frequently asked questions
   - System auto-generates variations
   - Industry-specific templates (SaaS, Healthcare, Fintech)

---

## 8. Conclusion

Sago demonstrates how AI agents can transform pitch deck analysis from a manual, time-consuming process to an automated, evidence-based workflow. By integrating seamlessly into existing tools (Gmail), personalizing analysis for each pitch deck, and autonomously verifying claims with real-time research, Sago embodies the three core design principles.

The current implementation is a working prototype suitable for demonstration and light usage. With the production enhancements outlined in Section 5, Sago can scale to handle hundreds of investors analyzing thousands of pitch decks per month.

### Key Metrics (Current Implementation)

- **27 claims extracted** from average pitch deck
- **3 claims verified** with web research
- **12 questions generated** for due diligence
- **60 seconds** end-to-end analysis time
- **$0 cost** (free tier usage)

### Next Steps

1. Deploy backend to cloud (AWS/Render)
2. Implement async job processing (Celery)
3. Add database (PostgreSQL)
4. Create user accounts and authentication
5. Launch beta with 10-20 investors
6. Iterate based on feedback

---

**For technical questions, see README.md or contact the developer.**
