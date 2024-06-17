"""
This is just for a conversation with others monog, and so on
Import Statement in other main module is:


from conversation_1 import start, gender, photo, skip_photo, location, skip_location, bio, cancel, conv_handler
"""

import logging, cv2, io, random, json, pymongo,os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ChatAction

from basic_logging import setup_logger
from conversation_1 import start, gender, photo, skip_photo, location, skip_location, bio, cancel, conv_handler
from commands_1 import help_command, echo, random_text, send_file, send_random_photo

logger = setup_logger()



async def download_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Download The Photo Directly"""
    user = update.message.from_user
    chat = update.message.chat
    await context.bot.send_chat_action(chat.id, action=ChatAction.TYPING)
    photo_file = await update.message.photo[-1].get_file()

    download_location = os.path.join("files","images","Download")
    print(download_location)

    await photo_file.download_to_drive(download_location)
    await update.message.reply_text(f"Photo has Been Dowload")



async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    await context.bot.sendPhoto(chat_id=user_id, photo='a.jpg')





def main() -> None:
    """Run the bot."""
    application = Application.builder().token("6780033449:AAFKWBuWlPcBHLm303owSEvDriPZjCxs9ZU").build()

    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("help", help_command, block=False))  #This is fsrom commands_1.py
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  #This is fsrom commands_1.py
    application.add_handler(MessageHandler(filters.PHOTO,download_photo,block=False))
    # application.add_handler(MessageHandler(filters.PHOTO,photo_handler,block=False))
    # application.add_handler(CommandHandler("a",send_photo))
    application.add_handler(CommandHandler(["a","about"],send_random_photo,block=False))  #This is fsrom commands_1.py
    application.add_handler(CommandHandler("b",send_file,block=False))  #This is fsrom commands_1.py
    application.add_handler(CommandHandler("c",random_text,block=False))  #This is fsrom commands_1.py



    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
