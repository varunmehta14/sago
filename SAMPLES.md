# Sample Inputs and Outputs

This document provides example inputs and outputs for the Sago Pitch Deck Analyzer.

## Sample Input: Pitch Deck Content

### Example Pitch Deck (FinTech Startup)

**Company:** PayFlow - Digital Payment Platform

**Slide 1: Problem & Opportunity**
- Small businesses lose $50B annually due to payment processing inefficiencies
- 45% of SMBs are dissatisfied with current payment processors
- The global digital payments market is worth $200B and growing at 25% annually

**Slide 2: Solution**
- AI-powered payment routing reduces failed transactions by 40%
- Unified API integrates with 50+ payment providers
- Real-time fraud detection using proprietary ML models

**Slide 3: Traction**
- 10,000 active merchants
- Processing $100M in annual transaction volume
- Growing 300% year-over-year
- Average merchant saves $25K annually

**Slide 4: Market**
- TAM: $200B digital payments market
- SAM: $30B SMB payment processing
- SOM: $3B (10% of SAM over 5 years)

**Slide 5: Business Model**
- 2.5% transaction fee
- $99/month SaaS subscription
- $50M projected revenue in Year 3

**Slide 6: Team**
- CEO: Former VP at Stripe with 15 years in payments
- CTO: Ex-Google engineer, built payment systems at scale
- CFO: Former Goldman Sachs investment banker

**Slide 7: Competition**
- Stripe: Too complex for SMBs
- Square: Limited customization
- PayFlow: Best of both worlds

**Slide 8: Ask**
- Raising $5M Series A
- 18-month runway
- Plan to hire 25 engineers

---

## Sample Output: Analysis Results

### Summary Statistics

```json
{
  "total_claims": 12,
  "verified_claims": 5,
  "questions_generated": 10
}
```

### Extracted Claims

```json
[
  {
    "claim": "Small businesses lose $50B annually due to payment processing inefficiencies",
    "category": "market",
    "importance": "high"
  },
  {
    "claim": "The global digital payments market is worth $200B and growing at 25% annually",
    "category": "market",
    "importance": "high"
  },
  {
    "claim": "10,000 active merchants",
    "category": "traction",
    "importance": "high"
  },
  {
    "claim": "Processing $100M in annual transaction volume",
    "category": "revenue",
    "importance": "high"
  },
  {
    "claim": "Growing 300% year-over-year",
    "category": "growth",
    "importance": "high"
  },
  {
    "claim": "Average merchant saves $25K annually",
    "category": "value_proposition",
    "importance": "medium"
  },
  {
    "claim": "CEO: Former VP at Stripe with 15 years in payments",
    "category": "team",
    "importance": "high"
  },
  {
    "claim": "AI-powered payment routing reduces failed transactions by 40%",
    "category": "technology",
    "importance": "high"
  }
]
```

### Verification Results

#### Claim 1: Market Size
```
Claim: "The global digital payments market is worth $200B and growing at 25% annually"

Verification Status: ✓ Verified

Supporting Evidence:
Multiple industry reports confirm similar market sizes:
- Statista estimates the global digital payments market at $196B in 2023
- Allied Market Research projects 24.8% CAGR through 2030
- McKinsey reports similar growth rates in their Global Payments Report

Red Flags: None

Concerns:
- Ensure they're targeting a specific segment (B2B, B2C, SMB) rather than the entire market
- The 25% growth rate is for the overall market, not necessarily their segment

Recommended Verification Steps:
1. Ask for their specific serviceable addressable market (SAM)
2. Verify which geographic regions they're targeting
3. Request breakdown by payment type (card, ACH, digital wallet, etc.)
```

#### Claim 2: Customer Traction
```
Claim: "10,000 active merchants processing $100M annually"

Verification Status: ⚠ Cannot Independently Verify

Supporting Evidence:
- Cannot verify without access to company data
- Numbers are plausible for an early-stage fintech

Red Flags:
- Need to understand definition of "active" merchant
- $100M across 10K merchants = $10K average, which is low for B2B payments

Concerns:
1. "Active" could mean different things (monthly, quarterly, annually)
2. Average transaction volume per merchant seems low
3. Need to understand revenue concentration (top 10 merchants vs. long tail)

Recommended Verification Steps:
1. Request merchant cohort analysis
2. Ask for MRR/ARR breakdown
3. Verify churn rates
4. Review anonymized transaction data or bank statements
5. Check if any merchants are pilot/beta vs. paying customers
```

#### Claim 3: Growth Rate
```
Claim: "Growing 300% year-over-year"

Verification Status: ⚠ Requires Context

Supporting Evidence:
- High growth rates are common for early-stage startups from small base
- Plausible if starting from low base (e.g., $1M → $3M)

Red Flags:
- 300% YoY growth is difficult to sustain
- Need to understand what metric is growing (revenue, users, transaction volume)
- Small base effect: easier to triple from $100K than from $10M

Concerns:
1. Which metric is growing at 300%? (Merchants? Revenue? Transaction volume?)
2. What's the time period? (Last quarter? Last year? Last month?)
3. What's causing the growth? (Paid acquisition? Organic? One big customer?)
4. Is this growth sustainable?

Recommended Verification Steps:
1. Ask for monthly growth metrics for past 12 months
2. Understand CAC payback period
3. Verify if growth is organic or paid
4. Check unit economics at current scale
```

#### Claim 4: Technology Performance
```
Claim: "AI-powered payment routing reduces failed transactions by 40%"

Verification Status: ⚠ Potentially Overstated

Supporting Evidence:
- Payment optimization is a known use case for ML
- Industry benchmarks show 10-20% reduction in failed transactions is typical
- 40% seems on the higher end but not impossible

Red Flags:
- 40% is significantly higher than industry benchmarks
- Need to understand baseline and methodology

Concerns:
1. What was the baseline failure rate?
2. How was this measured? (A/B test? Before/after?)
3. Sample size and statistical significance?
4. Is this for all merchants or cherry-picked best cases?
5. What types of failures are being reduced? (Technical? Fraud? Insufficient funds?)

Recommended Verification Steps:
1. Request data on the A/B test or before/after analysis
2. Ask for breakdown by failure type
3. Understand if this is average across all merchants or best-case
4. Review technical architecture of the ML model
5. Ask independent technical advisor to evaluate
```

#### Claim 5: Team Credentials
```
Claim: "CEO: Former VP at Stripe with 15 years in payments"

Verification Status: ⚠ Should Verify on LinkedIn

Supporting Evidence:
- Can be easily verified via LinkedIn, press releases, or Stripe contacts
- 15 years in payments is substantial industry experience
- Stripe VP would have relevant expertise

Red Flags:
- "VP" at Stripe could mean different things (there are many VPs)
- Need to verify actual scope of responsibility

Concerns:
1. What was their specific role at Stripe?
2. How long were they at Stripe?
3. What did they accomplish there?
4. Why did they leave?
5. Are they still in good standing with Stripe?

Recommended Verification Steps:
1. Check LinkedIn profile
2. Reach out to Stripe contacts for reference
3. Google search for press mentions or interviews
4. Ask about their specific accomplishments at Stripe
5. Understand reporting structure and team size managed
```

### Generated Questions for Founder Meeting

Based on the verification results, here are personalized questions to ask the founders:

#### Business Model & Unit Economics
1. **Can you break down your $100M transaction volume by merchant size?** What's your revenue concentration—how much comes from your top 10 merchants vs. the long tail?

2. **What's your average revenue per merchant, and how does this vary by merchant size?** Given $100M across 10K merchants is $10K average, help me understand the distribution.

3. **Walk me through your unit economics in detail:** What's your CAC, LTV, payback period, and gross margin? How do these change as merchants scale?

#### Growth & Sustainability
4. **You mention 300% YoY growth—which specific metric is this referring to?** Can you show me month-over-month metrics for merchants, revenue, and transaction volume over the past 12-18 months?

5. **What's driving your growth?** Is it paid acquisition, organic, partnerships, or one or two large customers? What's your CAC by channel?

6. **What's your current monthly burn and runway?** How does the $5M you're raising get you to your next milestone?

#### Technology & Product
7. **Can you share the data behind your 40% reduction in failed transactions?** What was the baseline, sample size, and methodology? Is this consistent across all merchant types?

8. **What's your technical moat?** Why couldn't Stripe or Square build similar AI routing in 6 months?

9. **Describe your fraud detection system:** What's your fraud rate compared to industry benchmarks? Have you had any major fraud incidents?

#### Market & Competition
10. **Stripe and Square have massive network effects and economies of scale.** What's your sustainable competitive advantage beyond just being "simpler"? How do you win long-term?

11. **You claim SMBs are your target market, but your average merchant only processes $10K/year.** Is this really an SMB play, or are you going after micro-merchants? What's the addressable market for this segment?

#### Team & Execution
12. **I'd like to do a reference check on your CEO's time at Stripe.** Can you provide contacts who can speak to their specific accomplishments and leadership?

13. **You plan to hire 25 engineers with this $5M raise.** What are your biggest product gaps right now, and what will these engineers work on specifically?

---

## API Response Example

### POST /api/pitch-deck/upload

**Request:**
```bash
curl -X POST "http://localhost:8000/api/pitch-deck/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@payflow_pitch_deck.pdf"
```

**Response:**
```json
{
  "file_id": "8f7e6d5c-4b3a-2918-7f6e-5d4c3b2a1918",
  "filename": "payflow_pitch_deck.pdf",
  "text_preview": "PayFlow Digital Payment Platform Problem & Opportunity Small businesses lose $50B annually due to payment processing inefficiencies. 45% of SMBs are dissatisfied with current payment processors...",
  "word_count": 456,
  "message": "Pitch deck uploaded successfully"
}
```

### POST /api/pitch-deck/analyze/{file_id}

**Request:**
```bash
curl -X POST "http://localhost:8000/api/pitch-deck/analyze/8f7e6d5c-4b3a-2918-7f6e-5d4c3b2a1918" \
  -H "accept: application/json"
```

**Response:**
```json
{
  "file_id": "8f7e6d5c-4b3a-2918-7f6e-5d4c3b2a1918",
  "claims": [
    {
      "claim": "The global digital payments market is worth $200B and growing at 25% annually",
      "category": "market",
      "importance": "high"
    },
    {
      "claim": "10,000 active merchants processing $100M annually",
      "category": "traction",
      "importance": "high"
    }
  ],
  "verification_results": [
    {
      "claim": "The global digital payments market is worth $200B and growing at 25% annually",
      "verification_result": "Verification Status: ✓ Verified\n\nSupporting Evidence: Multiple industry reports confirm..."
    }
  ],
  "questions": [
    "Can you break down your $100M transaction volume by merchant size?",
    "What's your average revenue per merchant?",
    "Walk me through your unit economics in detail",
    "You mention 300% YoY growth—which specific metric is this referring to?",
    "What's driving your growth?",
    "Can you share the data behind your 40% reduction in failed transactions?",
    "What's your technical moat?",
    "Stripe and Square have massive network effects—what's your sustainable advantage?",
    "I'd like to do a reference check on your CEO's time at Stripe",
    "You plan to hire 25 engineers—what are your biggest product gaps?"
  ],
  "summary": {
    "total_claims": 12,
    "verified_claims": 5,
    "questions_generated": 10
  }
}
```

---

## Frontend UI Example

### Upload Screen
```
┌─────────────────────────────────────────────────┐
│                                                 │
│         Sago Pitch Deck Analyzer                │
│  AI-powered verification and due diligence      │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │        Upload Pitch Deck                  │ │
│  │                                           │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │      📄  Choose PDF File            │ │ │
│  │  │                                     │ │ │
│  │  │  Selected: payflow_pitch_deck.pdf  │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  │                                           │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │     Analyze Pitch Deck              │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### Results Screen
```
┌─────────────────────────────────────────────────┐
│  ┌─────────┐  ┌─────────┐  ┌──────────────┐    │
│  │ Claims  │  │Verified │  │  Questions   │    │
│  │   12    │  │    5    │  │     10       │    │
│  └─────────┘  └─────────┘  └──────────────┘    │
│                                                 │
│  Verification Results                           │
│  ┌───────────────────────────────────────────┐ │
│  │ Claim: Global digital payments $200B...  │ │
│  │ Status: ✓ Verified                        │ │
│  │ Evidence: Industry reports confirm...    │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  Questions to Ask the Founder                   │
│  ┌───────────────────────────────────────────┐ │
│  │ 1  Can you break down your $100M...      │ │
│  │ 2  What's your average revenue per...    │ │
│  │ 3  Walk me through your unit economics...│ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## Notes on Sample Quality

The AI-generated questions demonstrate:

1. **Hyper-Personalization:** Questions are specific to PayFlow's claims, not generic
2. **True Agency:** Goes beyond summarization to actionable insights
3. **Investor Sophistication:** Questions show deep understanding of fintech metrics
4. **Gap Identification:** Highlights missing information (cohort analysis, unit economics)
5. **Risk Assessment:** Identifies red flags (high growth claims, competitive moats)

This shows the system delivers on Sago's three design principles.
