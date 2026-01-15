-- Product Briefs table - stores product information for marketing plan generation
CREATE TABLE IF NOT EXISTS product_briefs (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT NOT NULL,
  
  -- Product Information (only product_name is required)
  product_name TEXT NOT NULL,
  product_category TEXT,
  product_features TEXT,
  product_usp TEXT,
  product_branding TEXT,
  product_variants TEXT,
  
  -- Target Audience
  target_primary TEXT,
  target_secondary TEXT,
  target_demographics TEXT,
  target_psychographics TEXT,
  target_personas TEXT,
  target_problems TEXT,
  
  -- Market & Competition
  market_size TEXT,
  competitors TEXT,
  competitor_pricing TEXT,
  competitor_distribution TEXT,
  market_benchmarks TEXT,
  
  -- Pricing
  production_cost TEXT,
  desired_margin TEXT,
  suggested_price TEXT,
  price_elasticity TEXT,
  
  -- Promotion
  marketing_channels TEXT[],
  historical_campaigns TEXT,
  marketing_budget TEXT,
  tone_of_voice TEXT,
  
  -- Distribution
  distribution_channels TEXT[],
  logistics TEXT,
  seasonality TEXT,
  
  -- Timing
  launch_date DATE,
  seasonal_factors TEXT,
  campaign_timeline TEXT,
  
  -- Goals
  sales_goals TEXT,
  market_share_goals TEXT,
  brand_awareness_goals TEXT,
  success_metrics TEXT,
  
  -- Generated marketing plan (will be filled after AI generates the plan)
  generated_marketing_plan TEXT,
  
  -- Metadata
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_product_briefs_session_id ON product_briefs(session_id);
CREATE INDEX IF NOT EXISTS idx_product_briefs_created_at ON product_briefs(created_at);
