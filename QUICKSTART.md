# Quick Start Guide

## Get Your Free Google Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

## Setup (One-time)

```bash
# Run the setup script
./setup.sh

# Add your Google API key to backend/.env
# Edit the file and replace the placeholder with your actual key
```

## Run the Application

```bash
# Option 1: Use the run script (runs both frontend & backend)
./run.sh

# Option 2: Run manually in separate terminals
# Terminal 1 - Backend:
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend:
cd frontend
npm run dev
```

## Access the Application

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Test the Application

1. Open http://localhost:3000
2. Click "Choose PDF File" and select a pitch deck PDF
3. Click "Analyze Pitch Deck"
4. Wait 30-60 seconds for AI analysis
5. Review the results:
   - Claims extracted from the deck
   - Verification results with evidence
   - Personalized questions to ask the founder

## Project Structure

```
sago/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # FastAPI app
│   │   ├── config.py    # Configuration
│   │   ├── routes/      # API endpoints
│   │   └── services/    # Business logic
│   ├── requirements.txt # Python dependencies
│   └── .env            # API keys (create from .env.example)
│
├── frontend/            # Next.js frontend
│   ├── app/
│   │   └── page.tsx    # Main UI
│   ├── lib/
│   │   └── api.ts      # API client
│   └── package.json    # Node dependencies
│
├── README.md           # Full documentation
├── ARCHITECTURE.md     # System architecture (1-2 pages)
├── SAMPLES.md          # Sample inputs/outputs
├── setup.sh           # Setup script
└── run.sh             # Run script
```

## Deliverables Checklist

- ✅ **GitHub repo** - Complete codebase
- ✅ **README.md** - Setup instructions and documentation
- ✅ **ARCHITECTURE.md** - 2-page system architecture document
- ✅ **SAMPLES.md** - Sample inputs and outputs
- ✅ **Working prototype** - Upload PDF → Get verification results & questions

## Key Features Implemented

### 1. Seamless Integration ✅
- Web-based interface (no download required)
- Drag-and-drop PDF upload
- Ready for integration with Gmail/Slack via webhooks

### 2. Hyper-Personalization ✅
- Analyzes specific claims from each unique pitch deck
- Generates customized questions based on verification results
- Categorizes claims by importance and type

### 3. True Agency ✅
- Automatically extracts claims from pitch decks
- Proactively verifies information using Gemini AI
- Generates actionable questions for meetings

## Tech Stack

- **Backend:** FastAPI + Python 3.11 + Google Gemini API (FREE)
- **Frontend:** Next.js 16 + React 19 + TypeScript + Tailwind CSS
- **AI:** Google Gemini Pro (free tier)

## Troubleshooting

### Backend won't start
- Check that Python 3.11 is installed: `python3.11 --version`
- Check that virtual environment is activated: `which python` should show venv path
- Check that dependencies are installed: `pip list`

### Frontend won't start
- Check that Node.js is installed: `node --version`
- Run `npm install` in frontend directory

### API key errors
- Make sure you've added your Google Gemini API key to `backend/.env`
- Get a free key at: https://makersuite.google.com/app/apikey

### CORS errors
- Make sure backend is running on port 8000
- Make sure frontend is running on port 3000
- Check browser console for specific errors

## Next Steps for Production

1. **Add user authentication** (JWT/OAuth)
2. **Implement queue system** (Celery + Redis) for async processing
3. **Add database** (PostgreSQL) for storing analysis history
4. **Deploy to cloud** (AWS/GCP/Vercel)
5. **Integrate with Gmail/Slack** via webhooks
6. **Add monitoring** (Sentry, DataDog)

## Support

For questions about this implementation, please check:
- README.md for detailed documentation
- ARCHITECTURE.md for system design
- SAMPLES.md for example outputs
