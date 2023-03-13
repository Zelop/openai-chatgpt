import logging
import config
import uuid
from pydub import AudioSegment
from utils import get_text_from_audio, send_chat_msg, clear_db

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user = update.effective_user
    if update.message.chat_id in config.telegram_whitelist:
        await update.message.reply_html(
            rf"Hi {user.mention_html()}, your ID is {update.message.chat_id}, you ARE whitelisted, resetting DB!",
            reply_markup=ForceReply(selective=True),
        )
        await clear_db(update)
    else:
        await update.message.reply_html(
            rf"Hi {user.mention_html()}, your ID is {update.message.chat_id}, you are NOT whitelisted!",
            reply_markup=ForceReply(selective=True),
        )


async def read_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat_id not in config.telegram_whitelist:
        await update.message.reply_text("Unauthorized")
    elif update.message.text.lower() == "reset":
        await clear_db(update)
    else:
        await update.message.reply_text(await send_chat_msg(update))


async def listen_audio(update: Update, context) -> None:
    if update.message.chat_id in config.telegram_whitelist:
        audio_file = await context.bot.get_file(update.message.voice.file_id)
        # TODO use UUIDs then remove.
        file_name = str(uuid.uuid4())
        await audio_file.download_to_drive("audios/" + file_name + ".ogg")
        AudioSegment.from_ogg("audios/" + file_name + ".ogg").export("audios/" + file_name + ".wav", format="wav")

        replytext = await get_text_from_audio("audios/" + file_name + ".wav")
        print(replytext)
        await update.message.reply_text(await send_chat_msg(update, replytext["text"]))


def main() -> None:
    application = Application.builder().token(config.telegram_key).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, read_text))
    application.add_handler(MessageHandler(filters.VOICE & ~filters.COMMAND, listen_audio))

    application.run_polling()


if __name__ == "__main__":
    main()
