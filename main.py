from Controller import CurrencyController
TELEGRAM_BOT_TOKEN = 'PASTE HERE YOUR BOT TOKEN'

if __name__ == '__main__':
    controller = CurrencyController(TELEGRAM_BOT_TOKEN)
    controller.run()