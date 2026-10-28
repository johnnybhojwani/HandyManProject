
import os
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

CREDENTIALS_FILE = BASE_DIR / os.getenv(
    "GOOGLE_CREDENTIALS_FILE", "credentials.json"
)
TOKEN_FILE = BASE_DIR / os.getenv(
    "GOOGLE_TOKEN_FILE", "token.json"
)

# One set of permissions for Sheets and Calendar.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/calendar"
]


def get_google_credentials():
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE), SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(
            creds.to_json(), encoding="utf-8"
        )

    return creds


def get_sheets_service():
    return build(
        "sheets",
        "v4",
        credentials=get_google_credentials()
    )


def get_calendar_service():
    return build(
        "calendar",
        "v3",
        credentials=get_google_credentials()
    )


if __name__ == "__main__":
    get_google_credentials()
    print("Google authentication successful!")