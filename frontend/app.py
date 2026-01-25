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

# Helper function to display SWOT as a table
def display_swot_table(swot_data):
    """Display SWOT analysis as a simple 2x2 layout"""
    st.markdown("### 📊 SWOT Analysis Matrix")
    
    # Extract SWOT data
    strengths = swot_data.get('strengths', [])
    weaknesses = swot_data.get('weaknesses', [])
    opportunities = swot_data.get('opportunities', [])
    threats = swot_data.get('threats', [])
    
    # Create 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        # Strengths
        st.markdown("#### 💪 Strengths (Internal)")
        if isinstance(strengths, list):
            for item in strengths:
                if isinstance(item, dict):
                    title = item.get('title', '')
                    desc = item.get('description', '')
                    if title:
                        st.markdown(f"**{title}**")
                    if desc:
                        st.write(desc)
                    st.write("")
                else:
                    st.markdown(f"• {item}")
        else:
            st.write(str(strengths))
        
        st.divider()
        
        # Opportunities
        st.markdown("#### 🌟 Opportunities (External)")
        if isinstance(opportunities, list):
            for item in opportunities:
                if isinstance(item, dict):
                    title = item.get('title', '')
                    desc = item.get('description', '')
                    if title:
                        st.markdown(f"**{title}**")
                    if desc:
                        st.write(desc)
                    st.write("")
                else:
                    st.markdown(f"• {item}")
        else:
            st.write(str(opportunities))
    
    with col2:
        # Weaknesses
        st.markdown("#### ⚠️ Weaknesses (Internal)")
        if isinstance(weaknesses, list):
            for item in weaknesses:
                if isinstance(item, dict):
                    title = item.get('title', '')
                    desc = item.get('description', '')
                    if title:
                        st.markdown(f"**{title}**")
                    if desc:
                        st.write(desc)
                    st.write("")
                else:
                    st.markdown(f"• {item}")
        else:
            st.write(str(weaknesses))
        
        st.divider()
        
        # Threats
        st.markdown("#### 🚨 Threats (External)")
        if isinstance(threats, list):
            for item in threats:
                if isinstance(item, dict):
                    title = item.get('title', '')
                    desc = item.get('description', '')
                    if title:
                        st.markdown(f"**{title}**")
                    if desc:
                        st.write(desc)
                    st.write("")
                else:
                    st.markdown(f"• {item}")
        else:
            st.write(str(threats))

# Helper function to display nested dictionary content
def display_dict_content(data, level=0, section_key=""):
    """Recursively display dictionary content in a simple, readable format"""
    
    # Special handling for SWOT section
    if section_key == "4_swot_analysis" or ('strengths' in data and 'weaknesses' in data and 'opportunities' in data and 'threats' in data):
        display_swot_table(data)
        return
    
    # Special handling for raw/unparsed content
    if 'raw' in data and len(data) == 1:
        raw_text = data.get('raw', '')
        if raw_text:
            st.write(raw_text)
        return
    
    for key, value in data.items():
        # Skip 'raw' key when displaying
        if key == 'raw':
            continue
            
        header = key.replace('_', ' ').title()
        
        if isinstance(value, dict):
            # Styled subheadings with icons
            icon = "📌"
            if "budget" in key.lower(): icon = "💰"
            elif "goal" in key.lower() or "kpi" in key.lower(): icon = "🎯"
            elif "competitor" in key.lower(): icon = "🏢"
            elif "target" in key.lower() or "audience" in key.lower(): icon = "👥"
            elif "channel" in key.lower(): icon = "📢"
            elif "risk" in key.lower(): icon = "⚠️"
            elif "timeline" in key.lower() or "launch" in key.lower(): icon = "📅"
            
            st.markdown(f"{'#' * (4 + level)} {icon} {header}")
            display_dict_content(value, level + 1, section_key)
            
        elif isinstance(value, list):
            st.markdown(f"**{header}:**")
            
            # Check if list is empty
            if not value:
                st.caption("_No data available_")
                st.write("")
                continue
            
            # Check if list contains dicts (structured data)
            has_dicts = any(isinstance(item, dict) for item in value)
            
            if has_dicts:
                # Display structured data in expanders
                for idx, item in enumerate(value):
                    if isinstance(item, dict):
                        # Get title from common fields with smart fallbacks
                        item_title = None
                        
                        # Try common title fields
                        if 'title' in item:
                            item_title = item.get('title')
                        elif 'name' in item:
                            item_title = item.get('name')
                        elif 'goal' in item:
                            item_title = item.get('goal')
                        elif 'activity' in item:
                            item_title = item.get('activity')
                        elif 'risk' in item:
                            item_title = item.get('risk')
                        elif 'phase' in item:
                            item_title = item.get('phase')
                        elif 'type' in item:
                            item_title = item.get('type')
                        
                        # Smart fallback based on parent key
                        if not item_title:
                            if 'risk' in key.lower():
                                item_title = f"Risk {idx+1}"
                            elif 'cost' in key.lower() or 'budget' in key.lower():
                                item_title = f"Cost Item {idx+1}"
                            elif 'phase' in key.lower() or 'launch' in key.lower():
                                item_title = f"Phase {idx+1}"
                            elif 'milestone' in key.lower():
                                item_title = f"Milestone {idx+1}"
                            elif 'goal' in key.lower() or 'kpi' in key.lower():
                                item_title = f"Goal {idx+1}"
                            elif 'activity' in key.lower() or 'action' in key.lower():
                                item_title = f"Activity {idx+1}"
                            else:
                                item_title = f"Item {idx+1}"
                        
                        with st.expander(f"📄 {item_title}", expanded=False):
                            # Display dict items as simple key-value pairs
                            for k, v in item.items():
                                if v and str(v).strip() and str(v) != 'None':
                                    k_display = k.replace('_', ' ').title()
                                    st.markdown(f"**{k_display}:** {v}")
                    else:
                        st.markdown(f"• {item}")
            else:
                # Simple bullet list for strings
                for item in value:
                    if item and str(item).strip():
                        st.markdown(f"• {item}")
            st.write("")
            
        else:
            # Simple text display
            if value and str(value).strip() and str(value) != 'None':
                st.markdown(f"**{header}:** {value}")
            st.write("")

st.title("📊 Marketing Plan Generator")
st.caption("AI-powered marketing plan creation: Streamlit → FastAPI → MCP → Groq/Ollama → Postgres")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "brief_id" not in st.session_state:
    st.session_state.brief_id = None

if "brief_saved" not in st.session_state:
    st.session_state.brief_saved = False

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
    st.write("Session ID:", st.session_state.session_id[:8] + "...")
    if st.session_state.brief_id:
        st.write("Brief ID:", st.session_state.brief_id)
        st.success("✅ Brief saved")
    
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

# Demo Mode Toggle
col_demo1, col_demo2 = st.columns([2, 3])
with col_demo1:
    demo_mode = st.toggle("🎬 Fill Demo Data", value=False, help="Auto-fill all fields with demo data for presentation")
    
    if demo_mode and not st.session_state.get("demo_loaded", False):
        st.session_state.form_data = {
            "product_name": "EcoBottle Pro",
            "product_category": "Reusable Smart Water Bottles",
            "product_features": "• Temperature display (hot/cold indicator)\n• Double-wall vacuum insulation (keeps drinks cold 24h, hot 12h)\n• Leak-proof lid with one-hand operation\n• BPA-free stainless steel\n• Built-in UV-C sterilization\n• Wireless charging base\n• Eco-friendly materials (recycled steel)",
            "product_usp": "• Only smart bottle with UV-C self-cleaning\n• 100% sustainable materials\n• Temperature monitoring via app\n• Lifetime warranty\n• Carbon-neutral production",
            "product_branding": "Modern minimalist design with matte finish. Available in 5 nature-inspired colors (Ocean Blue, Forest Green, Stone Gray, Sunset Orange, Arctic White). Premium feel with subtle logo embossing. Recyclable packaging with zero plastic.",
            "product_variants": "• Standard (500ml) - $29.99\n• Large (750ml) - $34.99\n• XL (1L) - $39.99\n• Limited Edition Artist Series - $49.99",
            "target_primary": "Environmentally conscious millennials and Gen Z (25-40 years) who value sustainability, health, and technology",
            "target_secondary": "Fitness enthusiasts, office workers, outdoor adventurers",
            "target_demographics": "Age: 25-40, Income: $40k-$80k, Urban dwellers, College-educated, Tech-savvy, 60% female / 40% male",
            "target_psychographics": "Values: sustainability, health, innovation. Lifestyle: active, eco-conscious, early tech adopters. Interests: fitness, hiking, yoga, zero-waste living. Online shoppers who research before buying.",
            "target_personas": "Sarah (32): Marketing manager, gym-goer, reduces plastic waste\nDavid (28): Software developer, hiker, loves gadgets\nEmily (35): Yoga instructor, sustainability advocate",
            "target_problems": "• Plastic pollution concerns\n• Forgetting to clean water bottles\n• Drinks not staying at desired temperature\n• Low-quality bottles leaking or breaking\n• Lack of temperature awareness",
            "market_size": "$8.4 billion global reusable bottle market, growing 6.2% annually. Sustainability-focused segment growing at 12% CAGR.",
            "competitors": "• Hydro Flask ($30-45) - market leader, no smart features\n• LARQ ($95-150) - UV cleaning, premium pricing\n• S'well ($25-45) - fashion-focused, no tech\n• Yeti ($30-50) - durability-focused\n• CamelBak ($20-35) - sports-focused",
            "competitor_pricing": "Premium segment: $25-$50. Smart bottles: $50-$150. Our positioning: affordable smart bottle at $30-$40.",
            "competitor_distribution": "REI, Amazon, Target, Whole Foods, direct-to-consumer websites, specialty outdoor stores",
            "market_benchmarks": "Average customer acquisition cost: $15-25. Conversion rate: 2-4%. Email open rate: 18-22%. Social media engagement: 3-5%.",
            "production_cost": "$14 per unit (includes manufacturing, materials, packaging)",
            "desired_margin": "50% gross margin",
            "suggested_price": "$29.99 (standard), $34.99 (large), $39.99 (XL)",
            "price_elasticity": "Price-sensitive market. At $25: high volume but low margin. At $35+: lower volume but competing with premium brands. Sweet spot: $28-32.",
            "marketing_channels": ["Social Media", "Influencer Marketing", "Content Marketing", "Email Marketing", "Paid Ads (Google/Meta)", "Partnerships"],
            "historical_campaigns": "Beta launch campaign (Q4 2025): 500 units sold via Instagram ads, 4.2% conversion, $18 CAC. Influencer partnership test: 2 micro-influencers, 12k reach, 250 clicks.",
            "marketing_budget": "$85,000 for 6-month launch period (pre-launch: $25k, launch: $40k, post-launch: $20k)",
            "tone_of_voice": "Friendly, inspiring, eco-conscious. Key messages: 'Hydrate sustainably', 'Smart hydration for a better planet', 'Clean water, clean conscience'",
            "distribution_channels": ["E-commerce (Own Website)", "Amazon/Marketplaces", "Retail Stores"],
            "logistics": "Warehouse in California. 2-3 day US shipping. International via DHL. Initial inventory: 5,000 units. Dropshipping partner for EU market.",
            "seasonality": "Peak: January (New Year resolutions), April-May (spring fitness), September (back-to-school). Launch: March 2026 (capitalize on spring momentum).",
            "launch_date": "2026-03-15",
            "launch_phases": "Phase 1 (Feb 1-28): Pre-launch teaser, early bird sign-ups\nPhase 2 (Mar 1-14): Soft launch to email list\nPhase 3 (Mar 15): Public launch\nPhase 4 (Mar 16-Apr 30): Scaling phase",
            "sales_goals": "• Month 1: 1,000 units ($30k revenue)\n• Month 3: 2,500 units ($75k revenue)\n• Month 6: 5,000 units ($150k revenue)\n• Year 1: 25,000 units ($750k revenue)",
            "kpi_tracking": "Daily: website traffic, conversion rate, ad spend ROI\nWeekly: email list growth, social engagement\nMonthly: revenue, CAC, LTV, inventory levels",
            "internal_resources": "Team: 1 founder, 1 marketing manager, 1 designer (freelance), 2 part-time customer service. Tools: Shopify, Klaviyo, Meta Ads Manager, Google Analytics.",
            "external_resources": "• 3D product rendering agency\n• PR firm for launch\n• 5 micro-influencers (10k-50k followers)\n• Meta Ads consultant",
            "company_context": "Sustainability-first startup founded in 2025. Mission: reduce single-use plastic. Previous crowdfunding success: $120k raised on Kickstarter for prototype.",
            "product_development_stage": "Manufacturing complete. First batch ready Feb 2026. All certifications obtained (FDA, EU compliance).",
            "regulatory_compliance": "FDA food-safe certified, BPA-free, EU REACH compliant, Prop 65 compliant, FCC certified (wireless charging)",
            "sustainability_certificates": "Certified B Corporation (pending), Carbon Neutral certified, 1% for the Planet member, Ocean Cleanup partner"
        }
        st.session_state.demo_loaded = True
        st.success("✅ Demo data loaded! Scroll through all 8 steps to see the filled fields.")
        st.balloons()
        st.rerun()
    elif not demo_mode and st.session_state.get("demo_loaded", False):
        st.session_state.form_data = {}
        st.session_state.demo_loaded = False
        st.info("Demo data cleared!")
        st.rerun()

with col_demo2:
    st.caption("👆 Use demo mode for quick presentations without typing")

# Initialize field values in session state
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# Initialize current step
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

# Progress indicator
total_steps = 8
st.progress((st.session_state.current_step - 1) / total_steps)
st.caption(f"Step {st.session_state.current_step} of {total_steps}")

# AI Assistant info
st.info("✨ Click the ✨ button next to any field to get AI-powered suggestions based on the information you've already provided.")
st.caption("💡 Fill in at least the Product Name first for more accurate AI suggestions!")

# Placeholder for AI loading message
ai_status_placeholder = st.empty()

st.divider()

# Initialize AI suggestion state
if "ai_suggestion" not in st.session_state:
    st.session_state.ai_suggestion = None
if "ai_field" not in st.session_state:
    st.session_state.ai_field = None

# Helper function to get AI suggestion for a field
def get_ai_suggestion(field_name, field_label):
    if not st.session_state.api_key:
        ai_status_placeholder.error("❌ Please configure API key in sidebar")
        return
    
    if not st.session_state.form_data.get("product_name"):
        ai_status_placeholder.warning("💡 Fill in at least the Product Name first for better AI suggestions!")
        return
    
    # Build context from filled fields
    context = {k: v for k, v in st.session_state.form_data.items() if v}
    
    try:
        ai_status_placeholder.info("✨ Generating AI suggestion...")
        response = requests.post(
            f"{API_BASE_URL}/suggest-field",
            json={
                "field_name": field_name,
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
                    ai_status_placeholder.success(f"⚡ {provider_tag}")
                else:
                    ai_status_placeholder.info(f"🔄 {provider_tag}")
            
            # Auto-update form data
            st.session_state.form_data[field_name] = content
            ai_status_placeholder.success(f"✅ AI suggestion applied to {field_label}!")
            st.rerun()
        else:
            ai_status_placeholder.error(f"❌ API error: {response.status_code}")
    except Exception as e:
        ai_status_placeholder.error(f"❌ Error: {str(e)}")

# Helper function to update form data
def update_field(field_name):
    def callback():
        st.session_state.form_data[field_name] = st.session_state[f"input_{field_name}"]
    return callback

# Step content
if st.session_state.current_step == 1:
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
        
        col_cat, col_cat_btn = st.columns([5, 1])
        with col_cat:
            st.text_input("Category/Type", 
                         value=st.session_state.form_data.get("product_category", ""),
                         placeholder="e.g., Reusable Water Bottles",
                         key="input_product_category",
                         on_change=update_field("product_category"),
                         label_visibility="visible",
                         help="Define the product category or market segment (e.g., consumer electronics, sustainable products, home goods)")
        with col_cat_btn:
            st.write("")  # Spacing
            if st.button("✨", key="ai_product_category", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("product_category", "Category/Type")
                
    with col2:
        col_feat, col_feat_btn = st.columns([5, 1])
        with col_feat:
            st.text_area("Key Features & Functionalities", 
                        value=st.session_state.form_data.get("product_features", ""),
                        placeholder="List main features...", height=100,
                        key="input_product_features",
                        on_change=update_field("product_features"),
                        help="List the main features, technical specifications, and functionalities that define your product's capabilities")
        with col_feat_btn:
            st.write("")  # Spacing
            if st.button("✨", key="ai_product_features", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("product_features", "Key Features")
                
        col_usp, col_usp_btn = st.columns([5, 1])
        with col_usp:
            st.text_area("USPs (Unique Selling Points)", 
                        value=st.session_state.form_data.get("product_usp", ""),
                        placeholder="What makes it unique?", height=100,
                        key="input_product_usp",
                        on_change=update_field("product_usp"),
                        help="Describe what makes your product unique and different from competitors. What specific benefits set it apart?")
        with col_usp_btn:
            st.write("")  # Spacing
            if st.button("✨", key="ai_product_usp", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("product_usp", "Unique Selling Points")

    col_brand, col_brand_btn = st.columns([10, 1])
    with col_brand:
        st.text_area("Packaging, Branding & Brand Identity", 
                    value=st.session_state.form_data.get("product_branding", ""),
                    placeholder="Describe visual identity, packaging design...",
                    key="input_product_branding",
                    on_change=update_field("product_branding"),
                    help="Describe the visual identity, packaging design, logo, colors, materials, and overall brand aesthetic that represents your product")
    with col_brand_btn:
        st.write("")  # Spacing
        if st.button("✨", key="ai_product_branding", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
            get_ai_suggestion("product_branding", "Branding & Packaging")
            
    col_var, col_var_btn = st.columns([10, 1])
    with col_var:
        st.text_area("Product Variants or Lines", 
                    value=st.session_state.form_data.get("product_variants", ""),
                    placeholder="Different sizes, colors, editions...",
                    key="input_product_variants",
                    on_change=update_field("product_variants"),
                    help="List different variants of your product (e.g., sizes, colors, special editions, bundle options, limited releases)")
    with col_var_btn:
        st.write("")  # Spacing
        if st.button("✨", key="ai_product_variants", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
            get_ai_suggestion("product_variants", "Product Variants")

elif st.session_state.current_step == 2:
    # 2. Target Audience Information
    st.markdown("### 2️⃣ Target Audience Information")
    col1, col2 = st.columns(2)
    with col1:
        col_prim, col_prim_btn = st.columns([5, 1])
        with col_prim:
            st.text_area("Primary Target Audience", 
                        value=st.session_state.form_data.get("target_primary", ""),
                        placeholder="Main customer segment...", height=80,
                        key="input_target_primary",
                        on_change=update_field("target_primary"),
                        help="Define your main customer segment - who is most likely to buy and use your product regularly?")
        with col_prim_btn:
            st.write("")
            if st.button("✨", key="ai_target_primary", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("target_primary", "Primary Target Audience")
                
        col_sec, col_sec_btn = st.columns([5, 1])
        with col_sec:
            st.text_area("Secondary Target Audience", 
                        value=st.session_state.form_data.get("target_secondary", ""),
                        placeholder="Additional segments...", height=80,
                        key="input_target_secondary",
                        on_change=update_field("target_secondary"),
                        help="Identify additional customer segments that might be interested, such as gift buyers, secondary users, or niche markets")
        with col_sec_btn:
            st.write("")
            if st.button("✨", key="ai_target_secondary", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("target_secondary", "Secondary Target Audience")
        
        col_demo, col_demo_btn = st.columns([5, 1])
        with col_demo:
            st.text_area("Demographics", 
                        value=st.session_state.form_data.get("target_demographics", ""),
                        placeholder="Age, gender, location, income...", height=80,
                        key="input_target_demographics",
                        on_change=update_field("target_demographics"),
                        help="Provide demographic details: age range, gender, geographic location, income level, education, occupation, family status")
        with col_demo_btn:
            st.write("")
            if st.button("✨", key="ai_target_demographics", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("target_demographics", "Demographics")
                
    with col2:
        col_psych, col_psych_btn = st.columns([5, 1])
        with col_psych:
            st.text_area("Psychographics", 
                        value=st.session_state.form_data.get("target_psychographics", ""),
                        placeholder="Interests, lifestyle, buying behavior...", height=80,
                        key="input_target_psychographics",
                        on_change=update_field("target_psychographics"),
                        help="Describe psychological attributes: lifestyle, values, interests, attitudes, buying behavior, brand preferences, social status")
        with col_psych_btn:
            st.write("")
            if st.button("✨", key="ai_target_psychographics", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("target_psychographics", "Psychographics")
                
        col_pers, col_pers_btn = st.columns([5, 1])
        with col_pers:
            st.text_area("Buyer Personas", 
                        value=st.session_state.form_data.get("target_personas", ""),
                        placeholder="Describe typical customers...", height=80,
                        key="input_target_personas",
                        on_change=update_field("target_personas"),
                        help="Create detailed profiles of typical customers with names, backgrounds, motivations, goals, and pain points")
        with col_pers_btn:
            st.write("")
            if st.button("✨", key="ai_target_personas", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("target_personas", "Buyer Personas")
                
        col_prob, col_prob_btn = st.columns([5, 1])
        with col_prob:
            st.text_area("Customer Needs & Problems Solved", 
                        value=st.session_state.form_data.get("target_problems", ""),
                        placeholder="Pain points addressed...", height=80,
                        key="input_target_problems",
                        on_change=update_field("target_problems"),
                        help="Identify the specific customer pain points, needs, and problems that your product solves or addresses")
        with col_prob_btn:
            st.write("")
            if st.button("✨", key="ai_target_problems", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("target_problems", "Customer Needs & Problems")

elif st.session_state.current_step == 3:
    # 3. Market & Competition Data
    st.markdown("### 3️⃣ Market & Competition Data")
    col1, col2 = st.columns(2)
    with col1:
        col_size, col_size_btn = st.columns([5, 1])
        with col_size:
            st.text_input("Market Size & Growth Trends", 
                         value=st.session_state.form_data.get("market_size", ""),
                         placeholder="e.g., $5B market, 8% annual growth",
                         key="input_market_size",
                         on_change=update_field("market_size"),
                         help="Provide the total addressable market (TAM), market value, and expected growth rate or trends in your industry")
        with col_size_btn:
            st.write("")
            if st.button("✨", key="ai_market_size", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("market_size", "Market Size")
                
        col_comp, col_comp_btn = st.columns([5, 1])
        with col_comp:
            st.text_area("Key Competitors & Products", 
                        value=st.session_state.form_data.get("competitors", ""),
                        placeholder="List main competitors...", height=100,
                        key="input_competitors",
                        on_change=update_field("competitors"),
                        help="List your main direct and indirect competitors, their product names, and their market position or strengths")
        with col_comp_btn:
            st.write("")
            if st.button("✨", key="ai_competitors", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("competitors", "Competitors")
                
        col_price, col_price_btn = st.columns([5, 1])
        with col_price:
            st.text_area("Competitor Pricing & Positioning", 
                        value=st.session_state.form_data.get("competitor_pricing", ""),
                        placeholder="How are competitors priced?", height=100,
                        key="input_competitor_pricing",
                        on_change=update_field("competitor_pricing"),
                        help="Describe how competitors price their products, their positioning strategy (premium, mid-range, budget), and price ranges")
        with col_price_btn:
            st.write("")
            if st.button("✨", key="ai_competitor_pricing", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("competitor_pricing", "Competitor Pricing")
                
    with col2:
        col_dist, col_dist_btn = st.columns([5, 1])
        with col_dist:
            st.text_area("Competitor Distribution Channels", 
                        value=st.session_state.form_data.get("competitor_distribution", ""),
                        placeholder="Where do they sell?", height=100,
                        key="input_competitor_distribution",
                        on_change=update_field("competitor_distribution"),
                        help="Identify where and how competitors sell their products (online, retail stores, distributors, direct sales, marketplaces)")
        with col_dist_btn:
            st.write("")
            if st.button("✨", key="ai_competitor_distribution", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("competitor_distribution", "Competitor Distribution")
                
        col_bench, col_bench_btn = st.columns([5, 1])
        with col_bench:
            st.text_area("Benchmarks & Best Practices", 
                        value=st.session_state.form_data.get("market_benchmarks", ""),
                        placeholder="Industry standards...", height=100,
                        key="input_market_benchmarks",
                        on_change=update_field("market_benchmarks"),
                        help="Describe industry standards, best practices, success metrics, typical conversion rates, or performance benchmarks in your market")
        with col_bench_btn:
            st.write("")
            if st.button("✨", key="ai_market_benchmarks", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("market_benchmarks", "Benchmarks & Best Practices")

elif st.session_state.current_step == 4:
    # 4. Price & Margin Data
    st.markdown("### 4️⃣ Price & Margin Data")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Production Cost/Cost Price", 
                     value=st.session_state.form_data.get("production_cost", ""),
                     placeholder="e.g., $12 per unit",
                     key="input_production_cost",
                     on_change=update_field("production_cost"),
                     help="Enter the total cost to produce or procure one unit, including materials, labor, and manufacturing expenses")
                
        st.text_input("Desired Margin", 
                     value=st.session_state.form_data.get("desired_margin", ""),
                     placeholder="e.g., 40%",
                     key="input_desired_margin",
                     on_change=update_field("desired_margin"),
                     help="Specify your target profit margin as a percentage (e.g., 40% means $10 profit on a $25 retail price with $15 cost)")
                
    with col2:
        col_price, col_price_btn = st.columns([5, 1])
        with col_price:
            st.text_input("Suggested Price or Price Range", 
                         value=st.session_state.form_data.get("suggested_price", ""),
                         placeholder="e.g., $25-$30",
                         key="input_suggested_price",
                         on_change=update_field("suggested_price"),
                         help="Enter your recommended retail price or price range based on costs, margins, and competitive positioning")
        with col_price_btn:
            st.write("")
            if st.button("✨", key="ai_suggested_price", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("suggested_price", "Suggested Price")
                
        col_elas, col_elas_btn = st.columns([5, 1])
        with col_elas:
            st.text_area("Price Elasticity & Demand Expectations", 
                        value=st.session_state.form_data.get("price_elasticity", ""),
                        placeholder="Expected demand at different price points...",
                        key="input_price_elasticity",
                        on_change=update_field("price_elasticity"),
                        help="Describe how demand changes with price variations - will customers buy more at lower prices? Is demand sensitive to price changes?")
        with col_elas_btn:
            st.write("")
            if st.button("✨", key="ai_price_elasticity", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("price_elasticity", "Price Elasticity")

elif st.session_state.current_step == 5:
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
            key="input_marketing_channels",
            help="Select all marketing channels you plan to use to promote your product and reach your target audience"
        )
        st.session_state.form_data["marketing_channels"] = selected_channels
        
        st.text_area("Historical Campaigns & Results", 
                    value=st.session_state.form_data.get("historical_campaigns", ""),
                    placeholder="Previous marketing efforts and their outcomes...",
                    key="input_historical_campaigns",
                    on_change=update_field("historical_campaigns"),
                    help="Describe past marketing campaigns, their performance metrics, ROI, lessons learned, and what worked or didn't work")
    with col2:
        st.text_input("Marketing Budget", 
                     value=st.session_state.form_data.get("marketing_budget", ""),
                     placeholder="e.g., $50,000 for 6 months",
                     key="input_marketing_budget",
                     on_change=update_field("marketing_budget"),
                     help="Specify your total marketing budget and time period - this will be allocated across different channels and activities")
        
        col_tone, col_tone_btn = st.columns([5, 1])
        with col_tone:
            st.text_area("Tone of Voice & Key Message", 
                        value=st.session_state.form_data.get("tone_of_voice", ""),
                        placeholder="Brand voice and core messaging...",
                        key="input_tone_of_voice",
                        on_change=update_field("tone_of_voice"),
                        help="Define your brand's communication style (professional, playful, inspirational) and the core message you want to convey")
        with col_tone_btn:
            st.write("")
            if st.button("✨", key="ai_tone_of_voice", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("tone_of_voice", "Tone of Voice")

elif st.session_state.current_step == 6:
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
            key="input_distribution_channels",
            help="Select all channels through which customers can purchase your product - where will it be available?"
        )
        st.session_state.form_data["distribution_channels"] = selected_dist
        
        col_log, col_log_btn = st.columns([5, 1])
        with col_log:
            st.text_area("Logistical Considerations & Capacity", 
                        value=st.session_state.form_data.get("logistics", ""),
                        placeholder="Shipping, warehousing, fulfillment...",
                        key="input_logistics",
                        on_change=update_field("logistics"),
                        help="Describe shipping methods, warehousing needs, fulfillment capacity, delivery times, and any logistical constraints or partnerships")
        with col_log_btn:
            st.write("")
            if st.button("✨", key="ai_logistics", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("logistics", "Logistical Considerations")
                
    with col2:
        col_seas, col_seas_btn = st.columns([5, 1])
        with col_seas:
            st.text_area("Seasonal Availability or Special Launches", 
                        value=st.session_state.form_data.get("seasonality", ""),
                        placeholder="Seasonal factors, limited editions...",
                        key="input_seasonality",
                        on_change=update_field("seasonality"),
                        help="Describe any seasonal patterns, limited edition releases, special launches, or time-sensitive product availability")
        with col_seas_btn:
            st.write("")
            if st.button("✨", key="ai_seasonality", help="Fill in at least the Product Name first for more accurate AI suggestions!"):
                get_ai_suggestion("seasonality", "Seasonal Availability")

elif st.session_state.current_step == 7:
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
                                     key="input_launch_date",
                                     help="Choose your target product launch date - when you plan to make the product available to customers")
        st.session_state.form_data["launch_date"] = str(selected_date)
        
        col_seas_fac, col_seas_fac_btn = st.columns([5, 1])
        with col_seas_fac:
            st.text_area("Seasonal Factors or Relevant Events", 
                        value=st.session_state.form_data.get("seasonal_factors", ""),
                        placeholder="Holidays, events, trends...",
                        key="input_seasonal_factors",
                        on_change=update_field("seasonal_factors"),
                        help="Identify holidays, events, cultural moments, or seasonal trends that align with your launch date and could boost visibility")
        with col_seas_fac_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("✨", key="btn_seasonal_factors", help="AI suggestion"):
                get_ai_suggestion("seasonal_factors", "Seasonal Factors or Relevant Events")
    with col2:
        col_timeline, col_timeline_btn = st.columns([5, 1])
        with col_timeline:
            st.text_area("Timeline for Promotion Activities", 
                        value=st.session_state.form_data.get("campaign_timeline", ""),
                        placeholder="Pre-launch, launch, post-launch phases...",
                        key="input_campaign_timeline",
                        on_change=update_field("campaign_timeline"),
                        help="Outline the promotional timeline with pre-launch (teasers, PR), launch day activities, and post-launch campaigns")
        with col_timeline_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("✨", key="btn_campaign_timeline", help="AI suggestion"):
                get_ai_suggestion("campaign_timeline", "Timeline for Promotion Activities")

elif st.session_state.current_step == 8:
    # 8. Goals & KPIs
    st.markdown("### 8️⃣ Goals & KPIs")
    col1, col2 = st.columns(2)
    with col1:
        col_sales, col_sales_btn = st.columns([5, 1])
        with col_sales:
            st.text_input("Sales Goals", 
                         value=st.session_state.form_data.get("sales_goals", ""),
                         placeholder="e.g., 10,000 units in first year",
                         key="input_sales_goals",
                         on_change=update_field("sales_goals"),
                         help="Define your target sales volume - how many units do you aim to sell in a specific timeframe (monthly, quarterly, yearly)?")
        with col_sales_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("✨", key="btn_sales_goals", help="AI suggestion"):
                get_ai_suggestion("sales_goals", "Sales Goals")
        
        col_market, col_market_btn = st.columns([5, 1])
        with col_market:
            st.text_input("Market Share Goals", 
                         value=st.session_state.form_data.get("market_share_goals", ""),
                         placeholder="e.g., 5% of market",
                         key="input_market_share_goals",
                         on_change=update_field("market_share_goals"),
                         help="Specify your target market share percentage - what portion of the total market do you aim to capture?")
        with col_market_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("✨", key="btn_market_share_goals", help="AI suggestion"):
                get_ai_suggestion("market_share_goals", "Market Share Goals")
    with col2:
        col_brand, col_brand_btn = st.columns([5, 1])
        with col_brand:
            st.text_area("Brand Awareness & Engagement Goals", 
                        value=st.session_state.form_data.get("brand_awareness_goals", ""),
                        placeholder="Social followers, website traffic...",
                        key="input_brand_awareness_goals",
                        on_change=update_field("brand_awareness_goals"),
                        help="Set targets for brand visibility and engagement - social media followers, website visitors, engagement rates, brand recall")
        with col_brand_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("✨", key="btn_brand_awareness_goals", help="AI suggestion"):
                get_ai_suggestion("brand_awareness_goals", "Brand Awareness & Engagement Goals")
        
        col_kpi, col_kpi_btn = st.columns([5, 1])
        with col_kpi:
            st.text_area("Metrics to Measure Success (KPIs)", 
                        value=st.session_state.form_data.get("success_metrics", ""),
                        placeholder="ROI, conversion rates, CAC, CLV...",
                        key="input_success_metrics",
                        on_change=update_field("success_metrics"),
                        help="List key performance indicators to track - ROI, conversion rates, customer acquisition cost (CAC), customer lifetime value (CLV), etc.")
        with col_kpi_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("✨", key="btn_success_metrics", help="AI suggestion"):
                get_ai_suggestion("success_metrics", "Metrics to Measure Success (KPIs)")

st.divider()

# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.session_state.current_step > 1:
        if st.button("⬅️ Previous", use_container_width=True):
            st.session_state.current_step -= 1
            st.rerun()
with col3:
    if st.session_state.current_step < total_steps:
        if st.button("Next ➡️", use_container_width=True, type="primary"):
            st.session_state.current_step += 1
            st.rerun()
    else:
        # Submit button on final step
        if st.button("💾 Save Product Information", use_container_width=True, type="primary"):
            # Get product_name from session state
            product_name = st.session_state.form_data.get("product_name", "")
            
            # Only check for product name (minimum requirement)
            if not product_name:
                st.error("❌ Please provide at least a Product Name (Step 1)")
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
                            
                            # Save brief_id in session state
                            st.session_state.brief_id = result.get('brief_id')
                            st.session_state.brief_saved = True
                            
                            st.success(f"✅ Product information saved successfully! (Brief ID: {st.session_state.brief_id})")
                            st.info(f"📝 {result.get('message', 'Saved successfully')}")
                            
                            # Show collected data
                            with st.expander("📋 Saved Product Information"):
                                st.json(brief_data)
                
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Failed to save product information: {str(e)}")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

# Marketing Plan Generation Section
if st.session_state.get("brief_saved") and st.session_state.brief_id:
    st.divider()
    st.markdown("---")
    st.header("🚀 Generate Marketing Plan")
    st.write("Your product information is saved. Now generate a complete 12-section marketing plan!")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info(f"📋 **Product Brief ID:** {st.session_state.brief_id} | Session: {st.session_state.session_id[:13]}...")
        st.write("**What will be generated:**")
        st.markdown("""
        - ✅ Executive Summary
        - ✅ Mission, Vision & Value Proposition
        - ✅ Market & Situation Analysis
        - ✅ SWOT Analysis
        - ✅ Target Audience & Positioning
        - ✅ Marketing Goals & KPIs
        - ✅ Marketing Mix (7Ps)
        - ✅ Tactics & Action Plan
        - ✅ Budget & Resources
        - ✅ Monitoring & Evaluation
        - ✅ Risks & Mitigation
        - ✅ Launch Strategy
        """)
    
    with col2:
        st.markdown("**Estimated Time:**")
        st.write("⏱️ 2-5 minutes")
    
    # Generate button
    if st.button("🎯 Generate Complete Marketing Plan", use_container_width=True, type="primary"):
        if not st.session_state.api_key:
            st.error("❌ Please configure API key in sidebar")
        elif not st.session_state.brief_id:
            st.error("❌ No product brief found. Please save your product information first.")
        else:
            try:
                headers = {"X-API-KEY": st.session_state.api_key}
                
                with st.spinner("🤖 AI agents are working on your marketing plan... This may take 2-5 minutes."):
                    # Add status updates
                    status_container = st.empty()
                    
                    status_container.info("📊 Phase 1: Market Research Agent analyzing market, competitors, and trends...")
                    
                    # Ensure brief_id is converted to string (could be int or None)
                    brief_id_str = str(st.session_state.brief_id)
                    
                    # Make the API call
                    response = requests.post(
                        f"{API_BASE_URL}/generate-marketing-plan",
                        json={
                            "brief_id": brief_id_str
                        },
                        headers=headers,
                        timeout=30  # Short timeout since we get immediate response
                    )
                    
                    if response.status_code == 401:
                        st.error("❌ Unauthorized - check your API key")
                    elif response.status_code == 422:
                        st.error(f"❌ Invalid request format. Brief ID: {brief_id_str}, Details: {response.text}")
                    elif response.status_code == 404:
                        st.error("❌ Product brief not found. Please save your product information first.")
                    else:
                        response.raise_for_status()
                        result = response.json()
                        
                        if result.get('status') == 'processing':
                            # Background task started, now poll for completion
                            status_container.info("✅ Generation started! Polling for completion...")
                            
                            import time
                            max_attempts = 60  # 5 minutes (5 second intervals)
                            attempt = 0
                            
                            while attempt < max_attempts:
                                time.sleep(5)
                                attempt += 1
                                
                                # Update status message
                                elapsed = attempt * 5
                                status_container.info(f"⏳ Generating plan... ({elapsed}s elapsed)")
                                
                                # Check if plan is ready
                                try:
                                    plan_response = requests.get(
                                        f"{API_BASE_URL}/marketing-plan/{st.session_state.brief_id}",
                                        headers=headers,
                                        timeout=10
                                    )
                                    
                                    if plan_response.status_code == 200:
                                        # Plan is ready!
                                        plan_data = plan_response.json()
                                        st.session_state.plan_id = plan_data.get('id')
                                        st.session_state.quality_score = plan_data.get('quality_score', 0)
                                        st.session_state.plan_generated = True
                                        
                                        status_container.empty()
                                        
                                        # Success message with score
                                        st.success(f"✅ Marketing Plan Generated Successfully!")
                                        
                                        # Display quality score
                                        score = plan_data.get('quality_score', 0)
                                        if score >= 8.0:
                                            st.success(f"🌟 **Quality Score: {score:.1f}/10** - Excellent!")
                                        elif score >= 7.0:
                                            st.info(f"👍 **Quality Score: {score:.1f}/10** - Good!")
                                        else:
                                            st.info(f"💡 **Quality Score: {score:.1f}/10**")
                                        
                                        st.info(f"📋 Plan ID: {plan_data.get('id')} | Brief ID: {st.session_state.brief_id}")
                                        break
                                    elif plan_response.status_code == 202:
                                        # Still processing, continue polling
                                        continue
                                    elif plan_response.status_code == 404:
                                        st.error("❌ Product brief not found")
                                        break
                                    else:
                                        # Show detailed error
                                        try:
                                            error_detail = plan_response.json().get('detail', plan_response.text)
                                        except:
                                            error_detail = plan_response.text[:200]
                                        st.error(f"❌ Error checking status ({plan_response.status_code}): {error_detail}")
                                        break
                                except requests.exceptions.RequestException as req_err:
                                    # Continue polling on network errors
                                    if attempt >= max_attempts - 1:
                                        st.error(f"❌ Network error: {str(req_err)}")
                                    continue
                            
                            if attempt >= max_attempts:
                                st.warning("⏱️ Plan generation is taking longer than expected. Check back in a few minutes or view backend logs.")
                        else:
                            st.error(f"Unexpected status: {result.get('status')}")
                        
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The plan generation is taking longer than expected. Please check the backend logs.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Failed to generate marketing plan: {str(e)}")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

# Display Marketing Plan Section
if st.session_state.get("plan_generated") and st.session_state.get("plan_id"):
    st.divider()
    st.markdown("---")
    st.header("📄 Your Marketing Plan")
    
    # Fetch and display the marketing plan
    if st.button("🔄 Reload Marketing Plan", use_container_width=True):
        st.rerun()
    
    try:
        headers = {"X-API-KEY": st.session_state.api_key}
        
        with st.spinner("📥 Loading your marketing plan..."):
            response = requests.get(
                f"{API_BASE_URL}/marketing-plan/{st.session_state.brief_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                plan_data = response.json()
                plan_content = plan_data.get('plan_data', {})
                
                # Display metadata
                metadata = plan_content.get('metadata', {})
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Product", metadata.get('product_name', 'N/A'))
                with col2:
                    st.metric("Quality Score", f"{metadata.get('quality_score', 0):.1f}/10")
                with col3:
                    st.metric("Version", metadata.get('version', 'N/A'))
                
                st.caption(f"Generated: {metadata.get('generated_at', 'N/A')}")
                
                # Display evaluation summary
                st.divider()
                evaluation = plan_content.get('evaluation', {})
                
                st.subheader("📊 Evaluation Summary")
                
                # Criterion scores
                criterion_scores = evaluation.get('criterion_scores', {})
                if criterion_scores:
                    cols = st.columns(3)
                    for idx, (criterion, score) in enumerate(criterion_scores.items()):
                        with cols[idx % 3]:
                            st.metric(criterion.replace('_', ' ').title(), f"{score:.1f}/10")
                
                # Strengths and Weaknesses
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**💪 Strengths:**")
                    for strength in evaluation.get('strengths', [])[:5]:
                        st.markdown(f"- {strength}")
                
                with col2:
                    st.markdown("**🔍 Areas for Improvement:**")
                    for weakness in evaluation.get('weaknesses', [])[:5]:
                        st.markdown(f"- {weakness}")
                
                # Recommendations
                if evaluation.get('recommendations'):
                    st.markdown("**💡 Recommendations:**")
                    for rec in evaluation.get('recommendations', []):
                        st.info(rec)
                
                # Display all 12 sections
                st.divider()
                st.subheader("📋 Complete Marketing Plan")
                
                sections = plan_content.get('sections', {})
                
                # Create tabs for each section
                section_names = [
                    "1. Executive Summary",
                    "2. Mission & Vision",
                    "3. Market Analysis",
                    "4. SWOT",
                    "5. Target & Positioning",
                    "6. Goals & KPIs",
                    "7. Marketing Mix (7Ps)",
                    "8. Action Plan",
                    "9. Budget",
                    "10. Monitoring",
                    "11. Risks",
                    "12. Launch Strategy"
                ]
                
                tabs = st.tabs(section_names)
                
                section_keys = [
                    "1_executive_summary",
                    "2_mission_vision_value",
                    "3_situation_market_analysis",
                    "4_swot_analysis",
                    "5_target_audience_positioning",
                    "6_marketing_goals_kpis",
                    "7_strategy_marketing_mix",
                    "8_tactics_action_plan",
                    "9_budget_resources",
                    "10_monitoring_evaluation",
                    "11_risks_mitigation",
                    "12_launch_strategy"
                ]
                
                for idx, (tab, section_key) in enumerate(zip(tabs, section_keys)):
                    with tab:
                        section = sections.get(section_key, {})
                        
                        # Display section title with icon and description
                        title = section.get('title', 'Section')
                        description = section.get('description', '')
                        
                        st.markdown(f"## {title}")
                        if description:
                            st.info(f"ℹ️ {description}")
                        
                        st.markdown("---")
                        
                        # Display section content with section_key for special formatting
                        content = section.get('content', {})
                        if isinstance(content, dict):
                            display_dict_content(content, section_key=section_key)
                        else:
                            st.write(content)
                
                # Download options
                st.divider()
                st.subheader("💾 Export Options")
                
                col1, col2 = st.columns(2)
                with col1:
                    # Download as JSON
                    import json
                    json_str = json.dumps(plan_content, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="📥 Download as JSON",
                        data=json_str,
                        file_name=f"marketing_plan_{metadata.get('product_name', 'plan')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col2:
                    # Download full data
                    full_json = json.dumps(plan_data, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="📥 Download Full Data",
                        data=full_json,
                        file_name=f"marketing_plan_full_{metadata.get('product_name', 'plan')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
            elif response.status_code == 404:
                st.warning("📭 No marketing plan found yet. Click 'Generate Complete Marketing Plan' above.")
            else:
                st.error(f"❌ Error loading plan: {response.status_code}")
                
    except Exception as e:
        st.error(f"❌ Error loading marketing plan: {str(e)}")
