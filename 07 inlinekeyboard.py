#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging
import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo,SwitchInlineQueryChosenChat, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def start_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Url with website", url = "www.youtube.com"),
            InlineKeyboardButton("Url with user information", url = "tg://user?id=1895194333"),
        ],

        [
            InlineKeyboardButton("With CallBack Data", callback_data= "Manik"),
            InlineKeyboardButton("Callback with int", callback_data= 123)
        ],


        [InlineKeyboardButton(text="Open the color picker! WEb App", web_app=WebAppInfo(url="https://python-telegram-bot.org/static/webappbot"),)],

        [InlineKeyboardButton(text="Open Youtube Application Web App", web_app=WebAppInfo(url="https://www.youtube.com"),)],

        
        [InlineKeyboardButton("Switch inline Query", switch_inline_query= "Hello")],
        [InlineKeyboardButton("Switch Inline Query CUrrent Chat", switch_inline_query_current_chat= "Manik Rana")],

        [InlineKeyboardButton("Only User Chosen Chat", switch_inline_query_chosen_chat = SwitchInlineQueryChosenChat("This is User", allow_user_chats=True))],
        [InlineKeyboardButton("Only Bot Chosen Chat", switch_inline_query_chosen_chat = SwitchInlineQueryChosenChat("This is Bot", allow_bot_chats=True))],
        [InlineKeyboardButton("Only Group Chosen Chat", switch_inline_query_chosen_chat = SwitchInlineQueryChosenChat("This is Group", allow_group_chats=True))],
        [InlineKeyboardButton("Only Channel Chosen Chat", switch_inline_query_chosen_chat = SwitchInlineQueryChosenChat("This is Channel", allow_channel_chats=True))],
        [InlineKeyboardButton("User & Bot Query Select", switch_inline_query_chosen_chat = SwitchInlineQueryChosenChat("This is Channel", allow_bot_chats=True, allow_user_chats=True))],


        [InlineKeyboardButton("Option Four", callback_data="four")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose Anything From Below:::", reply_markup=reply_markup)











async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Url with website", url="www.youtube.com"),
            InlineKeyboardButton("Url with user information", url="tg://user?id=1895194333"),
        ],

        [
            InlineKeyboardButton("With CallBack Data", callback_data="Manik"),
            InlineKeyboardButton("Callback with int", callback_data=123),
        ],

        [InlineKeyboardButton(text="Open the color picker! WEb App", web_app=WebAppInfo(url="https://python-telegram-bot.org/static/webappbot"))],

        [InlineKeyboardButton(text="Open Youtube Application Web App", web_app=WebAppInfo(url="https://www.youtube.com"))],

        [InlineKeyboardButton("Switch inline Query", switch_inline_query="Hello")],
        [InlineKeyboardButton("Switch Inline Query Current Chat", switch_inline_query_current_chat="Manik Rana")],

        [
            InlineKeyboardButton("Only User Chosen Chat 🧑", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("This is User", allow_user_chats=True)),
            InlineKeyboardButton("Only Bot Chosen Chat 🤖", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("This is Bot", allow_bot_chats=True)),
        ],

        [
            InlineKeyboardButton("Only Group Chosen Chat 👥", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("This is Group", allow_group_chats=True)),
            InlineKeyboardButton("Only Channel Chosen Chat 📢", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("This is Channel", allow_channel_chats=True)),
        ],

        [InlineKeyboardButton("User & Bot Query Select 🧑‍💻🤖", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("User & Bot", allow_bot_chats=True, allow_user_chats=True))],
        [InlineKeyboardButton("User & Channel Query Select 🧑‍💻📢", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("User & Channel", allow_user_chats=True, allow_channel_chats=True))],
        [InlineKeyboardButton("User & Group Query Select 🧑‍💻👥", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("User & Group", allow_user_chats=True, allow_group_chats=True))],
        [InlineKeyboardButton("Bot & Channel Query Select 🤖📢", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("Bot & Channel", allow_bot_chats=True, allow_channel_chats=True))],
        [InlineKeyboardButton("Bot & Group Query Select 🤖👥", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("Bot & Group", allow_bot_chats=True, allow_group_chats=True))],

        [InlineKeyboardButton("User, Bot & Channel Query Select 🧑‍💻🤖📢", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("User, Bot & Channel", allow_bot_chats=True, allow_user_chats=True, allow_channel_chats=True))],
        [InlineKeyboardButton("User, Bot & Group Query Select 🧑‍💻🤖👥", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("User, Bot & Group", allow_bot_chats=True, allow_user_chats=True, allow_group_chats=True))],
        [InlineKeyboardButton("User, Channel & Group Query Select 🧑‍💻📢👥", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("User, Channel & Group", allow_user_chats=True, allow_channel_chats=True, allow_group_chats=True))],
        [InlineKeyboardButton("Bot, Channel & Group Query Select 🤖📢👥", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("Bot, Channel & Group", allow_bot_chats=True, allow_channel_chats=True, allow_group_chats=True))],

        [InlineKeyboardButton("User, Bot, Channel & Group Query Select 🧑‍💻🤖📢👥", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("User, Bot, Channel & Group", allow_bot_chats=True, allow_user_chats=True, allow_channel_chats=True, allow_group_chats=True))],

        [InlineKeyboardButton("Group & Channel Query Select 👥📢", switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat("Group & Channel", allow_group_chats=True, allow_channel_chats=True))],

        [InlineKeyboardButton("Option Four", callback_data="four")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose Anything From Below:::", reply_markup=reply_markup)













async def button_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    # current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
    # await query.answer(text=f"Rana Universe\n🍌🍌🍌\nCurrent Time is\n {current_time}", show_alert=True)
    
    selected_option = query.data
    await query.edit_message_text(text=f"You have Just Selected option: {selected_option}")
    await query.delete_message(connect_timeout=3)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user = query.from_user
    full_name = user.full_name
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if query.data == "1":
        dynamic_text = f"Hello\nThanks\nRana Universe\n🍌🍌🍌\n'https://www.google.com'"
        await query.answer(text=dynamic_text, show_alert=True)
        user_id = update.callback_query.from_user.id
        await context.bot.send_message(user_id, text= f"You have selected the {query.data}")
    if query.data == "2":
        dynamic_text = f"Hello\nThanks\nRana Universe\n🍌🍌🍌\nyou select Option 2 Selected at\n {current_time}"
        await update.callback_query.answer(text=dynamic_text, show_alert=False,url="t.me/Rana3bot?start=XXXX")
    if query.data == "123":
        dynamic_text = f"Hello\nThanks\nRana Universe\n🍌🍌🍌\nyou select Option 3 Selected at\n {current_time}"
        await query.answer(text=dynamic_text)
    else:
        dynamic_text = "Unknown Option ❌❌❌"
        await query.answer(text=dynamic_text)



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6780033449:AAFKWBuWlPcBHLm303owSEvDriPZjCxs9ZU").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
