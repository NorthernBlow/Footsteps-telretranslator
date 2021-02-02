from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import (API_ID, API_HASH, SESSION_STRING)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

import database

from config import (API_HASH, API_ID, SOURCE_CHANNEL, SESSION_STRING,
                      TARGET_CHANNEL)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Обработчик новых сообщений
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler_new_message(event):
    try:
# Отправим пришедшее нам сообщение и сохраним его ид в базе
        mirror_message_id = await client.send_message(TARGET_CHANNEL, event.message)
        database.insert({
            'message_id': event.message.id,
            'mirror_message_id': mirror_message_id
        })
    except Exception as e:
        print(e)
# Обработчик отредактированных сообщений
@client.on(events.MessageEdited(chats=SOURCE_CHANNEL))
async def handler_edit_message(event):
    try:
# попытаемся найти в базе данных сообщение-клон
        message_to_edit = database.find_by_id(event.message.id)
        if message_to_edit is None:
            return
# если такое нашлось -- отредактируем его
        id_message_to_edit = message_to_edit['mirror_message_id']
        await client.edit_message(TARGET_CHANNEL, id_message_to_edit, event.message.message)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()