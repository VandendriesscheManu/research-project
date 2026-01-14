import os
from typing import Optional, List
from datetime import date
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from core.db import init_db, save_message, get_history, save_marketing_plan, get_marketing_plan
from core.mcp_client import mcp_generate_marketing_plan

app = FastAPI(title="Marketing Plan Generator API", version="0.1.0")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY is not set. Set API_KEY in your .env file.")


def require_api_key(x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


class ChatRequest(BaseModel):
    session_id: str
    user_message: str


class ChatResponse(BaseModel):
    session_id: str
    assistant_message: str


class MarketingPlanRequest(BaseModel):
    session_id: str
    # Product Information
    product_name: str
    product_category: str
    product_features: str
    product_usp: str
    product_branding: Optional[str] = None
    product_variants: Optional[str] = None
    # Target Audience
    target_primary: str
    target_secondary: Optional[str] = None
    target_demographics: str
    target_psychographics: str
    target_personas: Optional[str] = None
    target_problems: str
    # Market & Competition
    market_size: Optional[str] = None
    competitors: str
    competitor_pricing: Optional[str] = None
    competitor_distribution: Optional[str] = None
    market_benchmarks: Optional[str] = None
    # Pricing
    production_cost: Optional[str] = None
    desired_margin: Optional[str] = None
    suggested_price: str
    price_elasticity: Optional[str] = None
    # Promotion
    marketing_channels: List[str]
    historical_campaigns: Optional[str] = None
    marketing_budget: Optional[str] = None
    tone_of_voice: str
    # Distribution
    distribution_channels: List[str]
    logistics: Optional[str] = None
    seasonality: Optional[str] = None
    # Timing
    launch_date: Optional[date] = None
    seasonal_factors: Optional[str] = None
    campaign_timeline: Optional[str] = None
    # Goals
    sales_goals: str
    market_share_goals: Optional[str] = None
    brand_awareness_goals: Optional[str] = None
    success_metrics: str


class MarketingPlanResponse(BaseModel):
    session_id: str
    plan_id: int
    message: str


@app.on_event("startup")
def _startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/history/{session_id}")
def history(session_id: str, _: None = Depends(require_api_key)):
    return {"session_id": session_id, "messages": get_history(session_id)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, _: None = Depends(require_api_key)):
    try:
        history_msgs = get_history(req.session_id)

        save_message(req.session_id, role="user", content=req.user_message)

        # Forward to MCP server for AI processing
        assistant = mcp_generate_marketing_plan(
            user_message=req.user_message,
            history=history_msgs,
        )

        save_message(req.session_id, role="assistant", content=assistant)

        return ChatResponse(session_id=req.session_id, assistant_message=assistant)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/marketing-plan", response_model=MarketingPlanResponse)
def create_marketing_plan(req: MarketingPlanRequest, _: None = Depends(require_api_key)):
    """Store comprehensive marketing plan form data"""
    try:
        # Convert request to dict
        plan_data = req.model_dump()
        
        # Save to database
        plan_id = save_marketing_plan(req.session_id, plan_data)
        
        return MarketingPlanResponse(
            session_id=req.session_id,
            plan_id=plan_id,
            message="Marketing plan data saved successfully. AI generation will be implemented next."
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save marketing plan: {str(e)}")


@app.get("/marketing-plan/{session_id}")
def get_plan(session_id: str, _: None = Depends(require_api_key)):
    """Retrieve the latest marketing plan for a session"""
    try:
        plan = get_marketing_plan(session_id)
        if not plan:
            raise HTTPException(status_code=404, detail="No marketing plan found for this session")
        return plan
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

