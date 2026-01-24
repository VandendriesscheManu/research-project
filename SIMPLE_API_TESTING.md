# Simple API Testing Guide - Marketing Plan Generation

## 🎯 What You'll Do

You'll make 3 simple API calls:

1. **Save product information** (like filling a form)
2. **Ask AI to create marketing plan** (the magic happens here)
3. **Get the finished marketing plan** (see the results)

---

## 📋 Prerequisites

Before testing, make sure:

1. **Your system is running:**

   ```bash
   docker-compose up
   ```

   Wait until you see logs saying everything is ready.

2. **Find your API key:**
   - Open the `.env` file in your project
   - Look for `API_KEY=something`
   - Copy that value (you'll need it for every request)

---

## 🧪 The 3 Simple Steps

### **Step 1: Save Your Product Information**

This is like filling out a form about your product.

**Using PowerShell (Windows):**

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = "your_api_key_here"  # Replace with your actual key from .env
}

$body = @{
    session_id = "test-001"
    product_name = "EcoBottle"
    product_category = "Sustainable Products"
    product_features = "Made from recycled ocean plastic, keeps drinks cold for 24 hours, leak-proof"
    product_usp = "100% ocean plastic recycled, eco-friendly"
    target_primary = "Environmentally conscious millennials"
    competitors = "Hydro Flask, S'well"
    suggested_price = "$39.99"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/product-brief" -Method Post -Headers $headers -Body $body
```

**What you'll get back:**

```json
{
  "session_id": "test-001",
  "brief_id": 1,
  "message": "Product information saved successfully. Ready to generate marketing plan."
}
```

**Important:** Write down the `brief_id` number (you'll need it for step 2)

---

### **Step 2: Generate the Marketing Plan**

Now ask the AI to create the marketing plan. **This takes 2-5 minutes!**

**Using PowerShell:**

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = "your_api_key_here"  # Same key as before
}

$body = @{
    brief_id = 1  # Use the number from Step 1
    auto_iterate = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/generate-marketing-plan" -Method Post -Headers $headers -Body $body
```

**What you'll get back:**

```json
{
  "brief_id": 1,
  "plan_id": 1,
  "status": "completed",
  "quality_score": 8.5,
  "message": "Marketing plan generated successfully"
}
```

The `quality_score` tells you how good the plan is (0-10, higher is better).

---

### **Step 3: Get Your Marketing Plan**

Now retrieve the complete marketing plan with all 12 sections.

**Using PowerShell:**

```powershell
$headers = @{
    "X-API-Key" = "your_api_key_here"  # Same key
}

$result = Invoke-RestMethod -Uri "http://localhost:8000/marketing-plan/1" -Method Get -Headers $headers

# Save to a file so you can read it
$result.plan_data | ConvertTo-Json -Depth 10 | Out-File "marketing_plan.json"

Write-Host "Marketing plan saved to marketing_plan.json!"
```

**What you'll get:**
A JSON file with your complete marketing plan containing:

- 12 detailed sections
- Market research
- Strategy recommendations
- Quality evaluation

---

## 🖥️ Even Simpler: Use a Tool

### **Option A: Use Postman (Visual Tool)**

1. **Download Postman:** https://www.postman.com/downloads/
2. **Create a new request**

**Request 1 - Save Product:**

- Method: `POST`
- URL: `http://localhost:8000/product-brief`
- Headers tab:
  - Key: `X-API-Key`, Value: `your_key_from_env_file`
  - Key: `Content-Type`, Value: `application/json`
- Body tab (select "raw" and "JSON"):

```json
{
  "session_id": "test-001",
  "product_name": "EcoBottle",
  "product_category": "Sustainable Products",
  "product_features": "Recycled plastic, insulated",
  "product_usp": "100% ocean plastic",
  "target_primary": "Eco-conscious millennials",
  "suggested_price": "$39.99"
}
```

- Click **Send**
- Note the `brief_id` from the response

**Request 2 - Generate Plan:**

- Method: `POST`
- URL: `http://localhost:8000/generate-marketing-plan`
- Headers: Same as before
- Body:

```json
{
  "brief_id": 1,
  "auto_iterate": false
}
```

- Click **Send**
- Wait 2-5 minutes for completion

**Request 3 - Get Plan:**

- Method: `GET`
- URL: `http://localhost:8000/marketing-plan/1`
- Headers: Just the API key
- Click **Send**
- View the complete plan in the response

---

### **Option B: Use VS Code REST Client Extension**

1. **Install "REST Client" extension** in VS Code
2. **Create a file** called `test.http` in your project
3. **Copy this content:**

```http
### Variables
@api_key = your_api_key_here
@base_url = http://localhost:8000

### Step 1: Save Product Information
POST {{base_url}}/product-brief
Content-Type: application/json
X-API-Key: {{api_key}}

{
  "session_id": "test-001",
  "product_name": "EcoBottle",
  "product_category": "Sustainable Products",
  "product_features": "Recycled plastic, insulated",
  "product_usp": "100% ocean plastic",
  "target_primary": "Eco-conscious millennials",
  "suggested_price": "$39.99"
}

### Step 2: Generate Marketing Plan (wait 2-5 minutes)
POST {{base_url}}/generate-marketing-plan
Content-Type: application/json
X-API-Key: {{api_key}}

{
  "brief_id": 1,
  "auto_iterate": false
}

### Step 3: Get Marketing Plan
GET {{base_url}}/marketing-plan/1
X-API-Key: {{api_key}}
```

4. **Click "Send Request"** above each section

---

## 📊 What's in the Marketing Plan?

After Step 3, you'll get a plan with these 12 sections:

1. **Executive Summary** - Overview of everything
2. **Mission, Vision, Value** - What the product stands for
3. **Market Analysis** - Market size, trends, opportunities
4. **SWOT Analysis** - Strengths, Weaknesses, Opportunities, Threats
5. **Target Audience & Positioning** - Who to sell to and how to position
6. **Marketing Goals** - Specific goals and KPIs
7. **Marketing Mix (7Ps)** - Product, Price, Place, Promotion, People, Process, Physical Evidence
8. **Action Plan** - Step-by-step tasks with timeline
9. **Budget** - Cost estimates and ROI
10. **Monitoring** - How to track success
11. **Risks** - Potential problems and solutions
12. **Launch Strategy** - How to launch the product

---

## ⏱️ Timeline

- **Step 1:** Takes 1 second
- **Step 2:** Takes 2-5 minutes (the AI is thinking!)
- **Step 3:** Takes 1 second

**Total: About 5 minutes** from start to finish

---

## 🐛 Common Problems

### "Unauthorized" Error

**Problem:** Wrong API key  
**Solution:** Check your `.env` file and copy the exact API key

### "Connection refused"

**Problem:** Backend not running  
**Solution:** Run `docker-compose up` and wait for it to start

### "404 Not Found"

**Problem:** Wrong URL or brief_id doesn't exist  
**Solution:** Double-check the URL and use the correct brief_id from Step 1

### Step 2 takes too long

**Problem:** AI is processing (normal)  
**Solution:** Wait up to 10 minutes. Check logs: `docker logs mcp-server`

---

## ✅ Success Checklist

After testing, you should have:

- [ ] Created a product brief (Step 1)
- [ ] Generated a marketing plan (Step 2)
- [ ] Retrieved the complete plan (Step 3)
- [ ] A JSON file with 12 sections
- [ ] A quality score between 6-9

---

## 🎯 Quick Test (Copy & Paste)

**PowerShell - All 3 Steps in One Script:**

```powershell
# Configuration
$apiKey = "your_api_key_here"  # CHANGE THIS
$baseUrl = "http://localhost:8000"

# Step 1: Save product
Write-Host "Step 1: Saving product information..."
$brief = Invoke-RestMethod -Uri "$baseUrl/product-brief" -Method Post `
    -Headers @{"Content-Type"="application/json"; "X-API-Key"=$apiKey} `
    -Body (@{
        session_id = "test-001"
        product_name = "EcoBottle"
        product_category = "Sustainable Products"
        product_features = "Recycled plastic, insulated"
        product_usp = "100% ocean plastic"
        target_primary = "Eco-conscious millennials"
        suggested_price = "$39.99"
    } | ConvertTo-Json)

$briefId = $brief.brief_id
Write-Host "✓ Product saved! Brief ID: $briefId"

# Step 2: Generate plan
Write-Host "`nStep 2: Generating marketing plan (this takes 2-5 minutes)..."
$plan = Invoke-RestMethod -Uri "$baseUrl/generate-marketing-plan" -Method Post `
    -Headers @{"Content-Type"="application/json"; "X-API-Key"=$apiKey} `
    -Body (@{
        brief_id = $briefId
        auto_iterate = $false
    } | ConvertTo-Json)

Write-Host "✓ Plan generated! Quality Score: $($plan.quality_score)/10"

# Step 3: Get the plan
Write-Host "`nStep 3: Retrieving marketing plan..."
$fullPlan = Invoke-RestMethod -Uri "$baseUrl/marketing-plan/$briefId" -Method Get `
    -Headers @{"X-API-Key"=$apiKey}

# Save to file
$fullPlan.plan_data | ConvertTo-Json -Depth 10 | Out-File "marketing_plan_result.json"

Write-Host "✓ Complete! Marketing plan saved to: marketing_plan_result.json"
Write-Host "`nOpen the file to see your 12-section marketing plan!"
```

Just change the `$apiKey` and run it!

---

**That's it!** You've tested the complete marketing plan generation system via the API. 🎉
