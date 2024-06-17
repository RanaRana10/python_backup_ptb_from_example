import sys
sys.dont_write_bytecode = True
from datetime import timedelta, datetime
from pathlib import Path
import asyncio
import logging
from typing import Optional, Tuple

from telegram import Chat, ChatMember, ChatMemberUpdated, Update
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import (
    Application,
    ChatMemberHandler,
    ChatJoinRequestHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
        ChatMember.MEMBER,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
        ChatMember.MEMBER,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tracks the chats the bot is in."""
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    cause_name = update.effective_user.full_name

    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if not was_member and is_member:
            # This may not be really needed in practice because most clients will automatically
            # send a /start command after the user unblocks the bot, and start_private_chat()
            # will add the user to "user_ids".
            # We're including this here for the sake of the example.
            logger.info("%s unblocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s blocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).discard(chat.id)
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if not was_member and is_member:
            logger.info("%s added the bot to the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).discard(chat.id)
    elif not was_member and is_member:
        logger.info("%s added the bot to the channel %s", cause_name, chat.title)
        context.bot_data.setdefault("channel_ids", set()).add(chat.id)
    elif was_member and not is_member:
        logger.info("%s removed the bot from the channel %s", cause_name, chat.title)
        context.bot_data.setdefault("channel_ids", set()).discard(chat.id)


async def show_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows which chats the bot is in"""
    user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", set()))
    group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", set()))
    channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", set()))
    text = (
        f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}."
        f" Moreover it is a member of the groups with IDs {group_ids} "
        f"and administrator in the channels with IDs {channel_ids}."
    )
    await update.effective_message.reply_text(text)


async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets new users in chats and announces when someone leaves"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()

    if not was_member and is_member:
        await update.effective_chat.send_message(
            f"{member_name} was added by {cause_name}. Welcome!",
            parse_mode=ParseMode.HTML,
        )
    elif was_member and not is_member:
        await update.effective_chat.send_message(
            f"{member_name} is no longer with us. Thanks a lot, {cause_name} ...",
            parse_mode=ParseMode.HTML,
        )


async def start_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets the user and records that they started a chat with the bot if it's a private chat.
    Since no `my_chat_member` update is issued when a user starts a private chat with the bot
    for the first time, we have to track it explicitly here.
    """
    user_name = update.effective_user.full_name
    chat = update.effective_chat
    if chat.type != Chat.PRIVATE or chat.id in context.bot_data.get("user_ids", set()):
        return

    logger.info("%s started a private chat with the bot", user_name)
    context.bot_data.setdefault("user_ids", set()).add(chat.id)

    await update.effective_message.reply_text(
        f"Welcome {user_name}. Use /show_chats to see what chats I'm in."
    )



async def join_req_fun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    user = update.chat_join_request.from_user
    chat = update.chat_join_request.chat
    await context.bot.send_message(user.id, f"{update}")
    text = f"{user.full_name} has send a Join Request in this Group {chat.title} at {update.chat_join_request.date + timedelta(hours= 5, minutes= 30)}\nUsers Bio is: {update.chat_join_request.bio}"

    await context.bot.send_message(chat.id, text)

    chat_member = await context.bot.get_chat_member(chat.id, user.id)

    i = 1
    while True:
        await asyncio.sleep(1)
        chat_member = await context.bot.get_chat_member(chat.id, user.id)

        # if chat_member.status == "member":
        print(i, chat_member.status)
        if chat_member.status != "left":
            await context.bot.send_message(chat.id, f"{user.full_name} has joined the group.")
            break  # Exit the loop if the user joins the group any admin or bott
        else:
            await context.bot.send_message(chat.id, f"{user.full_name} Join Request has been {i*1} Seconds and still not approved.")
            i += 1
            if i> 5:
                await context.bot.approve_chat_join_request(chat.id, user.id)
                await context.bot.send_message(chat.id, f"I have successfully inserted the user in our group")
                break




async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    chat = update.message.chat
    await context.bot.ban_chat_member(chat.id, user.id, 31)
    await context.bot.send_message(user.id, f"You Have Banned for 31 SEconds")



async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.message.chat

    user_id = context.args[0]

    await context.bot.unban_chat_member(chat.id, user_id)
    await context.bot.send_message(user_id, f"You have now Unban from the group")
    ...






    # await asyncio.sleep(2)
    # await context.bot.send_message(chat.id, f"Your Join Request has been 2 Seconds and still not approve 1")
    # await asyncio.sleep(2)
    # await context.bot.send_message(chat.id, f"Your Join Request has been 2 Seconds and still not approve 2")
    # await asyncio.sleep(2)
    # await context.bot.send_message(chat.id, f"Your Join Request has been 2 Seconds and still not approve 3")
    # await asyncio.sleep(2)
    # await context.bot.send_message(chat.id, f"Your Join Request has been 2 Seconds and still not approve 4")
    # await asyncio.sleep(2)
    # await context.bot.send_message(chat.id, f"Your Join Request has been 2 Seconds and still not approve 5")
    # await asyncio.sleep(2)
    # await context.bot.send_message(chat.id, f"Your Join Request has been 2 Seconds and still not approve 6")
    # await asyncio.sleep(2)
    # await context.bot.send_message(chat.id, f"Your Join Request has been 2 Seconds and still not approve 7")


    # for i in range(10):
    #     await asyncio.sleep(2)
    #     await context.bot.send_message(chat.id, f"Your Join Request has been 2 Seconds and still not approve {i}")




async def user_checking(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    if len(context.args) != 2:
        await update.message.reply_text(f"Please provide both chat_id and user_id.You have only passed:\n{len(context.args)} Things")
        return
    
    chat_id = context.args[0]
    user_id = context.args[1]


    try:
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        await context.bot.send_message(user.id, str(chat_member))
        # await context.bot.send_message(user.id, f"Users More info is: \n{str(chat_member.status)}")
        chat_member_info = f"This Below is the more information:\n"

        if chat_member.status == "creator":
            chat_member_info += "Chat Member Status: Chat Creator (Owner)\n"
        elif chat_member.status == "administrator":
            chat_member_info += "Chat Member Status: Administrator\n"
        elif chat_member.status == "member":
            chat_member_info += "Chat Member Status: Member\n"
        elif chat_member.status == "restricted":
            chat_member_info += "Chat Member Status: Restricted Member\n"
        elif chat_member.status == "left":
            chat_member_info += "Chat Member Status: Left\n"
        elif chat_member.status == "kicked":
            chat_member_info += "Chat Member Status: Banned (Kicked)\n"

        await context.bot.send_message(user.id, chat_member_info)


    except BadRequest as e:
        # Check the error message to determine the type of error
        if "User not found" in str(e):
            # Perform task1 if user is not found
            await update.message.reply_text("Please Send correct user id")
            # Perform Task 1 here
        elif "Chat not found" in str(e):
            # Perform task2 if chat is not found
            await update.message.reply_text("Please Send Correct Caht id:::")
            # Perform Task 2 here
        else:
            # If it's another BadRequest error, handle it accordingly
            await update.message.reply_text(f"Error: Another Bad REquest::: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        await update.message.reply_text(f"Fully Another Error: {e}")




async def photo_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.message.chat
    caption_text = update.message.caption
    print(caption_text)
    photo_file_id = update.message.photo[-1].file_id
    photo_file = await context.bot.get_file(photo_file_id)
    location = Path()
    name = f"{chat.id}_{datetime.now().timestamp()}.jpg"
    await photo_file.download_to_drive(name)

    if caption_text == "new":
        try:
            # Set the chat photo using the downloaded image file
            await context.bot.set_chat_photo(chat.id, name)
            await context.bot.send_message(chat.id, "New Photo Has Been inserted")
        except Exception as e:
            await context.bot.send_message(chat.id, f"An error occurred: {e}")


async def del_chat_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.message.chat
    await context.bot.delete_chat_photo(chat.id)
    await context.bot.send_message(chat.id, f"Photo has been deleted")
    ...



async def update_msg_2(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    text = f"Hello Boss Your Name is {user.full_name}\nCurrent Time: {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}"
    await context.bot.send_message(user.id, text)
    await asyncio.sleep(2)
    await context.bot.send_message(user.id, text)
    await asyncio.sleep(3)
    await context.bot.send_message(user.id, text)


async def update_msg_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = f"Hello Boss Your Name is {user.full_name}\nCurrent Time: "
    
    await context.bot.send_message(user.id, f"{text}{get_current_time()}")
    await asyncio.sleep(1)
    await context.bot.send_message(user.id, f"{text}{get_current_time()}")
    await asyncio.sleep(2)
    await context.bot.send_message(user.id, f"{text}{get_current_time()}")
    await asyncio.sleep(3)
    await context.bot.send_message(user.id, f"{text}{get_current_time()}")
    await asyncio.sleep(4)
    await context.bot.send_message(user.id, f"{text}{get_current_time()}")


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H-%M-%S')

# Dictionary to store user IDs and their corresponding message IDs
user_message_ids = {}

async def update_msg_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = f"Hello Boss Your Name is {user.full_name}\nCurrent Time: "

    if user.id in user_message_ids:
        message_id = user_message_ids[user.id]
        await context.bot.edit_message_text(chat_id=user.id, message_id=message_id, text=f"{text}{get_current_time()}")
    else:
        sent_message = await context.bot.send_message(user.id, f"{text}{get_current_time()}")
        user_message_ids[user.id] = sent_message.message_id

    await asyncio.sleep(1)
    await context.bot.edit_message_text(chat_id=user.id, message_id=user_message_ids[user.id], text=f"{text}{get_current_time()}")
    await asyncio.sleep(1)
    await context.bot.edit_message_text(chat_id=user.id, message_id=user_message_ids[user.id], text=f"{text}{get_current_time()}")
    await asyncio.sleep(1)
    await context.bot.edit_message_text(chat_id=user.id, message_id=user_message_ids[user.id], text=f"{text}{get_current_time()}")
    await asyncio.sleep(1)
    await context.bot.edit_message_text(chat_id=user.id, message_id=user_message_ids[user.id], text=f"{text}{get_current_time()}")


async def reply_msg_fun(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    reply_msg_id = update.message.reply_to_message.message_id
    await context.bot.send_message(user.id, f"{reply_msg_id} This msg will delete")
    try:
        await context.bot.delete_message(user.id, reply_msg_id)
    except Exception as e:
        await context.bot.send_message(user.id, f"{e}")


async def delete_msgs_from(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    reply_msg_id = update.message.reply_to_message.message_id

    current_msg_id = reply_msg_id + 1

    while True:
        try:
            await context.bot.delete_message(user.id, current_msg_id)
        except Exception as e:
            problem = f"Failed to delete message with ID {current_msg_id}: {e}"
            print(problem)
            await context.bot.send_message(user.id, problem)
            # break  # Break the loop if deletion fails or there are no more messages

        current_msg_id += 1  # Increment to delete the next message

        # Add a small delay to avoid hitting API rate limits
        await asyncio.sleep(0.5)

    await context.bot.send_message(user.id, "All messages have been deleted.")



async def send_msg_and_del(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    chat = update.message.chat
    text = f"Thanks, {user.full_name} You Send The msg in this Chat: {chat.title}"
    text += f"I will edit this msg after 2 seconds"
    send_msg = await context.bot.send_message(chat.id, text)
    await asyncio.sleep(1)
    await context.bot.send_message(chat.id, f"I am replying to old msg", reply_to_message_id= send_msg.message_id)
    await context.bot.send_message(chat.id, f"I will delete the old msg after 1 ssecond")
    await context.bot.edit_message_text("I have edit this now it will del",chat.id, send_msg.message_id)
    await context.bot.send_chat_action(chat.id, "typing")
    await asyncio.sleep(5)
    await context.bot.deleteMessage(chat.id, send_msg.message_id)
    


async def edit_msg_continuously(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    chat = update.message.chat
    send_msg = await context.bot.send_message(chat.id, f"First Time MSG:{get_current_time()}")
    await asyncio.sleep(2)

    for i in range(1, 11):
        send_msg = await context.bot.edit_message_text(f"{get_current_time()}", chat.id, send_msg.message_id)
        await asyncio.sleep(1)

    await asyncio.sleep(3)
    await context.bot.send_message(chat.id, f"All Successful NOw i will delete the old msg")
    await context.bot.delete_message(chat.id, send_msg.message_id)
    send_msg = await context.bot.send_message(chat.id, "Delete Successful")
    await context.bot.delete_message(chat.id, send_msg.message_id)
    await context.bot.send_message(chat.id, "⚡️")
    await context.bot.send_message(chat.id, "💩")
    await context.bot.send_message(chat.id, "🤣")




async def image_processing_fun(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    chat = update.message.chat

    photo_file_id = update.message.photo[-1].file_id
    photo_file = await context.bot.get_file(photo_file_id)
    folder_name = Path("image") / "send_by_user"
    folder_name.mkdir(parents=True, exist_ok=True)
    image_name = f"{chat.id}_{datetime.now().timestamp()}.jpg"
    image_path = folder_name / image_name

    await photo_file.download_to_drive(image_path)
    await context.bot.send_message(chat.id, f"Your image has been saved in: {image_path}")





processed_media_group_ids = set()

async def docs_processing_fun_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global processed_media_group_ids

    user = update.message.from_user
    chat = update.message.chat

    if update.message.media_group_id:
        media_group_id = update.message.media_group_id
        if media_group_id not in processed_media_group_ids:
            await context.bot.send_message(chat.id, "Sorry, this action is not allowed for multiple files uploaded together.")
            processed_media_group_ids.add(media_group_id)
    else:
        document = update.message.document
        file_name = document.file_name
        mime_type = document.mime_type
        file_size = document.file_size

        text = (
            f"File Name: {file_name}\n"
            f"Mime Type: {mime_type}\n"
            f"File Size: {file_size} bytes\n"
        )

        await context.bot.send_message(chat.id, text)
        await context.bot.send_message(chat.id, update)




async def docs_processing_fun (update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.message.chat
    document = update.message.document

    file_name = document.file_name
    mime_type = document.mime_type
    file_size = document.file_size

    text = (
        f"File Name: {file_name}\n"
        f"Mime Type: {mime_type}\n"
        f"File Size: {file_size} bytes\n"
    )

    await context.bot.send_message(chat.id, text)
    await context.bot.send_message(chat.id, update)









def main() -> None:
    """Start the bot."""
    application = Application.builder().token("6780033449:AAFKWBuWlPcBHLm303owSEvDriPZjCxs9ZU").build()

    application.add_handler(CommandHandler("show_chats", show_chats, block= False))
    application.add_handler(CommandHandler("user", user_checking, block= False))
    application.add_handler(CommandHandler("a", user_checking, block= False))
    application.add_handler(CommandHandler("k", kick_user, block= False))
    application.add_handler(CommandHandler("kick", kick_user, block= False))
    application.add_handler(CommandHandler("u", unban_user, block= False))
    application.add_handler(CommandHandler("d", del_chat_photo, block= False))
    application.add_handler(CommandHandler("e", update_msg_1, block= False))
    application.add_handler(CommandHandler("f", send_msg_and_del, block= False))
    application.add_handler(CommandHandler("g", edit_msg_continuously, block= False))

    application.add_handler(MessageHandler(filters.Document.ALL, docs_processing_fun, block= False))
    application.add_handler(MessageHandler(filters.PHOTO, image_processing_fun, block= False))
    application.add_handler(MessageHandler(filters.REPLY, reply_msg_fun, block= False))
    application.add_handler(MessageHandler(filters.REPLY, delete_msgs_from, block= False))
    application.add_handler(MessageHandler(filters.Caption(["new"]), photo_with_caption))
    application.add_handler(MessageHandler(filters.ALL, start_private_chat))

    application.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(ChatJoinRequestHandler(join_req_fun, block= False))

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()
