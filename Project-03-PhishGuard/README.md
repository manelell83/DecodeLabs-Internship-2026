# PhishGuard

A professional phishing awareness and email analysis platform — a Blue Team SOC tool for
detecting, scoring, and reporting on phishing emails.

## Overview

PhishGuard simulates the kind of internal tool a Security Operations Center analyst would use to
triage suspicious emails. It parses raw email content, runs it through a rule-based detection
engine covering URL structure, brand impersonation, and social-engineering language, and produces
a fully explainable 0–100 risk score with concrete indicators and recommendations — never an
opaque black box. Every scan is stored, searchable, and exportable as a JSON or PDF report.

This project extends the DecodeLabs internship brief into a full-stack application: a FastAPI
backend with a layered, testable detection pipeline, and a modern React/TypeScript SOC console
frontend.

## Features

- Email parsing: extracts headers, body, URLs, and domains from raw email text
- Multi-vector detection: IP-based URLs, shortened links, suspicious TLDs, homograph/typosquat
  domains, credential-theft phrasing, fake-login pages, urgency language, financial/lottery/
  crypto/gift-card scam language, and brand impersonation (Microsoft, Google, PayPal, banking)
- Explainable 0–100 risk scoring with Low/Medium/High/Critical bands
- Actionable, de-duplicated recommendations per scan
- Scan history with search, filtering, and pagination
- JSON and PDF report generation (via ReportLab), downloadable per scan
- Dashboard with live charts (risk trend, category breakdown, risk distribution)
- Suspicious content highlighting directly in the original email body
- Dark/light mode, responsive layout, toast notifications, loading & empty states
- Interactive API documentation via Swagger UI (`/docs`) and ReDoc (`/redoc`)

## Architecture

**Backend** — Clean, layered architecture: routers depend only on services, services depend only
on models/schemas, and each detection concern (URL analysis, content analysis, scoring,
recommendations, reporting) is an independently unit-tested class.

```
backend/
├── app/
│   ├── api/            # FastAPI routers (scans, reports, stats, health) + dependencies
│   ├── core/           # settings, logging, exception handling
│   ├── models/         # SQLAlchemy ORM models (Scan, Indicator, Report)
│   ├── schemas/        # Pydantic request/response schemas
│   ├── services/       # email parser, URL/content analyzers, risk scorer,
│   │                    recommendation engine, report generator, orchestration
│   ├── database/       # engine/session management
│   └── main.py         # app factory, middleware, router wiring
├── tests/               # pytest unit + API integration tests
└── requirements.txt
```

Dashboard "statistics" are computed via live SQL aggregate queries over `Scan`/`Indicator`
(`services/stats_service.py`) rather than a separately-maintained snapshot table — this avoids
sync bugs and is always accurate as of the latest scan.

**Frontend** — Vite + React + TypeScript, TailwindCSS v4 for styling, React Router for navigation,
Axios for API access, React Hook Form + Zod for validated forms, and Recharts for data
visualization.

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/      # sidebar, topbar, mobile nav, theme toggle
│   │   ├── ui/           # button, card, badge, input, score gauge, empty state, skeleton
│   │   ├── analyzer/     # email form, scan result, highlighted content
│   │   ├── dashboard/    # stat cards, trend/category charts
│   │   └── scans/        # shared scan table (history + dashboard)
│   ├── pages/            # Landing, Dashboard, Analyzer, History, Scan Detail, Reports,
│   │                      Statistics, Settings, About
│   ├── services/         # Axios client + typed API wrappers
│   ├── types/            # TypeScript types mirroring backend schemas
│   └── hooks/            # data-fetching hook
└── package.json
```

## Installation

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is served at `http://127.0.0.1:8000`, with interactive docs at `/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app is served at `http://localhost:5173` (Vite will pick another port if that one is busy).
Copy `.env.example` to `.env` to point the frontend at a different backend URL if needed.

## Usage

1. Start the backend and frontend as above.
2. Open the frontend in your browser — the landing page introduces the tool.
3. Go to **Email Analyzer**, paste a suspicious email (or click "Load sample phishing email"),
   and submit it for analysis.
4. Review the risk score, highlighted suspicious content, triggered indicators, and
   recommendations. Copy the summary or download a JSON/PDF report.
5. Browse **Scan History** to search and filter past scans, **Dashboard**/**Statistics** for
   aggregate trends, and **Reports** to re-download any past scan's report.

## API Documentation

Full interactive documentation is generated automatically by FastAPI:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Key endpoints (all under `/api/v1`):

| Method | Path | Description |
|---|---|---|
| POST | `/scans` | Analyze a submitted email and persist the scan |
| GET | `/scans` | List scans (pagination, search, risk-level filter) |
| GET | `/scans/{id}` | Full scan detail with indicators and recommendations |
| DELETE | `/scans/{id}` | Delete a scan |
| GET | `/scans/{id}/report?format=json\|pdf` | Generate/download a report |
| GET | `/stats` | Aggregate dashboard statistics |
| GET | `/health` | Liveness check |

## Testing

```bash
cd backend
pytest
```

26 tests cover the URL analyzer, content analyzer, risk scorer, and the full API flow
(scan → history → report) via `TestClient` against an isolated in-memory SQLite database.

## Screenshots

_Placeholder — add screenshots of the Landing page, Dashboard, and Email Analyzer here._

## Future Improvements

- Persist generated reports to disk with a dedicated download endpoint per stored report
- Add authentication for multi-analyst SOC deployments
- Integrate real-time threat-intelligence feeds for domain reputation lookups
- Support `.eml` file upload in addition to pasted text
- Add WebSocket-based live scan notifications

## License

This project is licensed under the MIT License.
