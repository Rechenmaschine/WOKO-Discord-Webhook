class Room:
    def __init__(self, id, title, description, address, submitted, price):
        self.id = id
        self.title = title
        self.description = description
        self.address = address
        self.submitted = submitted
        self.price = price

    def url(self):
        return "https://www.woko.ch/en/zimmer-in-zuerich-details/" + str(self.id)

    def price_fmt(self):
        return str(self.price) + " CHF/Month"

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id