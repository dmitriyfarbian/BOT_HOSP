import telebot
import config
from config import *
import main

bot = telebot.TeleBot(config_bot, parse_mode=None)

application = dict()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    # print(message.user.id)
    keyboard.add(
        telebot.types.InlineKeyboardButton(text='Создать заявку', callback_data='make-app')
    )
    bot.send_message(message.chat.id, "Добрый день!\n Для начала оформления заявки - нажмите кнопку ниже", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'make-app')
def generate_data(call):
    if call.data == 'make-app':
        bot.send_message(call.message.chat.id, 'Начнем!')
        bot.send_message(call.message.chat.id, 'Введите наименование медицинской организации отправителя')
        main.set_state(call.message.chat.id, config.States.St_MO)
        print(main.set_state(call.message.chat.id, config.States.St_MO))


@bot.message_handler(content_types=['text'], func=lambda message: main.get_current_state(message.chat.id) == config.States.St_MO)
def input_text(message):
    bot.send_message(message.chat.id, 'Теперь введите ФИО пациента')
    application['МО'] = message.text
    main.set_state(message.chat.id, config.States.St_FIO)


@bot.message_handler(content_types=['text'], func=lambda message: main.get_current_state(message.chat.id) == config.States.St_FIO)
def input_text(message):
    bot.send_message(message.chat.id, 'Теперь введите возраст пациента')
    application['ФИО пациента'] = message.text
    main.set_state(message.chat.id, config.States.St_AGE)


@bot.message_handler(content_types=['text'], func=lambda message: main.get_current_state(message.chat.id) == config.States.St_AGE)
def input_text(message):
    bot.send_message(message.chat.id, 'Контактное лицо (ФИО + номер телефона)')
    application['Возраст'] = message.text
    main.set_state(message.chat.id, config.States.St_CONTACT)


@bot.message_handler(content_types=['text'], func=lambda message: main.get_current_state(message.chat.id) == config.States.St_CONTACT)
def input_text(message):
    bot.send_message(message.chat.id, 'Приложите выписной эпикриз в формате PDF')
    application['Контактоное лицо'] = message.text
    main.set_state(message.chat.id, config.States.St_EPICRISIS)


@bot.message_handler(content_types=['document'], func=lambda message: main.get_current_state(message.chat.id) == config.States.St_EPICRISIS)
def input_text(message):
    print(message)
    application['Отправитель'] = '@' + message.from_user.username
    application_text = ''
    for i in application.keys():
        application_text = application_text + f'{i}: {application[i]}\n'

    chat_id = -579112582
    bot.send_message(chat_id=chat_id, text=application_text)
    bot.forward_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.id)
    main.set_state(message.chat.id, config.States.St_OUTPUT)
    bot.send_message(message.chat.id, 'Спасибо, заявка сформирована и отправлена!')




print(bot.polling())
bot.polling()
