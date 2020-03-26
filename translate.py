import logging

from Yandex import Translate

from .. import loader, utils

logger = logging.getLogger(__name__)

def register(cb):

    cb(TranslateMod())

class TranslateMod(loader.Module):

    """Translator"""

    def __init__(self):

        self.commands = {"translate": self.translatecmd}

        self.config = loader.ModuleConfig("DEFAULT_LANG", "ru", "Language to translate to by default",

                                          "API_KEY", "trnsl.1.1.20200325T233511Z.1c94fd010d92bf3e.969452b20ecfa2e3e393703c97ca83f43bf34bd8", "API key from https://translate.yandex.com/developers/keys")

        self.name = _("Translator")

    def config_complete(self):

        self.tr = Translate(self.config["API_KEY"])

    async def translatecmd(self, message):

        """.translate [from_lang->][->to_lang] <text>"""

        args = utils.get_args(message)

        if len(args) == 0 or "->" not in args[0]:

            text = " ".join(args)

            args = ["", self.config["DEFAULT_LANG"]]

        else:

            text = " ".join(args[1:])

            args = args[0].split("->")

        if len(text) == 0 and message.is_reply:

            text = (await message.get_reply_message()).message

        if len(text) == 0:

            await message.edit(_("Invalid text to translate"))

            return

        if args[0] == "":

            args[0] = self.tr.detect(text)

        if len(args) == 3:

            del args[1]

        if len(args) == 1:

            logging.error("python split() error, if there is -> in the text, it must split!")

            raise RuntimeError()

        if args[1] == "":

            args[1] = self.config["DEFAULT_LANG"]

        args[0] = args[0].lower()

        logger.debug(args)

        translated = self.tr.translate(text, args[1], args[0])

        ret = _("<b>[ <code>{frlang}</code> - </b>"

                + "<b><code>{to}</code> ]</b>\n<code>{output}</code>")

        ret = ret.format(text=utils.escape_html(text), frlang=utils.escape_html(args[0]),

                         to=utils.escape_html(args[1]), output=utils.escape_html(translated))

        await utils.answer(message, ret)
