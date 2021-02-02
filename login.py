from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import (API_ID, API_HASH)

# авторизация и печать ключа сессии
with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print(client.session.save())

# тэкс ето у нас обработчик новых мессагов паехал

@client.on(events.NewMessage)
async def handler_new_message(event):
    try:
        # event.message содержит информацию о новом сообщении
        print(event.message)
    except Exception as e:
        print(e)
         # отправляем мессагу в таргетченнел
        await client.send_message(TARGET_CHANNEL, event.message)
        # либо вместо переотправки можно репостнуть:
        # захолдил: await client.forward_messages(TARGET_CHANNEL, event.message)

        if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()