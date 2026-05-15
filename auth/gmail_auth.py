import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

CREDENTIALS_PATH = "credentials/credentials.json"
TOKENS_DIR = "tokens"


def get_token_path(account_email):
    """
    Create unique token file path for each Gmail account.
    """

    safe_name = (
        account_email
        .replace('@', '_at_')
        .replace('.', '_')
    )

    return os.path.join(
        TOKENS_DIR,
        f"token_{safe_name}.pickle"
    )


def get_gmail_service(account_email):
    """
    Authenticate Gmail account and return Gmail API service.
    """

    os.makedirs(TOKENS_DIR, exist_ok=True)

    token_file = get_token_path(account_email)

    creds = None

    # Load existing token
    if os.path.exists(token_file):
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)

    # Refresh expired token
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())

            with open(token_file, 'wb') as f:
                pickle.dump(creds, f)

            print(f"Token refreshed: {account_email}")

        except Exception:
            creds = None

    # Authenticate if needed
    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH,
            SCOPES
        )

        creds = flow.run_local_server(
            port=0
        )

        # Save token
        with open(token_file, 'wb') as f:
            pickle.dump(creds, f)

        print(f"Authenticated: {account_email}")

    return build(
        'gmail',
        'v1',
        credentials=creds
    )


def authenticate_multiple_accounts(accounts):
    """
    Authenticate multiple Gmail accounts.
    """

    services = {}

    for account in accounts:

        print(f"\nConnecting: {account}")

        try:
            services[account] = get_gmail_service(account)

            print(f"Connected: {account}")

        except Exception as e:

            print(f"Failed: {account}")
            print(e)

    return services