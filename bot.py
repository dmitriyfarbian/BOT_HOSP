import time

import telebot
from telebot.types import InputMediaPhoto, BotCommand

import config
from config import *
import main

bot = telebot.TeleBot(config_bot, parse_mode=None)
command = BotCommand('sendapp', 'Для отправки заявки введите данную комманду')
bot.set_my_commands([command])

application = dict()
photos = []



@bot.message_handler(commands=['sendapp', 'start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    # print(message.user.id)
    keyboard.add(
        telebot.types.InlineKeyboardButton(text='Создать заявку', callback_data='make-app')
    )
    bot.send_message(message.chat.id, "Добрый день!\n Для начала оформления заявки - нажмите кнопку ниже", reply_markup=keyboard)


@bot.message_handler(commands=['reset'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    # print(message.user.id)
    keyboard.add(
        telebot.types.InlineKeyboardButton(text='Создать заявку', callback_data='make-app')
    )
    main.set_state(message.chat.id, config.States.St_MO)
    bot.send_message(message.chat.id, "Добрый день!\n Для начала оформления заявки - нажмите кнопку ниже", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'make-app')
def generate_data(call):
    if call.data == 'make-app':
        bot.send_message(call.message.chat.id, 'Начнем!')
        bot.send_message(call.message.chat.id, 'Введите наименование медицинской организации отправителя')
        main.set_state(call.message.chat.id, config.States.St_MO)
        print(main.set_state(call.message.chat.id, config.States.St_MO))


@bot.callback_query_handler(func=lambda call: call.data == 'end_photo')
def generate_data(call):
    if call.data == 'end_photo':
        chat_id = -572032075
        print(photos)
        bot.send_media_group(chat_id=chat_id, media=photos)
        print('Попало')
        photos.clear()
        main.set_state(call.message.chat.id, config.States.St_OUTPUT)
        bot.send_message(call.message.chat.id, 'Заявка отправлена!')


@bot.callback_query_handler(func=lambda call: call.data == 'more_photo')
def generate_data(call):
    if call.data == 'more_photo':
        bot.send_message(call.message.chat.id, 'Загрузите дополнительные фото')


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
    bot.send_message(message.chat.id, 'Приложите выписной эпикриз в формате PDF\nили фотографию\n(Если фото несколько, необходимо загружать по одной!)')
    application['Контактоное лицо'] = message.text
    main.set_state(message.chat.id, config.States.St_EPICRISIS)


@bot.message_handler(content_types=['document'], func=lambda message: main.get_current_state(message.chat.id) == config.States.St_EPICRISIS)
def input_text(message):
    if message.document.file_name.split('.')[-1] == 'pdf':
        print(message.document.file_name.split('.')[-1])
        try:
            application['Отправитель'] = '@' + message.from_user.username
        except TypeError as e:
            application['Отправитель'] = f'tg://user?id={message.from_user.id}'
        application_text = ''
        for i in application.keys():
            application_text = application_text + f'*{i}*: {application[i]}\n'

        chat_id = -572032075
        bot.send_document(chat_id=chat_id, data=message.document.file_id, caption=application_text, parse_mode='Markdown')
        # bot.forward_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.id)
        main.set_state(message.chat.id, config.States.St_OUTPUT)
        bot.send_message(message.chat.id, 'Спасибо, заявка сформирована и отправлена!')
    else:
        bot.send_message(message.chat.id, 'Принимаются файлы формата pdf!\nПопробуйте загрузить заново')
        main.set_state(message.chat.id, config.States.St_EPICRISIS)


@bot.message_handler(content_types=['photo'], func=lambda message: main.get_current_state(message.chat.id) == config.States.St_EPICRISIS)
def pictures(message):
    global photos
    if message.media_group_id:
        bot.send_message(message.chat.id, 'Фотографии необходимо отправлять по одной!')

    else:
        photo = InputMediaPhoto(media=message.photo[-1].file_id)
        photos.append(photo)
        if len(photos) == 1:
            print(message)
            try:
                application['Отправитель'] = '@' + message.from_user.username
            except TypeError as e:
                application['Отправитель'] = f'tg://user?id={message.from_user.id}'
            application_text = ''
            for i in application.keys():
                application_text = application_text + f'*{i}*: {application[i]}\n'
            photos.pop(0)
            print('массив после удаления', photos)
            photo = InputMediaPhoto(media=message.photo[-1].file_id, caption=application_text, parse_mode='Markdown')
            photos.append(photo)
            print('массив после Добавления в условии', photos)
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(
                telebot.types.InlineKeyboardButton(text='Добавить доп. фото', callback_data='more_photo')
            )
            keyboard.add(
                telebot.types.InlineKeyboardButton(text='Завершить отправку фото', callback_data='end_photo')
            )
            bot.send_message(message.chat.id, 'Добавить дополнительные фото?', reply_markup=keyboard)

        else:

            print('массив после Добавления не в условии', photos)
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(
                telebot.types.InlineKeyboardButton(text='Добавить доп. фото', callback_data='more_photo')
            )
            keyboard.add(
                telebot.types.InlineKeyboardButton(text='Завершить отправку фото', callback_data='end_photo')
            )
            bot.send_message(message.chat.id, 'Добавить дополнитлеьные фото?', reply_markup=keyboard)
print(bot.polling())
bot.polling()
