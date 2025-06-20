# MCP Server - Allure Test Failure Analyzer

A FastAPI-based server that accepts Allure report uploads, parses failed and broken test cases, uses OpenAI GPT to explain failures, and saves results in a database. Includes a web dashboard for viewing analyzed failures.

---

## Features
- Upload Allure results as a zip file
- Parses failed and broken test cases from Allure results
- Uses GPT (OpenAI) to generate explanations for failures
- Saves results in a SQLite database
- Web dashboard to view all analyzed failures

---

## Quick Start

### 1. Clone the repository
```sh
git clone <your-repo-url>
cd mcp-allure-analyzer
```

### 2. Build and Run with Docker

**Build the Docker image:**
```sh
docker build -t mcp-server .
```

**Run the container (replace `sk-...` with your OpenAI API key):**
```sh
docker run -p 8080:80 -e OPENAI_API_KEY=sk-... mcp-server
```

### 3. Running Locally (without Docker)

**Install dependencies:**
```sh
pip install -r requirements.txt
```

**Set your OpenAI API key:**
```sh
export OPENAI_API_KEY=sk-...
```

**Start the server:**
```sh
uvicorn app.main:app --reload
```

---

## Usage

### Upload Allure Results
Send a POST request to `/upload` with your Allure results zip file:
```sh
curl -F "file=@results.zip" http://localhost:8080/upload
```

### View Dashboard
Open your browser and go to:
```
http://localhost:8080/dashboard
```

### API Endpoints
- `GET /` — Health check
- `POST /upload` — Upload Allure results zip
- `GET /reports` — Get all analyzed failures (JSON)
- `GET /dashboard` — Web dashboard

---

## Environment Variables
- `OPENAI_API_KEY` — Your OpenAI API key (required)
- `DB_PATH` — Path to SQLite DB (default: `/app/data/failures.db` in Docker)

---

## Notes
- The server expects the Allure results zip to contain a `results/` folder with `*-result.json` files.
- Both `failed` and `broken` test statuses are analyzed.
- If you see quota or API key errors, check your OpenAI account and billing.

---

## License
MIT
