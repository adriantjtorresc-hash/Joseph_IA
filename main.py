import os
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram import Update
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=GROQ_KEY,
    base_url="https://api.groq.com/openai/v1"
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_text}]
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Uy, tuve un error, intenta de nuevo.")

def main():
    print("Bot Joseph iniciando...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
