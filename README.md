# AI Sentiment Analysis Demo

Real-time sentiment analysis application using NLP/ML. Fetches social media data, analyzes sentiment with Hugging Face Transformers, and displays results in an interactive dashboard.

## Tech Stack

- **Backend:** Python 3.12, FastAPI, Motor (async MongoDB)
- **Frontend:** React 19, Vite, TypeScript, Tailwind CSS, Chart.js
- **ML/NLP:** Hugging Face Transformers (DistilBERT)
- **Database:** MongoDB Atlas
- **Hosting:** Render (API), Vercel (Frontend), GitHub Actions (Worker)

## Project Structure

```
/backend     # FastAPI REST API
/frontend    # React Dashboard
/worker      # Sentiment analysis worker (GitHub Actions)
```

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- MongoDB Atlas account

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Edit with your credentials
uvicorn main:app --reload
```

API available at http://localhost:8000

### Frontend

```bash
cd frontend
npm install
cp .env.example .env      # Edit if needed
npm run dev
```

Dashboard available at http://localhost:5173

## Environment Variables

Create a `.env` file in each directory (backend, frontend, worker) based on `.env.example`:

| Variable | Description |
|----------|-------------|
| `MONGODB_URI` | MongoDB Atlas connection string |
| `TWITTER_BEARER_TOKEN` | Twitter/X API bearer token |
| `HUGGINGFACE_API_KEY` | Hugging Face API key |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/health` | API v1 health check |

## License

MIT
