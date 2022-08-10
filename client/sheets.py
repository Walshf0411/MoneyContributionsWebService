import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/drive"
]

class GoogleSheetsClient:
    def __init__(self):
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("google-credentials.json")
        self.sheets = gspread.authorize(self.creds)

    def get_or_create_spreadsheet(self, spreadsheet_name):
        spreadsheet = None
        try:
            spreadsheet = self.sheets.open(spreadsheet_name)
        except gspread.exceptions.SpreadsheetNotFound:
            spreadsheet = self.sheets.create(spreadsheet_name)
            spreadsheet.share('walshernades.320@gmail.com', perm_type='user', role='writer')

        return spreadsheet

    def read_range(self, workbook, range):
        sheet = workbook.sheet1
        return sheet.range(range)

    def add_row(self, spreadsheet, data):
        # F1 cell will hold the position of the last updated row in the format last_row:<row_num>
        last_updated_row = spreadsheet.sheet1.acell('F1').value.split(":")
        new_row_num = int(last_updated_row[1]) + 1
        # TODO update this logic, to fetch columns dynamically
        range_start = "A" + str(new_row_num)
        range_end = "C" + str(new_row_num)
        range = range_start + ":" + range_end
        spreadsheet.sheet1.update(range, [data, ])
        spreadsheet.sheet1.update("F1", last_updated_row[0] + ":" + str(new_row_num))
    
    def get_all_data(self, spreadsheet):
        return spreadsheet.sheet1.get_all_values()
        