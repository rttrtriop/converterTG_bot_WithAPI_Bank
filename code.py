from aiogram import Bot, Dispatcher, types, DefaultBotProperties
from aiogram.filters import Command
from aiogram.enums import ParseMode
import asyncio
import logging
import sys
import aiohttp
import json

TOKEN = "7131471765:AAFBpFBOnHH1DA-UJateBtlKFRtOG5svKDk"
dp = Dispatcher()

async def fetch_currency_rates():
    url = "https://api.tinkoff.ru/v1/currency_rates"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = {}
                    for item in data.get('payload', {}).get('rates', []):
                        from_currency = item.get('fromCurrency', {}).get('iso')
                        to_currency = item.get('toCurrency', {}).get('iso')
                        buy_rate = item.get('buy')

                        if to_currency == 'RUB' and from_currency in ['USD', 'EUR', 'CNY'] and buy_rate:
                            rates[from_currency.lower()] = buy_rate
                    return rates
                else:
                    logging.error(f"Ошибка при запросе к API Тинькофф Банка: {response.status}")
                    return None
        except aiohttp.ClientError as e:
            logging.error(f"Ошибка соединения с API Тинькофф Банка: {e}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"Ошибка декодирования JSON от API Тинькофф Банка: {e}")
            return None

@dp.message(Command("start"))
async def start(message: types.Message):
    rates = await fetch_currency_rates()
    if rates:
        available_currencies = "\n".join(rates.keys())
        await message.answer(f"Доступные валюты:\n{available_currencies}")
        await message.answer("Введите сумму и валюту которую надо перевести в рубль (пример: 100 usd)")
    else:
        await message.answer("Не удалось получить курсы валют. Попробуйте позже.")

@dp.message()
async def convert_currency(message: types.Message):
    try:
        amount_str, currency_code = message.text.split()
        amount = float(amount_str)
        currency_code = currency_code.lower()
        rates = await fetch_currency_rates()
        if rates and currency_code in rates:
            rub_amount = amount * rates[currency_code]
            await message.answer(f"{amount:.2f} {currency_code.upper()} = {rub_amount:.2f} руб.")
        else:
            await message.answer("Некорректный ввод валюты или валюта не найдена. Доступные валюты: USD, EUR, CNY.")
    except ValueError:
        await message.answer("Некорректный формат ввода. Пожалуйста, введите сумму и валюту (пример: 100 usd).")

async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
