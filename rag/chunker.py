def chunk_emails(
    emails,
    chunk_size=800,
    overlap=150
):
    """
    Convert emails into overlapping chunks.
    """

    all_chunks = []

    for email_index, email in enumerate(emails):

        header = (
            f"Gmail Account: {email['account']}\n"
            f"From: {email['from']}\n"
            f"To: {email['to']}\n"
            f"Date: {email['date']}\n"
            f"Subject: {email['subject']}\n\n"
        )

        body = email.get(
            'body',
            ''
        )

        full_text = header + body

        # Skip tiny emails
        if len(full_text.strip()) < 30:
            continue

        start = 0
        chunk_number = 0

        while start < len(full_text):

            end = start + chunk_size

            chunk_text = (
                full_text[start:end]
                .strip()
            )

            if chunk_text:

                all_chunks.append({
                    'email_index': email_index,
                    'chunk_number': chunk_number,
                    'text': chunk_text,
                    'account': email['account'],
                    'subject': email['subject'],
                    'from': email['from'],
                    'date': email['date']
                })

            if end >= len(full_text):
                break

            start += chunk_size - overlap
            chunk_number += 1

    return all_chunks