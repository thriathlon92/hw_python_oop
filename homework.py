import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
        else:
            self.date = dt.date.today()

    def __str__(self):
        return f'{self.amount} {self.comment} {self.date}'


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        return self.get_sum_amount(1)

    # "Get 7-days status count"
    def get_week_stats(self):
        return self.get_sum_amount(7)

    # "Function for using in calculation sum amount for a day or week"
    def get_sum_amount(self, days):
        today = dt.date.today()
        delta = dt.timedelta(days=days)
        start_date = today - delta
        return sum([i.amount for i in self.records
                    if start_date < i.date <= today])

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


if __name__ == "__main__":
    cash_calculator = CashCalculator(1000)

    # дата в параметрах не указана,
    # так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))

    print(cash_calculator.get_today_cash_remained("rub"))
