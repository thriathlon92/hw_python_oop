import datetime as dt


class Record:
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.strptime(date, self.date_format).date() if date else dt.datetime.now().date()

    def __str__(self):
        return f'{self.amount}'


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        today_amount = 0
        now = dt.datetime.now()
        for i in self.records:
            if i.date == now.date():
                today_amount += i.amount
        return today_amount

    # "Get 7-days status count"
    def get_week_stats(self):
        sum_amount = 0
        today = dt.datetime.now()
        delta = dt.timedelta(days=7)
        start_date = today - delta
        for i in self.records:
            if start_date < i.date <= today:
                sum_amount += i.amount
        return sum_amount

    def __str__(self):
        return ', '.join(str(s) for s in self.records)


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today_calories = super().get_today_stats()
        today_calories_left = self.limit - today_calories
        if today_calories_left > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {today_calories_left} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    EURO_RATE = 90.0
    USD_RATE = 77.0

    def __str__(self):
        return f'{self.limit}'

    def get_today_cash_remained(self, currency):
        currencies = {
            'rub': [1, 'руб'],
            'usd': [self.USD_RATE, 'USD'],
            'eur': [self.EURO_RATE, 'Euro'],
        }
        today_cash_spend = super().get_today_stats()
        today_cash_left = self.limit - today_cash_spend
        rate = currencies[currency]
        money = round(today_cash_left / rate[0], 2)
        if money > 0:
            return f'На сегодня осталось {money} {rate[1]}'
        elif money == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {abs(money)} {rate[1]}'
