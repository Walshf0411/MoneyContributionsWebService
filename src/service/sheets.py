class ContributionsSheetsService:
    def __init__(self, google_sheets_client):
        self.google_sheets_client = google_sheets_client
        self.spreadsheet = google_sheets_client.get_or_create_spreadsheet("2022")
    
    def add_new_contribution(self, contribution):
        self.google_sheets_client.add_row(self.spreadsheet, [
                contribution.name, contribution.amount, contribution.date
            ])