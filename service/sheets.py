from beans.contributions import Contribution

class ContributionsSheetsService:
    def __init__(self, google_sheets_client):
        self.google_sheets_client = google_sheets_client
        self.spreadsheet = google_sheets_client.get_or_create_spreadsheet("2022")
    
    def add_new_contribution(self, contribution):
        self.google_sheets_client.add_row(self.spreadsheet, [
                contribution.name, contribution.amount, contribution.date
            ])

    def get_all_contributions(self):
        contributions = []
        contributions_data = self.google_sheets_client.get_all_data(self.spreadsheet)
        
        for i in range(1, len(contributions_data)):
            contributions.append(Contribution(excel_row=contributions_data[i]))

        return contributions