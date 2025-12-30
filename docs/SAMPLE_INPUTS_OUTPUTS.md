# Sample Inputs and Outputs

## Test Case: Airbnb Pitch Deck

### Input

**File:** `Pitch-Example-Air-BnB-PDF.pdf`

**Content Preview:**
- Company: Airbnb
- Market size claims: "$1.3B market opportunity"
- Growth metrics: "50% quarterly growth"
- User stats: "10,000+ bookings"
- Team credentials: "Ex-Google, Yahoo engineers"

### Processing

**Method:** Multi-Agent Analysis (LangGraph)
**Processing Time:** ~58 seconds
**API Calls:** 32 (Gemini) + 3 (DuckDuckGo Search)

### Output

#### Summary Statistics
```json
{
  "total_claims": 27,
  "claims_researched": 3,
  "verified_claims": 3,
  "questions_generated": 12
}
```

#### Sample Extracted Claims

**Claim 1:**
```json
{
  "claim": "The short-term rental market is worth $1.3B annually",
  "category": "market_size",
  "importance": 9,
  "source": "Slide 3: Market Opportunity"
}
```

**Claim 2:**
```json
{
  "claim": "Airbnb is growing at 50% quarter-over-quarter",
  "category": "growth",
  "importance": 8,
  "source": "Slide 7: Traction"
}
```

**Claim 3:**
```json
{
  "claim": "Platform has facilitated 10,000+ bookings",
  "category": "traction",
  "importance": 7,
  "source": "Slide 7: Traction"
}
```

#### Sample Verification Results

**Verification 1:**
```
Claim: "The short-term rental market is worth $1.3B annually"

Verification Status: Partially Verified

Research Conducted:
- Searched: "short-term rental market size 2008"
- Found: Multiple sources indicating growing vacation rental market
- Sources: TechCrunch, industry reports

Evidence:
The vacation rental market was estimated at several billion dollars globally
in 2008. The $1.3B figure appears conservative for the global market but may
be specific to a particular geographic region or segment.

Concerns:
- Need clarification on market definition (US only? Global?)
- Year of market data not specified
- TAM vs SAM vs SOM not clearly defined

Confidence: Medium (60%)
```

**Verification 2:**
```
Claim: "Airbnb is growing at 50% quarter-over-quarter"

Verification Status: Cannot Verify (Insufficient Public Data)

Research Conducted:
- Searched: "Airbnb growth rate 2008"
- Limited public data available for early-stage startup

Evidence:
No public third-party verification available. Early-stage startups typically
don't publish detailed financial metrics.

Recommendation:
Request internal analytics showing:
- Monthly active users
- Booking volume by month
- Revenue growth (if any)
- Customer cohort retention

Confidence: Low (20%) - Requires internal data access
```

**Verification 3:**
```
Claim: "Platform has facilitated 10,000+ bookings"

Verification Status: Plausible

Research Conducted:
- Cross-referenced with growth timeline
- Compared against similar platforms

Evidence:
For a platform that launched in 2008, 10,000 bookings is reasonable given:
- Growing interest in sharing economy
- Multiple markets (SF, NYC, etc.)
- Average 50-100 bookings per week would achieve this in 2-4 months

Concerns:
- Define "booking" (completed stays vs listings?)
- Timeframe not specified (since launch? This quarter?)
- Repeat vs unique users?

Confidence: Medium (65%)
```

#### Sample Generated Questions

**Market Questions:**
1. Can you clarify whether the $1.3B market size refers to the US market or global market? What's your data source?
2. How do you define your TAM, SAM, and SOM? What percentage of the short-term rental market can realistically be captured through an online platform?
3. What are the key assumptions behind your market sizing, and how sensitive is your business model to changes in these assumptions?

**Traction Questions:**
4. Can you share the breakdown of your 10,000+ bookings by city and over time? What's your month-over-month growth trend?
5. What's your repeat booking rate? What percentage of hosts and guests are active after their first transaction?
6. What are your unit economics? (Customer acquisition cost, lifetime value, take rate, etc.)

**Growth Questions:**
7. What specific channels are driving your 50% quarterly growth? Is this organic or paid?
8. What's your burn rate and runway at the current growth trajectory?
9. What are the key bottlenecks to scaling to 100,000+ bookings?

**Competition Questions:**
10. How do you differentiate from existing vacation rental platforms like VRBO and HomeAway?
11. What's your defensibility against well-funded competitors entering the space?

**Team Questions:**
12. What relevant experience does your team have in hospitality, marketplace businesses, or payments?

---

## Test Case: Email Integration

### Input (Gmail)

**Email:**
```
From: investor@vc.com
To: collegePracticals118@gmail.com
Subject: Airbnb Pitch Deck Review
Body: "Hey Sago, analyze this pitch deck"
Attachment: Pitch-Example-Air-BnB-PDF.pdf (245 KB)
```

### Processing

**Trigger Detection:**
✅ Found trigger phrase: "hey sago"
✅ Found PDF attachment
✅ Not previously processed (no "Sago/Analyzed" label)

**Workflow:**
1. Upload PDF to backend API
2. Extract text with PyPDF2
3. Run multi-agent analysis
4. Format results as HTML email
5. Send via Gmail SMTP
6. Add "Sago/Analyzed" label

**Processing Time:** ~62 seconds

### Output (Email Reply)

**Email:**
```
From: Sago Analysis <collegePracticals118@gmail.com>
To: investor@vc.com
Subject: Re: Airbnb Pitch Deck Review
Format: HTML
```

**HTML Body Preview:**

```html
<!DOCTYPE html>
<html>
<body>
  <!-- Beautiful gradient header -->
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); ...">
    <h1>🚀 Sago Analysis</h1>
    <p>Pitch Deck Verification Report</p>
  </div>

  <!-- Summary Cards -->
  <table>
    <tr>
      <td>
        <div style="background: #dbeafe; ...">
          <div>27</div>
          <div>Claims Extracted</div>
        </div>
      </td>
      <td>
        <div style="background: #d1fae5; ...">
          <div>3</div>
          <div>Verified Claims</div>
        </div>
      </td>
      <td>
        <div style="background: #e9d5ff; ...">
          <div>12</div>
          <div>Questions</div>
        </div>
      </td>
    </tr>
  </table>

  <!-- Verification Results -->
  <h2>✓ Verification Results</h2>
  <div style="margin-bottom: 20px; padding: 15px; background: #f9fafb; ...">
    <h3>1. The short-term rental market is worth $1.3B annually</h3>
    <div>
      Verification Status: Partially Verified

      Research Conducted:
      - Searched: "short-term rental market size 2008"
      ...
    </div>
  </div>

  <!-- Questions -->
  <h2>❓ Questions for the Founder</h2>
  <ol>
    <li>Can you clarify whether the $1.3B market size refers to...</li>
    <li>How do you define your TAM, SAM, and SOM?...</li>
    ...
  </ol>

  <!-- Footer -->
  <div>
    <p>🤖 Generated by Sago - AI-Powered Pitch Deck Analyzer</p>
    <p><a href="https://github.com/varunmehta14/sago">View on GitHub</a></p>
  </div>
</body>
</html>
```

---

## Performance Metrics

### Web Interface
- **Upload time:** < 1 second
- **Text extraction:** 2-3 seconds
- **Simple AI analysis:** 30-40 seconds
- **Multi-agent analysis:** 55-65 seconds
- **Total end-to-end:** ~60 seconds

### Gmail Integration
- **Email detection latency:** Up to 5 minutes (trigger interval)
- **Analysis time:** 55-65 seconds
- **Email sending:** 2-3 seconds
- **Total from email sent to reply received:** 5-7 minutes

### API Usage (per analysis)
- **Gemini API calls:** ~32 requests
- **DuckDuckGo searches:** 3 searches
- **Cost:** $0.00 (free tier)
- **Rate limit status:** Within limits

---

## Error Handling Examples

### Invalid Input

**Input:** Non-PDF file (e.g., .docx)
**Output:**
```json
{
  "error": "Invalid file type. Please upload a PDF file.",
  "status_code": 400
}
```

### No Claims Found

**Input:** PDF with only images, no text
**Output:**
```json
{
  "file_id": "abc123",
  "company_name": "Unknown",
  "claims": [],
  "verification_results": [],
  "questions": ["Unable to extract text from PDF. Please provide a text-based pitch deck."],
  "summary": {
    "total_claims": 0,
    "verified_claims": 0,
    "questions_generated": 1
  }
}
```

### API Rate Limit

**Error:**
```json
{
  "error": "RESOURCE_EXHAUSTED: API rate limit exceeded. Please try again later.",
  "status_code": 429,
  "retry_after": 60
}
```

### Email Without Trigger Phrase

**Input:** Email without "hey sago" in body
**Execution Log:**
```
[INFO] 📧 Processing: Airbnb Deck
[INFO] ⏭️ Skipped: No trigger phrase found (need "hey sago", "sago analyze", etc.)
```
**Output:** No email reply sent, no label added
