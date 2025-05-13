from telebot import TeleBot, types
from Model import CurrencyModel
from View import CurrencyView


class CurrencyController:
    def __init__(self, bot_token):
        self.bot = TeleBot(bot_token)
        self.model = CurrencyModel()
        self.view = CurrencyView(self.bot)
        self.user_state = {}
        self._setup_handlers()

    def _setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.view.send_welcome(message.chat.id)

        @self.bot.message_handler(func=lambda m: m.text == "📊 Посмотреть курсы")
        def handle_show_rates(message):
            rates = self.model.get_currency_rates()
            formatted_rates = self.model.format_rates(rates)
            self.view.send_rates(message.chat.id, formatted_rates)

        @self.bot.message_handler(func=lambda m: m.text == "🔄 Конвертировать")
        def handle_convert(message):
            self.user_state[message.chat.id] = {'step': 'select_from'}
            self.view.ask_conversion_from(message.chat.id)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('curr_'))
        def handle_currency_selection(call):
            chat_id = call.message.chat.id
            currency = call.data[5:]

            if chat_id not in self.user_state:
                self.user_state[chat_id] = {'step': 'select_from'}

            if self.user_state[chat_id]['step'] == 'select_from':
                self.user_state[chat_id] = {
                    'step': 'select_to',
                    'from_currency': currency
                }
                self.view.ask_conversion_to(chat_id, currency)
            elif self.user_state[chat_id]['step'] == 'select_to':
                self.user_state[chat_id]['to_currency'] = currency
                self.user_state[chat_id]['step'] = 'enter_amount'
                self.view.ask_conversion_amount(
                    chat_id,
                    self.user_state[chat_id]['from_currency'],
                    currency
                )

            self.bot.answer_callback_query(call.id)

        @self.bot.message_handler(func=lambda m: m.chat.id in self.user_state and
                                                 self.user_state[m.chat.id]['step'] == 'enter_amount')
        def handle_amount_input(message):
            chat_id = message.chat.id
            state = self.user_state[chat_id]

            try:
                amount = float(message.text)
                rates = self.model.get_currency_rates()
                result = self.model.convert_currency(
                    amount,
                    state['from_currency'],
                    state['to_currency'],
                    rates
                )
                self.view.send_conversion_result(chat_id, result)
                del self.user_state[chat_id]  # Очищаем состояние
            except ValueError:
                self.view.send_error(chat_id, "Пожалуйста, введите корректную сумму")
                self.view.ask_conversion_amount(
                    chat_id,
                    state['from_currency'],
                    state['to_currency']
                )
    def run(self):
        print('Бот запущен (использует данные ЦБ РФ)!')
        self.bot.polling(none_stop=True)