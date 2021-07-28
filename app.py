import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = f'Привет, {message.chat.username}! \
\nЯ ConvertBot и я могу:\
\n- Показать список доступных валют через команду /values;\
\n- Конвертировать валюту через команду в формате: <имя валюты> <в какую валюту перевести> <количество переводимой валюты>;\
\n- Напомнить, что я могу через команду /help.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
        sum = total_base*float(amount)
    except ConvertionException as e:
        bot. reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать камонду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {sum}'
        bot.send_message(message.chat.id, text)


bot.polling()
