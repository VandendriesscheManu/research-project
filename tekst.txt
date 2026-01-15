npx @modelcontextprotocol/inspector docker exec -i mcp-server python server.py


How to Add New Agents

1. Create a new agent file (e.g., agents/seo_agent.py):
class SEOAgent:
    def __init__(self):
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "...")
        
    def optimize_content(self, content: str) -> str:
        # Your SEO logic here
        return self._call_ollama(messages)


2. Register in agents/__init__.py:

from .marketing_agent import MarketingAgent
from .seo_agent import SEOAgent

marketing_agent = MarketingAgent()
seo_agent = SEOAgent()


3. Add tool in server.py:

from agents import marketing_agent, seo_agent

@mcp.tool()
def optimize_seo(content: str) -> str:
    return seo_agent.optimize_content(content)