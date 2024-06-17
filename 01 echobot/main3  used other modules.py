import sys
sys.dont_write_bytecode = True


import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from other_module import start, help_command, echo
from photo_process_module import photo_process

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# def extract_text_from_image(image_path) -> str:
#     try:
#         img = Image.open(image_path)
#         extracted_text = pytesseract.image_to_string(img)
#         print(extracted_text)
#         return str(extracted_text)

#     except Exception as e:
#         print("Error:", e)
#         return None


# async def photo_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user = update.message.from_user
#     await context.bot.send_message(user.id, f"Processing your photo... 🖼️")
    
#     photo_file = await update.message.photo[-1].get_file()
#     image_path = "user_photo.jpg"
    
#     await photo_file.download_to_drive(image_path)
    
#     extracted_text = await extract_text_from_image(image_path)
    
#     if extracted_text:
#         await context.bot.send_message(update.message.chat_id, extracted_text)
#     else:
#         await context.bot.send_message(update.message.chat_id, "Sorry, I couldn't extract text from your photo. 🤖😕")




# async def extract_text_from_image(image_path) -> str:
#     try:
#         print("extract function is running")
#         img = Image.open(image_path)
#         extracted_text = pytesseract.image_to_string(img)
#         print(extracted_text)
#         return str(extracted_text)
      
#     except Exception as e:
#         print("Error is good:", e)
#         return None


# async def photo_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user = update.message.from_user
#     await context.bot.send_message(user.id, f"Processing your photo... 🖼️")

#     photo_file = await update.message.photo[-1].get_file()
#     image_path = "user_photo.jpg"
    
#     await photo_file.download_to_drive(image_path)
    
#     extracted_text = await extract_text_from_image(image_path)


#     if extracted_text is None:
#         await context.bot.send_message(user.id, "A error occurs during this")


#     elif len(extracted_text) == 0:
#         await context.bot.send_message(update.message.chat_id, "TThis contains no text")
#         print("0 len text has came")

#     elif extracted_text:
#         print(len(extracted_text))
#         await context.bot.send_message(update.message.chat_id, extracted_text)

#     else:
#         print("Below extract text")
#         print (extracted_text)
#         print("upper")
#         await context.bot.send_message(update.message.chat_id, "Sorry, I couldn't extract text from your photo. 🤖😕")








def main() -> None:
    """Start the bot."""
    application = Application.builder().token("6780033449:AAFKWBuWlPcBHLm303owSEvDriPZjCxs9ZU").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.PHOTO, photo_process, block=False))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()