# 📊 Marketing Plan Generator

AI-powered marketing plan creation using Streamlit, FastAPI, MCP (Model Context Protocol), and LLMs (Groq/Ollama).

## 🏗️ Architecture

```
Streamlit Frontend (Cloud) → Cloudflare Tunnel → FastAPI Backend → MCP Server → LLM (Groq/Ollama) → PostgreSQL
                                    ↓
                             GitHub Gist (URL sync)
```

## ✨ Features

- **Dual Mode Interface**: Chat mode for testing and Full mode for comprehensive marketing plans
- **AI-Powered Agents**: Marketing and Field Assistant agents using LLM
- **Dynamic URL Management**: Automatic Cloudflare tunnel URL updates via GitHub Gist
- **Multiple LLM Support**: Groq (fast, free) and Ollama (local) with automatic fallback
- **Persistent Storage**: PostgreSQL database for conversation history and product briefs
- **Docker Compose**: Complete containerized setup

## 📋 Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- [Git](https://git-scm.com/downloads)
- [GitHub Account](https://github.com) (for Gist URL management)
- [Groq API Key](https://console.groq.com) (free tier available)
- (Optional) [Ollama](https://ollama.ai) installed locally for offline LLM

## 🚀 Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/VandendriesscheManu/research-project.git
cd research-project
```

### 2. Create Environment File

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and set these required values:

```env
# API Configuration
API_KEY=your_secret_api_key_here

# Groq API (Get free key at https://console.groq.com)
GROQ_API_KEY=your_groq_api_key_here

# Postgres
POSTGRES_PASSWORD=your_secure_postgres_password

# GitHub Gist (for Cloudflare URL sync)
GITHUB_TOKEN=your_github_personal_access_token
```

### 3. Create GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `Cloudflare URL Gist`
4. Select scope: **`gist`** (only this one)
5. Click **"Generate token"** and copy it
6. Add it to your `.env` file as `GITHUB_TOKEN`

### 4. Start the Services

```bash
docker-compose up -d
```

This will:

- Start PostgreSQL database
- Start MCP server
- Start FastAPI backend
- Start Cloudflare tunnel
- Create a GitHub Gist with the tunnel URL

### 5. Get Your Cloudflare URL

After starting, check the logs:

```bash
docker logs url-extractor
```

You'll see output like:

```
✅ Created new Gist!
📋 Gist ID: abc123def456
📎 Raw URL: https://gist.githubusercontent.com/.../cloudflare_url.txt

⚠️  IMPORTANT: Add these to your .env file:
   GIST_ID=abc123def456
   GIST_RAW_URL=https://gist.githubusercontent.com/.../cloudflare_url.txt
```

**Important:** Add `GIST_ID` and `GIST_RAW_URL` to your `.env` file:

```env
GIST_ID=abc123def456
GIST_RAW_URL=https://gist.githubusercontent.com/YOUR_USERNAME/YOUR_GIST_ID/raw/cloudflare_url.txt
```

**Note:** Remove the commit hash from the URL (anything after `/raw/`) to always get the latest version.

### 6. Deploy Frontend to Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to https://share.streamlit.io/
3. Click **"New app"**
4. Select your forked repository
5. Set **Main file path**: `frontend/app.py`
6. Click **"Advanced settings"** → **"Secrets"**
7. Add:

```toml
API_KEY = "your_secret_api_key_here"
GIST_RAW_URL = "https://gist.githubusercontent.com/YOUR_USERNAME/YOUR_GIST_ID/raw/cloudflare_url.txt"
```

8. Click **"Deploy"**

## 🔧 Configuration

### LLM Provider Options

#### Groq (Recommended for Production)

- Fast responses (< 2 seconds)
- Free tier: 30 requests/minute
- Models: llama-3.3-70b-versatile, mixtral, etc.

```env
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile
GROQ_API_KEY=your_groq_api_key
```

#### Ollama (Local, Offline)

- Install Ollama: https://ollama.ai
- Pull a model: `ollama pull llama3.2`
- Used as automatic fallback when Groq fails

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

### Environment Variables

| Variable            | Description                                  | Required                              |
| ------------------- | -------------------------------------------- | ------------------------------------- |
| `API_KEY`           | Secret key for API authentication            | ✅ Yes                                |
| `GROQ_API_KEY`      | Groq API key for LLM                         | ✅ Yes                                |
| `GITHUB_TOKEN`      | GitHub PAT with gist scope                   | ✅ Yes                                |
| `GIST_ID`           | GitHub Gist ID (auto-generated on first run) | After first run                       |
| `GIST_RAW_URL`      | Raw URL to Gist (without commit hash)        | After first run                       |
| `POSTGRES_PASSWORD` | PostgreSQL password                          | ✅ Yes                                |
| `LLM_PROVIDER`      | `groq` or `ollama`                           | No (default: groq)                    |
| `LLM_MODEL`         | Model name for selected provider             | No (default: llama-3.3-70b-versatile) |

## 📖 Usage

### Chat Mode (Quick Testing)

1. Open your Streamlit app
2. Select **"💬 Chat Mode (Test)"**
3. Ask questions like:
   - "What are good marketing strategies for a new coffee brand?"
   - "How should I price my SaaS product?"

### Full Marketing Plan Mode

1. Select **"📝 Full Marketing Plan"**
2. Fill in the comprehensive form:
   - Product details
   - Target audience
   - Competition analysis
   - Pricing strategy
   - Distribution channels
   - Goals and metrics
3. Click **"Generate Marketing Plan"**
4. Get a complete marketing strategy

### Updating Cloudflare URL

When you restart your Docker containers, the Cloudflare URL changes automatically:

1. `docker-compose restart` → New tunnel URL created
2. `url-extractor` detects it and updates the Gist
3. Frontend fetches the new URL within 10 seconds
4. **No manual updates needed!** ✅

### Custom Gist URL in Frontend

Users can override the Gist URL in the Streamlit sidebar under **"🌐 Cloudflare URL Source"** without editing secrets.

## 🛠️ Development

### Project Structure

```
research-project/
├── backend/           # FastAPI backend
│   ├── main.py
│   ├── core/
│   │   ├── db.py     # PostgreSQL operations
│   │   └── mcp_client.py  # MCP communication
│   └── Dockerfile
├── frontend/          # Streamlit frontend
│   ├── app.py
│   └── requirements.txt
├── mcp-server/        # MCP server with agents
│   ├── server.py
│   ├── agents/
│   │   ├── marketing_agent.py
│   │   ├── field_assistant_agent.py
│   │   └── llm_client.py
│   └── dockerfile
├── url-extractor/     # Cloudflare URL sync service
│   ├── extract_url.py
│   └── Dockerfile
├── db/
│   └── init.sql      # Database initialization
├── docker-compose.yml
├── .env.example
└── README.md
```

### Local Development

#### Backend API

```bash
# View API documentation
# Access: https://your-cloudflare-url.trycloudflare.com/docs

# Check logs
docker logs api

# Run tests
docker exec api pytest
```

#### Frontend

```bash
# Run locally
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

#### MCP Server

```bash
# Check MCP server logs
docker logs mcp-server

# Access MCP inspector UI (if enabled)
# http://localhost:6274
```

## 🔍 Troubleshooting

### Cloudflare URL Not Updating

Check url-extractor logs:

```bash
docker logs url-extractor
```

Common issues:

- ❌ `GITHUB_TOKEN` not set → Add token to `.env`
- ❌ 404 error → Gist ID is incorrect
- ❌ Old URL showing → Remove commit hash from `GIST_RAW_URL`

### Frontend Shows Wrong URL

1. Make sure `GIST_RAW_URL` in Streamlit secrets has **no commit hash**
2. Correct format: `.../raw/cloudflare_url.txt`
3. Wrong format: `.../raw/abc123.../cloudflare_url.txt`
4. Wait 10 seconds for cache to refresh

### LLM Errors

```bash
# Check MCP server logs
docker logs mcp-server

# Test Groq API
curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models

# Test Ollama (if running locally)
curl http://localhost:11434/api/tags
```

### Database Connection Issues

```bash
# Check database health
docker exec db pg_isready -U chatuser -d chatdb

# View database logs
docker logs db

# Reset database
docker-compose down -v
docker-compose up -d
```

## 🔐 Security Notes

- Never commit `.env` file to Git
- Keep `API_KEY` and `GITHUB_TOKEN` secret
- Gists are private by default (check your Gist settings)
- Rotate tokens regularly
- Use strong passwords for PostgreSQL

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Groq](https://console.groq.com/) - Fast LLM inference
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/) - Secure tunneling

## 📧 Support

For issues and questions:

- Create an issue on GitHub
- Check existing documentation
- Review Docker logs

---

Made with ❤️ for AI-powered marketing automation
