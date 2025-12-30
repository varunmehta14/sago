# System Architecture - Sago Pitch Deck Analyzer

## Overview

The Sago Pitch Deck Analyzer is a full-stack application that helps investors verify pitch deck claims and generate personalized questions for founder meetings.

## High-Level Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  Next.js        │────────▶│  FastAPI         │────────▶│  Google Gemini  │
│  Frontend       │  HTTP   │  Backend         │  API    │  AI             │
│                 │         │                  │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
       │                             │
       │                             │
       ▼                             ▼
┌─────────────────┐         ┌──────────────────┐
│  Browser        │         │  File System     │
│  (User)         │         │  (PDF Storage)   │
└─────────────────┘         └──────────────────┘
```

## Component Architecture

### Frontend (Next.js + React + TypeScript)

**Components:**
- `app/page.tsx` - Main UI component
  - File upload interface
  - Analysis trigger
  - Results display (claims, verification, questions)

- `lib/api.ts` - API client
  - Upload pitch deck
  - Request analysis
  - Type-safe response handling

**Key Features:**
- Responsive design with Tailwind CSS
- Real-time loading states
- Error handling and validation
- Dark mode support

**Flow:**
1. User selects PDF file
2. Frontend uploads to backend
3. Triggers analysis with file ID
4. Displays results in organized sections

### Backend (FastAPI + Python 3.11)

**Structure:**
```
app/
├── main.py              # FastAPI app, CORS, routes
├── config.py            # Settings, env variables
├── routes/
│   └── pitch_deck.py    # Upload, analyze endpoints
└── services/
    ├── pdf_parser.py    # PDF text extraction
    └── gemini_service.py # AI analysis
```

**Services:**

1. **PDF Parser Service**
   - Extracts text from uploaded PDFs using PyPDF2
   - Returns structured document information
   - Error handling for corrupted files

2. **Gemini Service**
   - **Extract Claims:** Analyzes pitch deck text to identify verifiable claims
   - **Verify Claims:** For each claim, provides verification status and evidence
   - **Generate Questions:** Creates contextual questions based on gaps and concerns

**API Endpoints:**

```
POST /api/pitch-deck/upload
- Accepts: multipart/form-data (PDF)
- Returns: file_id, preview, metadata
- Stores: PDF in uploads/ directory

POST /api/pitch-deck/analyze/{file_id}
- Accepts: file_id path parameter
- Process:
  1. Extract text from PDF
  2. Send to Gemini for claim extraction
  3. Verify top 5 claims (rate limit consideration)
  4. Generate questions based on results
- Returns: claims, verification results, questions, summary

GET /api/health
- Health check endpoint
```

## Data Flow

### Upload Flow
```
1. User selects PDF ──▶ 2. Frontend validates file type
                         ▼
                    3. POST to /upload
                         ▼
                    4. Backend saves file
                         ▼
                    5. Extract text (PyPDF2)
                         ▼
                    6. Return file_id + preview
```

### Analysis Flow
```
1. Frontend sends file_id ──▶ 2. Backend reads PDF
                                ▼
                           3. Gemini: Extract claims
                                ▼
                           4. Gemini: Verify claims (top 5)
                                ▼
                           5. Gemini: Generate questions
                                ▼
                           6. Return structured results
                                ▼
                           7. Frontend displays in UI
```

## AI Integration - Google Gemini

**Model:** `gemini-pro`

**Prompting Strategy:**

1. **Claim Extraction:**
   - Structured prompt requesting JSON format
   - Categories: market, revenue, technology, team
   - Importance levels: high, medium, low
   - Extracts ALL verifiable claims from deck

2. **Claim Verification:**
   - For each claim, asks Gemini to:
     - Verify against its knowledge base
     - Provide supporting evidence or concerns
     - Flag potential red flags
     - Suggest verification steps

3. **Question Generation:**
   - Context-aware based on verification results
   - Focuses on:
     - Unverified claims
     - Gaps in the pitch
     - Critical assumptions
     - Competitive positioning
   - Generates 8-12 actionable questions

**Rate Limiting:**
- Currently verifies top 5 claims (avoids free tier limits)
- Can be expanded with paid tier or batching

## Design Decisions

### Technology Choices

| Decision | Rationale |
|----------|-----------|
| **Gemini API** | Free tier, excellent reasoning, easy integration |
| **FastAPI** | Modern Python, async support, auto docs |
| **Next.js** | SSR/CSR flexibility, TypeScript support |
| **Tailwind CSS** | Rapid UI development, consistent design |
| **File-based storage** | Simple for prototype, easy to migrate to S3 |

### Security Considerations

**Current Implementation:**
- CORS restricted to localhost:3000
- File type validation (PDF only)
- API key stored in environment variables

**Production Requirements:**
- User authentication (JWT/OAuth)
- File scanning (virus detection)
- Rate limiting per user
- HTTPS only
- Encrypted file storage
- API key rotation

### Scalability Considerations

**Current Bottlenecks:**
1. Synchronous AI processing (30-60s per deck)
2. Local file storage
3. No caching layer

**Production Architecture:**

```
┌─────────────┐
│   CDN       │
└──────┬──────┘
       │
┌──────▼──────────────────┐
│  Load Balancer          │
└──────┬──────────────────┘
       │
┌──────▼──────┐  ┌────────────┐
│  Next.js    │  │  Next.js   │  (Multiple instances)
│  Frontend   │  │  Frontend  │
└──────┬──────┘  └──────┬─────┘
       │                │
       └────────┬───────┘
                │
┌───────────────▼────────────┐
│   API Gateway              │
└───────────────┬────────────┘
                │
┌───────────────▼────────┐  ┌───────────────┐
│  FastAPI Backend       │  │  FastAPI      │  (Multiple instances)
└───────────────┬────────┘  └───────┬───────┘
                │                    │
                └──────┬─────────────┘
                       │
        ┌──────────────┼──────────────┬─────────────┐
        │              │              │             │
┌───────▼─────┐ ┌──────▼─────┐ ┌─────▼────┐ ┌──────▼─────┐
│ PostgreSQL  │ │   Redis    │ │   S3     │ │   Celery   │
│  (Metadata) │ │  (Cache)   │ │  (Files) │ │  (Queue)   │
└─────────────┘ └────────────┘ └──────────┘ └──────┬─────┘
                                                    │
                                             ┌──────▼─────┐
                                             │   Gemini   │
                                             │    API     │
                                             └────────────┘
```

**Enhancements:**
- **Queue System:** Celery + Redis for async processing
- **Caching:** Redis for frequent claims
- **Database:** PostgreSQL for user data, analysis history
- **Object Storage:** S3 for PDFs
- **Monitoring:** Prometheus + Grafana
- **Logging:** ELK stack

## Integration Points (Future)

### Gmail Integration
```
Email with PDF ──▶ Webhook ──▶ Auto-analyze ──▶ Send summary email
```

### Slack Integration
```
PDF shared in channel ──▶ Bot analyzes ──▶ Posts results in thread
```

### Calendar Integration
```
Analysis complete ──▶ Schedule follow-up ──▶ Add to calendar with questions
```

## Testing Strategy

### Backend Tests
- Unit tests for PDF parsing
- Mock Gemini API responses
- Integration tests for endpoints
- Load testing for scalability

### Frontend Tests
- Component tests (Jest + React Testing Library)
- E2E tests (Playwright)
- Accessibility tests

## Deployment Strategy

### Development
- Local: Docker Compose for full stack
- Backend: `uvicorn` with hot reload
- Frontend: `npm run dev`

### Production
- Backend: AWS ECS or Cloud Run
- Frontend: Vercel or Netlify
- Database: RDS PostgreSQL
- Storage: S3
- CDN: CloudFront

## Monitoring & Observability

**Metrics to Track:**
- API response times
- Gemini API call success rate
- PDF processing errors
- User engagement (uploads, analyses)
- Question quality feedback

**Logging:**
- Request/response logs
- AI prompt/response logs (for debugging)
- Error tracking (Sentry)

## Cost Estimation

### Current (Free Tier)
- Gemini API: Free (with limits)
- Development: $0/month

### Production (Estimated)
- Gemini API: ~$50-200/month (depends on usage)
- Infrastructure: ~$100-300/month
- Storage: ~$10-50/month
- **Total:** ~$160-550/month for 1000 analyses/month

## Conclusion

This architecture provides a solid foundation for the Sago Pitch Deck Analyzer while remaining simple and cost-effective. The modular design allows for easy scaling and feature additions as the product evolves.
