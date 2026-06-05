import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "7677853690:AAEojBCXKBPuC9ZolL42X9XDiU4CJbh84XM"
ADMIN_GROUP_ID = -1003918137281

logging.basicConfig(level=logging.INFO)

new_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_users.add(update.effective_user.id)
    await update.message.reply_text("أهلاً بالقارئ الكريم!")

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text
    text = f"📩 رسالة جديدة من @{user.username or user.first_name}:\n\n{message}"
    await context.bot.send_message(chat_id=ADMIN_GROUP_ID, text=text)
    if user.id not in new_users:
        new_users.add(user.id)
        await update.message.reply_text("أهلاً بالقارئ الكريم! تم إرسال رسالتك، شكراً! ✅")
    else:
        await update.message.reply_text("تم إرسال رسالتك، شكراً! ✅")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
    app.run_polling()

if __name__ == "__main__":
    main()
