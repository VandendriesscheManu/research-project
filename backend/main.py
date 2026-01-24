import os
import json
from typing import Optional, List
from datetime import date
from fastapi import FastAPI, HTTPException, Header, Depends, BackgroundTasks
from pydantic import BaseModel
from core.db import (
    init_db, 
    save_product_brief, 
    get_product_brief,
    save_marketing_plan,
    get_marketing_plan
)
from core.mcp_client import mcp_suggest_field

app = FastAPI(title="Marketing Plan Generator API", version="0.1.0")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY is not set. Set API_KEY in your .env file.")


def require_api_key(x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


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


# ============================================================================
# Marketing Plan Generation Endpoints
# ============================================================================

class GenerateMarketingPlanRequest(BaseModel):
    brief_id: int
    auto_iterate: bool = False


class GenerateMarketingPlanResponse(BaseModel):
    brief_id: int
    plan_id: int
    status: str
    quality_score: float
    message: str


@app.post("/generate-marketing-plan", response_model=GenerateMarketingPlanResponse)
def generate_marketing_plan(req: GenerateMarketingPlanRequest, _: None = Depends(require_api_key)):
    """Generate a complete marketing plan from product brief"""
    try:
        # Import MCP client function
        from core.mcp_client import mcp_generate_marketing_plan
        
        # Get product brief
        brief = get_product_brief_by_id(req.brief_id)
        if not brief:
            raise HTTPException(status_code=404, detail="Product brief not found")
        
        # Generate marketing plan via MCP
        marketing_plan_json = mcp_generate_marketing_plan(brief, req.auto_iterate)
        marketing_plan = json.loads(marketing_plan_json)
        
        # Save to database
        quality_score = marketing_plan.get('evaluation', {}).get('overall_score', 0)
        plan_id = save_marketing_plan(req.brief_id, marketing_plan_json, quality_score)
        
        return GenerateMarketingPlanResponse(
            brief_id=req.brief_id,
            plan_id=plan_id,
            status="completed",
            quality_score=quality_score,
            message="Marketing plan generated successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate marketing plan: {str(e)}")


@app.get("/marketing-plan/{brief_id}")
def get_plan(brief_id: int, _: None = Depends(require_api_key)):
    """Retrieve the marketing plan for a product brief"""
    try:
        plan = get_marketing_plan(brief_id)
        if not plan:
            raise HTTPException(status_code=404, detail="No marketing plan found for this brief")
        
        # Parse JSON data
        plan['plan_data'] = json.loads(plan['plan_data']) if isinstance(plan['plan_data'], str) else plan['plan_data']
        return plan
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_product_brief_by_id(brief_id: int) -> dict:
    """Helper function to get product brief by ID"""
    from core.db import _conn
    from psycopg2.extras import RealDictCursor
    
    with _conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM product_briefs WHERE id = %s", (brief_id,))
        result = cur.fetchone()
        return dict(result) if result else None

