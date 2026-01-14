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


def save_product_brief(session_id: str, brief_data: dict) -> int:
    """Save product information for marketing plan generation"""
    with _conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO product_briefs (
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
                brief_data.get('product_name'),
                brief_data.get('product_category'),
                brief_data.get('product_features'),
                brief_data.get('product_usp'),
                brief_data.get('product_branding'),
                brief_data.get('product_variants'),
                brief_data.get('target_primary'),
                brief_data.get('target_secondary'),
                brief_data.get('target_demographics'),
                brief_data.get('target_psychographics'),
                brief_data.get('target_personas'),
                brief_data.get('target_problems'),
                brief_data.get('market_size'),
                brief_data.get('competitors'),
                brief_data.get('competitor_pricing'),
                brief_data.get('competitor_distribution'),
                brief_data.get('market_benchmarks'),
                brief_data.get('production_cost'),
                brief_data.get('desired_margin'),
                brief_data.get('suggested_price'),
                brief_data.get('price_elasticity'),
                brief_data.get('marketing_channels', []),
                brief_data.get('historical_campaigns'),
                brief_data.get('marketing_budget'),
                brief_data.get('tone_of_voice'),
                brief_data.get('distribution_channels', []),
                brief_data.get('logistics'),
                brief_data.get('seasonality'),
                brief_data.get('launch_date'),
                brief_data.get('seasonal_factors'),
                brief_data.get('campaign_timeline'),
                brief_data.get('sales_goals'),
                brief_data.get('market_share_goals'),
                brief_data.get('brand_awareness_goals'),
                brief_data.get('success_metrics')
            )
        )
        plan_id = cur.fetchone()[0]
        return plan_id


def get_product_brief(session_id: str) -> dict:
    """Get the latest product brief for a session"""
    with _conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            SELECT * FROM product_briefs
            WHERE session_id = %s
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (session_id,),
        )
        result = cur.fetchone()
        return dict(result) if result else None


def update_generated_marketing_plan(brief_id: int, marketing_plan: str):
    """Update the generated_marketing_plan field after AI generates the plan"""
    with _conn.cursor() as cur:
        cur.execute(
            """
            UPDATE product_briefs
            SET generated_marketing_plan = %s, updated_at = NOW()
            WHERE id = %s
            """,
            (marketing_plan, brief_id)
        )
