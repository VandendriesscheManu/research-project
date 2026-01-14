# Quick Setup Checklist

## To Switch from Ollama to Groq:

### Step 1: Get API Key

1. Go to https://console.groq.com
2. Sign up (free)
3. Copy your API key (starts with `gsk_`)

### Step 2: Update .env File

Open `.env` and paste your key:

```env
LLM_PROVIDER=groq
LLM_MODEL=llama-3.2-90b-text-preview
GROQ_API_KEY=gsk_paste_your_key_here
```

### Step 3: Restart Containers

```bash
docker-compose restart mcp-server api
```

### Step 4: Verify It's Working

**Check the logs to see which provider is active:**

```bash
docker logs mcp-server
```

You should see:

```
============================================================
🤖 LLM CLIENT INITIALIZED
   Provider: GROQ
   Model: llama-3.2-90b-text-preview
============================================================
```

**Test a request:**
When you make a chat request, check API logs:

```bash
docker logs api --tail 20
```

You'll see:

```
📤 Sending request to GROQ (llama-3.2-90b-text-preview)...
```

## That's It!

No code changes needed, just:

1. ✅ Paste API key in `.env`
2. ✅ Make sure `LLM_PROVIDER=groq`
3. ✅ Restart containers

## Troubleshooting

**If you see warnings about missing API key:**

- Check your `.env` file has the correct key
- Make sure there are no extra spaces
- Restart containers again

**If requests fail:**

- Verify your API key is valid at https://console.groq.com
- Check you have credits/requests remaining
- Try a different model (e.g., `llama-3.2-3b-preview` is faster)
