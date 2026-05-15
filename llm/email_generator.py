from llm.groq_client import client


def generate_email_reply(context, instruction):

    prompt = f"""
You are an AI email drafting assistant.

The user wants to SEND an email to another person.

Original email/context:
{context}

What the user wants to say:
{instruction}

Your task:
- Write the actual email that should be sent
- Do NOT respond as an assistant
- Do NOT explain anything
- Do NOT give suggestions
- Do NOT analyze
- Do NOT say "I reviewed"
- ONLY generate the outgoing email body

The email should:
- sound human
- be concise
- be professional
- start with a greeting
- end with a sign off
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

    return response.choices[0].message.content.strip()