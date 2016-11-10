class Hotel:
    def __init__(self):
        self.url = ""
        self.address = ""
        self.name = ""

    def __str__(self):
        return self.url + " " + self.address
