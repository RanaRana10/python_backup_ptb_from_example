import sys
sys.dont_write_bytecode = True


from telegram import Update
from telegram.ext import Application, CommandHandler,MessageHandler, ContextTypes, filters
from basic_logging import logger
import datetime
import random

from database_2_stickers import add_sticker_and_return_id, get_sticker_by_id
from database_3_photo import add_photo_and_return_id, get_photo_by_id, update_photo_user_id


STICKER_GIRL_BACK = "CAACAgIAAxkBAAJaWGYDk3cIuubF_oSry3EC7Xh5A0nvAAJKBwACRvusBCNCmw1f3sTgNAQ"
STICKER_SLAP = "CAACAgEAAxkBAAJaWWYDk3nUNqt0nK6m5B-_xo42t8u_AAKJAwACdOcrAmY71QU0ZSv6NAQ"



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /set <seconds> to set a timer")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")

async def alarm_with_update_need(context: ContextTypes.DEFAULT_TYPE):
    
    job = context.job
    update:Update = job.data
    

    user = update.message.from_user
    full_name = user.full_name
    user_id = user.id
    user_name = user.name
    chat_id = update.message.chat.id
    text_to_send = f"{job.name} Hello {job.chat_id} Next time: {(job.next_t + datetime.timedelta(hours= 5, minutes= 30)).strftime("%Y-%m-%d %H-%M-%S")} \n{job.user_id}This msg is coming to you after the which you passed in the cmd,\nAs Per as we check your details is: Full Name is: {user.full_name}, @Username is: {user.username}, You MSG US from the chat which is {update.message.chat.title}"
    print(type(job.chat_id))



    await context.bot.send_message(chat_id, text_to_send)


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        # job_removed = remove_job_if_exists(str(chat_id), context)
        # context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)
        context.job_queue.run_once(alarm_with_update_need, due -1 , name= str(update.message.from_user.id), chat_id= str(due) + "Noob🍌🍌🍌",  data= update)

        # context.job_queue.run_repeating(alarm_with_update_need, 1, name=str(update.message.from_user.id), chat_id= str(2), data= update)
        context.job_queue.run_repeating(send_sticker_job, 3, data = update)

        text = "Timer successfully set!"
        # if job_removed:
        #     text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)


async def send_sticker_job(context: ContextTypes.DEFAULT_TYPE):
    print("starting🍌🍌🍌")
    job = context.job
    update: Update = job.data
    user = update.message.from_user
    chat = update.message.chat
    # await context.bot.send_sticker(chat.id, STICKER_GIRL_BACK)
    # await context.bot.send_sticker(chat.id, STICKER_SLAP)
    await context.bot.send_sticker(chat.id, random.choice([STICKER_GIRL_BACK, STICKER_SLAP]))

    ...


async def sticker_processing_fun(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    chat = update.message.chat

    unique_id = update.message.sticker.file_unique_id
    file_id = update.message.sticker.file_id
    sticker_set_name = update.message.sticker.set_name
    text = f"You Have Send a Sticker with Set Name: <code>{sticker_set_name}</code>\nUnique id: {unique_id} file id to send the sticker back is: <code>{file_id}</code>"
    await context.bot.send_message(chat.id, text=text, parse_mode= "html")

    insert_information = add_sticker_and_return_id(file_unique_id_=unique_id, file_id_= file_id,set_name_=sticker_set_name,user_id_=user.id, user_name_= user.name, time_of_saved_= update.message.date)

    if insert_information is not None:
        id_ = insert_information
        text = f"Your Sticker has been inserted with the details:\nID IS: {id_}\nTo Get Your sticker send <code>/get Number</code>"

    else:
        text = f"Your Sticker has not inserted"

    await context.bot.send_message(chat.id, text, parse_mode="html")



async def get_sticker_information_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat = update.message.chat

    try:
        required_id = int(context.args[0])
    except Exception as e:
        await context.bot.send_message(chat.id, "Please provide a valid sticker ID.\nExample: /get 3\n\n{e}")
        return
    
    sticker_information = get_sticker_by_id(required_id)

    if sticker_information:
        await context.bot.send_sticker(chat.id, sticker_information['file_id_'])

    else:
        await context.bot.send_message(chat.id, "No sticker found, send me a sticker i will send you back the id to use later")


async def get_sticker_information(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat = update.message.chat

    try:
        required_id = int(context.args[0])
        if required_id > 1_00_00_000:
            await context.bot.send_message(chat.id, "Please provide a valid sticker ID within 1 crore (10 million).")
            return
    except Exception as e:
        await context.bot.send_message(chat.id, f"Please provide a valid sticker ID.\nExample: /get 3\n\n{e}")
        return
    
    sticker_information = get_sticker_by_id(required_id)

    if sticker_information:
        if user.id == sticker_information["user_id_"]:
            await context.bot.send_sticker(chat.id, sticker_information['file_id_'])
        else:
            await context.bot.send_message(chat.id, "Sorry, you are not the owner of this sticker.")
    else:
        await context.bot.send_message(chat.id, "No sticker found with the provided ID.")


async def photo_processing_fun(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    chat = update.message.chat
    last_photo = update.message.photo[-1]
    unique_id = last_photo.file_unique_id
    file_id = last_photo.file_id
    file_size = last_photo.file_size

    text = f"You have send the Photo with its size is: {file_size} KB\nFile ID: {last_photo.file_id}\nFile Unique ID: {last_photo.file_unique_id}"
    # await context.bot.send_message(user.id, text, parse_mode= "html")
    insert_information = add_photo_and_return_id(unique_id, file_id, file_size, user.id, user.name, update.message.date)

    # if insert_information is not None:
    #     id_ = insert_information
    #     text = f"Your Images Has Been saved to {id_} to get the photo back send <code>/pho 1</code>"
    #     await context.bot.send_message(user.id, text=text, parse_mode= "html")
    
    # else: 
    #     text = "Photo has not inserted"
    #     await context.bot.send_message(user.id,text)



async def get_photo_information(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat = update.message.chat

    try:
        required_id = int(context.args[0])
        if required_id > 1_00_00_000:
            await context.bot.send_message(chat.id, "Please provide a valid photo ID within 1 crore (10 million).")
            return
    except Exception as e:
        await context.bot.send_message(chat.id, f"Please provide a valid photo ID.\nExample: /getphoto 3\n\n{e}")
        return
    
    photo_information = get_photo_by_id(required_id)

    if photo_information:
        if user.id == photo_information["user_id_"]:
            await context.bot.sendPhoto(chat.id, photo_information["file_id_"])
        else:
            await context.bot.send_message(chat.id, "Sorry, you are not the owner of this photo.")
    else:
        await context.bot.send_message(chat.id, "No photo found with the provided ID.")


async def update_db_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    old_id = context.args[0]
    new_id = context.args[1]

    values_of_updated_id_ = update_photo_user_id(old_id, new_id)
    text = f"Database Has Been Updated{values_of_updated_id_}"
    await context.bot.send_message(user.id, text)


    ...

















def main() -> None:
    """Run bot."""
    application = Application.builder().token("6780033449:AAFKWBuWlPcBHLm303owSEvDriPZjCxs9ZU").build()

    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    application.add_handler(CommandHandler("get", get_sticker_information))
    application.add_handler(CommandHandler("pho", get_photo_information))
    application.add_handler(CommandHandler("db", update_db_user_id))

    application.add_handler(MessageHandler(filters.Sticker.ALL, sticker_processing_fun))
    application.add_handler(MessageHandler(filters.PHOTO, photo_processing_fun))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":

    logger.info("Starting the bot...")
    main()