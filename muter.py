


from .. import loader, utils
from telethon import events
import json
import os

@loader.tds
class muteus(loader.Module):
    """Модуль для мута пользователей в ЛС"""
    strings = {'name': 'muteus'}
    
    __version__ = (1,2,0)

    def __init__(self):
        self.config_file = "muted_users.json"
        self.muted_users = set()
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.muted_users = set(json.load(f))

    async def client_ready(self, client, db):
        self._client = client
        self._db = db

    async def mutecmd(self, message):
        """Замьютить пользователя. Используйте .mute в ответ на сообщение."""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, "❌ <b>Ответьте на сообщение пользователя, которого хотите замьютить.</b> ❌")
            return
        my_user_id = message.sender_id  
        if reply.sender_id == my_user_id:
            await utils.answer(message, "❌ <b>Вы не можете замьютить сами себя.</b> ❌")
            return
        if reply.sender_id in self.muted_users:
            await utils.answer(message, "⚠️ <b>Пользователь уже замьючен.</b> ⚠️")
            return
        self.muted_users.add(reply.sender_id)
        with open(self.config_file, 'w') as f:
            json.dump(list(self.muted_users), f)
        await utils.answer(message, "✅ <b>Пользователь замьючен.</b> ✅")


    async def unmutecmd(self, message):
        """Размьютить пользователя. Используйте .unmute на сообщение от пользователя."""
        reply = await message.get_reply_message()
        if reply:
            if reply.sender_id not in self.muted_users:
                await utils.answer(message, f"❌ <b>Пользователь не находится в муте.</b> ❌")
                return
            self.muted_users.remove(reply.sender_id)
            with open(self.config_file, 'w') as f:
                json.dump(list(self.muted_users), f)
            await utils.answer(message, f"✅ <b>Пользователь размьючен.</b> ✅")

    @loader.unrestricted
    @loader.ratelimit
    async def watcher(self, event):
        if event.sender_id in self.muted_users:
            await event.delete()
