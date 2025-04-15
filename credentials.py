import telebot
from telebot import apihelper
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
DEBUG = False

if DEBUG:
    API_TOKEN = '7478300229:AAE564apvxMdwm0kJF13M3chNpt7FsMewwY'
    RECEIVER_CHAT_ID = 865222212
else:
    API_TOKEN = '7478300229:AAE564apvxMdwm0kJF13M3chNpt7FsMewwY'
    RECEIVER_CHAT_ID = -1002570792329


ALLOWED_CONTENT_TYPES = ['text', 'photo', 'voice', 'document', 'audio', 'video', 'video_note']

session = requests.Session()
session.verify = False
apihelper.session = session

bot = telebot.TeleBot(token=API_TOKEN)


