#developer: @thelisx
#repos: https://github.com/thelisx/hkmods

#============================================

from telethon import events
from .. import loader, utils
import asyncio

@loader.tds
class AutoClickerMod(loader.Module):
    """Модуль для автоматического нажатия на инлайн кнопки.\n  Dev:@thelisx"""
    strings = {'name': 'InlineAutoClicker'}
    async def clickoncmd(self, message):
        """Используйте .clickon <интервал в секундах> <позиция кнопки> для начала кликов.
        Позиция кнопки: '0' для первой кнопки, '1' для второй и т.д."""
        if not message.is_reply:
            await message.edit('<b>Нету реплая.</b>')
            return
        args = utils.get_args_raw(message).split()
        interval = int(args[0]) if args and args[0].isdigit() else 20
        button_index = int(args[1]) if len(args) > 1 and args[1].isdigit() else 0
        self.clicker = True
        await message.edit(f'<b>Кликер включен. Интервал: {interval} секунд. Позиция кнопки: {button_index}.</b>')
        while self.clicker:
            reply = await message.get_reply_message()
            if reply and reply.buttons:
                if len(reply.buttons) > 0 and len(reply.buttons[0]) > button_index:
                    button = reply.buttons[0][button_index]
                    await button.click()
                    await asyncio.sleep(interval)
                else:
                    await message.edit('<b>В сообщении нет инлайн кнопок с указанным индексом.</b>')
                    self.clicker = False
                    break
            else:
                await message.edit('<b>В сообщении нет инлайн кнопок для нажатия.</b>')
                self.clicker = False
                break
    async def clickoffcmd(self, message):
        """Используйте .clickoff для остановки кликера."""
        self.clicker = False
        await message.edit('<b>Кликер выключен.</b>')
    async def client_ready(self, client, db):
        self.db = db

        
