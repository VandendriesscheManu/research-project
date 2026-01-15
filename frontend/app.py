import os
import uuid
import requests
import streamlit as st
from pathlib import Path

# MUST be the first Streamlit command
st.set_page_config(page_title="Marketing Plan Generator", page_icon="📊")

# Read the dynamically generated URL from GitHub Gist
@st.cache_data(ttl=10)  # Cache for 10 seconds, then refresh
def get_api_base_url(custom_gist_url=None):
    """Read PUBLIC_API_BASE_URL from GitHub Gist if configured, fallback to env or localhost."""
    gist_raw_url = custom_gist_url or os.getenv("GIST_RAW_URL")
    
    # Try to fetch from Gist first
    if gist_raw_url:
        try:
            response = requests.get(gist_raw_url, timeout=5)
            if response.status_code == 200:
                url = response.text.strip()
                if url:
                    return url
        except Exception as e:
            st.sidebar.warning(f"⚠️ Could not read from Gist: {e}")
    
    # Fallback to shared env file (backward compatibility)
    shared_env_file = Path(__file__).parent.parent / "shared" / ".env.public"
    if shared_env_file.exists():
        try:
            with open(shared_env_file, 'r') as f:
                for line in f:
                    if line.startswith('PUBLIC_API_BASE_URL='):
                        return line.split('=', 1)[1].strip()
        except Exception as e:
            st.sidebar.warning(f"⚠️ Could not read shared env file: {e}")
    
    # Final fallback
    return os.getenv("PUBLIC_API_BASE_URL", "http://localhost:8001")

st.title("📊 Marketing Plan Generator")
st.caption("AI-powered marketing plan creation: Streamlit → FastAPI → MCP → Groq/Ollama → Postgres")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize API key from secrets (default) or allow override
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets.get("API_KEY", os.getenv("API_KEY", ""))

# Initialize Gist URL from secrets (default) or allow override
if "gist_url" not in st.session_state:
    st.session_state.gist_url = st.secrets.get("GIST_RAW_URL", os.getenv("GIST_RAW_URL", ""))

# Get the current API base URL (refreshes every 10 seconds)
API_BASE_URL = get_api_base_url(st.session_state.gist_url)

with st.sidebar:
    st.subheader("Settings")
    
    # Display URL with /docs for user reference
    display_url = f"{API_BASE_URL.rstrip('/')}/docs" if API_BASE_URL else "Not configured"
    st.write("API:", display_url)
    st.write("Session:", st.session_state.session_id)
    
    st.divider()
    
    # API Key configuration (with override option)
    st.subheader("🔑 API Key")
    api_key_input = st.text_input(
        "API Key",
        value=st.session_state.api_key,
        type="password",
        help="Default from Streamlit secrets. Change here to override.",
        placeholder="Enter API key..."
    )
    
    # Update session state if changed
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        st.success("✅ API key updated!")
    
    # Show status
    if st.session_state.api_key:
        st.caption("✅ API key is configured")
    else:
        st.caption("⚠️ No API key configured")

    st.divider()
    
    # Gist URL configuration (with override option)
    st.subheader("🌐 Cloudflare URL Source")
    gist_url_input = st.text_input(
        "GitHub Gist Raw URL",
        value=st.session_state.gist_url,
        help="Default from Streamlit secrets. Change here to use a different Gist.",
        placeholder="https://gist.githubusercontent.com/..."
    )
    
    # Update session state if changed
    if gist_url_input != st.session_state.gist_url:
        st.session_state.gist_url = gist_url_input
        st.success("✅ Gist URL updated!")
        st.rerun()
    
    # Show status
    if st.session_state.gist_url:
        st.caption("✅ Gist URL is configured")
    else:
        st.caption("⚠️ No Gist URL configured")

    st.divider()
    
    if st.button("New Marketing Plan"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("💡 Tips")
    st.markdown("""
    **Fill in all sections for a comprehensive AI-generated marketing strategy.**
    
    Use the AI Field Assistant to get suggestions for any field based on your existing information.
    """)

# Full Marketing Plan Form
st.subheader("📝 Product Information Form")
st.write("Fill in product details to generate a comprehensive marketing plan.")

# Initialize field values in session state
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# AI Assistant Section - Prominent placement
st.markdown("---")
st.subheader("✨ AI Field Assistant")
st.write("Get AI-powered suggestions for any field based on the information you've already provided.")

# Field selection
field_options = {
    "product_category": "Product Category",
    "product_features": "Key Features",
    "product_usp": "Unique Selling Points",
    "product_branding": "Branding & Packaging",
    "target_primary": "Primary Target Audience",
    "target_demographics": "Demographics",
    "target_psychographics": "Psychographics",
    "competitors": "Key Competitors",
    "market_size": "Market Size",
    "marketing_channels": "Marketing Channels",
    "tone_of_voice": "Tone of Voice",
    "sales_goals": "Sales Goals"
}

col1, col2 = st.columns([3, 1])
with col1:
    selected_field = st.selectbox(
        "Select field to get AI suggestion:",
        options=list(field_options.keys()),
        format_func=lambda x: field_options[x]
    )
with col2:
    st.write("")  # Spacing
    st.write("")  # Spacing
    suggest_button = st.button("✨ Get Suggestion", use_container_width=True)

if suggest_button:
    if not st.session_state.api_key:
        st.error("❌ Please configure API key in sidebar")
    elif not st.session_state.form_data.get("product_name"):
        st.warning("💡 Fill in at least the Product Name first for better AI suggestions!")
    else:
        # Build context from filled fields
        context = {k: v for k, v in st.session_state.form_data.items() if v}
        
        try:
            with st.spinner(f"✨ AI is generating suggestion for {field_options[selected_field]}..."):
                response = requests.post(
                    f"{API_BASE_URL}/suggest-field",
                    json={
                        "field_name": selected_field,
                        "context": context
                    },
                    headers={"X-API-Key": st.session_state.api_key},
                    timeout=30
                )
                
                if response.status_code == 200:
                    suggestion = response.json()["suggestion"]
                    
                    # Extract provider tag if present
                    content = suggestion
                    if "[Generated by" in suggestion:
                        parts = suggestion.split("\n\n", 1)
                        provider_tag = parts[0]
                        content = parts[1] if len(parts) > 1 else parts[0]
                        
                        # Show provider badge
                        if "GROQ" in provider_tag:
                            st.success(f"⚡ {provider_tag}")
                        else:
                            st.info(f"🔄 {provider_tag}")
                    
                    # Display suggestion
                    st.markdown("**AI Suggestion:**")
                    st.info(content)
                    st.caption("💡 Copy this suggestion and paste it into the form field below")
                    
                    # Auto-update form data (user can still edit)
                    st.session_state.form_data[selected_field] = content
                    st.success("✅ Suggestion stored! Scroll down to see it in the form.")
                else:
                    st.error(f"❌ API error: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.caption("💡 Tip: Fill in basic fields first (Product Name, Category) for more accurate AI suggestions!")

st.divider()

# Helper function to update form data
def update_field(field_name):
    def callback():
        st.session_state.form_data[field_name] = st.session_state[f"input_{field_name}"]
    return callback
    
    # 1. Product Information
    st.markdown("### 1️⃣ Product Information")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Product Name *", 
                     value=st.session_state.form_data.get("product_name", ""),
                     placeholder="e.g., EcoBottle Pro", 
                     help="Required field",
                     key="input_product_name",
                     on_change=update_field("product_name"))
        st.text_input("Category/Type", 
                     value=st.session_state.form_data.get("product_category", ""),
                     placeholder="e.g., Reusable Water Bottles",
                     key="input_product_category",
                     on_change=update_field("product_category"))
    with col2:
        st.text_area("Key Features & Functionalities", 
                    value=st.session_state.form_data.get("product_features", ""),
                    placeholder="List main features...", height=100,
                    key="input_product_features",
                    on_change=update_field("product_features"))
        st.text_area("USPs (Unique Selling Points)", 
                    value=st.session_state.form_data.get("product_usp", ""),
                    placeholder="What makes it unique?", height=100,
                    key="input_product_usp",
                    on_change=update_field("product_usp"))
    
    st.text_area("Packaging, Branding & Brand Identity", 
                value=st.session_state.form_data.get("product_branding", ""),
                placeholder="Describe visual identity, packaging design...",
                key="input_product_branding",
                on_change=update_field("product_branding"))
    st.text_area("Product Variants or Lines", 
                value=st.session_state.form_data.get("product_variants", ""),
                placeholder="Different sizes, colors, editions...",
                key="input_product_variants",
                on_change=update_field("product_variants"))
        
    st.divider()
    
    # 2. Target Audience Information
    st.markdown("### 2️⃣ Target Audience Information")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Primary Target Audience", 
                    value=st.session_state.form_data.get("target_primary", ""),
                    placeholder="Main customer segment...", height=80,
                    key="input_target_primary",
                    on_change=update_field("target_primary"))
        st.text_area("Secondary Target Audience", 
                    value=st.session_state.form_data.get("target_secondary", ""),
                    placeholder="Additional segments...", height=80,
                    key="input_target_secondary",
                    on_change=update_field("target_secondary"))
        st.text_area("Demographics", 
                    value=st.session_state.form_data.get("target_demographics", ""),
                    placeholder="Age, gender, location, income...", height=80,
                    key="input_target_demographics",
                    on_change=update_field("target_demographics"))
    with col2:
        st.text_area("Psychographics", 
                    value=st.session_state.form_data.get("target_psychographics", ""),
                    placeholder="Interests, lifestyle, buying behavior...", height=80,
                    key="input_target_psychographics",
                    on_change=update_field("target_psychographics"))
        st.text_area("Buyer Personas", 
                    value=st.session_state.form_data.get("target_personas", ""),
                    placeholder="Describe typical customers...", height=80,
                    key="input_target_personas",
                    on_change=update_field("target_personas"))
        st.text_area("Customer Needs & Problems Solved", 
                    value=st.session_state.form_data.get("target_problems", ""),
                    placeholder="Pain points addressed...", height=80,
                    key="input_target_problems",
                    on_change=update_field("target_problems"))
        
    st.divider()
    
    # 3. Market & Competition Data
    st.markdown("### 3️⃣ Market & Competition Data")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Market Size & Growth Trends", 
                     value=st.session_state.form_data.get("market_size", ""),
                     placeholder="e.g., $5B market, 8% annual growth",
                     key="input_market_size",
                     on_change=update_field("market_size"))
        st.text_area("Key Competitors & Products", 
                    value=st.session_state.form_data.get("competitors", ""),
                    placeholder="List main competitors...", height=100,
                    key="input_competitors",
                    on_change=update_field("competitors"))
        st.text_area("Competitor Pricing & Positioning", 
                    value=st.session_state.form_data.get("competitor_pricing", ""),
                    placeholder="How are competitors priced?", height=100,
                    key="input_competitor_pricing",
                    on_change=update_field("competitor_pricing"))
    with col2:
        st.text_area("Competitor Distribution Channels", 
                    value=st.session_state.form_data.get("competitor_distribution", ""),
                    placeholder="Where do they sell?", height=100,
                    key="input_competitor_distribution",
                    on_change=update_field("competitor_distribution"))
        st.text_area("Benchmarks & Best Practices", 
                    value=st.session_state.form_data.get("market_benchmarks", ""),
                    placeholder="Industry standards...", height=100,
                    key="input_market_benchmarks",
                    on_change=update_field("market_benchmarks"))
    
    st.divider()
    
    # 4. Price & Margin Data
    st.markdown("### 4️⃣ Price & Margin Data")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Production Cost/Cost Price", 
                     value=st.session_state.form_data.get("production_cost", ""),
                     placeholder="e.g., $12 per unit",
                     key="input_production_cost",
                     on_change=update_field("production_cost"))
        st.text_input("Desired Margin", 
                     value=st.session_state.form_data.get("desired_margin", ""),
                     placeholder="e.g., 40%",
                     key="input_desired_margin",
                     on_change=update_field("desired_margin"))
    with col2:
        st.text_input("Suggested Price or Price Range", 
                     value=st.session_state.form_data.get("suggested_price", ""),
                     placeholder="e.g., $25-$30",
                     key="input_suggested_price",
                     on_change=update_field("suggested_price"))
        st.text_area("Price Elasticity & Demand Expectations", 
                    value=st.session_state.form_data.get("price_elasticity", ""),
                    placeholder="Expected demand at different price points...",
                    key="input_price_elasticity",
                    on_change=update_field("price_elasticity"))
        
    st.divider()
    
    # 5. Promotion & Communication Data
    st.markdown("### 5️⃣ Promotion & Communication Data")
    col1, col2 = st.columns(2)
    with col1:
        default_channels = st.session_state.form_data.get("marketing_channels", ["Social Media", "Content Marketing"])
        selected_channels = st.multiselect(
            "Possible Marketing Channels",
            ["Social Media", "Influencer Marketing", "Paid Ads (Google/Meta)", "Email Marketing", 
             "Content Marketing", "Events", "PR/Media", "SEO", "Affiliate Marketing", "Partnerships"],
            default=default_channels if isinstance(default_channels, list) else ["Social Media", "Content Marketing"],
            key="input_marketing_channels"
        )
        st.session_state.form_data["marketing_channels"] = selected_channels
        
        st.text_area("Historical Campaigns & Results", 
                    value=st.session_state.form_data.get("historical_campaigns", ""),
                    placeholder="Previous marketing efforts and their outcomes...",
                    key="input_historical_campaigns",
                    on_change=update_field("historical_campaigns"))
    with col2:
        st.text_input("Marketing Budget", 
                     value=st.session_state.form_data.get("marketing_budget", ""),
                     placeholder="e.g., $50,000 for 6 months",
                     key="input_marketing_budget",
                     on_change=update_field("marketing_budget"))
        st.text_area("Tone of Voice & Key Message", 
                    value=st.session_state.form_data.get("tone_of_voice", ""),
                    placeholder="Brand voice and core messaging...",
                    key="input_tone_of_voice",
                    on_change=update_field("tone_of_voice"))
    
    st.divider()
    
    # 6. Distribution & Sales
    st.markdown("### 6️⃣ Distribution & Sales")
    col1, col2 = st.columns(2)
    with col1:
        default_dist = st.session_state.form_data.get("distribution_channels", ["E-commerce (Own Website)"])
        selected_dist = st.multiselect(
            "Available Distribution Channels",
            ["E-commerce (Own Website)", "Amazon/Marketplaces", "Retail Stores", "Wholesale", 
             "Direct Sales", "Distributors", "Subscription Model"],
            default=default_dist if isinstance(default_dist, list) else ["E-commerce (Own Website)"],
            key="input_distribution_channels"
        )
        st.session_state.form_data["distribution_channels"] = selected_dist
        
        st.text_area("Logistical Considerations & Capacity", 
                    value=st.session_state.form_data.get("logistics", ""),
                    placeholder="Shipping, warehousing, fulfillment...",
                    key="input_logistics",
                    on_change=update_field("logistics"))
    with col2:
        st.text_area("Seasonal Availability or Special Launches", 
                    value=st.session_state.form_data.get("seasonality", ""),
                    placeholder="Seasonal factors, limited editions...",
                    key="input_seasonality",
                    on_change=update_field("seasonality"))
    
    st.divider()
    
    # 7. Timing & Launch
    st.markdown("### 7️⃣ Timing & Launch")
    col1, col2 = st.columns(2)
    with col1:
        from datetime import date as date_type
        saved_date = st.session_state.form_data.get("launch_date")
        if saved_date and isinstance(saved_date, str):
            try:
                saved_date = date_type.fromisoformat(saved_date)
            except:
                saved_date = None
        selected_date = st.date_input("Desired Launch Date", 
                                     value=saved_date if saved_date else date_type.today(),
                                     key="input_launch_date")
        st.session_state.form_data["launch_date"] = str(selected_date)
        
        st.text_area("Seasonal Factors or Relevant Events", 
                    value=st.session_state.form_data.get("seasonal_factors", ""),
                    placeholder="Holidays, events, trends...",
                    key="input_seasonal_factors",
                    on_change=update_field("seasonal_factors"))
    with col2:
        st.text_area("Timeline for Promotion Activities", 
                    value=st.session_state.form_data.get("campaign_timeline", ""),
                    placeholder="Pre-launch, launch, post-launch phases...",
                    key="input_campaign_timeline",
                    on_change=update_field("campaign_timeline"))
    
    st.divider()
    
    # 8. Goals & KPIs
    st.markdown("### 8️⃣ Goals & KPIs")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Sales Goals", 
                     value=st.session_state.form_data.get("sales_goals", ""),
                     placeholder="e.g., 10,000 units in first year",
                     key="input_sales_goals",
                     on_change=update_field("sales_goals"))
        st.text_input("Market Share Goals", 
                     value=st.session_state.form_data.get("market_share_goals", ""),
                     placeholder="e.g., 5% of market",
                     key="input_market_share_goals",
                     on_change=update_field("market_share_goals"))
    with col2:
        st.text_area("Brand Awareness & Engagement Goals", 
                    value=st.session_state.form_data.get("brand_awareness_goals", ""),
                    placeholder="Social followers, website traffic...",
                    key="input_brand_awareness_goals",
                    on_change=update_field("brand_awareness_goals"))
        st.text_area("Metrics to Measure Success (KPIs)", 
                    value=st.session_state.form_data.get("success_metrics", ""),
                    placeholder="ROI, conversion rates, CAC, CLV...",
                    key="input_success_metrics",
                    on_change=update_field("success_metrics"))
    
    st.divider()
    
    # Submit button (now outside form)
    if st.button("💾 Save Product Info & Generate Marketing Plan", use_container_width=True, type="primary"):
        # Get product_name from session state
        product_name = st.session_state.form_data.get("product_name", "")
        
        # Only check for product name (minimum requirement)
        if not product_name:
            st.error("❌ Please provide at least a Product Name")
        else:
            # Prepare data for API (now using form_data from session state)
            brief_data = st.session_state.form_data.copy()
            brief_data["session_id"] = st.session_state.session_id
            
            try:
                # Call API to save product brief
                headers = {}
                if st.session_state.api_key:
                    headers["X-API-KEY"] = st.session_state.api_key
                
                with st.spinner("💾 Saving your product information..."):
                    response = requests.post(
                        f"{API_BASE_URL}/product-brief",
                        json=brief_data,
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code == 401:
                        st.error("❌ Unauthorized - check your API key")
                    else:
                        response.raise_for_status()
                        result = response.json()
                        
                        st.success(f"✅ Product information saved successfully! (Brief ID: {result['brief_id']})")
                        st.info(f"📝 {result['message']}")
                        
                        # Show collected data
                        with st.expander("📋 Saved Product Information"):
                            st.json(brief_data)
            
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Failed to save product information: {str(e)}")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
