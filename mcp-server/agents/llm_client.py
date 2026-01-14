"""
LLM Client - Handles communication with different LLM providers
Supports: Ollama (local), Groq (API), Google Gemini (API), OpenRouter (API)
"""
import os
import requests
from typing import List, Dict


class LLMClient:
    """Unified client for multiple LLM providers"""
    
    def __init__(self):
        # Read configuration from environment
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.model = os.getenv("LLM_MODEL", "llama3.2")
        
        # Provider-specific configuration
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        
        # Validate configuration
        self._validate_config()
        
        print("=" * 60)
        print(f"🤖 LLM CLIENT INITIALIZED")
        print(f"   Provider: {self.provider.upper()}")
        print(f"   Model: {self.model}")
        print("=" * 60)
    
    def _validate_config(self):
        """Validate that required API keys are present for the selected provider"""
        if self.provider == "groq" and not self.groq_api_key:
            print("⚠️  WARNING: GROQ_API_KEY not set, will fail on first request")
        elif self.provider in ("google", "gemini") and not self.google_api_key:
            print("⚠️  WARNING: GOOGLE_API_KEY not set, will fail on first request")
        elif self.provider == "openrouter" and not self.openrouter_api_key:
            print("⚠️  WARNING: OPENROUTER_API_KEY not set, will fail on first request")
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        Send chat messages to the configured LLM provider.
        Automatically falls back to Ollama if the primary provider fails.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0)
            
        Returns:
            Response text from the LLM
        """
        print(f"📤 Sending request to {self.provider.upper()} ({self.model})...")
        
        try:
            if self.provider == "ollama":
                return self._call_ollama(messages, temperature)
            elif self.provider == "groq":
                return self._call_groq(messages, temperature)
            elif self.provider == "google" or self.provider == "gemini":
                return self._call_google(messages, temperature)
            elif self.provider == "openrouter":
                return self._call_openrouter(messages, temperature)
            else:
                raise ValueError(f"Unknown LLM provider: {self.provider}")
        except Exception as e:
            # If primary provider fails and we're not already using Ollama, fall back
            if self.provider != "ollama":
                print(f"❌ {self.provider.upper()} failed: {str(e)}")
                print(f"🔄 Falling back to local Ollama...")
                try:
                    return self._call_ollama(messages, temperature)
                except Exception as fallback_error:
                    print(f"❌ Ollama fallback also failed: {str(fallback_error)}")
                    raise Exception(f"Both {self.provider} and Ollama fallback failed. Primary error: {str(e)}")
            else:
                # Already using Ollama, no fallback available
                raise
    
    def _call_ollama(self, messages: List[Dict], temperature: float) -> str:
        """Call local Ollama instance"""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature}
        }
        r = requests.post(f"{self.ollama_base_url}/api/chat", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"]
    
    def _call_groq(self, messages: List[Dict], temperature: float) -> str:
        """
        Call Groq API (very fast inference, free tier available)
        Sign up at: https://console.groq.com
        Free tier: 30 requests/minute, 14,400 requests/day
        """
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not set in environment variables")
        
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,  # e.g., "llama-3.2-90b-text-preview" or "mixtral-8x7b-32768"
            "messages": messages,
            "temperature": temperature
        }
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                         headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    
    def _call_google(self, messages: List[Dict], temperature: float) -> str:
        """
        Call Google Gemini API (generous free tier)
        Get API key at: https://aistudio.google.com/app/apikey
        Free tier: 15 RPM, 1 million tokens/day
        """
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not set in environment variables")
        
        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            role = "user" if msg["role"] in ("user", "system") else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        
        payload = {
            "contents": contents,
            "generationConfig": {"temperature": temperature}
        }
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.google_api_key}"
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    
    def _call_openrouter(self, messages: List[Dict], temperature: float) -> str:
        """
        Call OpenRouter API (aggregates multiple free models)
        Sign up at: https://openrouter.ai
        Has various free models available
        """
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY not set in environment variables")
        
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",  # Optional
        }
        payload = {
            "model": self.model,  # e.g., "meta-llama/llama-3.2-3b-instruct:free"
            "messages": messages,
            "temperature": temperature
        }
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                         headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


# Singleton instance
llm_client = LLMClient()
