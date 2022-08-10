class HtmlTable:
    TABLE_STR_FORMAT = '''
    <table class="table table-responsive table-bordered table-hover">
        <thead class="table-dark">%s</thead>
        <tbody>%s</tbody>
    </table>
    '''
    TABLE_ROW_FORMAT = "<tr>%s</tr>"
    TABLE_HEADING_CELL_FORMAT = "<th>%s</th>"
    TABLE_CELL_FORMAT = "<td>%s</td>"

    def __init__(self, headers):
        self.rows = []
        self.header = self.__add_headers(headers)
        self.table_str = ""
    
    def __add_headers(self, headers):
        row_str = ""
        for cell in headers:
            row_str += self.TABLE_HEADING_CELL_FORMAT % (cell)

        return row_str

    def add_rows(self, rows):
        for row in rows:
            row_str = ""
            for cell in row:
                row_str += self.TABLE_CELL_FORMAT % (cell)

            self.rows.append(self.TABLE_ROW_FORMAT % (row_str))
    
    def build(self):
        body_str = ""
        for row in self.rows:
            body_str += row
        
        self.table_str = self.TABLE_STR_FORMAT % (self.header, body_str)
        

    def string_representation(self):
        return self.table_str
    
    def __str__(self):
        return self.string_representation()
    
    def __repr__(self):
        return self.string_representation()
    