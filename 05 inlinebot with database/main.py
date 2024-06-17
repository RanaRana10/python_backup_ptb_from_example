import sys
sys.dont_write_bytecode = True

import re
import logging, datetime
from html import escape
from uuid import uuid4

from telegram import InputTextMessageContent,InlineKeyboardButton,InlineKeyboardMarkup, Update, WebAppInfo, InlineQueryResultsButton

from telegram import (InlineQueryResultCachedAudio,
                      InlineQueryResultCachedDocument,
                      InlineQueryResultCachedGif,
                      InlineQueryResultCachedMpeg4Gif,
                      InlineQueryResultCachedPhoto,
                      InlineQueryResultCachedSticker,
                      InlineQueryResultCachedVideo,
                      InlineQueryResultCachedVoice                      
                      )

from telegram import (InlineQueryResultArticle,
                      InlineQueryResultAudio,
                      InlineQueryResultContact,
                      InlineQueryResultGame,
                      InlineQueryResultDocument,
                      InlineQueryResultGif,
                      InlineQueryResultLocation,
                      InlineQueryResultMpeg4Gif,
                      InlineQueryResultPhoto,
                      InlineQueryResultVenue,
                      InlineQueryResultVideo,
                      InlineQueryResultVoice
                      )




from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler,MessageHandler, ContextTypes, InlineQueryHandler, CallbackQueryHandler, filters


from db_operation import add_document, get_document_by_id, get_documents, session, add_document_no_commit
from db_operation import (add_photo,
                          get_all_photo,
                          get_photo_by_id)

allow_users_list = [1895194333, 5393096971]

pattern = r'a|ab|abc'





logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


GOOGLE_LOGO_LINK : str = "https://te.legra.ph/file/553d5eaa0031fcf48e21d.png"
YOUTUBE_LOGO_LINK : str = "https://te.legra.ph/file/08f23be52f3cdd49bb820.jpg"
RANA_UNIVERSE_LOGO : str = "https://te.legra.ph/file/27eb23494ee0ccba5580a.png"





keyboard =[
            InlineKeyboardButton("Url with website", url="www.youtube.com"),
            InlineKeyboardButton("Select to do the text in placeholder below", switch_inline_query_current_chat= "Hello Boss"),
            InlineKeyboardButton("With a callback Data", callback_data = 1),
        ],

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






async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hi!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def text_msg_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    information = get_document_by_id(text)
    
    if information is not None:
        document_id, title, file_id = information
        response_text = f"Document ID: {document_id}\nTitle: {title}\nFile ID: {file_id}"
    else:
        response_text = "Document not found with the provided ID."

    await update.message.reply_text(response_text)


async def text_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    if text.isdigit():
        document_id = int(text)
        
        information = get_document_by_id(document_id)
        
        if information is not None:
            document_id, title, file_id = information
            response_text = f"Document ID: <code>{document_id}</code>\nTitle: <b>{title}</b>\nFile ID: <code>{file_id}</code>"
            try:
                await context.bot.send_document(user.id, document=file_id, caption= response_text, parse_mode="html")
            except: await context.bot.send_message(user.id, f"{response_text}", parse_mode= "HTML")
        else:
            response_text = "Document not found with the provided ID."
            await update.message.reply_text(f"You have send me:\n{response_text}", parse_mode= "HTML")
    else:
        response_text = text.upper()
        await update.message.reply_text(f"Started")

        for i in range(100):
            add_document(title=f"{i} 🍌🍌🍌{user.full_name}", file_id= response_text)
        print(f"New TExt inserted {user.full_name}")

        await update.message.reply_text(f"You have send me:\n{response_text}", parse_mode= "HTML")






async def text_msg_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    if text.isdigit():
        document_id = int(text)
        
        information = get_document_by_id(document_id)
        
        if information is not None:
            document_id, title, file_id = information
            response_text = f"Document ID: <code>{document_id}</code>\nTitle: <b>{title}</b>\nFile ID: <code>{file_id}</code>"
            try:
                await context.bot.send_document(user.id, document=file_id, caption= response_text, parse_mode="html")
            except: await context.bot.send_message(user.id, f"{response_text}", parse_mode= "HTML")
        else:
            response_text = "Document not found with the provided ID."
            await update.message.reply_text(f"You have send me:\n{response_text}", parse_mode= "HTML")
    else:
        response_text = text.upper()
        await update.message.reply_text(f"Started Your Value is adding in our DATABASE 50000 times", reply_to_message_id=update.message.id)
        print(f"Processing Has Started, {user.full_name}")
        documents_to_insert = []
        for i in range(500000):
            title = f"{i} 🍌🍌🍌 {user.full_name}"
            file_id = response_text
            doc_obj = add_document_no_commit(title=title, file_id=file_id)
            documents_to_insert.append(doc_obj)
        session.add_all(documents_to_insert)
        session.commit()

        await update.message.reply_text(f"You have send me:\n{response_text}", parse_mode= "HTML",reply_to_message_id=update.message.id)














async def documents_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    file_name = update.message.document.file_name
    file_id = update.message.document.file_id

    add_document(title=file_name, file_id= file_id)
    print(f"success {file_name}")
    # await context.bot.send_message(user.id, f"Your File Has saved as <code>{file_id}</code>", parse_mode= "html")
    ...






async def inline_query_cache_documents_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
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




async def inline_query_documents_cache_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    documents = get_documents()[:10]

    default_title = "Default Title without any 🍌"

    results = []
    for document in documents:
        title = f"This is Document No {document.id}"
        file_id = document.file_id

        result_title = title if title else default_title

        result = InlineQueryResultCachedDocument(
            id=str(uuid4()),
            title=result_title,
            document_file_id=file_id
        )
        results.append(result)

    await context.bot.answerInlineQuery(update.inline_query.id, results=results)




async def inline_query_documents_cache(update: Update, context: ContextTypes.DEFAULT_TYPE):
    offset = int(update.inline_query.offset) if update.inline_query.offset else 0
    results_per_page = 10

    documents = get_documents()[offset : offset + results_per_page]

    results = []
    for document in documents:
        title = f"{document.id} {document.title} This is Document No "
        file_id = document.file_id

        result = InlineQueryResultCachedDocument(
            id=str(uuid4()),
            title=title,
            document_file_id=file_id
        )
        results.append(result)

    next_offset = str(offset + results_per_page)

    await context.bot.answerInlineQuery(
        inline_query_id=update.inline_query.id,
        results=results,
        next_offset=next_offset,
        button= InlineQueryResultsButton(
            text = f"{update.inline_query.from_user.full_name} This is Button",
            start_parameter= "__hello__"
        )
        )


async def photo_processing_fun(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    photo_id = update.message.photo[-1].file_id
    row_id = add_photo(photo_name=f"{user.id}_{update.message.date}", photo_file_id=f'{photo_id}')
    # await context.bot.send_message(user.id, f"Your data has saved in: \n<code>{row_id}</code>", parse_mode="html")
    print(f"Your data has saved in: \n<code>{row_id}</code>")
    ...




async def inline_query_photo_cache(update: Update, context: ContextTypes.DEFAULT_TYPE):
    offset = int(update.inline_query.offset) if update.inline_query.offset else 0
    results_per_page = 10

    documents = get_all_photo()[offset : offset + results_per_page]

    results = []
    for document in documents:
        title = f"{document.id}_{document.photo_name}"
        file_id = document.photo_file_id

        result = InlineQueryResultCachedPhoto(
            id=str(uuid4()),
            title=document.id,
            photo_file_id= file_id,
            caption= f"Caption is the Title:\n{title}"
        )
        results.append(result)

    next_offset = str(offset + results_per_page)

    await context.bot.answerInlineQuery(
        inline_query_id=update.inline_query.id,
        results=results,
        cache_time= 3,
        next_offset=next_offset,
        button= InlineQueryResultsButton(
            text = f"{update.inline_query.from_user.full_name} This is Button",
            start_parameter= "string"
        )
        )


async def inline_query_empty_string(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.inline_query.from_user
    query_id = update.inline_query.id
    query = update.inline_query.query

    results_list = []
    results_list = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()+f"\nThis is for Caps Query"),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"<b>{escape(query)}</b>"+f"\nThis is for Bold Query", parse_mode=ParseMode.HTML
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"<i>{escape(query)}</i>"+f"\nThis is for italic Query", parse_mode=ParseMode.HTML
            ),
        ),
    ]
    await context.bot.answer_inline_query(query_id, results_list)
    ...


async def inline_query_documents_cache_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    offset = int(update.inline_query.offset) if update.inline_query.offset else 0

    documents = get_documents()

    results_list = []
    for document in documents:
        title = f"{document.id} {document.title} This is Document No "
        file_id = document.file_id

        result = InlineQueryResultCachedDocument(
            id=str(uuid4()),
            title=title,
            document_file_id=file_id
        )
        results_list.append(result)


    await update.inline_query.answer(
        results=results_list,
        auto_pagination=True,
    )




async def deep_link_start_string(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text("You have use string hidden link")

    
    ...












def main() -> None:
    """Run the bot."""
    application = Application.builder().token("6780033449:AAFKWBuWlPcBHLm303owSEvDriPZjCxs9ZU").build()


    application.add_handler(CommandHandler("start", deep_link_start_string, filters.Regex("__hello__")))
    application.add_handler(CommandHandler("start", deep_link_start_string, filters.Regex("string")))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button))

    application.add_handler(MessageHandler(filters=filters.TEXT, callback= text_msg,block = False))
    application.add_handler(MessageHandler(filters=filters.Document.ALL, callback= documents_file_id))
    application.add_handler(MessageHandler(filters=filters.PHOTO, callback= photo_processing_fun, block= False))
    

    # application.add_handler(InlineQueryHandler(inline_query_documents_cache_2, "docs", block= False))
    application.add_handler(InlineQueryHandler(inline_query_empty_string,pattern=pattern, block = False, chat_types= "private"))
    application.add_handler(InlineQueryHandler(inline_query_photo_cache, "doc", block= False, chat_types="private"))
    application.add_handler(InlineQueryHandler(inline_query_documents_cache, "doc", block= False))

    application.add_handler(InlineQueryHandler(inline_query_photo_cache, "pho", block = False))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
