import sys
from client.twilio import TwilioClient
from client.sheets import GoogleSheetsClient
from service.sheets import ContributionsSheetsService
from beans.contributions import Contribution

def main(args):
    # twilio_client = TwilioClient()
    # sid = twilio_client.send_message("+919757221040", "Hi Walsh")
    google_sheets_client = GoogleSheetsClient("/workspace/WhatsappWebApp/secrets.json")

    contributions_sheet_service = ContributionsSheetsService(google_sheets_client)
    contributions = [Contribution("Walsh", "7000"), Contribution("Lara", "10000"), Contribution("Ankit", "5000")]
    
    for contribution in contributions:
        contributions_sheet_service.add_new_contribution(contribution)
    

if __name__ == '__main__':
    main(sys.argv[1:])