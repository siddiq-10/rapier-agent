import os
from datetime import datetime
from duckduckgo_search import DDGS

PRIORITY_COMPANIES = [
    "Cashfree Payments", "PayU India", "Instamojo", "CCAvenue",
    "Stripe", "PayPal", "Adyen", "Razorpay"
]

def fetch_news(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=6))
        
        if not results:
            return f"No recent news found for: {query}"

        news_text = f"Real News Results for: {query}\nDate: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        for i, r in enumerate(results, 1):
            news_text += f"{i}. {r.get('title', 'No title')}\n"
            news_text += f"   Source: {r.get('source', 'Unknown')} | {r.get('date', '')}\n"
            news_text += f"   {r.get('body', '')[:250]}...\n\n"
        return news_text
    except Exception as e:
        return f"Error fetching news: {str(e)}"

def web_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        if not results:
            return f"No search results for: {query}"
        text = f"Web Search: {query}\n\n"
        for i, r in enumerate(results, 1):
            text += f"{i}. {r.get('title')}\n{r.get('body', '')[:200]}...\n\n"
        return text
    except Exception as e:
        return f"Search error: {str(e)}"

def read_memory() -> str:
    try:
        with open("data/memory.json", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "No previous memory found."

def write_memory(content: str) -> str:
    os.makedirs("data", exist_ok=True)
    with open("data/memory.json", "w", encoding="utf-8") as f:
        f.write(content)
    return "Memory updated successfully."