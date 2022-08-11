from datetime import datetime

class Tshirt:
    def __init__(self, data_row, is_excel=False):
        self.id = data_row[0]
        self.name = data_row[1]
        self.quantity = data_row[2]
        self.size = data_row[3]

        if is_excel:    
            self.date = data_row[4]
            self.notes = self.__get_or_default(5, data_row)
            self.payment = self.__get_or_default(6, data_row, 0)
        elif len(data_row) == 6:
            self.date = str(datetime.now().strftime("%a %d %B, %Y"))
            self.notes = self.__get_or_default(4, data_row)
            self.payment = self.__get_or_default(5, data_row, 0)

    def update_date(self):
        self.date = str(datetime.now().strftime("%a %d %B, %Y"))

    def __str__(self):
        return self.__convert_to_string()

    def __repr__(self):
        return self.__convert_to_string()

    def __convert_to_string(self):
        return "Tshirt[name=%s, quantity=%s, size=%s, payment=%s, date=%s]" % (self.name, str(self.quantity), str(self.size), str(self.payment), str(self.date))

    def __get_or_default(self, index, list, default=""):
        value = None
        try:
            value = list[index]
        except IndexError:
            value = default
        return value
