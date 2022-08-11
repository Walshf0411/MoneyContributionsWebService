from datetime import datetime

class Contribution:

    def __init__(self, json=None, excel_row=None):
        if json:
            self.init(json["name"], json["amount"])
        elif excel_row:
            self.init(excel_row[0], excel_row[1], excel_row[2], excel_row[3])
        
    
    def init(self, id, name, amount, date=None):
        self.id = id
        self.name = name
        self.amount = amount
        self.date = date if date else str(datetime.now().strftime("%a %d %B, %Y"))

    def __str__(self):
        return self.__convert_to_string()
    
    def __repr__(self):
        return self.__convert_to_string()
    
    def __convert_to_string(self):
        return "Contribution[name=%s, amount=%s, date=%s]" % (self.name, str(self.amount), str(self.date))