"""
LLM Client - Handles communication with different LLM providers
Supports: Ollama (local), Groq (API)
"""
import os
import requests
from typing import List, Dict


class LLMClient:
    """Unified client for Ollama and Groq LLM providers"""
    
    def __init__(self):
        # Read configuration from environment
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.model = os.getenv("LLM_MODEL", "llama3.2")
        
        # Provider-specific configuration
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        
        print("=" * 60)
        print(f"🤖 LLM CLIENT INITIALIZED")
        print(f"   Provider: {self.provider.upper()}")
        print(f"   Model: {self.model}")
        if self.provider != "ollama":
            print(f"   Fallback: Ollama ({self.ollama_model})")
        print("=" * 60)
    
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
            else:
                raise ValueError(f"Unknown LLM provider: {self.provider}. Use 'ollama' or 'groq'")
        except Exception as e:
            # If primary provider fails and we're not already using Ollama, fall back
            if self.provider != "ollama":
                print(f"❌ {self.provider.upper()} failed: {str(e)}")
                print(f"🔄 Falling back to local Ollama ({self.ollama_model})...")
                try:
                    return self._call_ollama_fallback(messages, temperature)
                except Exception as fallback_error:
                    print(f"❌ Ollama fallback also failed: {str(fallback_error)}")
                    raise Exception(f"Both {self.provider} and Ollama fallback failed. Primary error: {str(e)}, Ollama error: {str(fallback_error)}")
            else:
                # Already using Ollama, no fallback available
                raise
    
    def _call_ollama(self, messages: List[Dict], temperature: float) -> str:
        """Call local Ollama instance with configured model"""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature}
        }
        print(f"🔧 Ollama request: {self.ollama_base_url}/api/chat with model {self.model}")
        r = requests.post(f"{self.ollama_base_url}/api/chat", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"]
    
    def _call_ollama_fallback(self, messages: List[Dict], temperature: float) -> str:
        """Call local Ollama instance with fallback model"""
        payload = {
            "model": self.ollama_model,  # Use the dedicated fallback model
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature}
        }
        print(f"🔧 Ollama fallback request: {self.ollama_base_url}/api/chat with model {self.ollama_model}")
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
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        print(f"🔧 Groq request with model: {self.model}")
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                             headers=headers, json=payload, timeout=60)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            # Print the actual error response for debugging
            error_detail = "No response"
            if e.response is not None:
                try:
                    error_detail = e.response.json()
                except:
                    error_detail = e.response.text if e.response.text else "No response body"
            
            print(f"❌ Groq API Error Details:")
            print(f"   Status: {e.response.status_code if e.response else 'Unknown'}")
            print(f"   Error: {error_detail}")
            raise Exception(f"Groq API error: {e.response.status_code if e.response else 'Unknown'} - {error_detail}")


# Singleton instance
llm_client = LLMClient()
