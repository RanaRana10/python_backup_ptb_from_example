import logging, datetime
from html import escape
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardButton,InlineKeyboardMarkup, InlineQueryResultPhoto, InlineQueryResultCachedPhoto, Update, InlineQueryResultCachedDocument
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler, CallbackQueryHandler


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


GOOGLE_LOGO_LINK : str = "https://te.legra.ph/file/553d5eaa0031fcf48e21d.png"
YOUTUBE_LOGO_LINK : str = "https://te.legra.ph/file/08f23be52f3cdd49bb820.jpg"
RANA_UNIVERSE_LOGO : str = "https://te.legra.ph/file/27eb23494ee0ccba5580a.png"


def create_youtube_search_url(query: str) -> str:

    base_url = "https://www.youtube.com/results?"
    search_query = "+".join(query.split())
    url = f"{base_url}search_query={search_query}"
    return url


def create_google_search_url(query: str) -> str:

    base_url = "https://www.google.com/search?"
    search_query = "+".join(query.split())
    url = f"{base_url}q={search_query}"
    return url



keyboard =[
            InlineKeyboardButton("Url with website", url="www.youtube.com"),
            InlineKeyboardButton("Select to do the text in placeholder below", switch_inline_query_current_chat= "Hello Boss"),
            InlineKeyboardButton("With a callback Data", callback_data = 1),
        ],


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hi!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")



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
    if query.data == "3":
        dynamic_text = f"Hello\nThanks\nRana Universe\n🍌🍌🍌\nyou select Option 3 Selected at\n {current_time}"
        await query.answer(text=dynamic_text)
    else:
        dynamic_text = "Unknown Option ❌❌❌"
        await query.answer(text=dynamic_text)



async def inline_query_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    user = update.effective_user
    query = update.inline_query.query
    inline_query_id = update.inline_query.id
    message = f"Hello Boss Can You Make Your Private Bot\nThanks Rana Universe{user.name}\n🍌🍌🍌"
    if not query:
        await context.bot.send_message(user.id, "Thanks For Blank Chat")
        return

    results = [
        InlineQueryResultArticle(
            id=1,
            title="Youtube Search",
            input_message_content=InputTextMessageContent(message_text=f"Watch The Video in Youtube Below:\n{create_youtube_search_url(escape(query))}",
            parse_mode= "html"),
            url = create_youtube_search_url(escape(query)),
            thumbnail_url = YOUTUBE_LOGO_LINK
        ),

        InlineQueryResultArticle(
            id=2,
            title="Google Search",
            input_message_content=InputTextMessageContent(message_text=create_google_search_url(escape(query)), parse_mode= ParseMode.HTML),
            thumbnail_url = GOOGLE_LOGO_LINK
        ),
        
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"<b>{escape(query)}</b>", parse_mode=ParseMode.HTML),
            url= "www.google.com",
            hide_url= False,
            description= "This is descritpitpn",
            thumbnail_url=RANA_UNIVERSE_LOGO,
            reply_markup= InlineKeyboardMarkup(keyboard)
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"<i>{escape(query)}</i>", parse_mode=ParseMode.HTML
            ),
            thumbnail_url= "https://core.telegram.org/file/811140530/1/h-eMmPp2vp4/cd4a109f75e6561305"
        ),
    ]

    await context.bot.answer_inline_query(inline_query_id, results)



async def inline_query_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    user = update.effective_user
    query = update.inline_query.query
    inline_query_id = update.inline_query.id
    message = f"Hello Boss Can You Make Your Private Bot\nThanks Rana Universe{user.name}\n🍌🍌🍌"
    if not query:
        await context.bot.send_message(user.id, "Thanks For Blank Chat")
        return

    results = [
        InlineQueryResultPhoto(
            id = 1,
            photo_url= GOOGLE_LOGO_LINK,
            thumbnail_url= "www.com",
            title= "This is the Title",
            description= "This is the description"
        ),

        InlineQueryResultPhoto(
            id=2,
            photo_url= GOOGLE_LOGO_LINK,
            thumbnail_url= "www.com",
            caption= "This is The Caption",
            reply_markup= InlineKeyboardMarkup(keyboard)
        ),
    ]

    await context.bot.answer_inline_query(inline_query_id, results)



nature_1 = "AgACAgQAAxkBAAI_CWX7Br9HUyshA7DbMZbhggU518hZAAIWvjEb6AZgUMNQaaBEbXJPAQADAgADeQADNAQ"
nature_2 = "AgACAgQAAxkBAAI_CmX7Br-OSh8ei53-8dCYCZbdnIQQAAK4vTEblrjJUCj8NU-3v2wjAQADAgADeQADNAQ"
nature_3 = "AgACAgQAAxkBAAI_C2X7Br97gi5mWlOMpQ6VfwxZOEfIAAK6vTEblrjJUM4zErDdUIYSAQADAgADeQADNAQ"
nature_4 = "AgACAgQAAxkBAAI_DGX7Br-mMm5L1rvrbkuiKz5DSsyAAAK7vTEblrjJUPdNtOJbhVadAQADAgADeQADNAQ"
nature_5 = "AgACAgQAAxkBAAI_DWX7Br_Zp3cKThySBmYC0OyIHKBOAAK8vTEblrjJUOKEpZAkIZJhAQADAgADeQADNAQ"


async def inline_query_cache_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    user = update.effective_user
    query = update.inline_query.query
    inline_query_id = update.inline_query.id
    message = f"Hello Boss Can You Make Your Private Bot\nThanks Rana Universe{user.name}\n🍌🍌🍌"
    if not query:
        await context.bot.send_message(user.id, "Thanks For Blank Chat")
        return

    results = [
        InlineQueryResultCachedPhoto(
            id = str(uuid4()),
            photo_file_id= nature_1,
            caption= f"This is the caption of this image of file id:\n<code>Rana Universe</code>",
            parse_mode= "html"
        ),

        InlineQueryResultCachedPhoto(
            id= str(uuid4()),
            photo_file_id= nature_2,
            caption= f"This is caption for nature 2"
        )
    ]
    await context.bot.answer_inline_query(inline_query_id, results)


async def inline_query_cache_documents_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the inline query. This is run when you type: @botusername <query>"""
    user = update.inline_query.from_user
    query = update.inline_query.query

    file_1 = "BQACAgUAAxkBAAJBsWX_5Xgcb01e9HxMxEPveC74Otn5AAIKCwACrPOIVlv5q-sJu4wUNAQ"
    file_2 = "BQACAgUAAxkBAAJBsmX_5XivVNkKnNkZYeK1wZhiyZ1-AAILCwACrPOIVgmW2t-I87haNAQ"
    file_3 = "BQACAgUAAxkBAAJBs2X_5XhjJCphXug0z1hN1DlwnEteAAIMCwACrPOIVsBR9fpl86oiNAQ"
    file_4 = "BQACAgUAAxkBAAJBtGX_5XhKXCLfwxEHl-e2LgZyvhwsAAINCwACrPOIVsd5it0osCluNAQ"
    file_5 = "BQACAgUAAxkBAAJBtWX_5XiVmD9GLK3XfEzbz6XgQ2eyAAIOCwACrPOIVjRgtjeGLAAB-TQE"

    if not query:
        await context.bot.send_message(user.id, f"This is Blank Please Write any Thing {user.full_name}")
        return
    results = [
        InlineQueryResultCachedDocument(
            id = 1,
            title = "This is Document No. 1",
            document_file_id= file_1,            
        ),
        InlineQueryResultCachedDocument(
            id = 2,
            title = "This is Document No. 2",
            document_file_id= file_2,            
        ),
        InlineQueryResultCachedDocument(
            id = 3,
            title = "This is Document No. 3",
            document_file_id= file_3,            
        ),
        InlineQueryResultCachedDocument(
            id = 4,
            title = "This is Document No. 4",
            document_file_id= file_4,            
        ),
        InlineQueryResultCachedDocument(
            id = 5,
            title = "This is Document No. 5",
            document_file_id= file_5,   
        ),
    ]

    await context.bot.answerInlineQuery(update.inline_query.id, results= results)



async def inline_query_cache_documents_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Having file id list and title list and connect it"""
    user = update.inline_query.from_user
    query = update.inline_query.query

    # List of file IDs
    file_ids = [
        "BQACAgUAAxkBAAJB02X_7YwVBbxHIWHJQIdx8KIlsxYEAAIOCwACrPOIVjRgtjeGLAAB-TQE",
        "BQACAgUAAxkBAAJB0mX_7Yz43ODL0qYY03sBjOx1Ggb7AAINCwACrPOIVsd5it0osCluNAQ",
        "BQACAgUAAxkBAAJB0WX_7YwXJV8PJT4_O7mPxOS3LrB3AAIMCwACrPOIVsBR9fpl86oiNAQ",
        "BQACAgUAAxkBAAJB0GX_7YxWLr269cZT7o99gMckhhSjAAILCwACrPOIVgmW2t-I87haNAQ",
        "BQACAgUAAxkBAAJBz2X_7Yy3Ql1w7Vu5z9E7jSH9YVSOAAIKCwACrPOIVlv5q-sJu4wUNAQ",
    ]

    # List of titles for the documents
    titles = [
        "This is 1st Documents",
        "2nd Movie",
        "3rd list",
    ]

    results = []
    for i, file_id in enumerate(file_ids):
        title = titles[i] if i < len(titles) else f"This Has no Title, 🍌🍌🍌is Document No. {i + 1}"
        result = InlineQueryResultCachedDocument(
            id=str(i),
            title=title,
            document_file_id=file_id
        )
        results.append(result)

    await context.bot.answerInlineQuery(update.inline_query.id, results=results)



async def inline_query_cache_documents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_info = [
        ("", "BQACAgUAAxkBAAJB02X_7YwVBbxHIWHJQIdx8KIlsxYEAAIOCwACrPOIVjRgtjeGLAAB-TQE"),
        ("Tit for 2", "BQACAgUAAxkBAAJB0mX_7Yz43ODL0qYY03sBjOx1Ggb7AAINCwACrPOIVsd5it0osCluNAQ"),
        ("", "BQACAgUAAxkBAAJB0WX_7YwXJV8PJT4_O7mPxOS3LrB3AAIMCwACrPOIVsBR9fpl86oiNAQ"),
        ("Title this is movie", "BQACAgEAAxkBAAJB4WX_8uzka6rUJD4wrne4fLLVDkGfAAKKAwACOpiARfKkNxrrREz8NAQ"),
        ("thumbnail image file with 3", "BQACAgUAAxkBAAJB3WX_8Q_-5imNlMZdnGkUcCJwoJjiAALdDgACExT5V5U1gwYsHDyCNAQ"),
    ]
    default_title = "Default Title without any 🍌"

    results = []
    for i, (title, file_id) in enumerate(file_info):
        result_title = title if title else default_title

        result = InlineQueryResultCachedDocument(
            id=str(uuid4()),
            title=result_title,
            document_file_id=file_id
        )
        results.append(result)

    await context.bot.answerInlineQuery(update.inline_query.id, results=results)
















def main() -> None:
    """Run the bot."""
    application = Application.builder().token("6780033449:AAFKWBuWlPcBHLm303owSEvDriPZjCxs9ZU").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CallbackQueryHandler(button))

    application.add_handler(InlineQueryHandler(inline_query_cache_documents))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
