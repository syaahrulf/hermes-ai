import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# ======================
# ENV
# ======================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ======================
# OPENROUTER CLIENT
# ======================
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# ======================
# 9 MODELS ROUTER
# ======================
MODELS = [
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    "anthropic/claude-3.5-sonnet",
    "anthropic/claude-3-haiku",
    "google/gemini-1.5-pro",
    "google/gemini-1.5-flash",
    "deepseek/deepseek-chat",
    "qwen/qwen-2.5-72b-instruct",
    "meta-llama/llama-3.1-70b-instruct"
]

def pick_model():
    return random.choice(MODELS)

# ======================
# START COMMAND
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hermes aktif 🚀")

# ======================
# CHAT AI
# ======================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text

        model = pick_model()

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message.content

        await update.message.reply_text(
            f"🤖 Model: {model}\n\n{reply}"
        )

    except Exception as e:
        await update.message.reply_text(f"Error AI: {str(e)}")

# ======================
# MAIN APP
# ======================
def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN belum di-set")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    # handler WAJIB ini (ini yang tadi hilang di kamu)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Hermes AI running...")
    app.run_polling()

if __name__ == "__main__":
    main()
