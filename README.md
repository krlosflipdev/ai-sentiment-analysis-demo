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
- npm 10+
- MongoDB Atlas account

### Setup

1. **Clone and install all dependencies:**

```bash
git clone <repo-url>
cd ai-sentiment-analysis-demo
npm run setup
```

2. **Configure environment variables:**

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
cp worker/.env.example worker/.env
```

Edit each `.env` file with your credentials (see Environment Variables section below).

3. **Run all services:**

```bash
npm run dev
```

- Backend API: http://localhost:8000
- Frontend Dashboard: http://localhost:5173

## Available Commands

Run from the root directory:

| Command | Description |
|---------|-------------|
| `npm run dev` | Run all apps with Turborepo UI (sidebar) |
| `npm run dev:stream` | Run all apps with colored log prefixes |
| `npm run backend` | Run backend only |
| `npm run frontend` | Run frontend only |
| `npm run worker` | Run worker only |
| `npm run build` | Build all packages |
| `npm run lint` | Lint all packages |
| `npm run setup` | Install all dependencies (npm + Python) |

## Environment Variables

Create a `.env` file in each directory based on `.env.example`:

### backend/.env

| Variable | Description |
|----------|-------------|
| `MONGODB_URI` | MongoDB Atlas connection string |

### frontend/.env

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend API URL (default: http://localhost:8000) |

### worker/.env

| Variable | Description |
|----------|-------------|
| `MONGODB_URI` | MongoDB Atlas connection string |
| `TWITTER_BEARER_TOKEN` | Twitter/X API bearer token |
| `HUGGINGFACE_API_KEY` | Hugging Face API key |

## API Keys Setup

### MongoDB Atlas

1. Create a free account at [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Create a new cluster (free tier available)
3. Go to **Database Access** → Add a database user with password
4. Go to **Network Access** → Add IP `0.0.0.0/0` (allow all) or your specific IP
5. Go to **Database** → Click **Connect** → **Drivers** → Copy the connection string
6. Replace `<password>` with your database user password

```
mongodb+srv://username:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### Twitter/X API

1. Apply for a developer account at [developer.x.com](https://developer.x.com)
2. Create a new project and app
3. Go to **Keys and Tokens** → Generate **Bearer Token**
4. Copy the bearer token (starts with `AAAA...`)

> Note: Twitter API requires approval and may have rate limits on the free tier.

### Hugging Face API

1. Create a free account at [huggingface.co](https://huggingface.co)
2. Go to **Settings** → **Access Tokens** ([huggingface.co/settings/tokens](https://huggingface.co/settings/tokens))
3. Click **New token** → Name it → Select **Read** access
4. Copy the token (starts with `hf_...`)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/health` | API v1 health check |

## License

MIT
