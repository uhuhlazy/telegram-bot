import os
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

SPAM_WORDS = [
    "подарок","подарочки","подарок из профиля","подарочек из профиля",
    "приз","призы","выиграли","выигрыш","розыгрыш",
    "акция","акции","бонус","бонусы",
    "скидка","скидки","скидк","дешево","дёшево",
    "инвести","инвест","инвестировать",
    "крипт","крипта","криптовалют",
    "nft","куплю nft","купить nft","продам nft",
    "хочу nft","твое nft","твой nft",
    "куплю кот","куплю кота","купить кота","купить кот",
    "кот куплю","котик куплю","котика куплю","котёнка куплю",
    "куплю твоего кота",
    "куплю","купить","хочу купить","готов купить",
    "интересует покупка","предложение покупки",
    "предлагаю купить","куплю у тебя",
    "куплю твой подарок","купить подарок",
    "купить твой подарок","куплю подарок из профиля",
    "куплю твой подарок из профиля",
    "срочно","очень срочно",
    "перейди","перейди по ссылке","ссылка","по ссылке"
]

REPLY_TEXT = "Ваше сообщение было автоматически помечено как спам. Дальнейшая переписка по данному вопросу не ведется."


async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text:
        return

    text = msg.text.lower()

    for word in SPAM_WORDS:
        if word in text:
            await msg.reply_text(REPLY_TEXT)
            return


async def main():
    token = os.environ.get("BOT_TOKEN")

    print("BOT_TOKEN length:", len(token) if token else "None")

    if not token:
        print("ERROR: BOT_TOKEN missing")
        return

    # Создаем приложение
    application: Application = (
        ApplicationBuilder()
        .token(token)
        .build()
    )

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spam))

    print("Initializing bot...")
    await application.initialize()

    print("Starting bot...")
    await application.start()

    print("Bot is running. Polling is active!")

    # Блокируем до конца (run_polling больше не используем!)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
