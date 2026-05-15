import base64
import time


def extract_body(payload, max_chars=2000):
    """
    Recursively extract plain text body
    from Gmail message payload.
    """

    if 'parts' in payload:

        for part in payload['parts']:

            # Plain text part
            if (
                part.get('mimeType') == 'text/plain'
                and 'data' in part.get('body', {})
            ):

                return base64.urlsafe_b64decode(
                    part['body']['data']
                ).decode(
                    'utf-8',
                    errors='ignore'
                )[:max_chars]

            # Recursive nested multipart
            result = extract_body(part, max_chars)

            if result:
                return result

    elif 'data' in payload.get('body', {}):

        return base64.urlsafe_b64decode(
            payload['body']['data']
        ).decode(
            'utf-8',
            errors='ignore'
        )[:max_chars]

    return ''


def fetch_emails_from_account(
    service,
    account_email,
    query='',
    max_results=100
):
    """
    Fetch emails from a Gmail account.
    """

    emails = []

    page_token = None
    remaining = max_results

    while remaining > 0:

        fetch_count = min(remaining, 100)

        # Retry logic
        for attempt in range(3):

            try:

                list_kwargs = {
                    'userId': 'me',
                    'q': query,
                    'maxResults': fetch_count
                }

                if page_token:
                    list_kwargs['pageToken'] = page_token

                results = (
                    service.users()
                    .messages()
                    .list(**list_kwargs)
                    .execute()
                )

                break

            except Exception as e:

                wait = 2 ** attempt * 3

                print(
                    f"List retry {attempt+1}/3 "
                    f"for {account_email}"
                )

                print(e)

                time.sleep(wait)

        else:
            print(f"Failed page fetch: {account_email}")
            break

        messages = results.get('messages', [])

        if not messages:
            break

        # Fetch message details
        for msg in messages:

            for attempt in range(3):

                try:

                    detail = (
                        service.users()
                        .messages()
                        .get(
                            userId='me',
                            id=msg['id'],
                            format='full'
                        )
                        .execute()
                    )

                    break

                except Exception as e:

                    wait = 2 ** attempt * 2

                    print("Message retry")

                    print(e)

                    time.sleep(wait)

            else:
                continue

            headers = {
                h['name']: h['value']
                for h in detail['payload'].get(
                    'headers',
                    []
                )
            }

            body = extract_body(
                detail['payload']
            )

            emails.append({
                'account': account_email,
                'from': headers.get(
                    'From',
                    'Unknown'
                ),
                'to': headers.get(
                    'To',
                    ''
                ),
                'subject': headers.get(
                    'Subject',
                    'No Subject'
                ),
                'date': headers.get(
                    'Date',
                    ''
                ),
                'body': body.strip()
            })

        remaining -= len(messages)

        page_token = results.get(
            'nextPageToken'
        )

        if not page_token:
            break

        # Gentle rate limit
        time.sleep(0.3)

    print(
        f"[{account_email}] "
        f"Fetched {len(emails)} emails"
    )

    return emails


def fetch_all_emails(
    services,
    query='',
    max_results=100
):
    """
    Fetch emails from all connected accounts.
    """

    all_emails = []

    for account, service in services.items():

        account_emails = fetch_emails_from_account(
            service=service,
            account_email=account,
            query=query,
            max_results=max_results
        )

        all_emails.extend(account_emails)

    print(
        f"\nTotal emails fetched: "
        f"{len(all_emails)}"
    )

    return all_emails