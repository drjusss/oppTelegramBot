import telebot

# test_config
# API_TOKEN = '7478300229:AAHLO4zspS8IqyrmvCdqwTxLFVlR0lUIJmg'
# RECEIVER_CHAT_ID = 865222212

# prod_config
API_TOKEN = '7478300229:AAHLO4zspS8IqyrmvCdqwTxLFVlR0lUIJmg'
RECEIVER_CHAT_ID = -1002501401692

ALLOWED_CONTENT_TYPES = ['text', 'photo', 'voice', 'document', 'audio', 'video', 'video_note']
bot = telebot.TeleBot(token=API_TOKEN)

