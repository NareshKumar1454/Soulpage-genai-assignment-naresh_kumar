"""
Conversational Knowledge Bot - Core Module
Uses DeepSeek via OpenRouter (100% FREE)
"""
import os
from dotenv import load_dotenv
import requests
from typing import List, Dict

load_dotenv()


class DeepSeekBot:
    """Simple bot using DeepSeek via OpenRouter"""
    
    def __init__(self, model="deepseek/deepseek-chat", temperature=0.7):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set in .env file")
        self.model = model
        self.temperature = temperature
        self.base_url = "https://openrouter.ai/api/v1"
        self.conversation_history: List[Dict] = []
    
    def chat(self, user_message: str) -> str:
        """Send message to DeepSeek and get response"""
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Keep last 6 messages for context (3 exchanges)
        if len(self.conversation_history) > 6:
            self.conversation_history = self.conversation_history[-6:]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Knowledge Bot"
        }
        
        data = {
            "model": self.model,
            "messages": self.conversation_history,
            "temperature": self.temperature,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            bot_reply = result["choices"][0]["message"]["content"]
            
            # Add bot reply to history
            self.conversation_history.append({"role": "assistant", "content": bot_reply})
            
            return bot_reply
            
        except Exception as e:
            error_msg = f"Error: {str(e)[:100]}"
            return f"Sorry, I encountered an issue. {error_msg}"
    
    def clear_memory(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def search_web(self, query: str) -> str:
        """Simple web search using DuckDuckGo"""
        try:
            from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                
            if results:
                summary = "**Search Results:**\n\n"
                for i, r in enumerate(results, 1):
                    summary += f"**{i}. {r['title']}**\n{r['body'][:150]}...\n\n"
                return summary
            else:
                return "No search results found."
                
        except ImportError:
            return "Search module not available."
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def get_wikipedia(self, query: str) -> str:
        """Get information from Wikipedia"""
        try:
            import wikipedia
            wikipedia.set_lang("en")
            
            # Search for page
            search_results = wikipedia.search(query, results=1)
            if search_results:
                page = wikipedia.page(search_results[0])
                return f"**Wikipedia: {page.title}**\n\n{page.summary[:500]}..."
            else:
                return "No Wikipedia article found."
                
        except ImportError:
            return "Wikipedia module not available."
        except Exception as e:
            return f"Wikipedia error: {str(e)}"