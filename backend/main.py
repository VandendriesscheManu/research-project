import os
import json
from typing import Optional, List
from datetime import date
from fastapi import FastAPI, HTTPException, Header, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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

class ProductBriefGetResponse(BaseModel):
    brief_id: int
    session_id: str
    product_name: str
    # Include other fields as needed


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
        # Always include the brief ID in the response for clarity
        return {
            "brief_id": brief.get('id'),
            "session_id": session_id,
            **brief
        }
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
    brief_id: str  # Changed to str to handle both UUID and int
    auto_iterate: bool = False


class GenerateMarketingPlanResponse(BaseModel):
    brief_id: int  # Always return as int
    plan_id: Optional[int] = None
    status: str  # "processing", "completed", "failed"
    quality_score: Optional[float] = None
    message: str
    error: Optional[str] = None


def _generate_plan_background(brief_id_int: int, product_data: dict, auto_iterate: bool):
    """Background task to generate marketing plan"""
    try:
        from core.mcp_client import mcp_generate_marketing_plan
        
        # Generate marketing plan via MCP
        marketing_plan_json = mcp_generate_marketing_plan(product_data, auto_iterate)
        
        if not marketing_plan_json or marketing_plan_json.strip() == "":
            print(f"ERROR: MCP server returned empty response for brief {brief_id_int}")
            return
        
        try:
            marketing_plan = json.loads(marketing_plan_json)
        except json.JSONDecodeError as json_err:
            print(f"ERROR: Invalid JSON from MCP server for brief {brief_id_int}: {json_err}")
            return
        
        # Save to database
        quality_score = marketing_plan.get('evaluation', {}).get('overall_score', 0)
        plan_id = save_marketing_plan(brief_id_int, marketing_plan_json, quality_score)
        
        print(f"SUCCESS: Marketing plan generated for brief {brief_id_int}, plan_id {plan_id}, score {quality_score}")
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR: Failed to generate plan for brief {brief_id_int}: {str(e)}\n{error_details}")


@app.post("/generate-marketing-plan", response_model=GenerateMarketingPlanResponse)
def generate_marketing_plan(req: GenerateMarketingPlanRequest, background_tasks: BackgroundTasks, _: None = Depends(require_api_key)):
    """Generate a complete marketing plan from product brief (async via background task)"""
    try:
        # Try to convert brief_id to int, if it fails assume it's a session_id (UUID)
        try:
            brief_id_int = int(req.brief_id)
            brief = get_product_brief_by_id(brief_id_int)
        except (ValueError, TypeError):
            # Looks like a UUID/session_id, try to get brief by session_id
            brief = get_product_brief(req.brief_id)
            if brief:
                brief_id_int = brief.get('id')
            else:
                brief_id_int = None
        
        if not brief:
            raise HTTPException(
                status_code=404, 
                detail=f"Product brief not found. Provided value: {req.brief_id}. Expected integer brief_id or valid session_id."
            )
        
        # Clean up the brief data - remove metadata fields and convert to product_data format
        # Only include fields that have actual values (not None, not empty strings)
        product_data = {}
        
        field_mapping = {
            "product_name": "product_name",
            "product_category": "product_category",
            "product_features": "product_features",
            "product_usp": "product_usp",
            "product_branding": "product_branding",
            "product_variants": "product_variants",
            "target_primary": "target_primary",
            "target_secondary": "target_secondary",
            "target_demographics": "target_demographics",
            "target_psychographics": "target_psychographics",
            "target_personas": "target_personas",
            "target_problems": "target_problems",
            "market_size": "market_size",
            "competitors": "competitors",
            "competitor_pricing": "competitor_pricing",
            "competitor_distribution": "competitor_distribution",
            "market_benchmarks": "market_benchmarks",
            "production_cost": "production_cost",
            "desired_margin": "desired_margin",
            "suggested_price": "suggested_price",
            "price_elasticity": "price_elasticity",
            "marketing_channels": "marketing_channels",
            "historical_campaigns": "historical_campaigns",
            "marketing_budget": "marketing_budget",
            "tone_of_voice": "tone_of_voice",
            "distribution_channels": "distribution_channels",
            "logistics": "logistics",
            "seasonality": "seasonality",
            "launch_date": "launch_date",
            "seasonal_factors": "seasonal_factors",
            "campaign_timeline": "campaign_timeline",
            "sales_goals": "sales_goals",
            "market_share_goals": "market_share_goals",
            "brand_awareness_goals": "brand_awareness_goals",
            "success_metrics": "success_metrics"
        }
        
        for brief_key, data_key in field_mapping.items():
            value = brief.get(brief_key)
            # Only include non-None, non-empty values
            if value is not None and value != "" and value != []:
                # Convert date to string if needed
                if brief_key == "launch_date" and value:
                    product_data[data_key] = str(value)
                else:
                    product_data[data_key] = value
        
        # Ensure we at least have product_name
        if not product_data.get("product_name"):
            raise HTTPException(status_code=422, detail="Product name is required to generate marketing plan")
        
        # Start background task
        background_tasks.add_task(_generate_plan_background, brief_id_int, product_data, req.auto_iterate)
        
        # Return immediately
        return GenerateMarketingPlanResponse(
            brief_id=brief_id_int,
            plan_id=None,
            status="processing",
            quality_score=None,
            message="Marketing plan generation started. Use GET /marketing-plan/{brief_id} to check status."
        )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        raise HTTPException(status_code=500, detail=f"Failed to start marketing plan generation: {str(e)}\n\nDetails:\n{error_details}")


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
        resu# Check if brief exists but plan doesn't
            brief = get_product_brief_by_id(brief_id)
            if brief:
                raise HTTPException(
                    status_code=202, 
                    detail="Marketing plan is still being generated. Please try again in a moment."
                )
            else:
                raise HTTPException(status_code=404, detail="Product brief not found
        return dict(result) if result else None

