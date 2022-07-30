import time 

class Contribution:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        self.date = str(time.ctime())
        