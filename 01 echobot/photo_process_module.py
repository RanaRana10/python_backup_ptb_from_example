from telegram import Update
from telegram.ext import ContextTypes
from logger_setup import rana_logger, rico_logger
import pytesseract
from PIL import Image


async def extract_text_from_image(image_path) -> str:
    try:
        print("extract function is running")
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img)
        print(extracted_text)
        return str(extracted_text)
      
    except Exception as e:
        print("Error is good:", e)
        return None




async def photo_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await context.bot.send_message(user.id, f"Processing your photo... 🖼️")
    photo_file = await update.message.photo[-1].get_file()
    image_path = "user_photo.jpg"
    await photo_file.download_to_drive(image_path)
    extracted_text = await extract_text_from_image(image_path)    
    

    if extracted_text is not None:
        # if len(extracted_text) == 0:
        if extracted_text =="":
            user_text = extracted_text
            await context.bot.send_message(user.id, f"Your Text is 000 : {user_text}\n And its length is {len(user_text)}")
            await context.bot.send_message(user.id, f"Your response has been sent.")
        else:
            user_text = extracted_text
            await context.bot.send_message(user.id, f"Your Text is: {user_text}\n And its length is {len(user_text)}")
            await context.bot.send_message(user.id, f"Your response has been sent.")
    else:
        await context.bot.send_message(user.id, "There was an issue extracting the text from the image.")






























# async def photo_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user = update.message.from_user
#     await context.bot.send_message(user.id, f"Processing your photo... 🖼️")

#     photo_file = await update.message.photo[-1].get_file()
#     image_path = "user_photo.jpg"
    
#     await photo_file.download_to_drive(image_path)
    
#     extracted_text = await extract_text_from_image("hello")


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








# async def photo_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user = update.message.from_user
#     await context.bot.send_message(user.id, f"Processing your photo... 🖼️")
#     photo_file = await update.message.photo[-1].get_file()
#     image_path = "user_photo.jpg"
#     await photo_file.download_to_drive(image_path)
#     extracted_text = await extract_text_from_image(image_path)    
    

#     if extracted_text:
#         user_text = extracted_text
#         print(len(extracted_text))
#         await context.bot.send_message(user.id, f"Your Text is: {user_text}\n And its length is {len(user_text)}")
#         await context.bot.send_message(user.id, f"Your response has been send for if extracted text")

#     if len(extracted_text) == 0:
#         user_text = extracted_text
#         print(len(extracted_text))
#         await context.bot.send_message(user.id, f"Your Text is 000 : {user_text}\n And its length is {len(user_text)}")
#         await context.bot.send_message(user.id, f"Your response has been send len is 0")

#     if extracted_text==None:
#         user_text = extracted_text
#         print(len(extracted_text))
#         await context.bot.send_message(user.id, f"Your Text is: {user_text}\n And its length is {len(user_text)}")
#         await context.bot.send_message(user.id, f"Your response has been send when none")

        

# async def photo_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user = update.message.from_user
#     await context.bot.send_message(user.id, f"Processing your photo... 🖼️")
#     photo_file = await update.message.photo[-1].get_file()
#     image_path = "user_photo.jpg"
#     await photo_file.download_to_drive(image_path)
#     extracted_text = await extract_text_from_image(image_path)    
    

#     if extracted_text:
#         if len(extracted_text) > 0:
#             print(extracted_text)
#         else:
#             print("This is first else")
#             # len of text is 0
#     else:
#         print("This is second else")
#         # extracted text is None


# async def photo_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user = update.message.from_user
#     await context.bot.send_message(user.id, f"Processing your photo... 🖼️")
#     photo_file = await update.message.photo[-1].get_file()
#     image_path = "user_photo.jpg"
#     await photo_file.download_to_drive(image_path)
#     extracted_text = await extract_text_from_image(image_path)    
    
#     if extracted_text == "":
#         user_text = extracted_text
#         await context.bot.send_message(user.id, f"Your Text is 000 : {user_text}\n And its length is {len(user_text)}")
#         await context.bot.send_message(user.id, f"Your response has been sent.")
#     elif extracted_text is not None:
#         user_text = extracted_text
#         await context.bot.send_message(user.id, f"Your Text is: {user_text}\n And its length is {len(user_text)}")
#         await context.bot.send_message(user.id, f"Your response has been sent.")
#     else:
#         await context.bot.send_message(user.id, "There was an issue extracting the text from the image.")










