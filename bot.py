import telebot
import os

token = '1231441078:AAFzvpLywkM-G3bF0s6QvgafDUA7tVwHDBI'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['add'])
def add_name(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Отправте геопозицию места')
    bot.register_next_step_handler(message, add_finish)


def add_finish(message):
    try:
        place = message.location
        with open(f'data/{message.chat.id}.txt', 'a') as f:
            f.write(str(place.longitude) + ' ')
            f.write(str(place.latitude) + '\n')
        bot.send_message(chat_id=message.chat.id,
                         text='Локация добавлена успешно')
    except Exception:
        bot.send_message(chat_id=message.chat.id,
                         text='Геопозиия отправлена не верно.')


@bot.message_handler(commands=['reset'])
def reset(message):
    try:
        os.remove(f'data/{message.chat.id}.txt')
        bot.send_message(chat_id=message.chat.id,
                         text='Список локаций очищен')
    except Exception:
        bot.send_message(chat_id=message.chat.id,
                         text='Список локаций очищен')


@bot.message_handler(commands=['list'])
def list(message):
    if os.path.exists(f'data/{message.chat.id}.txt'):
        with open(f'data/{message.chat.id}.txt', 'r') as f:
            for line in f:
                line = line[:-1]
                longitude, latitude = line.split(' ')
                bot.send_location(chat_id=message.chat.id,
                                  latitude=latitude,
                                  longitude=longitude)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Список локаций пуст')


bot.polling()
