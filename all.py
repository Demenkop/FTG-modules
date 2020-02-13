# .all

from telethon import events


@borg.on(events.NewMessage(pattern=r"\.all", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    mentions = "@all"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, 10000):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await borg.send_message(
        chat, mentions, reply_to=event.message.reply_to_msg_id)
