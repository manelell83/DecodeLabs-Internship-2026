# BlueShield Auditor

A professional workstation security auditing platform — an enterprise Blue Team dashboard for
evaluating and improving the security posture of your own computer.

## Overview

BlueShield Auditor inspects real, local Windows security state — password policy, local accounts,
Windows Defender, firewall profiles, BitLocker, Windows Update recency, installed software, and
system information — and produces a single, explainable 0–100 security score. It extends the
DecodeLabs internship brief into a full-stack application with a resilient, honest architecture:
checks that need administrator rights or aren't supported on a given machine transparently fall
back to clearly-labeled simulated data instead of crashing or silently fabricating results.

## Features

- Real workstation audits: password policy, administrator accounts, Guest account, Windows
  Defender, firewall (all profiles), BitLocker (when available), Windows Update recency,
  installed software inventory, and system information
- **Real + simulated dual-mode design**: every finding is tagged `source: "real"` or
  `"simulated"` — a check that fails in real mode (no admin rights, unsupported edition, non-
  Windows host) automatically and transparently falls back to realistic demo data for that one
  check, never crashing the whole audit and never hiding that it happened
- Locale-independent checks: account/group lookups use well-known SIDs (not localized display
  names like "Administrateurs"/"Invité"), and password policy is read via `secedit /export`
  (stable English keys) instead of locale-dependent `net accounts` output
- Composite 0–100 security score with Excellent / Good / Fair / Poor bands
- Actionable, per-finding recommendations
- Audit history with search, filtering by level, and pagination
- JSON and PDF report generation (via ReportLab), downloadable per audit
- Dashboard with live charts (score trend, failing-category breakdown, level distribution)
- Dark/light mode, responsive layout, toast notifications, loading & empty states
- Interactive API documentation via Swagger UI (`/docs`) and ReDoc (`/redoc`)

## Architecture

**Backend** — Each security check is a small, independently testable class implementing a shared
`AuditCheck` interface with a `run_real()` and `run_simulated()` path; the base class handles the
real→simulated fallback so no check can crash the audit.

```
backend/
├── app/
│   ├── api/              # FastAPI routers (audits, reports, stats, health) + dependencies
│   ├── core/              # settings, logging, exception handling
│   ├── models/             # SQLAlchemy ORM models (AuditRun, Finding)
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/
│   │   ├── audit/            # one module per check + CommandRunner + AuditCheck base class
│   │   ├── audit_service.py    # orchestrates running all checks and persisting results
│   │   ├── audit_scorer.py      # aggregates findings into a 0-100 score + level
│   │   ├── stats_service.py      # dashboard aggregates via live SQL queries
│   │   └── report_generator.py    # JSON/PDF report generation
│   ├── database/           # engine/session management
│   └── main.py            # app factory, middleware, router wiring
├── tests/                  # pytest unit + API integration tests
└── requirements.txt
```

Dashboard "statistics" are computed via live SQL aggregate queries over `AuditRun`/`Finding`
rather than a separately-maintained snapshot table, so they're always accurate as of the latest
audit.

**Frontend** — Vite + React + TypeScript, TailwindCSS v4, React Router, Axios, React Hook Form +
Zod, and Recharts — the same stack as PhishGuard, re-skinned with a distinct enterprise blue
visual identity.

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/       # sidebar, topbar, mobile nav, theme toggle
│   │   ├── ui/            # button, card, badge, input, score gauge, empty state, skeleton
│   │   ├── audit/          # audit trigger (real/demo), audit result display, audit table
│   │   └── dashboard/       # stat cards, trend/category charts
│   ├── pages/              # Home, Dashboard, System Audit, Recommendations, History,
│   │                        Audit Detail, Reports, Statistics, Settings, About
│   ├── services/           # Axios client + typed API wrappers
│   ├── types/              # TypeScript types mirroring backend schemas
│   └── hooks/              # data-fetching hook
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
uvicorn app.main:app --reload --port 8001
```

The API is served at `http://127.0.0.1:8001`, with interactive docs at `/docs`.

> **Note:** the password policy check reads `secedit /export`, which requires the backend process
> to run **as Administrator** for real (non-simulated) results. Without elevation it gracefully
> falls back to simulated data for that one check — everything else (accounts, Defender, firewall,
> BitLocker, updates, software, system info) works without elevation.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app is served at the port Vite chooses (default 5180 here, configured in `vite.config.ts`;
Vite will pick another one if it's busy). Copy `.env.example` to `.env` to point the frontend at a
different backend URL if needed.

## Usage

1. Start the backend and frontend as above.
2. Open the frontend in your browser — the landing page introduces the tool.
3. Go to **System Audit**, choose **Real Audit** (inspects this machine) or **Demo Audit**
   (simulated data, safe on any OS), and run it.
4. Review the security score, findings (each tagged with severity and real/simulated source), and
   recommendations. Copy the summary or download a JSON/PDF report.
5. Browse **Recommendations** for a focused list of outstanding action items from your latest
   audit, **History** to search/filter past audits, **Dashboard**/**Statistics** for aggregate
   trends, and **Reports** to re-download any past audit's report.

## API Documentation

Full interactive documentation is generated automatically by FastAPI:

- Swagger UI: `http://127.0.0.1:8001/docs`
- ReDoc: `http://127.0.0.1:8001/redoc`

Key endpoints (all under `/api/v1`):

| Method | Path | Description |
|---|---|---|
| POST | `/audits` | Run a new audit (`mode: "real"` or `"demo"`) and persist the result |
| GET | `/audits` | List audits (pagination, level filter) |
| GET | `/audits/{id}` | Full audit detail with all findings |
| DELETE | `/audits/{id}` | Delete an audit |
| GET | `/audits/{id}/report?format=json\|pdf` | Generate/download a report |
| GET | `/stats` | Aggregate dashboard statistics |
| GET | `/health` | Liveness check |

## Testing

```bash
cd backend
pytest
```

32 tests cover the audit scorer, the real→simulated fallback behavior of the check base class,
each check's simulated output, the `CommandRunner`'s error handling, and the full API flow
(audit → history → report) via `TestClient`. All API/integration tests run in `mode: "demo"` so
they're deterministic and OS-independent — no admin rights or Windows host required to run the
suite.

## Screenshots

_Placeholder — add screenshots of the Landing page, Dashboard, and System Audit result here._

## Future Improvements

- Add authentication for multi-machine fleet auditing by a security team
- Historical diffing: highlight what changed between two audits of the same host
- Integrate a real Windows Update pending-patch count via the WU COM API (current check is a
  best-effort proxy based on the most recent installed hotfix date)
- Scheduled/automated periodic audits with alerting on regression
- Package the backend as a signed, installable Windows service

## License

This project is licensed under the MIT License.
