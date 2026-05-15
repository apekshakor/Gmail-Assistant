from llm.groq_client import client


def generate_email_reply(context, instruction):

    prompt = f"""
You are an AI email assistant.

EMAIL:
{context}

USER INSTRUCTION:
{instruction}

Write a professional email reply.
Only return the email body.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content