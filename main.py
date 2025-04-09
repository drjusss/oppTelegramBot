import telebot
from utils import user_messages, start_task
from credentials import bot, RECEIVER_CHAT_ID, ALLOWED_CONTENT_TYPES


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: telebot.types.Message) -> None:
    bot.reply_to(message=message, text='Привет, я бот поддержки учеников. Вы можете отправить мне сообщение, которое я отправлю инженерам, чтобы с вами оперативно связались.')


@bot.message_handler(func=lambda message: message.chat.id != RECEIVER_CHAT_ID, content_types=ALLOWED_CONTENT_TYPES)
def handle_appeals(message: telebot.types.Message) -> None:
    print(message.chat.id)
    if message.from_user.username in user_messages.keys():
        user_messages[message.from_user.username].append(message)
    else:
        user_messages[message.from_user.username] = [message]

    start_task(delay=10, username=message.from_user.username)


bot.infinity_polling()
