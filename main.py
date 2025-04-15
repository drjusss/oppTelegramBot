import telebot

from utils import user_messages, start_task
from credentials import bot, RECEIVER_CHAT_ID, ALLOWED_CONTENT_TYPES, DEBUG
import decorators


@bot.message_handler(commands=['help', 'start'])
@decorators.log_error
def send_welcome(message: telebot.types.Message) -> None:
    bot.reply_to(message=message, text='Привет, я бот поддержки учеников. Вы можете отправить мне сообщение, которое я отправлю инженерам, чтобы с вами оперативно связались.')


@bot.message_handler(func=lambda message: DEBUG or message.chat.id != RECEIVER_CHAT_ID, content_types=ALLOWED_CONTENT_TYPES)
@decorators.log_error
def handle_appeals(message: telebot.types.Message) -> None:
    if message.from_user.username in user_messages.keys():
        user_messages[message.from_user.username].append(message)
    else:
        user_messages[message.from_user.username] = [message]

    if DEBUG:
        delay = 10
    else:
        delay = 20

    start_task(delay=delay, username=message.from_user.username)


bot.infinity_polling()
