# -*- coding: utf-8 -*-
import config
from telebot import TeleBot, types

bot = TeleBot(config.token)

mainkeyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_help = types.KeyboardButton(text="/help")
button_add = types.KeyboardButton(text="/add_file")
button_list = types.KeyboardButton(text="/list")
button_delete = types.KeyboardButton(text="/delete_file")
mainkeyboard.add(button_help, button_add, button_list, button_delete)


@bot.message_handler(commands=["start"])
def start(message):
    clear_messages(message)
    bot.send_message(message.chat.id, "Список команд: ", reply_markup=mainkeyboard)
    log_msg(message)


@bot.message_handler(commands=["help"])
def help_msg(message):
    clear_messages(message)
    bot.send_message(message.chat.id, "PrintBot:\n"
                                      "*Інформація*", reply_markup=mainkeyboard)
    log_msg(message)


@bot.message_handler(commands=["add_file"])
def addfile(message):
    clear_messages(message)
    uid = message.from_user.id
    config.prev_message = message
    bot.send_message(message.chat.id, "Скинь файл...")
    bot.register_next_step_handler(message, add_document, uid)
    log_msg(message)


@bot.message_handler()
def add_log(message):
    clear_messages(message)
    log_msg(message)


def log_msg(message):
    config.prev_message_id = message.message_id
    print("Message id: " + str(config.prev_message_id))
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


def clear_messages(message):
    for i in range(config.numb):
        try:
            if config.prev_message_id + i != message.message_id:
                bot.delete_message(message.chat.id, config.prev_message_id + i)
        except:
            pass
    config.numb = 2


def add_document(msg, uid):
    uid_new = msg.from_user.id
    if uid == uid_new:
        if msg.content_type == 'document':
            bot.send_message(msg.chat.id, msg.document.file_name + " успішно добавлений!", reply_markup=mainkeyboard)
        else:
            bot.send_message(msg.chat.id, "\"" + msg.text + "\" - не документ!")
    log(msg, "Надіслав файл")
    config.numb = 4


if __name__ == '__main__':
    bot.polling(none_stop=True)
