import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот с ChatGPT. Напиши что-нибудь.")

def chatgpt_response(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": text}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    update.message.chat.send_action(action="typing")
    reply = chatgpt_response(user_text)
    update.message.reply_text(reply)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()