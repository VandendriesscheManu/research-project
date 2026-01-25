# 📊 Marketing Plan Generator

AI-powered complete 12-section marketing plan creation using Streamlit, FastAPI, MCP (Model Context Protocol), and LLMs (Groq).

## 🏗️ Architecture

```
Streamlit Frontend (Cloud) → Cloudflare Tunnel → FastAPI Backend → MCP Server → LLM (Groq) → PostgreSQL
                                    ↓
                             GitHub Gist (URL sync)
```

## ✨ Features

- **Complete 12-Section Marketing Plans**: Executive summary, mission/vision, market analysis, SWOT, positioning, goals, marketing mix (7Ps), action plan, budget, monitoring, risks, and launch strategy
- **AI Field Assistant**: Inline suggestions for every input field with ✨ button
- **AI-Powered Evaluation**: Automated quality assessment with scores for consistency, quality, originality, feasibility, completeness, and ethics
- **8-Step Guided Form**: Comprehensive product information collection
- **Demo Mode**: Toggle to fill form with example data (EcoBottle Pro)
- **Dynamic URL Management**: Automatic Cloudflare tunnel URL updates via GitHub Gist
- **Fast LLM**: Groq API with llama-3.1-8b-instant for speed and cost efficiency
- **Persistent Storage**: PostgreSQL database for product briefs and marketing plans
- **Docker Compose**: Complete containerized setup

## 📋 Prerequisites

### Required Software

1. **Docker Desktop** (Windows/Mac/Linux)
   - Download: https://www.docker.com/products/docker-desktop/
   - Install Docker Desktop and ensure it's running
   - Verify installation: `docker --version` and `docker-compose --version`

2. **Git** (for cloning the repository)
   - Download: https://git-scm.com/downloads
   - Verify installation: `git --version`

3. **GitHub Account** (for Gist URL management)
   - Sign up: https://github.com/join

4. **Groq API Key** (free, required for LLM)
   - Sign up: https://console.groq.com
   - Get your API key (pay-as-you-go recommended for unlimited rate limits)

### Optional

- **Text Editor** (VS Code recommended)
- **Python 3.11+** (only if running frontend locally outside Docker)

## 🚀 Quick Setup Guide

### Step 1: Install Docker Desktop

1. **Windows**: Download and install [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - Minimum: Windows 10 64-bit with WSL 2
   - After install, restart your computer
   - Start Docker Desktop from Start menu
2. **Mac**: Download and install [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
   - Choose the correct version (Apple Silicon or Intel)
3. **Linux**: Follow [Docker Engine installation guide](https://docs.docker.com/engine/install/)

**✅ Verify Docker is running:**

```bash
docker --version
docker-compose --version
```

Expected output: Version numbers for both commands (e.g., Docker version 24.x.x).

### Step 2: Clone the Repository

```bash
git clone https://github.com/VandendriesscheManu/research-project.git
cd research-project
```

### Step 3: Get API Keys

1. **Groq API Key** (required for LLM):
   - Go to https://console.groq.com
   - Sign up with Google/GitHub
   - Create an API key (pay-as-you-go recommended for unlimited rate limits)
   - Copy the key (starts with `gsk_`)

2. **GitHub Token** (required for Gist URL management):
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Give it a name: `Marketing Plan Generator`
   - Select only scope: `gist`
   - Click "Generate token" and copy it (starts with `ghp_`)

### Step 4: Create Environment File

### Step 4: Create Environment File

Copy the example environment file:

```bash
git clone https://github.com/VandendriesscheManu/research-project.git
cd research-project
```

### 2. Create Environment File

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and replace ALL placeholder values with your actual keys:

```env
# ========================================
# Backend Configuration
# ========================================
DATABASE_URL=postgresql://postgres:postgres@db:5432/marketing_db

# ========================================
# LLM Configuration
# ========================================
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_actual_groq_key_here

# ========================================
# MCP Server Configuration
# ========================================
MCP_SERVER_CONFIG={"groq": {"apiKey": "gsk_your_actual_groq_key_here"}}

# ========================================
# URL Management Configuration
# ========================================
GITHUB_TOKEN=ghp_your_actual_github_token_here
GITHUB_GIST_ID=leave_empty_will_be_created_automatically
TUNNEL_URL=http://localhost:8000

# ========================================
# Database Configuration
# ========================================
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=marketing_db
```

**⚠️ Important**:

- Replace `gsk_your_actual_groq_key_here` with your Groq API key (from Step 3)
- Replace `ghp_your_actual_github_token_here` with your GitHub token (from Step 3)
- Leave `GITHUB_GIST_ID` empty - it will be created automatically
- Use the SAME Groq key in both `GROQ_API_KEY` and `MCP_SERVER_CONFIG`

### Step 5: Start Services

```bash
docker-compose up -d
```

This will:

- Download all required Docker images (first time only, may take 5-10 minutes)
- Start PostgreSQL database
- Start FastAPI backend
- Start MCP server
- Start Cloudflare tunnel
- Start URL extractor service
- Initialize database with required tables

**✅ Verify all containers are running:**

```bash
docker-compose ps
```

Expected output: All 5 services (db, backend, mcp-server, cloudflare-tunnel, url-extractor) should show "Up" status.

**🔍 Check logs if something fails:**

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs mcp-server
docker-compose logs cloudflare-tunnel
```

### Step 6: Get Your Cloudflare Tunnel URL

After starting services, find your public tunnel URL:

```bash
docker-compose logs cloudflare-tunnel | grep "trycloudflare.com"
```

You'll see a line like:

```
cloudflare-tunnel | https://random-words-1234.trycloudflare.com
```

Copy this URL - you'll need it for the frontend deployment.

### Step 7: Deploy Frontend on Streamlit Cloud

The frontend runs on Streamlit Cloud (free hosting):

1. **Push code to GitHub** (if not already done):

```bash
git add .
git commit -m "Initial setup"
git push origin main
```

2. **Deploy on Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `your-username/research-project`
   - Set **Main file path**: `frontend/app.py`
   - Set **Python version**: `3.11`
   - Click "Advanced settings"
   - Click "Deploy"

3. **Configure Streamlit Secrets**:
   - After deployment, click on your app
   - Go to **Settings** → **Secrets**
   - Add your GitHub credentials:

```toml
GITHUB_TOKEN = "ghp_your_actual_github_token_here"
GITHUB_GIST_ID = "your_gist_id_from_docker_logs"
```

To find your `GITHUB_GIST_ID`, check backend logs:

```bash
docker-compose logs backend | grep "Gist ID"
```

4. **Save and Reboot** the Streamlit app

### Step 8: Verify Everything Works

1. **Check backend API**:

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy"}`

2. **Check tunnel is accessible**:
   - Open your Cloudflare tunnel URL in browser
   - You should see FastAPI documentation

3. **Test the frontend**:
   - Open your Streamlit app URL
   - Toggle "📝 Fill form with demo data" switch
   - Click through the 8 form steps
   - Click "🚀 Generate Marketing Plan"
   - Wait 30-60 seconds
   - You should see:
     - ✅ Evaluation scores (6 criteria)
     - ✅ 12 marketing plan sections
     - ✅ Strengths and weaknesses analysis

✅ **Setup Complete!** Your AI Marketing Plan Generator is fully operational.

---

## 💻 Local Development (Optional)

If you want to run the frontend locally instead of Streamlit Cloud:

### Prerequisites

- **Python 3.11+**: Download from https://www.python.org/downloads/

### Setup

1. **Navigate to frontend folder**:

```bash
cd frontend
```

2. **Create virtual environment**:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Create `.streamlit/secrets.toml`**:

```bash
mkdir .streamlit
```

Edit `.streamlit/secrets.toml`:

```toml
GITHUB_TOKEN = "ghp_your_actual_github_token_here"
GITHUB_GIST_ID = "your_gist_id"
```

5. **Run Streamlit**:

```bash
streamlit run app.py
```

6. **Open browser**: http://localhost:8501

### Hot Reloading

Streamlit automatically reloads when you save changes to `app.py`.

---

## 📊 Usage

### Generating a Marketing Plan

1. **Start with Demo Data** (recommended for first time):
   - Toggle "📝 Fill form with demo data"
   - This fills the form with EcoBottle Pro example

2. **Fill the 8-Step Form**:
   - Step 1: Product Information
   - Step 2: Target Audience
   - Step 3: Market Context
   - Step 4: Unique Selling Points
   - Step 5: Brand Identity
   - Step 6: Goals & Metrics
   - Step 7: Constraints
   - Step 8: Additional Information

3. **Use AI Assistants** (✨ buttons):
   - Click ✨ next to any field for AI suggestions
   - Copy suggestions or modify them
   - Available for all text inputs

4. **Generate Plan**:
   - Click "🚀 Generate Marketing Plan"
   - Wait 30-60 seconds (8-15 LLM calls)
   - Cost: ~$0.0008 per plan

5. **Review Results**:
   - **Evaluation Section**: AI-generated quality scores
     - Consistency, Quality, Originality
     - Feasibility, Completeness, Ethics
     - Strengths and weaknesses
   - **12 Marketing Sections**: Navigate with Previous/Next
     - Executive Summary
     - Mission & Vision
     - Market Analysis
     - SWOT Analysis
     - Positioning & Messaging
     - Marketing Goals
     - Marketing Mix (7Ps)
     - Action Plan
     - Budget
     - Monitoring Plan
     - Risk Management
     - Launch Strategy

### Understanding Costs

- **Generation**: ~8 LLM calls with llama-3.1-8b-instant
- **Evaluation**: ~6-7 LLM calls with llama-3.3-70b-versatile
- **Total cost**: ~$0.0008 per complete marketing plan
- **AI Assistant**: ~$0.00001 per suggestion

With Groq's pay-as-you-go plan:

- 1000 marketing plans = ~$0.80
- Unlimited rate limits
- Fast response times (<5s per call)

---

## 🔧 Configuration Details

### Environment Variables Reference

| Variable            | Description                  | Required        | Default               |
| ------------------- | ---------------------------- | --------------- | --------------------- |
| `GROQ_API_KEY`      | Groq API key for LLM         | ✅ Yes          | None                  |
| `MCP_SERVER_CONFIG` | JSON config with Groq key    | ✅ Yes          | None                  |
| `GITHUB_TOKEN`      | GitHub PAT with gist scope   | ✅ Yes          | None                  |
| `GITHUB_GIST_ID`    | Gist ID for URL storage      | After first run | Auto-created          |
| `DATABASE_URL`      | PostgreSQL connection string | ✅ Yes          | postgresql://...      |
| `POSTGRES_USER`     | Database username            | ✅ Yes          | postgres              |
| `POSTGRES_PASSWORD` | Database password            | ✅ Yes          | postgres              |
| `POSTGRES_DB`       | Database name                | ✅ Yes          | marketing_db          |
| `LLM_PROVIDER`      | LLM provider selection       | No              | groq                  |
| `TUNNEL_URL`        | Internal backend URL         | No              | http://localhost:8000 |

### LLM Models Used

- **Generation**: `llama-3.1-8b-instant` - Fast, cost-effective for plan generation
- **Evaluation**: `llama-3.3-70b-versatile` - More capable for quality assessment
- **AI Assistant**: `llama-3.1-8b-instant` - Quick suggestions

### Database Schema

The PostgreSQL database includes:

- `product_briefs` - Stores form submissions
- `marketing_plans` - Generated marketing plans
- `conversations` - Chat history (legacy)

---

## 🔍 Troubleshooting

### Docker Issues

**Problem**: `docker-compose: command not found`

```bash
# Solution: Install Docker Desktop or Docker Compose
# Windows/Mac: Install Docker Desktop
# Linux: sudo apt install docker-compose
```

**Problem**: Permission denied on Docker

```bash
# Linux solution
sudo usermod -aG docker $USER
newgrp docker
```

**Problem**: Containers not starting

```bash
# Check logs
docker-compose logs

# Restart services
docker-compose down
docker-compose up -d

# Check if ports are in use
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -i :8000
```

### API/Backend Issues

**Problem**: `curl http://localhost:8000/health` fails

```bash
# Check if backend container is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend

# Check if port 8000 is accessible
curl -v http://localhost:8000/health
```

**Problem**: "Internal server error" from API

```bash
# Check database connection
docker-compose logs db

# Restart backend
docker-compose restart backend
```

### Groq API Issues

**Problem**: "Invalid API key"

- Verify your `.env` has correct `GROQ_API_KEY`
- Check key starts with `gsk_`
- Ensure same key in `MCP_SERVER_CONFIG`
- Restart services: `docker-compose restart`

**Problem**: "Rate limit exceeded"

- Free tier: 30 requests/minute
- Upgrade to pay-as-you-go at https://console.groq.com
- Wait 60 seconds and try again

**Problem**: "Model not found"

- Check model name is correct: `llama-3.1-8b-instant`
- View available models at https://console.groq.com/docs/models

### Streamlit Frontend Issues

**Problem**: Frontend shows "Connection error"

- Check Cloudflare tunnel URL is correct
- Verify `GITHUB_GIST_ID` in Streamlit secrets
- Check backend logs: `docker-compose logs backend`
- Wait 30 seconds for tunnel to start

**Problem**: "Failed to fetch URL from Gist"

- Verify `GITHUB_TOKEN` has `gist` scope
- Check token is valid: https://github.com/settings/tokens
- Verify `GITHUB_GIST_ID` exists in backend logs
- Update Streamlit secrets with correct values

**Problem**: Demo data not filling form

- Refresh the page (Ctrl+R)
- Clear browser cache
- Check browser console for errors (F12)

### Cloudflare Tunnel Issues

**Problem**: Tunnel URL changes on restart

- This is normal behavior (free tunnel)
- URL automatically syncs via Gist
- Frontend fetches new URL within 10 seconds
- No action needed

**Problem**: Tunnel URL not accessible

```bash
# Check tunnel logs
docker-compose logs cloudflare-tunnel

# Look for URL in output
docker-compose logs cloudflare-tunnel | grep "trycloudflare.com"

# Restart tunnel
docker-compose restart cloudflare-tunnel
```

**Problem**: Gist not updating with new URL

```bash
# Check url-extractor logs
docker-compose logs url-extractor

# Verify GITHUB_TOKEN in .env
grep GITHUB_TOKEN .env

# Restart extractor
docker-compose restart url-extractor
```

### Generation Issues

**Problem**: "Evaluation unavailable" showing in plan

- This is normal - evaluator failed but plan succeeded
- Plan will still have all 12 sections
- Check MCP server logs: `docker-compose logs mcp-server`
- Retry generation for evaluation

**Problem**: Plan generation stuck/hanging

- Wait at least 60 seconds (15+ LLM calls needed)
- Check browser console for errors (F12)
- Verify backend is responding: `curl http://localhost:8000/health`
- Check Groq API status: https://status.groq.com

**Problem**: "Failed to generate plan"

```bash
# Check backend logs for details
docker-compose logs backend | tail -100

# Common causes:
# - Groq API rate limit (wait 60s)
# - Database connection failed (restart db)
# - MCP server timeout (restart mcp-server)
```

### First-Time Setup Issues

**Problem**: `.env` file not found

```bash
# Create from example
cp .env.example .env

# Then edit with your keys
```

**Problem**: Gist ID not generating

- Check `GITHUB_TOKEN` is set in `.env`
- Token must have `gist` scope
- Start backend and check logs: `docker-compose logs backend`
- Look for "Created new gist:" message

**Problem**: Python module errors in frontend

```bash
# Make sure you're in venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Getting Help

If you encounter issues not covered here:

1. **Check logs**: `docker-compose logs [service-name]`
2. **Verify configuration**: Double-check `.env` file
3. **Restart services**: `docker-compose restart`
4. **Full reset**:

```bash
docker-compose down
docker volume rm research-project_postgres_data
docker-compose up -d
```

**Common log commands**:

```bash
# All logs
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs mcp-server

# Follow logs live
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

---

## 🛠️ Development

### Project Structure

---

## 🛠️ Development

### Project Structure

```
research-project/
├── backend/                    # FastAPI backend
│   ├── main.py                # Main API endpoints
│   ├── core/
│   │   ├── db.py             # PostgreSQL operations
│   │   └── mcp_client.py     # MCP communication
│   ├── agents/
│   │   ├── fast_marketing_orchestrator.py  # Marketing plan generation
│   │   ├── field_assistant_agent.py        # AI field suggestions
│   │   └── evaluator_agent.py             # Plan quality evaluation
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # Streamlit frontend
│   ├── app.py                # Main UI (1400+ lines)
│   ├── requirements.txt      # streamlit, requests
│   └── .streamlit/
│       └── secrets.toml      # GitHub token, Gist ID
├── mcp-server/                # MCP server with LLM client
│   ├── server.py             # MCP protocol handler
│   ├── agents/
│   │   └── llm_client.py    # Groq API integration
│   ├── requirements.txt
│   └── dockerfile
├── url-extractor/             # Cloudflare URL sync service
│   ├── extract_url.py        # Monitors tunnel logs
│   ├── requirements.txt
│   └── Dockerfile
├── db/
│   └── init.sql              # Database schema
├── docker-compose.yml         # 5 services orchestration
├── .env.example              # Environment template
└── README.md                 # This file
```


### Development Workflow

#### Working on Backend

```bash
# View real-time logs
docker-compose logs -f backend

# Restart after code changes
docker-compose restart backend

# Access Python shell
docker exec -it backend python

# Run database migrations (if needed)
docker exec -it backend python -m alembic upgrade head
```

#### Working on Frontend

```bash
# Run locally for development
cd frontend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py

# Deploy to Streamlit Cloud
git push origin main
# Streamlit Cloud auto-deploys on push
```

#### Working on MCP Server

```bash
# View MCP logs
docker-compose logs -f mcp-server

# Test MCP connection
docker exec -it backend python -c "from core.mcp_client import MCPClient; print(MCPClient().get_llm_response('test'))"

# Restart MCP server
docker-compose restart mcp-server
```

#### Database Operations

```bash
# Connect to PostgreSQL
docker exec -it db psql -U postgres -d marketing_db

# View tables
\dt

# View product briefs
SELECT id, name, category FROM product_briefs;

# View marketing plans
SELECT id, brief_id, created_at FROM marketing_plans;

# Backup database
docker exec db pg_dump -U postgres marketing_db > backup.sql

# Restore database
docker exec -i db psql -U postgres marketing_db < backup.sql
```

### API Documentation

Once running, access interactive API docs:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Key endpoints:

- `POST /api/product-brief` - Create product brief
- `POST /api/marketing-plan` - Generate marketing plan
- `POST /api/field-assistant` - Get AI field suggestions
- `GET /api/product-brief/{id}` - Get product brief
- `GET /health` - Health check

### Testing

```bash
# Test backend health
curl http://localhost:8000/health

# Test field assistant
curl -X POST http://localhost:8000/api/field-assistant \
  -H "Content-Type: application/json" \
  -d '{"field":"target_audience","context":"eco-friendly water bottle"}'

# Test plan generation (will take 30-60s)
curl -X POST http://localhost:8000/api/marketing-plan \
  -H "Content-Type: application/json" \
  -d @sample_brief.json
```

### Monitoring

```bash
# Container resource usage
docker stats

# View all container logs
docker-compose logs

# Check container health
docker-compose ps

# Network inspection
docker network inspect research-project_default
```

---

## 🔐 Security

- ✅ Never commit `.env` file to Git
- ✅ Keep `GROQ_API_KEY` and `GITHUB_TOKEN` secret
- ✅ Rotate API keys regularly
- ✅ Use strong passwords for PostgreSQL
- ✅ Gists created are private by default
- ✅ Cloudflare tunnel provides HTTPS encryption
- ✅ Backend validates all inputs

**Important**: This setup uses a free Cloudflare tunnel which changes URL on restart. For production:

- Use Cloudflare Zero Trust with permanent tunnel
- Add custom domain
- Enable authentication
- Use managed database service

---

## 📝 License

This project is for educational/research purposes.

---

## 🙏 Acknowledgments

- **Streamlit** - Beautiful Python web apps
- **FastAPI** - Modern Python API framework
- **Groq** - Fast LLM inference
- **MCP** - Model Context Protocol
- **Cloudflare** - Free secure tunneling
- **PostgreSQL** - Reliable database

---

## 📧 Support

For questions or issues:

- Check this README first
- Review [Troubleshooting](#-troubleshooting) section
- Check Docker logs: `docker-compose logs`
- Verify `.env` configuration
- Test with demo data first

---

**Made with ❤️ for AI-powered marketing automation**
