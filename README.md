# Summarize & Sentiment API

Production-style FastAPI service that exposes LLM-powered text summarization and sentiment analysis endpoints using the OpenAI Responses API.

Built as an AI engineering portfolio project to demonstrate clean API design, schema validation, resilient model-output parsing, and deployment-ready structure.

## Why This Project

This repository showcases practical applied-AI backend skills recruiters and hiring managers look for:

- Designing typed, testable API contracts with Pydantic
- Integrating LLMs into backend services (not just notebooks)
- Hardening model outputs with parsing/validation logic
- Implementing structured JSON logging (`structlog`) for observability
- Organizing code into routes, services, and schemas for maintainability

## Features

- **Health endpoint** for service uptime checks
- **Summarization endpoint** with length control
- **Sentiment endpoint** returning structured JSON (`sentiment`, `confidence`, `explanation`)
- **Strict validation and normalization** of model sentiment labels
- **Environment-driven config** (`OPENAI_API_KEY`, optional `OPENAI_MODEL`)
- **Render-friendly entrypoint** via `main.py` (`uvicorn main:app`)

## Tech Stack

- Python
- FastAPI
- OpenAI Python SDK (`responses.create`)
- Pydantic v2
- Structlog
- Uvicorn
- python-dotenv

## Project Structure

```text
.
├── app/
│   ├── main.py                 # FastAPI app factory, logging setup
│   ├── routes/
│   │   ├── health.py           # GET /health
│   │   ├── summarize.py        # POST /summarize
│   │   └── sentiment.py        # POST /analyze-sentiment
│   ├── schemas/
│   │   └── models.py           # Request/response models
│   └── services/
│       ├── summarize.py        # LLM summarization logic
│       └── sentiment.py        # LLM sentiment + robust JSON parsing
├── main.py                     # host entrypoint (uvicorn main:app)
└── requirements.txt
```

## API Endpoints

### `GET /health`
Returns status and timestamp.

### `POST /summarize`
Generates a concise summary.

**Request body**
```json
{
  "text": "Long source text...",
  "max_length": 80
}
```

**Response body**
```json
{
  "summary": "Short summary text..."
}
```

### `POST /analyze-sentiment`
Analyzes sentiment and returns typed output.

**Request body**
```json
{
  "text": "I loved how smooth this release felt!"
}
```

**Response body**
```json
{
  "sentiment": "positive",
  "confidence": 0.93,
  "explanation": "The text expresses clear satisfaction and positive emotion."
}
```

## Local Setup

1. Clone and enter project
```bash
git clone https://github.com/zainabahmed4626-lab/AIEngineeringW1V2.git
cd AIEngineeringW1V2
```

2. Create virtual environment
```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```env
OPENAI_API_KEY=your_openai_key
# Optional
OPENAI_MODEL=gpt-4.1-mini
```

5. Run API
```bash
uvicorn app.main:app --reload
```

Alternative host-style run:
```bash
uvicorn main:app --reload
```

6. Open interactive docs
- Swagger UI: `http://127.0.0.1:8000/docs`

## Example cURL Commands

```bash
curl -X GET "http://127.0.0.1:8000/health"
```

```bash
curl -X POST "http://127.0.0.1:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text":"FastAPI makes building APIs fast and maintainable.","max_length":20}'
```

```bash
curl -X POST "http://127.0.0.1:8000/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text":"The onboarding flow is confusing and frustrating."}'
```

## Engineering Notes

- Sentiment service includes normalization for common label variants (`pos`, `mixed`, etc.) before mapping to strict enum values.
- Services fail fast when required env vars are missing.
- Route layer catches exceptions and returns controlled HTTP 500 errors while logging structured failure context.

## Recruiter Snapshot

This project demonstrates readiness for roles involving:

- AI/LLM backend engineering
- API productization of GenAI features
- Reliable model-in-the-loop service development
- Deployable Python service architecture

---

If you are reviewing this repository for a role, I can also provide a short architecture walkthrough and trade-off discussion (latency, cost, and model reliability choices).
