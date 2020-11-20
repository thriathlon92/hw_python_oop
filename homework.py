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
        amount = self.amount
        comment = self.comment
        date = self.date
        return f'{amount} {comment} {date:%d.%m.%Y}'


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
        return sum(i.amount for i in self.records
                   if start_date < i.date <= today)

    # "Function for today limit calculation"
    def get_remainder(self):
        return self.limit - self.get_today_stats()

    def __str__(self):
        return ', '.join(str(s) for s in self.records)


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_amount = self.get_remainder()
        if calories_amount <= 0:
            return 'Хватит есть!'
        return ('Сегодня можно съесть что-нибудь ещё,'
                f' но с общей калорийностью не более {calories_amount} кКал')


class CashCalculator(Calculator):
    EURO_RATE = 60.0
    USD_RATE = 50.0

    def __str__(self):
        return f'{self.limit}'

    def get_today_cash_remained(self, currency):

        currencies = {
            'rub': (1, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
        }
        try:
            rate, cash_currency = currencies[currency]
        except KeyError:
            return ('Incorrect currency was given: '
                    f'{currency}, instead of rub/usd/eur!')

        money = self.get_remainder() / rate

        if money == 0:
            return 'Денег нет, держись'
        if money > 0:
            return f'На сегодня осталось {money:.2f} {cash_currency}'
        money = abs(money)
        return ('Денег нет, держись: твой долг '
                f'- {money:.2f} {cash_currency}')


if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)

    # дата в параметрах не указана,
    # так что по умолчанию к записи
    # должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000,
                                      comment='бар в Танин др',
                                      date='08.11.2019'))

    print(cash_calculator.get_today_cash_remained('rub'))
