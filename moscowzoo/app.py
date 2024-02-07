import telebot
import logging
from config import (TOKEN, ID, questions,
                    page_mammals, page_reptiles, page_fish, page_amphibians, page_invertebrates, page_birds)
from basis import Error, Animal, Birds, Amphibians, Mammals, Reptiles, Fish, Invertebrates


bot = telebot.TeleBot(TOKEN)

logging.basicConfig(filename='bot_activity.log', level=logging.INFO)
winner_names = ''
number_ques = 0
count = 0


@bot.message_handler(commands=['start'])
def start_(message: telebot.types.Message):
    img = open('other/MZoo-logo.jpg', 'rb')
    text_start = (f'Приветствуем вас {message.from_user.first_name}! '
                  f'Желаете узнать с кем из наших меньших друзей вы уживетесь? Предлагаем вам пройти нашу викторину!\n'
                  f'Справка: команда /help')
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Начать викторину', callback_data='get_quiz'))
    bot.send_photo(message.chat.id, img, text_start, reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_(message: telebot.types.Message):
    text_help = ('Начать викторину: введите команду /start\n'
                 'Справка: введите команду /help\n'
                 'Попросить сотрудника связаться с вами: введите команду /contact\n'
                 'Оставить отзыв для улучшения: отправьте сообщение в виде "feedback {отзыв}"')
    bot.send_message(message.chat.id, text_help)


@bot.message_handler(commands=['contact'])
def contact_(message: telebot.types.Message):
    bot.send_message(ID, f'{message.from_user.first_name}: @{message.from_user.username}, {winner_names}')
    bot.send_message(message.chat.id, 'Информация передана. Ожидайте!')


@bot.message_handler(content_types=['text'])
def text_(message: telebot.types.Message):
    if message.text[0:8].lower() == 'feedback':
        if len(message.text) < 9:
            bot.send_message(message.chat.id, 'Отзыв необходимо оставить после слова "feedback"')
        else:
            fb = open('other/feedback.txt', 'a')
            fb.write(message.text + '\n')
            fb.close()
            bot.send_message(message.chat.id, 'Спасибо! Предложение принято!')

    else:
        bot.send_message(message.chat.id, 'Такой команды нет :( Вызвать справку: /help')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global number_ques, count
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Не про меня', callback_data='1'))
    keyboard.row(telebot.types.InlineKeyboardButton('Затрудняюсь ответить', callback_data='2'))
    keyboard.row(telebot.types.InlineKeyboardButton('Точно да', callback_data='3'))

    if call.data == 'get_quiz':
        bot.send_message(call.message.chat.id, questions[number_ques], reply_markup=keyboard)

    if call.data == '1' or call.data == '2' or call.data == '3':
        number_ques += 1

        if call.data == '1':
            count = count + 1
        if call.data == '2':
            count = count + 2
        if call.data == '3':
            count = count + 3

        if questions[number_ques] == "":
            result = telebot.types.InlineKeyboardMarkup()
            result.row(telebot.types.InlineKeyboardButton('Тык', callback_data='result'))
            bot.send_message(call.message.chat.id, "Нажмите для результата", reply_markup=result)
        else:
            bot.send_message(call.message.chat.id, questions[number_ques], reply_markup=keyboard)

    if call.data == 'result':
        if count == 3:
            x = Fish(page_fish)
            send_mess(call, x)

        if count == 4:
            x = Amphibians(page_amphibians)
            send_mess(call, x)

        if count == 5:
            x = Reptiles(page_reptiles)
            send_mess(call, x)

        if count == 6:
            x = Mammals(page_mammals)
            send_mess(call, x)

        if count == 7:
            x = Invertebrates(page_invertebrates)
            send_mess(call, x)

        if count > 7:
            x = Birds(page_birds)
            send_mess(call, x)

    if call.data == 'feedback':
        bot.send_message(call.message.chat.id, "Отправьте сообщение в формате: feedback {ваше предолжение}")


@bot.message_handler(func=lambda message: True)
def log_user_activity(message):
    user_id = message.from_user.id
    user_message = message.text
    logging.info(f"User {user_id}: {user_message}")


def send_mess(call, x):
    global count, number_ques, winner_names

    x.win_info()
    winner_names = x.winner_names
    more = telebot.types.InlineKeyboardMarkup()
    more.row(telebot.types.InlineKeyboardButton('Узнать больше', url=f'{x.winner_info}'))
    more.row(telebot.types.InlineKeyboardButton('Попробовать еще раз', callback_data='get_quiz'))
    more.row(telebot.types.InlineKeyboardButton('Предложения улучшения', callback_data='feedback'))
    text_send_mess = (f'Вы с {winner_names} из одного теста! Желаете узнать больше? '
                      f'Можно сделать это перейдя на сайт по кнопке "Узнать больше". '
                      f'Или вы можете ввести команду /contact и мы сами свяжемся с вами в телеграмме.')
    count, number_ques = 0, 0
    bot.send_photo(call.message.chat.id, photo=f'{x.winner_picture}')
    bot.send_message(call.message.chat.id, text_send_mess, reply_markup=more)
    guardianship = telebot.types.InlineKeyboardMarkup()
    guardianship.row(telebot.types.InlineKeyboardButton('Программа опеки',
                                                        url='https://moscowzoo.ru/my-zoo/become-a-guardian/'))
    guardianship_text = ('Так же вы можете принять участие в деле сохранения редких видов. '
                         'Программа «Возьми животное под опеку» дает возможность опекунам '
                         'ощутить свою причастность к делу сохранения природы. '
                         'Желаете узнать как?')
    return bot.send_message(call.message.chat.id, guardianship_text, reply_markup=guardianship)


bot.polling()