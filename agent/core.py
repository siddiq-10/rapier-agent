import os
from dotenv import load_dotenv
from groq import Groq
from agent.tools import fetch_news, web_search, read_memory, write_memory

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Define tools in OpenAI-compatible format
tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_news",
            "description": "Fetch recent news and market insights about a company or topic",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query (company name or topic)"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for additional information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_memory",
            "description": "Read previously stored insights",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_memory",
            "description": "Save important insights to memory",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content to save"
                    }
                },
                "required": ["content"]
            }
        }
    }
]

TOOL_FUNCTIONS = {
    "fetch_news": fetch_news,
    "web_search": web_search,
    "read_memory": read_memory,
    "write_memory": write_memory,
}


def run_agent(user_query: str, max_steps: int = 10):
    messages = [
    {
        "role": "system",
        "content": """You are Rapier, a Market Intelligence Agent for payments and fintech.

Priority companies: Razorpay, Cashfree Payments, PayU India, Instamojo, CCAvenue, Stripe, PayPal, Adyen.

Rules:
- Use tools only when necessary.
- After collecting enough information (usually 2-4 tool calls), you MUST give the final answer.
- Do not keep calling tools endlessly.
- Your final response must be a clear structured report with:
  1. Key Updates
  2. Competitive Analysis
  3. Impact
  4. Recommended Actions
"""
    },
    {"role": "user", "content": user_query}
]
    for step in range(max_steps):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.3,
            max_tokens=2048
        )

        message = response.choices[0].message
        messages.append(message)

        # If the model wants to call a tool
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = tool_call.function.arguments

                print(f"\n→ Calling tool: {function_name}")
                print(f"→ Arguments: {arguments}")

                # Parse arguments (simple version)
                import json
                try:
                    args = json.loads(arguments)
                except:
                    args = {}

                if function_name in TOOL_FUNCTIONS:
                    if function_name == "read_memory":
                        result = TOOL_FUNCTIONS[function_name]()
                    elif function_name == "write_memory":
                        result = TOOL_FUNCTIONS[function_name](args.get("content", ""))
                    else:
                        result = TOOL_FUNCTIONS[function_name](args.get("query", ""))
                else:
                    result = f"Tool {function_name} not found."

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(result)
                })
        else:
            # No tool call → this is the final answer
            return message.content
        
        # Force a final answer if max steps reached
    messages.append({
        "role": "user",
        "content": "You have enough information. Give the Final Answer now in a structured format."
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.3,
        max_tokens=2048
    )
    return response.choices[0].message.content

    return "Reached maximum steps."