# Infinity BOTs <https://t.me/Infinity_BOTs>
# @ImJanindu

import os
import time
import logging
from config import Config
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

Jebot = Client(
   "ForceSub Bot",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

# get mute request
static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")

@Jebot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, lel):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_u = Config.CHANNEL_USERNAME #channel for force sub
  if chat_u:
    channel = chat_u
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if lel.message.reply_to_message.from_user.id == user_id:
              lel.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(lel.id, text="❗ Join the mentioned 'channel' and press the 'UnMute Me' button again.", show_alert=True)
      else:
        client.answer_callback_query(lel.id, text="❗ You are muted by admins for other reasons.", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{lel.from_user.mention} is trying to Unmute himself but I can't unmute him because I am not an admin in this chat add me as admin again.**\n__I'm leaving__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(lel.id, text="❗ Warning: Don't click the button if you can speak freely.", show_alert=True)



@Jebot.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_u = Config.CHANNEL_USERNAME #channel for force sub
  if chat_u:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_u
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              "{}, you are **not subscribed** to our [channel](https://t.me/{}) yet. Please [join](https://t.me/{}) and **press the button below** to unmute yourself.".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("Unmute Me", callback_data="onUnMuteRequest")]]
              )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **I am not an admin here.**\n__Make me admin with ban user permission__")
          
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **I am not an admin in {channel}**\n__Make me admin in the channel__")
