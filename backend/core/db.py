import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

_conn = None


def init_db():
    global _conn
    _conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )
    _conn.autocommit = True


def save_message(session_id: str, role: str, content: str):
    with _conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO chat_messages (session_id, role, content)
            VALUES (%s, %s, %s)
            """,
            (session_id, role, content),
        )


def get_history(session_id: str) -> list[dict]:
    with _conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT role, content, created_at
            FROM chat_messages
            WHERE session_id = %s
            ORDER BY created_at ASC
            """,
            (session_id,),
        )
        return list(cur.fetchall())


def save_marketing_plan(session_id: str, plan_data: dict) -> int:
    """Save a comprehensive marketing plan form submission"""
    with _conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO marketing_plans (
                session_id,
                product_name, product_category, product_features, product_usp,
                product_branding, product_variants,
                target_primary, target_secondary, target_demographics, 
                target_psychographics, target_personas, target_problems,
                market_size, competitors, competitor_pricing, 
                competitor_distribution, market_benchmarks,
                production_cost, desired_margin, suggested_price, price_elasticity,
                marketing_channels, historical_campaigns, marketing_budget, tone_of_voice,
                distribution_channels, logistics, seasonality,
                launch_date, seasonal_factors, campaign_timeline,
                sales_goals, market_share_goals, brand_awareness_goals, success_metrics
            ) VALUES (
                %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s
            ) RETURNING id
            """,
            (
                session_id,
                plan_data.get('product_name'),
                plan_data.get('product_category'),
                plan_data.get('product_features'),
                plan_data.get('product_usp'),
                plan_data.get('product_branding'),
                plan_data.get('product_variants'),
                plan_data.get('target_primary'),
                plan_data.get('target_secondary'),
                plan_data.get('target_demographics'),
                plan_data.get('target_psychographics'),
                plan_data.get('target_personas'),
                plan_data.get('target_problems'),
                plan_data.get('market_size'),
                plan_data.get('competitors'),
                plan_data.get('competitor_pricing'),
                plan_data.get('competitor_distribution'),
                plan_data.get('market_benchmarks'),
                plan_data.get('production_cost'),
                plan_data.get('desired_margin'),
                plan_data.get('suggested_price'),
                plan_data.get('price_elasticity'),
                plan_data.get('marketing_channels', []),
                plan_data.get('historical_campaigns'),
                plan_data.get('marketing_budget'),
                plan_data.get('tone_of_voice'),
                plan_data.get('distribution_channels', []),
                plan_data.get('logistics'),
                plan_data.get('seasonality'),
                plan_data.get('launch_date'),
                plan_data.get('seasonal_factors'),
                plan_data.get('campaign_timeline'),
                plan_data.get('sales_goals'),
                plan_data.get('market_share_goals'),
                plan_data.get('brand_awareness_goals'),
                plan_data.get('success_metrics')
            )
        )
        plan_id = cur.fetchone()[0]
        return plan_id


def get_marketing_plan(session_id: str) -> dict:
    """Get the latest marketing plan for a session"""
    with _conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT * FROM marketing_plans
            WHERE session_id = %s
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (session_id,),
        )
        result = cur.fetchone()
        return dict(result) if result else None


def update_generated_plan(plan_id: int, generated_plan: str):
    """Update the generated_plan field after AI generates the plan"""
    with _conn.cursor() as cur:
        cur.execute(
            """
            UPDATE marketing_plans
            SET generated_plan = %s, updated_at = NOW()
            WHERE id = %s
            """,
            (generated_plan, plan_id)
        )
