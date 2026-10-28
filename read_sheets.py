from langchain_openai import ChatOpenAI
from google_auth_setup import get_sheets_service

SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1wrItgWsgLmed3PlkaE8nuHEGBdgN20rXJAvDEvWWo1E"
RANGE_NAME = "PricingSheet!A1:G10"

def main():

    sheets_service = get_sheets_service()
    result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()

    values = result.get("values", [])

    if not values:
        print("No data found.")
        return

    print("\nSUCCESS: Spreadsheet data retrieved\n")

    for row in values:
        print(row)

if __name__ == "__main__":
    main()