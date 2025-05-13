import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class CurrencyView:
    def __init__(self, bot):
        self.bot = bot
        self.currency_names = {
            'USD': 'Доллар США',
            'EUR': 'Евро',
            'GBP': 'Фунт стерлингов',
            'JPY': 'Японская иена',
            # Добавьте остальные валюты по аналогии
            'RUB': 'Российский рубль'
        }

    def create_main_keyboard(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            KeyboardButton("📊 Текущие курсы"),
            KeyboardButton("🔄 Конвертировать")
        )
        return keyboard

    def create_currency_keyboard(self):
        keyboard = InlineKeyboardMarkup(row_width=4)
        currencies = [
            ('USD', 'Доллар'), ('EUR', 'Евро'), ('GBP', 'Фунт'),
            ('JPY', 'Иена'), ('CNY', 'Юань'), ('RUB', 'Рубль')
        ]
        buttons = [
            InlineKeyboardButton(
                f"{code} ({name})",
                callback_data=f"curr_{code}"
            ) for code, name in currencies
        ]
        keyboard.add(*buttons)
        return keyboard

    def send_welcome(self, chat_id):
        welcome_msg = (
            "💱 *Валютный бот ЦБ РФ*\n\n"
            "Я предоставляю актуальные курсы валют и конвертацию.\n"
            "Выберите действие:"
        )
        self.bot.send_message(chat_id, welcome_msg,
                              reply_markup=self.create_main_keyboard(),
                              parse_mode='Markdown')

    def format_rates_table(self, rates):
        table = "📊 *Курсы ЦБ РФ на сегодня*\n\n"
        table += "| Валюта       | Курс к RUB |\n"
        table += "|--------------|------------|\n"

        for code, rate in rates.items():
            name = self.currency_names.get(code, code)
            table += f"| {code} ({name}) | {rate:.2f} |\n"

        return table
