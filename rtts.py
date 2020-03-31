# Russian tts for Friendly-telegram and Uniborg: .rtts
# By @Demenkop, based on Qoutly module for BotHub
# Test-build ID: 8

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from uniborg.util import admin_cmd

@borg.on(admin_cmd(pattern="rtts ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
        user_msg = """{}""".format(event.pattern_match.group(1))
        self_mess = True
        if not user_msg:
            await event.edit("Вы должны или написать шото, или ответить на шото")
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        self_mess = False
        sender = reply_message.sender
        if not reply_message.text:
            await event.edit("```Ты на текст должен ответить, диб*ил```")
            return
    chat = "@aleksobot"
    await event.edit("```Происходит магия Деменкопа```")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=616484527))
              if not self_mess:
                  await event.client.forward_messages(chat, reply_message)
              else: 
                  await event.client.send_message(chat, user_msg)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Разблокируй @aleksobot, ибо магия не произойдёт```")
              return
          if response.text.startswith("Hi!"):
             await event.edit("```А сейчас я не могу переслать. Разрешишь, сука ты?```")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)
