
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

class Establishment(object):
    """Establishments in Isracard output xls
    """
    def __init__(self,name, category = None):
        self.expenses = []
        self.category = category
        self.amount = 0
        self.name = name
        self.month_made = 0
        self.year_made = 0

    def get_expenses(self,):
        return self.expenses

    def get_category(self,):
        return self.category

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.amount += int(expense.get_amount())
        if self.month_made==0:
            self.month_made = expense.get_month()
            self.year_made = expense.get_year()

    def set_category (self, categeory):
        self.category = categeory

    def get_name(self):
        return self.name

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount

    def get_month(self,):
        return self.month_made

    def get_year(self,):
        return self.year_made

    def get_category(self,):
        return self.category

class Category(object):
    """Categories in Buisinesses csv
    """

    def __init__(self, name):
        self.establishments = []
        self.amount = 0
        self.name = name

    def get_amount(self,):
        return self.amount

    def get_establishments(self):
        return self.establishments

    def set_amount(self, amount):
        self.amount = amount

    def add_establishment(self, establishment):
        self.establishments.append(establishment)
        self.amount += int(establishment.get_amount())

    def get_name(self):
        return self.name