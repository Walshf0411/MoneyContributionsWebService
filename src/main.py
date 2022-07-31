import sys
from web.app import FlaskApp
from client.sheets import GoogleSheetsClient
from client.twilio import TwilioClient
from service.sheets import ContributionsSheetsService

def main():
    google_sheets_client = GoogleSheetsClient("/workspace/WhatsappWebApp/secrets.json")
    contributions_sheet_service = ContributionsSheetsService(google_sheets_client)
    twilio_client = TwilioClient()
    app = FlaskApp(contributions_sheet_service, twilio_client)

    app.run()

if __name__ == '__main__':
    main()