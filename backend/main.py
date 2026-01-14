import os
from typing import Optional, List
from datetime import date
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from core.db import init_db, save_message, get_history, save_product_brief, get_product_brief
from core.mcp_client import mcp_generate_marketing_plan, mcp_suggest_field

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


class ProductBriefRequest(BaseModel):
    session_id: str
    # Product Information
    product_name: str
    product_category: Optional[str] = None
    product_features: Optional[str] = None
    product_usp: Optional[str] = None
    product_branding: Optional[str] = None
    product_variants: Optional[str] = None
    # Target Audience
    target_primary: Optional[str] = None
    target_secondary: Optional[str] = None
    target_demographics: Optional[str] = None
    target_psychographics: Optional[str] = None
    target_personas: Optional[str] = None
    target_problems: Optional[str] = None
    # Market & Competition
    market_size: Optional[str] = None
    competitors: Optional[str] = None
    competitor_pricing: Optional[str] = None
    competitor_distribution: Optional[str] = None
    market_benchmarks: Optional[str] = None
    # Pricing
    production_cost: Optional[str] = None
    desired_margin: Optional[str] = None
    suggested_price: Optional[str] = None
    price_elasticity: Optional[str] = None
    # Promotion
    marketing_channels: Optional[List[str]] = None
    historical_campaigns: Optional[str] = None
    marketing_budget: Optional[str] = None
    tone_of_voice: Optional[str] = None
    # Distribution
    distribution_channels: Optional[List[str]] = None
    logistics: Optional[str] = None
    seasonality: Optional[str] = None
    # Timing
    launch_date: Optional[date] = None
    seasonal_factors: Optional[str] = None
    campaign_timeline: Optional[str] = None
    # Goals
    sales_goals: Optional[str] = None
    market_share_goals: Optional[str] = None
    brand_awareness_goals: Optional[str] = None
    success_metrics: Optional[str] = None


class ProductBriefResponse(BaseModel):
    session_id: str
    brief_id: int
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


@app.post("/product-brief", response_model=ProductBriefResponse)
def create_product_brief(req: ProductBriefRequest, _: None = Depends(require_api_key)):
    """Store product information for marketing plan generation"""
    try:
        # Convert request to dict
        brief_data = req.model_dump()
        
        # Save to database
        brief_id = save_product_brief(req.session_id, brief_data)
        
        return ProductBriefResponse(
            session_id=req.session_id,
            brief_id=brief_id,
            message="Product information saved successfully. Ready to generate marketing plan."
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save product brief: {str(e)}")


@app.get("/product-brief/{session_id}")
def get_brief(session_id: str, _: None = Depends(require_api_key)):
    """Retrieve the latest product brief for a session"""
    try:
        brief = get_product_brief(session_id)
        if not brief:
            raise HTTPException(status_code=404, detail="No product brief found for this session")
        return brief
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class SuggestFieldRequest(BaseModel):
    field_name: str
    context: dict


class SuggestFieldResponse(BaseModel):
    suggestion: str


@app.post("/suggest-field", response_model=SuggestFieldResponse)
def suggest_field(req: SuggestFieldRequest, _: None = Depends(require_api_key)):
    """Generate AI-powered suggestion for a form field based on context"""
    try:
        suggestion = mcp_suggest_field(req.field_name, req.context)
        return {"suggestion": suggestion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
