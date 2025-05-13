class CurrencyModel:
    def __init__(self):
        self.currency_full_names = {
            'USD': 'Доллар США',
            'EUR': 'Евро',
            'GBP': 'Фунт стерлингов',
        }

    def format_rates(self, rates):
        if isinstance(rates, str):
            return rates

        date = datetime.now().strftime('%d.%m.%Y')
        rates_table = f"📅 *Курсы на {date}*\n\n"
        rates_table += "```\n"
        rates_table += "Валюта      Курс к RUB\n"
        rates_table += "-----------------------\n"

        for code in sorted(rates.keys()):
            if code in self.currency_full_names:
                name = self.currency_full_names[code]
                rates_table += f"{code} ({name[:10]}): {rates[code]:.2f}\n"

        rates_table += "```"
        return rates_table