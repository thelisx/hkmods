from .. import loader, utils
import requests
import json
__version__ = "v1"
@loader.tds
class LinkShortener(loader.Module):
    """Модуль для сокращения ссылок через TinyURL
    dev:@thelisx"""
    strings = {"name": "LinkShortener"}

    async def slinkcmd(self, message):
        """.slink <ссылка, которую нужно сократить>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Необходимо указать ссылку для сокращения.")
            return

        url = 'http://tinyurl.com/api-create.php?url=' + args
        response = requests.get(url)
        if response.status_code == 200:
            short_url = response.text
            await utils.answer(message, f"🔗 Сокращённая ссылка: {short_url}")
        else:
            await utils.answer(message, "Ошибка при сокращении ссылки. Попробуйте позже.")
