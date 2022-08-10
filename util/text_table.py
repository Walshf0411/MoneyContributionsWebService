import texttable
from web.components import HtmlTable

class TextTableUtil:
    @staticmethod
    def build_text_table(headers, data):
        table = texttable.Texttable()
        table.set_cols_align(["l", "c"])
        rows = []
        rows.append(headers)
        
        for row in data:
            rows.append(row)

        table.add_rows(rows)

        return table.draw()

    @staticmethod
    def build_text_table2(headers, data):
        table = ""
        for header in headers:
            table += header + " "
        table += "\n"
        table += "-" * 15
        table += "\n"

        for row in data:
            for cell_data in row:
                table += cell_data + " "
            table += "\n"
        
        return table

    @staticmethod
    def build_html_table(headers, data):
        html_table = HtmlTable(headers)
        html_table.add_rows(data)
        html_table.build()
        return html_table

    @classmethod
    def build_text_table_from_contributions(cls, contributions, use_texttable=False, use_html=False):
        # removed date_contributed from the columns as it is breaking formatting
        contributions_headers = ["NAME", "AMOUNT(Rs)"]
        data = []
        total_amount = 0
        
        for contribution in contributions:
            data.append([contribution.name, contribution.amount])
            total_amount += int(contribution.amount)
        
        data.append(["TOTAL", str(total_amount)])

        return cls.build_text_table(contributions_headers, data) if use_texttable else cls.build_html_table(contributions_headers, data) if use_html else cls.build_text_table2(contributions_headers, data)

    @classmethod
    def build_text_table_from_tshirts(cls, tshirts, use_texttable=False, use_html=False):
        # removed date_contributed from the columns as it is breaking formatting
        tshirt_headers = ["NAME", "Quantity", "Size"]
        data = []

        for tshirt in tshirts:
            data.append([tshirt.name, tshirt.quantity, tshirt.size])

        return cls.build_text_table(tshirt_headers, data) if use_texttable else cls.build_html_table(tshirt_headers, data) if use_html else cls.build_text_table2(tshirt_headers, data)
