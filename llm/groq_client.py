import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def generate_response(user_query, context):
    """
    Generate AI response using retrieved email context.
    """

    prompt = f"""
    You are an intelligent Gmail assistant.

    Context Emails:
    {context}

    User Query:
    {user_query}

    Generate a helpful response.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=300
    )

    return response.choices[0].message.content