import texttable

class TextTableUtil:
    @staticmethod
    def build_text_table(headers, data):
        table = texttable.Texttable()
        table.set_cols_align(["l", "c"])
        
        # table.set_cols_dtype(["a", "i", "t"])
        
        # Adjust columns
        # table.set_cols_valign(["t", "m", "b"])
        
        # Insert rows
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

    @classmethod
    def build_text_table_from_contributions(cls, contributions):
        # removed date_contributed from the columns as it is breaking formatting
        contributions_headers = ["NAME", "AMOUNT(Rs)"]
        data = []
        total_amount = 0
        
        for contribution in contributions:
            data.append([contribution.name, contribution.amount])
            total_amount += int(contribution.amount)
        
        data.append(["TOTAL", str(total_amount)])

        return cls.build_text_table2(contributions_headers, data)
