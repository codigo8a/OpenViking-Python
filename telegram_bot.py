import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from memory import memory
from config import TELEGRAM_TOKEN, NGROK_AUTHTOKEN
from agent import OpenVikingAgent
from logger import get_logger
import os
import subprocess
from pyngrok import ngrok

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

async def start_ssh_ngrok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not NGROK_AUTHTOKEN:
        await update.message.reply_text("❌ No se encontró NGROK_AUTHTOKEN en los Secretos de Colab.")
        return

    await update.message.reply_text("⏳ Configurando SSH y Ngrok (esto tardará unos segundos)...")
    
    try:
        # 1. Configurar SSH
        subprocess.run(["apt-get", "update"], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["apt-get", "install", "-y", "openssh-server"], check=True, stdout=subprocess.DEVNULL)
        os.makedirs("/var/run/sshd", exist_ok=True)
        
        # Permitir login root
        with open("/etc/ssh/sshd_config", "a") as f:
            f.write("\nPermitRootLogin yes\nPasswordAuthentication yes\n")
            
        # Poner contraseña temporal
        temp_pass = "viking123"
        subprocess.run(f"echo 'root:{temp_pass}' | chpasswd", shell=True, check=True)
        
        subprocess.run(["service", "ssh", "start"], check=True)

        # 2. Configurar Ngrok
        ngrok.set_auth_token(NGROK_AUTHTOKEN)
        ssh_tunnel = ngrok.connect(22, "tcp")
        
        url = ssh_tunnel.public_url.replace("tcp://", "")
        host, port = url.split(":")
        
        msg = (
            "✅ **Conexión SSH Activa**\n\n"
            f"📍 **Host:** `{host}`\n"
            f"🔹 **Puerto:** `{port}`\n"
            f"👤 **Usuario:** `root` \n"
            f"🔑 **Pass temporal:** `{temp_pass}`\n\n"
            f"📟 **Comando:**\n`ssh root@{host} -p {port}`"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Error starting ngrok: {e}")
        await update.message.reply_text(f"❌ Error al configurar el túnel: {e}")

def run_bot():
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not found in .env")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("historymem", show_history))
    application.add_handler(CommandHandler("ngrok", start_ssh_ngrok))
    
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(msg_handler)
    
    logger.info("Starting Telegram bot...")
    application.run_polling()

if __name__ == "__main__":
    run_bot()
