from telethon import *
from chat_config import *

def read_key(files: str) -> dict:
    keys = {}
    file = open(files, 'r')
    for i in file:
        key, value = i.split('= ')
        keys.setdefault(key, value[:-1:])
    return keys

def authorization() -> TelegramClient:
    keys = read_key('api_key')
    api_id = keys['App_api_id']
    api_hash = keys['App_api_hash']
    return TelegramClient('Alex', api_id, api_hash)


async def loop():
    await chat_update(client)

client = authorization()

@client.on(events.NewMessage())
async def normal_handler(event):
    await new_message_event(event, client)

if __name__ == '__main__':

    with client:
        client.loop.run_until_complete(loop())
        client.run_until_disconnected()
