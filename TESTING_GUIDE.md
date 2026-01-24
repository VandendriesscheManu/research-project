# Marketing Plan Agent System - Testing Guide

## Overview

This guide will help you test the complete marketing plan generation system with all 3 agents (Market Research, Creative Strategy, and Evaluator).

---

## 🚀 Quick Start

### 1. **Start the System**

Make sure all services are running:

```bash
# From the project root
docker-compose up --build
```

This starts:

- **PostgreSQL Database** (port 5432)
- **Backend API** (port 8000)
- **Frontend** (port 8501)
- **MCP Server** (stdio communication)

---

## 🧪 Testing Levels

### **Level 1: Test Individual Agents (Python Console)**

Test each agent directly in Python to see their output.

#### A. Test Market Research Agent

```bash
# Enter the MCP server container
docker exec -it mcp-server bash

# Start Python
python

# Test the agent
from agents.marketing import market_research_agent

product_data = {
    "product_name": "EcoBottle",
    "product_category": "Sustainable Water Bottles",
    "product_features": "Made from recycled materials, insulated, leak-proof, BPA-free",
    "product_usp": "100% ocean plastic recycled, keeps drinks cold for 24h",
    "target_primary": "Environmentally conscious millennials and Gen Z",
    "competitors": "Hydro Flask, S'well, Klean Kanteen",
    "suggested_price": "$35-45"
}

# Run research
research = market_research_agent.conduct_full_research(product_data)

# Check results
print("Market Size:", research['market_analysis']['market_size'])
print("Number of Personas:", len(research['personas']))
print("SWOT - Strengths:", research['swot_analysis']['strengths'])
```

#### B. Test Creative Strategy Agent

```python
from agents.marketing import creative_strategy_agent

# Use research from above
strategy = creative_strategy_agent.develop_full_strategy(product_data, research)

# Check results
print("Mission:", strategy['mission_vision_value']['mission'])
print("Positioning:", strategy['positioning']['positioning_statement'])
print("Marketing Goals:", len(strategy['marketing_goals']['primary_goals']))
```

#### C. Test Evaluator Agent

```python
from agents.marketing import evaluator_agent

# Evaluate the plan
evaluation = evaluator_agent.evaluate_full_plan(product_data, research, strategy)

# Check results
print("Overall Score:", evaluation['overall_score'])
print("Strengths:", evaluation['strengths'])
print("Weaknesses:", evaluation['weaknesses'])
print("Recommendations:", evaluation['final_recommendations'])
```

#### D. Test Full Orchestrator

```python
from agents.marketing import marketing_plan_orchestrator

# Generate complete plan
plan = marketing_plan_orchestrator.generate_marketing_plan(product_data, auto_iterate=False)

# Check results
print("Quality Score:", plan['metadata']['quality_score'])
print("Sections Generated:", len(plan['sections']))
print("Section 1:", plan['sections']['1_executive_summary']['content'])

# Save to files
import json
with open('/tmp/marketing_plan.json', 'w') as f:
    json.dump(plan, f, indent=2)

# Export to markdown
marketing_plan_orchestrator.export_plan_to_markdown(plan, '/tmp/marketing_plan.md')
```

---

### **Level 2: Test MCP Server Tools**

Test the MCP server tools directly.

```bash
# In a new terminal, test MCP tools
docker exec -it mcp-server python -c "
import json
from agents.marketing import marketing_plan_orchestrator

product_data = {
    'product_name': 'SmartWatch Pro',
    'product_category': 'Wearable Technology',
    'product_features': 'Heart rate monitoring, GPS, sleep tracking, waterproof',
    'product_usp': '7-day battery life, medical-grade sensors',
    'target_primary': 'Health-conscious professionals aged 25-45'
}

plan = marketing_plan_orchestrator.generate_marketing_plan(product_data)
print('Plan Generated!')
print('Quality Score:', plan['metadata']['quality_score'])
print('Sections:', list(plan['sections'].keys()))
"
```

---

### **Level 3: Test Backend API Endpoints**

Test the REST API endpoints.

#### A. Create Product Brief

```bash
# Test with curl (replace YOUR_API_KEY with your actual key from .env)
curl -X POST http://localhost:8000/product-brief \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "session_id": "test-session-001",
    "product_name": "FitnessPro Tracker",
    "product_category": "Fitness Wearables",
    "product_features": "Heart rate monitor, calorie tracking, sleep analysis",
    "product_usp": "AI-powered workout recommendations",
    "target_primary": "Fitness enthusiasts aged 20-40",
    "competitors": "Fitbit, Garmin, Apple Watch",
    "suggested_price": "$199"
  }'
```

Expected response:

```json
{
  "session_id": "test-session-001",
  "brief_id": 1,
  "message": "Product information saved successfully. Ready to generate marketing plan."
}
```

#### B. Generate Marketing Plan

```bash
# Use the brief_id from the previous response
curl -X POST http://localhost:8000/generate-marketing-plan \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "brief_id": 1,
    "auto_iterate": false
  }'
```

Expected response:

```json
{
  "brief_id": 1,
  "plan_id": 1,
  "status": "completed",
  "quality_score": 8.5,
  "message": "Marketing plan generated successfully"
}
```

#### C. Retrieve Marketing Plan

```bash
curl -X GET http://localhost:8000/marketing-plan/1 \
  -H "X-API-Key: YOUR_API_KEY"
```

This returns the complete marketing plan with all 12 sections.

---

### **Level 4: Test via Frontend (Streamlit)**

#### A. Fill Product Information

1. Open browser: `http://localhost:8501`
2. Fill in product details:
   - Product Name: "EcoBottle"
   - Category: "Sustainable Products"
   - Features: "Recycled materials, insulated"
   - USP: "100% ocean plastic"
   - Target: "Eco-conscious millennials"
   - Price: "$39.99"

#### B. Generate Marketing Plan

3. Click "Generate Marketing Plan" button
4. Wait for processing (may take 2-5 minutes)
5. View the generated plan with all 12 sections

#### C. Review Results

Check that all sections are generated:

- ✅ Executive Summary
- ✅ Mission, Vision, Value
- ✅ Market Analysis
- ✅ SWOT Analysis
- ✅ Target Audience & Positioning
- ✅ Marketing Goals & KPIs
- ✅ Marketing Mix (7Ps)
- ✅ Action Plan
- ✅ Budget
- ✅ Monitoring
- ✅ Risks
- ✅ Launch Strategy

---

## 📊 Validation Checklist

Use this checklist to validate the system:

### ✅ System Health

- [ ] All Docker containers running
- [ ] Database initialized
- [ ] MCP server responding
- [ ] Backend API accessible
- [ ] Frontend loading

### ✅ Agent Functionality

- [ ] Market Research Agent generates SWOT
- [ ] Market Research Agent creates personas
- [ ] Strategy Agent creates positioning
- [ ] Strategy Agent defines marketing mix
- [ ] Evaluator Agent provides scores
- [ ] Evaluator Agent gives recommendations

### ✅ API Endpoints

- [ ] POST /product-brief works
- [ ] GET /product-brief/{session_id} works
- [ ] POST /suggest-field works
- [ ] POST /generate-marketing-plan works
- [ ] GET /marketing-plan/{brief_id} works

### ✅ Data Quality

- [ ] All 12 sections generated
- [ ] No empty sections
- [ ] Quality score > 6.0
- [ ] Evaluation includes strengths/weaknesses
- [ ] JSON structure valid

### ✅ Performance

- [ ] Plan generates in < 10 minutes
- [ ] No timeout errors
- [ ] Database saves correctly
- [ ] Files can be exported

---

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution:**

```bash
# Rebuild MCP server container
docker-compose build mcp-server
docker-compose up -d mcp-server
```

### Issue: LLM not responding

**Check LLM configuration:**

```bash
docker exec -it mcp-server bash
echo $LLM_PROVIDER
echo $LLM_MODEL

# Test Ollama
curl http://host.docker.internal:11434/api/tags
```

### Issue: Database connection error

**Solution:**

```bash
# Restart database
docker-compose restart db

# Check database logs
docker logs db
```

### Issue: Marketing plan generation fails

**Debug:**

```bash
# Check MCP server logs
docker logs mcp-server

# Check backend logs
docker logs backend

# Test agent directly
docker exec -it mcp-server python
>>> from agents.marketing import marketing_plan_orchestrator
>>> # Test with minimal data
```

### Issue: Low quality scores

This is normal! The agents work with the data provided. To improve:

- Provide more detailed product information
- Enable `auto_iterate=True` for automatic improvement
- Manually iterate by regenerating with more context

---

## 📝 Sample Test Cases

### Test Case 1: Minimal Data

```json
{
  "product_name": "Widget",
  "product_category": "General"
}
```

**Expected:** Plan generates with generic content, score ~6-7

### Test Case 2: Complete Data

```json
{
  "product_name": "SmartHome Hub",
  "product_category": "Smart Home Technology",
  "product_features": "Voice control, multi-device compatibility, AI automation",
  "product_usp": "Learns user patterns, 50% more energy efficient",
  "target_primary": "Tech-savvy homeowners aged 30-50",
  "target_demographics": "Middle to high income, urban/suburban",
  "competitors": "Amazon Echo, Google Nest, Apple HomePod",
  "suggested_price": "$299",
  "marketing_channels": ["Social Media", "Tech Blogs", "Amazon"],
  "sales_goals": "10,000 units in first quarter"
}
```

**Expected:** Detailed plan, score ~7.5-9

### Test Case 3: Auto-Iterate

```json
{
  "brief_id": 1,
  "auto_iterate": true
}
```

**Expected:** Higher quality score after iteration

---

## 🎯 Success Criteria

Your system is working correctly if:

1. **All agents execute without errors**
2. **12-section marketing plan is generated**
3. **Quality score is calculated (0-10)**
4. **Evaluation provides feedback**
5. **Plan is saved to database**
6. **Plan can be retrieved via API**
7. **Frontend displays the plan**

---

## 📧 Support

If you encounter issues:

1. Check Docker logs: `docker-compose logs`
2. Verify environment variables in `.env`
3. Ensure Ollama is running (if using local LLM)
4. Check database connectivity
5. Review MCP server logs for agent errors

---

## 🔄 Next Steps

After successful testing:

1. **Optimize prompts** in agent files for better quality
2. **Add more evaluation criteria** in evaluator_agent.py
3. **Implement web search** for real-time market data
4. **Add export formats** (PDF, DOCX)
5. **Create dashboard** for plan comparison
6. **Add user feedback loop** to improve agents

---

**Happy Testing! 🚀**
