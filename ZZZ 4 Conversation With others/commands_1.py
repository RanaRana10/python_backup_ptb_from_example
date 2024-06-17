"""This is just for some BAsic command handler functions
Import Statements🍌🍌🍌
from basic_commands_1 import help_command, echo, random_text, send_file, send_random_photo


"""
import os
import asyncio
import random
import pymongo
from telegram import Update
from telegram.ext import ContextTypes
from pathlib import Path


client = pymongo.MongoClient("mongodb://localhost:27017/")
mydatabase = client["multiple_user"]
users_collection = mydatabase["users"]



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = f"This is the Help Command For This Bot Send\nThanks {user.full_name}"


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message with upper letters."""
    input_text = update.message.text
    send_text = input_text.upper()
    await update.message.reply_text(send_text)



async def random_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get Random Text from the MOngo Dataabase"""

    query_man = {"name": "man"}
    man_document = users_collection.find_one(query_man)

    man_ages = man_document.get('age', [])

    random_age = random.choice(man_ages)

    send_text = f"Random Age: {random_age}"

    await update.message.reply_text(send_text)


async def random_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

    query_man = {"name": "man"}
    man_document = users_collection.find_one(query_man)
    if man_document:
        man_ages = man_document.get('age', [])

        if man_ages:
            random_age = random.choice(man_ages)

            send_text = f"Random Age: {random_age}"
        else:
            send_text = "No age values found."
    else:
        send_text = "No document found for 'man'."

    await update.message.reply_text(send_text)


async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ THis is BAsed on /b send files fun"""
    user = update.message.from_user
    chat = update.message.chat
    docs = "e.jpg"

    document_list = ["BAACAgEAAxkBAAICk2WO4HEmpyezpLe1AAEo4FyaHgyotgAC6wMAAm1hyUeRVN496aUoTTQE",
                    "BAACAgEAAxkBAAIClGWO4HF4qRhDnA79MU__m7SL6yfaAAL9AwAC4eXpR4OCfJ2mO9rqNAQ",
                    "BAACAgEAAxkBAAIClWWO4HHdo0A1S7Spf-mqbJJbTC23AAKFBAAC_nfwR9PC47QKPxeHNAQ",
                    "BAACAgEAAxkBAAIClmWO4HEAAdDSolpnUJscXAuvhr_cUwACOgMAAvJE8UdVpq_FZ87TWTQE",
                    "BAACAgEAAxkBAAICl2WO4HG9ohTSQypHw6tTNUArGVwhAAIQAAPGewFNwiz2ItrYJoE0BA",
                    "BAACAgQAAxkBAAICmGWO4HHj54GyZP5z-rGh2iCu4La5AAL4FQAC4-gBUp93-Hwv4IlrNAQ",
                    "BAACAgEAAxkBAAICmWWO4HHUAAE5_PSVJxKVU0NkfYMfJgADBAACyEc4RHX73oSXF6fZNAQ",
                    "BAACAgEAAxkBAAICmmWO4HHdcKJ_pXAuua0lc6PaZnPMAAJZBQACNo5JREovLWDdyyZwNAQ"]
                   
    # document_id = random.choice(document_list)
    # await context.bot.send_document(chat_id=user.id, document = document_id, caption="Hello Boss Thanks")

    # for document_id in document_list:
    #     await context.bot.send_document(chat_id=chat.id, document=document_id, caption="Hello Boss Thanks")

    for index, document_id in enumerate(document_list, start=1):
        caption = f"This file no. is {index}"
        await context.bot.send_document(chat_id=chat.id, document=document_id, caption=caption)




async def send_random_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ /a this is for send Random image form storage"""
    user = update.message.from_user
    chat = update.message.chat

    # files = ["a.jpg",'b.jpg', 'c.jpg', 'd.jpg', 'e.jpg']
    # one_file = random.choice(files)
    # await context.bot.send_photo(chat_id=chat.id,photo=one_file)

    # directory = "files/images/send"
    directory = os.path.join("files", "images", "send")
    filenames = ["a.jpg",'b.jpg', 'c.jpg', 'd.jpg', 'e.jpg']
    filename  = random.choice(filenames)
    image_path = os.path.join(directory,filename)
    await context.bot.send_photo(chat.id,image_path,"This is using os string")








