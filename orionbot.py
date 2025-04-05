import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TELEGRAM_TOKEN, OPENAI_API_KEY
import openai

openai.api_key = OPENAI_API_KEY

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text(
        "Я — юридический помощник OrionBot. Вы можете задать вопрос, связанный с законодательством РФ."
    )

def handle_message(update, context):
    text = update.message.text.lower()

    if any(word in text for word in ["президент", "путин", "зеленский", "политика", "война"]):
        update.message.reply_text("Извините, я не обрабатываю политические темы. Пожалуйста, задайте юридический вопрос.")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты юридический помощник. Отвечай строго по теме, официальным языком, коротко."},
                {"role": "user", "content": update.message.text}
            ]
        )
        reply = response['choices'][0]['message']['content']
        update.message.reply_text(reply)
    except Exception as e:
        logger.error(e)
        update.message.reply_text("Произошла ошибка при получении ответа от ИИ.")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
