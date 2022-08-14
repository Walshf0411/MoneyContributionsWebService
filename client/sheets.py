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

    def read_range(self, workbook, sheet_name, range):
        sheet = spreadsheet.worksheet(sheet_name)
        return sheet.range(range)

    def add_row(self, spreadsheet, sheet_name, data):
        meta_data_cell = "J1"
        first_col_char = "A"
        sheet = spreadsheet.worksheet(sheet_name)
        last_updated_row = sheet.acell(meta_data_cell).value.split(":")
        new_row_num = int(last_updated_row[1]) + 1
        range_start = first_col_char + str(new_row_num)
        range_end = chr(len(data) + ord(first_col_char)) + str(new_row_num)
        range = range_start + ":" + range_end
        data.insert(0, new_row_num - 1)
        sheet.update(range, [data, ])
        sheet.update(meta_data_cell,
                     last_updated_row[0] + ":" + str(new_row_num))
    
    def get_all_data(self, spreadsheet, sheet_name):
        sheet = spreadsheet.worksheet(sheet_name)
        return sheet.get_all_values()

    def get_row(self, spreadsheet, sheet_name, row_num):
        sheet = spreadsheet.worksheet(sheet_name)
        values_list = sheet.row_values(row_num)
        return values_list
    
    def get_rows(self, spreadsheet, sheet_name, start, end):
        rows = []

        for row_num in range(start, end + 1):
            rows.append(get_row(row_num))
        
        return rows
    
    def update_row(self, spreadsheet, sheet_name, row_num, data):
        first_col_char = "A"
        sheet = spreadsheet.worksheet(sheet_name)
        range_start = first_col_char + str(row_num)
        range_end = chr(len(data) + ord(first_col_char)) + str(row_num)
        range = range_start + ":" + range_end
        data.insert(0, row_num - 1)
        sheet.update(range, [data, ])