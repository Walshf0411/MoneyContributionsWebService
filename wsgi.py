import sys
from web.app import app
from client.sheets import GoogleSheetsClient
from client.twilio import TwilioClient
from service.sheets import ContributionsSheetsService

if __name__ == '__main__':
    app.run(debug=True)
