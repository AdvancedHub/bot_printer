# -*- coding: utf-8 -*-
import config
from telebot import TeleBot, types

bot = TeleBot(config.token)
status = 0

mainkeyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_help = types.KeyboardButton(text="/help")
button_add = types.KeyboardButton(text="/add_file")
button_list = types.KeyboardButton(text="/list")
button_delete = types.KeyboardButton(text="/delete_file")
mainkeyboard.add(button_help, button_add, button_list, button_delete)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Список команд:", reply_markup=mainkeyboard)
    config.chat_id = message.chat.id
    log(message)


@bot.message_handler(commands=["help"])
def help_msg(message):
    bot.send_message(message.chat.id, "PrintBot:\n"
                                      "*Інформація*", reply_markup=mainkeyboard)
    log(message)


@bot.message_handler(commands=["add_file"])
def addfile(message):
    uid = message.from_user.id
    config.prev_message = message
    bot.send_message(message.chat.id, "Скинь файл...")
    bot.register_next_step_handler(message, add_document, uid)
    log(message)


@bot.message_handler()
def add_log(message):
    log(message)


def log(message, text="Сповіщення від"):
    print("###################################################")
    from datetime import datetime
    if message.content_type != 'text':
        msg = message.document.file_name
    else:
        msg = message.text
    print(datetime.now())
    print(text + " {0} {1} (id = {2}) \n{3}".format(message.from_user.first_name,
                                                    message.from_user.last_name,
                                                    str(message.from_user.id), msg))
    print("###################################################")


def add_document(msg, uid):
    uid_new = msg.from_user.id
    if uid == uid_new:
        if msg.content_type == 'document':
            bot.send_message(msg.chat.id, msg.document.file_name + " успішно добавлений!", reply_markup=mainkeyboard)
        else:
            bot.send_message(msg.chat.id, "\"" + msg.text + "\" - не документ!")
    log(msg, "Надіслав файл")


if __name__ == '__main__':
    bot.polling(none_stop=True)
