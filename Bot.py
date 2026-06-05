import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = "7677853690:AAEojBCXKBPuC9ZolL42X9XDiU4CJbh84XM"
ADMIN_GROUP_ID = -1003918137281

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await update.message.reply_text("أهلاً بالقارئ الكريم!\n\nأرسل لنا اقتراحاتك وتعليقاتك.")

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
   user = update.effective_user
   message = update.message.text
   
   text = f"📩 رسالة جديدة من @{user.username or user.first_name}:\n\n{message}"
   
   await context.bot.send_message(chat_id=ADMIN_GROUP_ID, text=text)
   await update.message.reply_text("تم إرسال رسالتك، شكراً! ✅")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
app.run_polling()
