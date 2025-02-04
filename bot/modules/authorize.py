from bot.helper.telegram_helper.message_utils import sendMessage
from telegram.ext import run_async
from bot import AUTHORIZED_CHATS, dispatcher
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from telegram.ext import Filters
from telegram import Update
from bot.helper.telegram_helper.bot_commands import BotCommands
# from bot import redis_client, redis_authorised_chats_key

@run_async
def authorize(update,context):
    reply_message = update.message.reply_to_message
    msg = ''
    if reply_message is None:
        # Trying to authorize a chat
        chat_id = update.effective_chat.id
        if chat_id not in AUTHORIZED_CHATS:
            # redis_client.sadd(redis_authorised_chats_key, chat_id)
            AUTHORIZED_CHATS.add(chat_id)
            msg = 'Chat authorized'
        else:
            msg = 'Already authorized chat'
    else:
        # Trying to authorize someone in specific
        user_id = reply_message.from_user.id
        if user_id not in AUTHORIZED_CHATS:
            # redis_client.sadd(redis_authorised_chats_key, user_id)
            AUTHORIZED_CHATS.add(user_id)
            msg = 'Person Authorized to use the bot!'
        else:
            msg = 'Person already authorized'
    sendMessage(msg, context.bot, update)


@run_async
def unauthorize(update,context):
    reply_message = update.message.reply_to_message
    if reply_message is None:
        # Trying to unauthorize a chat
        chat_id = update.effective_chat.id
        if chat_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(chat_id)
            # redis_client.srem(redis_authorised_chats_key, chat_id)
            msg = 'Chat unauthorized'
        else:
            msg = 'Already unauthorized chat'
    else:
        # Trying to authorize someone in specific
        user_id = reply_message.from_user.id
        if user_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(user_id)
            # redis_client.srem(redis_authorised_chats_key, user_id)
            msg = 'Person unauthorized to use the bot!'
        else:
            msg = 'Person already unauthorized!'
        
    sendMessage(msg, context.bot, update)


authorize_handler = CommandHandler(command=BotCommands.AuthorizeCommand, callback=authorize,
                                   filters=CustomFilters.owner_filter & Filters.group)
unauthorize_handler = CommandHandler(command=BotCommands.UnAuthorizeCommand, callback=unauthorize,
                                     filters=CustomFilters.owner_filter & Filters.group)
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(unauthorize_handler)

