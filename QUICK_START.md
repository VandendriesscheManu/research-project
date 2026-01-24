# 🚀 Quick Start Guide - Testing Your Marketing Plan System

## Step 1: Start Everything

Open PowerShell in your project folder and run:

```powershell
cd "c:\Users\vddma\OneDrive\Bureaublad\Howest\3de jaar\Research Project\research-project"
docker-compose up --build
```

Wait until you see logs saying the services are ready.

---

## Step 2: Open the Frontend

Open your browser and go to:

```
http://localhost:8501
```

You should see: **"📊 Marketing Plan Generator"**

---

## Step 3: Fill in Product Information

### Minimum Required:

Just fill in **Step 1** (Product Information):

- **Product Name:** "EcoBottle" (or any product name)

### For Better Results:

Fill in more fields across all 8 steps:

- Product features
- Target audience
- Competitors
- Price
- Marketing channels
- Goals

**Tip:** Use the ✨ AI Field Assistant to get suggestions!

---

## Step 4: Save Your Product Info

After filling in the form:

1. Navigate through all 8 steps using "Next ➡️"
2. On Step 8, click **"💾 Save Product Information"**
3. You'll see: ✅ "Product information saved successfully!"
4. Note your **Brief ID** (e.g., Brief ID: 1)

---

## Step 5: Generate Marketing Plan

After saving, you'll see a new section: **"🚀 Generate Marketing Plan"**

1. **Optional:** Check "🔄 Auto-Improve" for higher quality (takes longer)
2. Click **"🎯 Generate Complete Marketing Plan"**
3. **Wait 2-5 minutes** (be patient, the AI is working!)
4. You'll see progress: "📊 Phase 1: Market Research Agent..."

---

## Step 6: View Your Marketing Plan

Once complete, you'll see:

- ✅ "Marketing Plan Generated Successfully!"
- 🌟 Quality Score (e.g., 8.5/10)

Scroll down to see:

- **📊 Evaluation Summary** (strengths, weaknesses, recommendations)
- **📋 Complete Marketing Plan** (12 tabs, one for each section)

---

## Step 7: Explore the 12 Sections

Click through the tabs to see:

1. **Executive Summary** - Overview of the plan
2. **Mission & Vision** - Brand purpose and values
3. **Market Analysis** - Market trends and opportunities
4. **SWOT** - Strengths, Weaknesses, Opportunities, Threats
5. **Target & Positioning** - Who to target and how to position
6. **Goals & KPIs** - Measurable objectives
7. **Marketing Mix** - The 7Ps strategy
8. **Action Plan** - Timeline of activities
9. **Budget** - Cost breakdown
10. **Monitoring** - How to track success
11. **Risks** - Potential problems and solutions
12. **Launch Strategy** - How to launch the product

---

## Step 8: Download Your Plan

At the bottom, click:

- **📥 Download as JSON** - Get the structured plan
- **📥 Download Full Data** - Get everything including evaluation

---

## 🎯 Quick Test Example

### Fast Test (Minimum Fields):

1. **Product Name:** "SmartWatch Pro"
2. Save
3. Generate Plan
4. Wait 2-5 minutes
5. View results

### Better Test (More Details):

1. **Product Name:** "EcoBottle"
2. **Category:** "Sustainable Water Bottles"
3. **Features:** "Made from recycled ocean plastic, keeps drinks cold 24h, leak-proof"
4. **USP:** "100% ocean plastic recycled"
5. **Target:** "Eco-conscious millennials aged 25-40"
6. **Competitors:** "Hydro Flask, S'well"
7. **Price:** "$39.99"
8. Save
9. Generate Plan
10. Wait 2-5 minutes
11. View detailed results

---

## 🐛 Troubleshooting

### "Unauthorized" Error

- Check your API key in `.env` file
- It should be: `API_KEY=demo-123`
- Restart: `docker-compose restart`

### "Connection refused"

- Make sure Docker is running
- Run: `docker-compose up`
- Wait for all services to start

### Plan Generation Takes Too Long

- Normal time: 2-5 minutes
- With auto-improve: 5-10 minutes
- Check logs: `docker logs mcp-server`
- Check logs: `docker logs backend`

### Low Quality Score (< 7)

- Add more product details
- Use Auto-Improve option
- Fill in more fields (target audience, competitors, etc.)

### Blank Sections in Plan

- Check MCP server logs: `docker logs mcp-server`
- Check LLM is responding: The system uses Groq (configured in your .env)
- Restart MCP server: `docker-compose restart mcp-server`

---

## ✅ What Should Happen

### After Saving (Step 4):

```
✅ Product information saved successfully! (Brief ID: 1)
📝 Ready to generate marketing plan.
```

### During Generation (Step 5):

```
🤖 AI agents are working on your marketing plan...
📊 Phase 1: Market Research Agent analyzing...
```

### After Generation (Step 6):

```
✅ Marketing Plan Generated Successfully!
🌟 Quality Score: 8.5/10 - Excellent!
📋 Plan ID: 1 | Brief ID: 1
```

---

## 📊 Expected Results

### Quality Scores:

- **8.0-10.0:** 🌟 Excellent
- **7.0-7.9:** 👍 Good
- **6.0-6.9:** 💡 Acceptable (could be better)
- **Below 6.0:** ⚠️ Needs more detail or auto-improve

### Sections Generated:

All 12 sections should have content. Some sections will be more detailed than others depending on your input.

---

## 🎉 Success!

You're done! You now have:

- ✅ A complete 12-section marketing plan
- ✅ Market research and SWOT analysis
- ✅ Target audience personas
- ✅ Marketing strategy and tactics
- ✅ Budget estimates
- ✅ Launch plan
- ✅ Quality evaluation and recommendations

---

## 🔄 Want to Test Again?

1. Click **"New Marketing Plan"** in the sidebar
2. Fill in different product details
3. Generate a new plan
4. Compare results

---

## 📧 Need Help?

### Check Logs:

```powershell
# All services
docker-compose logs

# Specific service
docker logs mcp-server
docker logs backend
docker logs frontend
```

### Restart Everything:

```powershell
docker-compose down
docker-compose up --build
```

### Check API:

Open in browser: http://localhost:8001/docs

---

**Happy Testing! 🚀**

Your system is now fully functional. Fill in product details, generate plans, and see the AI agents work their magic!
