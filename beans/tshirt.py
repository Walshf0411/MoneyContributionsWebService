from datetime import datetime

class Tshirt:
    def __init__(self, data_row):
        self.name = data_row[0]
        self.quantity = data_row[1]
        self.size = data_row[2]
        self.date = str(datetime.now().strftime("%a %d %B, %Y"))

    def __str__(self):
        return self.__convert_to_string()

    def __repr__(self):
        return self.__convert_to_string()

    def __convert_to_string(self):
        return "Tshirt[name=%s, quantity=%s, size=%s, date=%s]" % (self.name, str(self.quantity), str(self.size), str(self.date))
