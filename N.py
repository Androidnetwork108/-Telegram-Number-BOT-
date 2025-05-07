# Its Maked by:- @Hindu_papa 

import asyncio
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import Forbidden, NetworkError
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
contact_shared = {}

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"⚠️ Update {update} caused error: {context.error}")
    if isinstance(context.error, Forbidden):
        user_id_info = getattr(update.effective_user, 'id', 'N/A')
        chat_id_info = getattr(update.effective_chat, 'id', 'N/A')
        error_message = str(context.error).lower()
        if "bot was blocked by the user" in error_message:
            print(f"🚫 Bot was blocked by user {user_id_info} in chat {chat_id_info}.")
        elif "user is deactivated" in error_message:
            print(f"🚫 User {user_id_info} is deactivated.")
        elif "chat not found" in error_message:
            print(f"🚫 Chat {chat_id_info} not found.")
        else:
            print(f"🚫 A Forbidden error occurred: {context.error} (User: {user_id_info}, Chat: {chat_id_info})")
    elif isinstance(context.error, NetworkError):
        print(f"🌐 A NetworkError occurred: {context.error}.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if 'contact_check_task' in context.user_data:
        try:
            context.user_data['contact_check_task'].cancel()
        except Exception as e:
            print(f"Error cancelling previous task for user {user_id}: {e}")

    contact_shared[user_id] = False

    welcome_message = "Welcome to our VIP 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙥𝙧𝙞𝙢𝙞𝙪𝙢👑💎 BOT! ⚠️ please don't misused this BOT. ★𝟏st click 👇(𝘾𝙡𝙞𝙘𝙠 𝙈𝙚)👇 Button & allow permission."
    keyboard = [[KeyboardButton(text="💎Click Me💎", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    try:
        await update.message.reply_text(text=welcome_message, reply_markup=reply_markup)
    except Forbidden as e:
        if "bot was blocked by the user" in str(e).lower():
            print(f"🚫 Failed to send welcome message to {user_id} in {chat_id}: Bot blocked.")
        else:
            print(f"🚫 Forbidden sending welcome: {e}")

    async def check_contact_task_function():
        try:
            await asyncio.sleep(180)
            if user_id in contact_shared and not contact_shared[user_id]:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="★Request failed! Please give me permission. Tap ( 💎Click Me💎 ) button 🔘."
                )
        except asyncio.CancelledError:
            raise
        except Forbidden as e:
            print(f"🚫 Reminder error to {user_id}: {e}")
        except Exception as e:
            print(f"Error in reminder task for {user_id}: {e}")
        finally:
            if 'contact_check_task' in context.user_data and context.user_data['contact_check_task'].done():
                del context.user_data['contact_check_task']

    context.user_data['contact_check_task'] = asyncio.create_task(check_contact_task_function())

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    contact_shared[user_id] = True

    if 'contact_check_task' in context.user_data:
        try:
            context.user_data['contact_check_task'].cancel()
        except Exception as e:
            print(f"Error cancelling task: {e}")

    msg = "Nice👍 ★Now share this bot username ( @T_G_primium_108Bot ) 3-5 friends! Then i give you TG PRIMIUM👑💎 THX 🙏."
    try:
        await update.message.reply_text(msg)
    except Forbidden as e:
        print(f"🚫 Error sending contact reply to {user_id}: {e}")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_error_handler(error_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    print("Bot started...")
    application.run_polling()

if __name__ == "__main__":
    main()
