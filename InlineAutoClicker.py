
#developer: @thelisx

#============================================

from telethon import events
from .. import loader, utils
import asyncio

@loader.tds
class AutoClickerMod(loader.Module):
    """Модуль для автоматического нажатия на инлайн кнопки.(v1.2)\n  Dev:@thelisx"""
    strings = {'name': 'InlineAutoClicker'}

    async def get_button_by_index(self, reply, button_index):
        flat_buttons = [button for row in reply.buttons for button in row]
        if button_index < len(flat_buttons):
            return flat_buttons[button_index]
        return None

    async def sclickcmd(self, message):
        """Используйте .sclick <интервал в секундах> <позиция кнопки> для начала кликов.
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
                button = await self.get_button_by_index(reply, button_index)
                if button:
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

    async def rclickcmd(self, message):
        """Используйте .rclick <задержка в секундах> <позиция кнопки> <количество кликов> для многократного нажатия."""
        if not message.is_reply:
            await message.edit('<b>Нету реплая.</b>')
            return
        args = utils.get_args_raw(message).split()
        interval = int(args[0]) if args and args[0].isdigit() else 20
        button_index = int(args[1]) if len(args) > 1 and args[1].isdigit() else 0
        click_count = int(args[2]) if len(args) > 2 and args[2].isdigit() else 1
        await message.edit(f'<b>Многократный клик активирован. Задержка: {interval} секунд. Позиция кнопки: {button_index}. Количество кликов: {click_count}.</b>')
        
        reply = await message.get_reply_message()
        if reply and reply.buttons:
            button = await self.get_button_by_index(reply, button_index)
            if button:
                for _ in range(click_count):
                    await button.click()
                    await asyncio.sleep(interval)
            else:
                await message.edit('<b>В сообщении нет кнопки с таким индексом.</b>')
        else:
            await message.edit('<b>В сообщении нет инлайн кнопок для нажатия.</b>')

    async def oclickcmd(self, message):
        """Используйте .oclick для остановки кликера."""
        self.clicker = False
        await message.edit('<b>Кликер выключен.</b>')

    async def client_ready(self, client, db):
        self.db = db
