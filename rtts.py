# Russian tts for Friendly-telegram and Uniborg: .qbot
# By @Demenkop, based on Qoutly module for BotHub

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
       await event.edit("```Reply to any user message.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit("```Reply to text message```")
       return
    chat = "@aleksobot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
    await event.edit("```Происходит магия Деменкопа```")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=616484527))
              await event.client.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await event.reply("```Разблокируй @aleksobot, ибо магия не произойдёт```")
              return
          if response.text.startswith("Hi!"):
             await event.edit("```А сейчас я не могу переслать. Разрешишь, сука ты?```")
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)
