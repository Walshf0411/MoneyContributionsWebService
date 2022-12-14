import math

from beans.contributions import Contribution
from beans.tshirt import Tshirt

class ContributionsSheetsService:
    def __init__(self, google_sheets_client):
        self.google_sheets_client = google_sheets_client
        self.spreadsheet = google_sheets_client.get_or_create_spreadsheet("2022")
        self.sheet_name = "contribution"
    
    def add_new_contribution(self, contribution):
        self.google_sheets_client.add_row(self.spreadsheet, self.sheet_name, [
                contribution.name, contribution.amount, contribution.date
            ])

    def get_all_contributions(self):
        contributions = []
        contributions_data = self.google_sheets_client.get_all_data(self.spreadsheet, self.sheet_name)
        
        for i in range(1, len(contributions_data)):
            contributions.append(Contribution(excel_row=contributions_data[i]))

        return contributions


class TshirtSheetService:
    def __init__(self, google_sheets_client):
        self.google_sheets_client = google_sheets_client
        self.spreadsheet = google_sheets_client.get_or_create_spreadsheet("2022")
        self.sheet_name = "tshirt"

    def add_new_tshirt(self, tshirt):
        self.google_sheets_client.add_row(self.spreadsheet, self.sheet_name, [
            tshirt.name, tshirt.quantity, tshirt.size, tshirt.date, tshirt.notes, tshirt.payment
        ])

    def get_all_tshirt(self):
        tshirts = []
        tshirts_data = self.google_sheets_client.get_all_data(
            self.spreadsheet, self.sheet_name)

        for i in range(1, len(tshirts_data)):
            tshirts.append(Tshirt(tshirts_data[i], is_excel=True))

        return tshirts

    def get_paginated_data(self, page_num, page_size):
        tshirts = []
        row_count = self.google_sheets_client.get_row_count(
            self.spreadsheet, self.sheet_name)
        print(row_count)  
        page_count = math.ceil(row_count / page_size)
        start = (page_num - 1) * page_size + 1

        if page_num > page_count:
            return -1, []

        end = min(row_count, page_num * page_size)
        tshirts_data = self.google_sheets_client.get_rows(
            self.spreadsheet, self.sheet_name, start, end)

        for i in range(len(tshirts_data)):
            if tshirts_data[i]:
                tshirts.append(Tshirt(tshirts_data[i], is_excel=True))

        return page_count, tshirts

    def update_payment(self, id, payment):
        tshirt_data = self.google_sheets_client.get_row(
            self.spreadsheet, self.sheet_name, id + 1)
        tshirt = Tshirt(tshirt_data, is_excel=True)
        tshirt.payment = payment
        tshirt.update_date()

        self.google_sheets_client.update_row(
            self.spreadsheet, self.sheet_name, id + 1, [
                tshirt.name, tshirt.quantity, tshirt.size, tshirt.date, tshirt.notes, tshirt.payment
                ])

