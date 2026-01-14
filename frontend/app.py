import os
import uuid
import requests
import streamlit as st
from pathlib import Path

# Read the dynamically generated URL from shared/.env.public
def get_api_base_url():
    """Read PUBLIC_API_BASE_URL from shared/.env.public if it exists."""
    shared_env_file = Path(__file__).parent.parent / "shared" / ".env.public"
    
    if shared_env_file.exists():
        try:
            with open(shared_env_file, 'r') as f:
                for line in f:
                    if line.startswith('PUBLIC_API_BASE_URL='):
                        return line.split('=', 1)[1].strip()
        except Exception as e:
            st.sidebar.warning(f"⚠️ Could not read shared env file: {e}")
    
    return os.getenv("PUBLIC_API_BASE_URL", "http://localhost:8001")

API_BASE_URL = get_api_base_url()

st.set_page_config(page_title="Marketing Plan Generator", page_icon="📊")

st.title("📊 Marketing Plan Generator")
st.caption("AI-powered marketing plan creation: Streamlit → FastAPI → MCP → Groq/Ollama → Postgres")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "chat"  # "chat" or "form"

# Initialize API key from secrets (default) or allow override
if "api_key" not in st.session_state:
    st.session_state.api_key = st.secrets.get("API_KEY", os.getenv("API_KEY", ""))

with st.sidebar:
    st.subheader("Settings")
    
    # Display URL with /docs for user reference
    display_url = f"{API_BASE_URL.rstrip('/')}/docs" if API_BASE_URL else "Not configured"
    st.write("API:", display_url)
    st.write("Session:", st.session_state.session_id)
    
    st.divider()
    
    # Mode selection
    st.subheader("📋 Mode")
    mode_option = st.radio(
        "Choose mode:",
        ["💬 Chat Mode (Test)", "📝 Full Marketing Plan"],
        index=0 if st.session_state.mode == "chat" else 1,
        help="Chat mode for quick testing, Full mode for comprehensive marketing plans"
    )
    
    # Update mode based on selection
    new_mode = "chat" if "Chat Mode" in mode_option else "form"
    if new_mode != st.session_state.mode:
        st.session_state.mode = new_mode
        st.rerun()
    
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
    
    if st.button("New Marketing Plan"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("💡 Tips")
    if st.session_state.mode == "chat":
        st.markdown("""
        **Provide details about:**
        - Product name & description
        - Target market & customers
        - Budget range
        - Business goals
        - Timeline for launch
        - Unique features
        """)
    else:
        st.markdown("""
        **Full Marketing Plan:**
        Fill in all sections for a comprehensive AI-generated marketing strategy.
        """)

# MODE: Full Marketing Plan Form
if st.session_state.mode == "form":
    st.subheader("📝 Product Information Form")
    st.write("Fill in product details to generate a comprehensive marketing plan.")
    
    with st.form("marketing_plan_form"):
        # 1. Product Information
        st.markdown("### 1️⃣ Product Information")
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("Product Name *", placeholder="e.g., EcoBottle Pro", help="Required field")
            product_category = st.text_input("Category/Type", placeholder="e.g., Reusable Water Bottles")
        with col2:
            product_features = st.text_area("Key Features & Functionalities", placeholder="List main features...", height=100)
            product_usp = st.text_area("USPs (Unique Selling Points)", placeholder="What makes it unique?", height=100)
        
        product_branding = st.text_area("Packaging, Branding & Brand Identity", placeholder="Describe visual identity, packaging design...")
        product_variants = st.text_area("Product Variants or Lines", placeholder="Different sizes, colors, editions...")
        
        st.divider()
        
        # 2. Target Audience Information
        st.markdown("### 2️⃣ Target Audience Information")
        col1, col2 = st.columns(2)
        with col1:
            target_primary = st.text_area("Primary Target Audience", placeholder="Main customer segment...", height=80)
            target_secondary = st.text_area("Secondary Target Audience", placeholder="Additional segments...", height=80)
            target_demographics = st.text_area("Demographics", placeholder="Age, gender, location, income...", height=80)
        with col2:
            target_psychographics = st.text_area("Psychographics", placeholder="Interests, lifestyle, buying behavior...", height=80)
            target_personas = st.text_area("Buyer Personas", placeholder="Describe typical customers...", height=80)
            target_problems = st.text_area("Customer Needs & Problems Solved", placeholder="Pain points addressed...", height=80)
        
        st.divider()
        
        # 3. Market & Competition Data
        st.markdown("### 3️⃣ Market & Competition Data")
        col1, col2 = st.columns(2)
        with col1:
            market_size = st.text_input("Market Size & Growth Trends", placeholder="e.g., $5B market, 8% annual growth")
            competitors = st.text_area("Key Competitors & Products", placeholder="List main competitors...", height=100)
            competitor_pricing = st.text_area("Competitor Pricing & Positioning", placeholder="How are competitors priced?", height=100)
        with col2:
            competitor_distribution = st.text_area("Competitor Distribution Channels", placeholder="Where do they sell?", height=100)
            market_benchmarks = st.text_area("Benchmarks & Best Practices", placeholder="Industry standards...", height=100)
        
        st.divider()
        
        # 4. Price & Margin Data
        st.markdown("### 4️⃣ Price & Margin Data")
        col1, col2 = st.columns(2)
        with col1:
            production_cost = st.text_input("Production Cost/Cost Price", placeholder="e.g., $12 per unit")
            desired_margin = st.text_input("Desired Margin", placeholder="e.g., 40%")
        with col2:
            suggested_price = st.text_input("Suggested Price or Price Range", placeholder="e.g., $25-$30")
            price_elasticity = st.text_area("Price Elasticity & Demand Expectations", placeholder="Expected demand at different price points...")
        
        st.divider()
        
        # 5. Promotion & Communication Data
        st.markdown("### 5️⃣ Promotion & Communication Data")
        col1, col2 = st.columns(2)
        with col1:
            marketing_channels = st.multiselect(
                "Possible Marketing Channels",
                ["Social Media", "Influencer Marketing", "Paid Ads (Google/Meta)", "Email Marketing", 
                 "Content Marketing", "Events", "PR/Media", "SEO", "Affiliate Marketing", "Partnerships"],
                default=["Social Media", "Content Marketing"]
            )
            historical_campaigns = st.text_area("Historical Campaigns & Results", placeholder="Previous marketing efforts and their outcomes...")
        with col2:
            marketing_budget = st.text_input("Marketing Budget", placeholder="e.g., $50,000 for 6 months")
            tone_of_voice = st.text_area("Tone of Voice & Key Message", placeholder="Brand voice and core messaging...")
        
        st.divider()
        
        # 6. Distribution & Sales
        st.markdown("### 6️⃣ Distribution & Sales")
        col1, col2 = st.columns(2)
        with col1:
            distribution_channels = st.multiselect(
                "Available Distribution Channels",
                ["E-commerce (Own Website)", "Amazon/Marketplaces", "Retail Stores", "Wholesale", 
                 "Direct Sales", "Distributors", "Subscription Model"],
                default=["E-commerce (Own Website)"]
            )
            logistics = st.text_area("Logistical Considerations & Capacity", placeholder="Shipping, warehousing, fulfillment...")
        with col2:
            seasonality = st.text_area("Seasonal Availability or Special Launches", placeholder="Seasonal factors, limited editions...")
        
        st.divider()
        
        # 7. Timing & Launch
        st.markdown("### 7️⃣ Timing & Launch")
        col1, col2 = st.columns(2)
        with col1:
            launch_date = st.date_input("Desired Launch Date")
            seasonal_factors = st.text_area("Seasonal Factors or Relevant Events", placeholder="Holidays, events, trends...")
        with col2:
            campaign_timeline = st.text_area("Timeline for Promotion Activities", placeholder="Pre-launch, launch, post-launch phases...")
        
        st.divider()
        
        # 8. Goals & KPIs
        st.markdown("### 8️⃣ Goals & KPIs")
        col1, col2 = st.columns(2)
        with col1:
            sales_goals = st.text_input("Sales Goals", placeholder="e.g., 10,000 units in first year")
            market_share_goals = st.text_input("Market Share Goals", placeholder="e.g., 5% of market")
        with col2:
            brand_awareness_goals = st.text_area("Brand Awareness & Engagement Goals", placeholder="Social followers, website traffic...")
            success_metrics = st.text_area("Metrics to Measure Success (KPIs)", placeholder="ROI, conversion rates, CAC, CLV...")
        
        st.divider()
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Product Info & Generate Marketing Plan", use_container_width=True)
        
        if submitted:
            # Only check for product name (minimum requirement)
            if not product_name:
                st.error("❌ Please provide at least a Product Name")
            else:
                # Prepare data for API
                brief_data = {
                    "session_id": st.session_state.session_id,
                    "product_name": product_name,
                    "product_category": product_category,
                    "product_features": product_features,
                    "product_usp": product_usp,
                    "product_branding": product_branding,
                    "product_variants": product_variants,
                    "target_primary": target_primary,
                    "target_secondary": target_secondary,
                    "target_demographics": target_demographics,
                    "target_psychographics": target_psychographics,
                    "target_personas": target_personas,
                    "target_problems": target_problems,
                    "market_size": market_size,
                    "competitors": competitors,
                    "competitor_pricing": competitor_pricing,
                    "competitor_distribution": competitor_distribution,
                    "market_benchmarks": market_benchmarks,
                    "production_cost": production_cost,
                    "desired_margin": desired_margin,
                    "suggested_price": suggested_price,
                    "price_elasticity": price_elasticity,
                    "marketing_channels": marketing_channels,
                    "historical_campaigns": historical_campaigns,
                    "marketing_budget": marketing_budget,
                    "tone_of_voice": tone_of_voice,
                    "distribution_channels": distribution_channels,
                    "logistics": logistics,
                    "seasonality": seasonality,
                    "launch_date": str(launch_date),
                    "seasonal_factors": seasonal_factors,
                    "campaign_timeline": campaign_timeline,
                    "sales_goals": sales_goals,
                    "market_share_goals": market_share_goals,
                    "brand_awareness_goals": brand_awareness_goals,
                    "success_metrics": success_metrics
                }
                
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

# MODE: Chat Mode (existing functionality)
elif st.session_state.mode == "chat":
    # Toon berichten
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            content = m["content"]
            
            # Check if message has provider info
            if m["role"] == "assistant" and content.startswith("[Generated by "):
                # Extract provider info
                end_bracket = content.find("]")
                if end_bracket != -1:
                    provider_info = content[1:end_bracket]  # Remove [ and ]
                    actual_content = content[end_bracket+1:].strip()
                    
                    # Show provider badge
                    if "fallback" in provider_info.lower():
                        st.info(f"🔄 {provider_info}")
                    else:
                        st.success(f"✅ {provider_info}")
                    
                    st.markdown(actual_content)
                else:
                    st.markdown(content)
            else:
                st.markdown(content)

    prompt = st.chat_input("Describe your product and marketing needs...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            headers = {}
            if st.session_state.api_key:
                headers["X-API-KEY"] = st.session_state.api_key

            r = requests.post(
                f"{API_BASE_URL}/chat",
                json={"session_id": st.session_state.session_id, "user_message": prompt},
                headers=headers,
                timeout=60,
            )

            # Specifieke error handling voor auth
            if r.status_code == 401:
                raise Exception("Unauthorized (401) — check API_KEY in Streamlit Secrets and in your .env on the server.")

            r.raise_for_status()
            assistant = r.json().get("assistant_message", "")

            if not assistant:
                assistant = "I received an empty response from the API."

        except Exception as e:
            assistant = f"Something went wrong with the API: {e}"

        st.session_state.messages.append({"role": "assistant", "content": assistant})
        with st.chat_message("assistant"):
            # Check if response has provider info
            if assistant.startswith("[Generated by "):
                # Extract provider info
                end_bracket = assistant.find("]")
                if end_bracket != -1:
                    provider_info = assistant[1:end_bracket]  # Remove [ and ]
                    actual_content = assistant[end_bracket+1:].strip()
                    
                    # Show provider badge
                    if "fallback" in provider_info.lower():
                        st.info(f"🔄 {provider_info}")
                    else:
                        st.success(f"✅ {provider_info}")
                    
                    st.markdown(actual_content)
                else:
                    st.markdown(assistant)
            else:
                st.markdown(assistant)
