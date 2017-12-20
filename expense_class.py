
class Expense(object):
    """Expense entry taken from Isracard output xls
    """

    def __init__(self, date_made, establishment, amount, category):
        self.date_made = date_made
        self.establishment = establishment
        self.amount = amount
        self.category = category

    def get_amount(self,):
        return self.amount

    def get_establishment(self,):
        return self.establishment

    def get_date(self,):
        return self.date_made

    def get_month(self,):
        month_year = self.date_made[self.date_made.find('/')+1:]
        return int(month_year[:month_year.find('/')])

    def get_year(self,):
        month_year = self.date_made[self.date_made.find('/')+1:]
        return int(month_year[month_year.find('/')+1:])

    def get_category(self,):
        return self.category


