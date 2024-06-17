import logging,json,re,datetime, asyncio
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters,PrefixHandler

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

sticker_id = "CAACAgUAAxkBAAIfFmW6Tgwaw0I4rn5iLOkBvxwUHZlbAAKIBwACpEL5Vo28mVygOhn-NAQ"

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat = update.effective_chat
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    await context.bot.send_message(chat.id,f"Your Latitude is:\n<code>{latitude}</code>", parse_mode="html")
    await context.bot.send_message(chat.id,f"Your Longitude is:\n<code>{longitude}</code>", parse_mode="html")
    print("Manik")



async def start_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_message.from_user
    user = update.effective_user 
    chat = update.effective_message.chat
    await context.bot.send_message(chat.id,f"This is Start Function" )

async def start_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_message.from_user
    user = update.effective_user 
    chat = update.effective_message.chat
    await context.bot.send_message(chat.id,f"You have Send /start 2" )

async def start_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_message.from_user
    user = update.effective_user 
    chat = update.effective_message.chat
    await context.bot.send_message(chat.id,f"You have Send /start 3" )

async def prefix_fun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_message.chat
    await context.bot.send_message(chat.id,f"You have Send a Prefix Handler" )






async def animation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    chat = update.effective_chat
    await context.bot.send_message(chat.id,f"This is a <code>Animation</code> File", parse_mode="html")
    await context.bot.send_message()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Direct Help Command")

async def help_command1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Direct Help Command 1   ")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.effective_message.reply_text(update.effective_message.text.upper())
    await update.effective_message.reply_text(f"{update}")

async def all_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.effective_message.reply_text(f"This is Filters.ALL")
    await update.effective_message.reply_text(f"{update}")




async def sticker_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    user = update.effective_user
    sticker = update.effective_message.sticker
    abcd = sticker.file_id
    print(abcd)

    await context.bot.send_sticker(chat_id=update.effective_chat.id,sticker=abcd)
    await update.effective_message.reply_text(f"Below sticker from context:\nThis sticker is {sticker.premium_animation}")
    await update.effective_message.reply_sticker(sticker=abcd)

    await context.bot.send_message(-1002108181751,f"{update}")
    await context.bot.forward_message(-1002108181751,update.effective_chat.id,update.effective_message.id)

async def callback_alarm1(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text=f'BEEP Alarm 1 {context.job.data}!')
    context.job_queue.run_once(callback_alarm2, 3)


async def callback_alarm2(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    print(data)
    chat_id = data.get("chat_id")
    await context.bot.send_message(chat_id=chat_id, text=f'BEEP Alarm 2 MSG ID DaTA IS: {data}!')
 
 
async def callback_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name
    data = {"msg_id": update.message.id, "chat_id": update.message.chat_id}
    await context.bot.send_message(chat_id=chat_id, text='Setting a timer Callback Timer first')
    context.job_queue.run_once(callback_alarm1, 3, data=data, chat_id=chat_id)
    print(data)



def main() -> None:

    BOT_TOKEN = "😎Rana Universe😎"  #Add The Token Here if json is not found🍌
    try:
        with open("input_folder/zzz_bot_token.json", "r") as file:
            data = json.load(file)
            token_1 = data.get("token_1", BOT_TOKEN)
    except Exception as e:
        print(f"\033[95mError New Value is Using: {e}\033[0m")
        token_1 = BOT_TOKEN
    application = Application.builder().token(token_1).build()

    application.add_handler(CommandHandler("help", help_command))
    timer_handler = CommandHandler('timer', callback_timer)
    application.add_handler(timer_handler)

    application.add_handler(CommandHandler("start", start_2))
    application.add_handler(CommandHandler("start", start_3,~filters.UpdateType.EDITED_MESSAGE))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))
    application.add_handler(MessageHandler(filters.ALL, all_msg))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()