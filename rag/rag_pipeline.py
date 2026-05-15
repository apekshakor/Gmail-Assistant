from llm.groq_client import client


def build_context(
    retrieved_docs
):
    """
    Build context string for LLM.
    """

    context_blocks = []

    for i, doc in enumerate(
        retrieved_docs
    ):

        score = doc.get(
            'rerank_score',
            doc.get('score', 0)
        )

        block = (
            f"[Context {i+1} "
            f"| score: {score:.3f}]\n\n"

            f"Account: {doc['account']}\n"
            f"From: {doc['from']}\n"
            f"Subject: {doc['subject']}\n"
            f"Date: {doc['date']}\n\n"

            f"{doc['text']}"
        )

        context_blocks.append(
            block
        )

    return "\n\n".join(
        context_blocks
    )


def generate_rag_answer(
    query,
    retrieved_docs
):
    """
    Generate final RAG response.
    """

    if not retrieved_docs:

        return (
            "No relevant emails found."
        )

    context_text = build_context(
        retrieved_docs
    )

    prompt = f"""
You are a helpful AI assistant
with access to a user's emails.

Use ONLY the provided email context.

If information is not present,
say so honestly.

Always mention:
- sender
- account
- subject
when relevant.

User Question:
{query}

EMAIL CONTEXT:
{context_text}

ANSWER:
"""

    response = (
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000
        )
    )

    return (
        response
        .choices[0]
        .message
        .content
    )