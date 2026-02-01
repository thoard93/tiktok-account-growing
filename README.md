# TikTok Account Automation System

Automate TikTok Shop account growth using GeeLark cloud phones, Proxiware proxies, and AI-generated content.

## Features

- **Account Management**: Create and manage TikTok accounts via GeeLark cloud phones
- **Proxy Integration**: Assign Proxiware static residential proxies to each account
- **Progressive Warmup**: 5-7 day warmup with gradual engagement increase
- **Video Posting**: Upload and auto-post AI-generated videos
- **Task Monitoring**: Track GeeLark task status and retry failed tasks
- **Dashboard**: Streamlit UI for management (separate service)

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/YOUR_USERNAME/tiktok-account-growing.git
cd tiktok-account-growing
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your GeeLark credentials
```

**Required .env settings:**

```env
GEELARK_APP_TOKEN=your_bearer_token_from_geelark_dashboard
GEELARK_API_BASE_URL=https://openapi.geelark.com/open/v1
DATABASE_URL=sqlite:///./data/tiktok_automation.db
```

### 3. Run the API

```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Access the API

- **API Docs**: <http://localhost:8000/docs>
- **Health Check**: <http://localhost:8000/api/health>

## API Endpoints

### Accounts

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/accounts` | GET | List all accounts |
| `/api/accounts` | POST | Create single account |
| `/api/accounts/batch` | POST | Create multiple accounts |
| `/api/accounts/{id}/start` | POST | Start cloud phone |
| `/api/accounts/{id}/stop` | POST | Stop cloud phone |
| `/api/accounts/{id}/install-tiktok` | POST | Install TikTok app |

### Proxies

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/proxies` | GET | List all proxies |
| `/api/proxies/bulk` | POST | Import proxies (host:port:user:pass format) |

### Warmup

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/warmup/start` | POST | Initialize warmup for accounts |
| `/api/warmup/run-session` | POST | Run warmup session |
| `/api/warmup/pending` | GET | Get accounts needing warmup |

### Videos

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/videos` | GET | List all videos |
| `/api/videos/upload` | POST | Upload video file |
| `/api/videos/{id}/post` | POST | Post video to TikTok |
| `/api/posting/auto` | POST | Auto-assign and post videos |

### GeeLark Direct

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/geelark/phones` | GET | List GeeLark cloud phones |
| `/api/geelark/phones/start` | POST | Start phones directly |
| `/api/geelark/tasks/query` | POST | Query task status |
| `/api/geelark/tasks/history` | GET | Get 7-day task history |
| `/api/geelark/tasks/{id}/detail` | GET | Get task details with logs |
| `/api/geelark/tasks/cancel` | POST | Cancel tasks |
| `/api/geelark/tasks/retry` | POST | Retry failed tasks |

## Warmup Strategy

The system uses a progressive warmup over 5 days:

| Day | Duration | Likes | Follows | Comments |
|-----|----------|-------|---------|----------|
| 1 | 30 min | 5 | 0 | 0 |
| 2 | 40 min | 10 | 2 | 0 |
| 3 | 45 min | 20 | 5 | 2 |
| 4 | 50 min | 30 | 10 | 3 |
| 5 | 60 min | 40 | 15 | 5 |

All values are randomized slightly to avoid detection.

## Deployment on Render

### Prerequisites

- GitHub repository with this code
- Render account

### Steps

1. **Create Web Service** on Render
   - Connect your GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Add Environment Variables** in Render:
   - `GEELARK_APP_TOKEN`
   - `GEELARK_API_BASE_URL`
   - `DATABASE_URL` (use Render's PostgreSQL add-on for production)

3. **Deploy**!

### render.yaml (Auto-deploy)

```yaml
services:
  - type: web
    name: tiktok-automation
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GEELARK_APP_TOKEN
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: tiktok-db
          property: connectionString

databases:
  - name: tiktok-db
    plan: free
```

## Project Structure

```
tiktok-account-growing/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Settings & env vars
│   ├── database.py          # SQLAlchemy setup
│   ├── models/
│   │   └── account.py       # Database models
│   ├── api/
│   │   ├── routes.py        # API endpoints
│   │   └── schemas.py       # Pydantic schemas
│   └── services/
│       ├── geelark_client.py    # GeeLark API wrapper
│       ├── account_manager.py   # Account lifecycle
│       ├── warmup_service.py    # Warmup automation
│       └── posting_service.py   # Video posting
├── data/                    # Local data storage
│   └── videos/              # Uploaded videos
├── logs/                    # Application logs
├── .env.example
├── .gitignore
├── requirements.txt
├── render.yaml
└── README.md
```

## Getting GeeLark API Token

1. Log into [GeeLark Dashboard](https://open.geelark.com)
2. Navigate to API settings
3. Click "Generate Token"
4. Copy the Bearer token to your `.env` file

## License

MIT
