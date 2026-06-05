import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "7677853690:AAEojBCXKBPuC9ZolL42X9XDiU4CJbh84XM"
ADMIN_GROUP_ID = -1003918137281

logging.basicConfig(level=logging.INFO)

new_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   user = update.effective_user
   new_users.add(user.id)
   await update.message.reply_text("أهلاً بالقارئ الكريم!")

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
   user = update.effective_user
   message = update.message.text
   text = f"📩 رسالة من @{user.username or user.first_name}\nID:{user.id}\n\n{message}"
   await context.bot.send_message(chat_id=ADMIN_GROUP_ID, text=text)
   if user.id not in new_users:
       new_users.add(user.id)
       await update.message.reply_text("أهلاً بالقارئ الكريم! تم إرسال رسالتك، شكراً! ✅")
   else:
       await update.message.reply_text("تم إرسال رسالتك، شكراً! ✅")

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
   if update.effective_chat.id != ADMIN_GROUP_ID:
       return
   if not update.message.reply_to_message:
       return
   original = update.message.reply_to_message.text
   if not original or "ID:" not in original:
       return
   try:
       user_id = int(original.split("ID:")[1].split("\n")[0].strip())
       await context.bot.send_message(chat_id=user_id, text=update.message.text)
       await update.message.reply_text("✅.")
   except Exception:
       await update.message.reply_text("تعذر إرسال الرد.")

def main():
   app = ApplicationBuilder().token(TOKEN).build()
   app.add_handler(CommandHandler("start", start))
   app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Chat(ADMIN_GROUP_ID), handle_admin_reply))
   app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
   app.run_polling()

if __name__ == "__main__":
   main()
