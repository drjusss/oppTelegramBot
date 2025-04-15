import telebot
import threading

import decorators
from credentials import bot, RECEIVER_CHAT_ID
from telebot.types import InputMediaDocument, InputMediaAudio, InputMediaPhoto, InputMediaVideo


user_messages = dict()
user_timers = dict()
CAPTION_LIMIT = 1000
DOCUMENT_LIMIT = 10


def start_task(delay: int, username: str) -> None:
    def timer_function() -> None:
        check_timeout_and_send_notification(username=username)

    last_timer = user_timers.get(username)
    if last_timer is not None:
        last_timer.cancel()

    timer = threading.Timer(interval=delay, function=timer_function)
    timer.start()
    user_timers[username] = timer


@decorators.log_error   # логируем, потому что функция запускается в отдельном потоке
def check_timeout_and_send_notification(username: str) -> None:
    messages = user_messages.get(username, list())
    if len(messages) < 1:
        return

    chat_id = messages[0].chat.id
    structured_messages = create_messages_packs(messages=messages)

    send_photo_and_video_packs(photo_video_packs=structured_messages['photo+video'])
    send_audio_packs(audio_packs=structured_messages['audio'])
    send_document_packs(document_packs=structured_messages['documents'])
    send_text_messages(text_messages=structured_messages['text'])
    send_video_note_messages(video_note_messages=structured_messages['video_note'])
    send_voice_messages(voice_messages=structured_messages['voice'])
    user_messages[username] = list()
    bot.send_message(chat_id=chat_id, text='Спасибо за обращение! Инженер свяжется с вами в ближайшее время.')


def send_photo_and_video_packs(photo_video_packs: list[list[telebot.types.Message]]) -> None:
    for photo_video_pack in photo_video_packs:
        if len(photo_video_pack) == 1:
            if not photo_video_pack[0].caption:
                photo_video_pack[0].caption = ''
            if photo_video_pack[0].content_type == 'photo':
                photo_caption = f'Новое фото от [@{photo_video_pack[0].from_user.username}]: {photo_video_pack[0].caption}'
                bot.send_photo(chat_id=RECEIVER_CHAT_ID, photo=photo_video_pack[0].photo[-1].file_id, caption=photo_caption)
            else:
                video_caption = f'Новое видео от [@{photo_video_pack[0].from_user.username}]{photo_video_pack[0].caption}'
                bot.send_video(chat_id=RECEIVER_CHAT_ID, video=photo_video_pack[0].video.file_id, caption=video_caption)
        else:
            photo_video_pack_caption = list()
            photo_video_input_media = list()

            for element in photo_video_pack:
                if element.content_type == 'photo':
                    photo_video_input_media.append(InputMediaPhoto(element.photo[-1].file_id))
                    photo_video_pack_caption.append(element.caption)
                else:
                    photo_video_input_media.append(InputMediaVideo(element.video.file_id))
                    photo_video_pack_caption.append(element.caption)

            photo_video_input_media[-1].caption = '\n\n'.join(photo_video_pack_caption)
            photo_video_input_media[0].caption = f'Новый пакет фото/видео от [@{photo_video_pack[0].from_user.username}]' + photo_video_input_media[0].caption
            bot.send_media_group(chat_id=RECEIVER_CHAT_ID, media=photo_video_input_media)


def send_audio_packs(audio_packs: list[list[telebot.types.Message]]) -> None:
    for audio_pack in audio_packs:
        if len(audio_pack) == 1:
            if not audio_pack[0].caption:
                audio_pack[0].caption = ''
            audio_caption = f'Новый аудио-файл от [@{audio_pack[0].from_user.username}]: {audio_pack[0].caption}'
            bot.send_audio(chat_id=RECEIVER_CHAT_ID, audio=audio_pack[0].audio.file_id, caption=audio_caption)
        else:
            audio_input_media = list()
            audio_pack_caption = list()

            for element in audio_pack:
                audio_input_media.append(InputMediaAudio(media=element.audio.file_id, caption=element.caption))
                audio_pack_caption.append(element.caption)
            audio_input_media[0].caption = f'Новые аудиофайлы от [@{audio_pack[0].from_user.username}]' + audio_input_media[0].caption
            bot.send_media_group(chat_id=RECEIVER_CHAT_ID, media=audio_input_media)


def send_document_packs(document_packs: list[list[telebot.types.Message]]) -> None:
    for document_pack in document_packs:
        if len(document_pack) == 1:
            if not document_pack[0].caption:
                document_pack[0].caption = ''
            document_caption = f'Новый документ от [@{document_pack[0].from_user.username}]: {document_pack[0].caption}'
            bot.send_document(chat_id=RECEIVER_CHAT_ID, document=document_pack[0].document.file_id, caption=document_caption)
        else:
            document_input_media = list()
            document_pack_caption = list()

            for element in document_pack:
                document_input_media.append(InputMediaDocument(media=element.document.file_id, caption=element.caption))
                document_pack_caption.append(element.caption)
            document_input_media[0].caption = f'Новый пакет документов от [@{document_pack[0].from_user.username}]' + document_input_media[0].caption
            bot.send_media_group(chat_id=RECEIVER_CHAT_ID, media=document_input_media)


def send_text_messages(text_messages: list[telebot.types.Message]) -> None:
    user_text = str()
    for message in text_messages:
        if len(user_text + message.text) > 4096:
            bot.send_message(chat_id=RECEIVER_CHAT_ID, text=user_text)
            user_text = message.text
        else:
            user_text += '\n\n' + message.text

    if len(user_text) > 0:
        bot.send_message(chat_id=RECEIVER_CHAT_ID, text=f'Сообщение от [@{message.from_user.username}]: {user_text}')


def send_video_note_messages(video_note_messages: list[telebot.types.Message]) -> None:
    if video_note_messages:
        sender = video_note_messages[0].from_user.username
        for video_note in video_note_messages:
            bot.send_message(chat_id=RECEIVER_CHAT_ID, text=f'Новое видеосообщение от [@{sender}]')
            bot.send_video_note(chat_id=RECEIVER_CHAT_ID, data=video_note.video_note.file_id)


def send_voice_messages(voice_messages: list[telebot.types.Message]) -> None:
    for voice_message in voice_messages:
        if not voice_message.caption:
            voice_message.caption = ''
        voice_caption = f'Голосовое сообщение от [@{voice_message.from_user.username}]: {voice_message.caption}'
        bot.send_voice(chat_id=RECEIVER_CHAT_ID, voice=voice_message.voice.file_id, caption=voice_caption)


def create_messages_packs(messages: list[telebot.types.Message]) -> dict:
    structured_message = {
        'photo+video': list(),
        'audio': list(),
        'documents': list(),
        'text': list(),
        'video_note': list(),
        'voice': list()
    }

    document_pack = list()

    photo_video_pack = list()
    photo_video_pack_caption = str()

    audio_pack = list()

    for message in messages:
        message_content_type = message.content_type

        if message_content_type == 'document':
            if len(document_pack) < DOCUMENT_LIMIT:
                document_pack.append(message)
            else:
                structured_message['documents'].append(document_pack)
                document_pack = [message]
            continue

        if message_content_type == 'photo' or message_content_type == 'video':
            if not message.caption:
                message.caption = ''
            if len(photo_video_pack_caption + message.caption) <= CAPTION_LIMIT and len(photo_video_pack) < DOCUMENT_LIMIT:
                photo_video_pack.append(message)
                photo_video_pack_caption += message.caption + '\n\n'
            else:
                structured_message['photo+video'].append(photo_video_pack)
                photo_video_pack = [message]
                photo_video_pack_caption = message.caption
            continue

        if message_content_type == 'audio':
            if len(audio_pack) < DOCUMENT_LIMIT:
                audio_pack.append(message)
            else:
                structured_message['audio'].append(audio_pack)
                audio_pack = [message]
            continue

        structured_message[message_content_type].append(message)

    if len(document_pack) != 0:
        structured_message['documents'].append(document_pack)
    if len(photo_video_pack) != 0:
        structured_message['photo+video'].append(photo_video_pack)
    if len(audio_pack) != 0:
        structured_message['audio'].append(audio_pack)

    return structured_message



