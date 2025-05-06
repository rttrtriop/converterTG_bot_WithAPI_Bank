import telebot
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

TELEGRAM_BOT_TOKEN = '6938681555:AAF3oYXgwgJgMPLR-1s9vN77z5MONNKweUg'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
currency_codes = ['USD', 'EUR', 'GBP', 'CNY', 'JPY', 'CHF', 'CAD', 'AUD', 'HKD', 'TRY']

def get_currency_rates():
    try:
        today = datetime.now().strftime('%d/%m/%Y')
        url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={today}"
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        rates = {}
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            value = float(valute.find('Value').text.replace(',', '.'))
            rates[char_code] = value
        return rates
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе к ЦБ РФ: {e}"
    except ET.ParseError as e:
        return f"Ошибка обработки данных ЦБ РФ: {e}"
    except Exception as e:
        return f"Непредвиденная ошибка: {e}"

@bot.message_handler(commands=['start'])
def send_cbr_currency_rates(message):
    rates_data = get_currency_rates()
    if isinstance(rates_data, dict):
        rates_info = f"Курсы валют (ЦБ РФ на {datetime.now().strftime('%d.%m.%Y')}):\n"
        for code in currency_codes:
            if code in rates_data:
                rates_info += f"{code}/RUB: {rates_data[code]}\n"
            else:
                rates_info += f"Курс для {code} не найден.\n"
        bot.reply_to(message, rates_info)
    else:
        bot.reply_to(message, rates_data)

if __name__ == '__main__':
    print('Бот запущен (данные ЦБ РФ)!')
    bot.polling(none_stop=True)

