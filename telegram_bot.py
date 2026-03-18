import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from memory import memory
from config import TELEGRAM_TOKEN
from agent import OpenVikingAgent
from logger import get_logger

logger = get_logger("telegram")
agent = OpenVikingAgent()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    
    logger.info(f"Telegram msg from {chat_id}: {user_text}")
    
    # Notify user we are thinking
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    try:
        response = agent.execute_task(user_text)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Telegram agent error: {e}")
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"History request from {chat_id}")
    
    history = memory.get_history(limit=10)
    await update.message.reply_text(history, parse_mode="Markdown")

def run_bot():
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not found in .env")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("historymem", show_history))
    
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(msg_handler)
    
    logger.info("Starting Telegram bot...")
    application.run_polling()

if __name__ == "__main__":
    run_bot()
