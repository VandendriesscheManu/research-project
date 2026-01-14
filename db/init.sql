CREATE TABLE IF NOT EXISTS chat_messages (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('user','assistant','system')),
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_session_id ON chat_messages(session_id);

-- Marketing Plans table for comprehensive form submissions
CREATE TABLE IF NOT EXISTS marketing_plans (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT NOT NULL,
  
  -- Product Information
  product_name TEXT NOT NULL,
  product_category TEXT NOT NULL,
  product_features TEXT NOT NULL,
  product_usp TEXT NOT NULL,
  product_branding TEXT,
  product_variants TEXT,
  
  -- Target Audience
  target_primary TEXT NOT NULL,
  target_secondary TEXT,
  target_demographics TEXT NOT NULL,
  target_psychographics TEXT NOT NULL,
  target_personas TEXT,
  target_problems TEXT NOT NULL,
  
  -- Market & Competition
  market_size TEXT,
  competitors TEXT NOT NULL,
  competitor_pricing TEXT,
  competitor_distribution TEXT,
  market_benchmarks TEXT,
  
  -- Pricing
  production_cost TEXT,
  desired_margin TEXT,
  suggested_price TEXT NOT NULL,
  price_elasticity TEXT,
  
  -- Promotion
  marketing_channels TEXT[] NOT NULL,
  historical_campaigns TEXT,
  marketing_budget TEXT,
  tone_of_voice TEXT NOT NULL,
  
  -- Distribution
  distribution_channels TEXT[] NOT NULL,
  logistics TEXT,
  seasonality TEXT,
  
  -- Timing
  launch_date DATE,
  seasonal_factors TEXT,
  campaign_timeline TEXT,
  
  -- Goals
  sales_goals TEXT NOT NULL,
  market_share_goals TEXT,
  brand_awareness_goals TEXT,
  success_metrics TEXT NOT NULL,
  
  -- Generated plan (will be filled after AI generates the plan)
  generated_plan TEXT,
  
  -- Metadata
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_marketing_plans_session_id ON marketing_plans(session_id);
CREATE INDEX IF NOT EXISTS idx_marketing_plans_created_at ON marketing_plans(created_at);
