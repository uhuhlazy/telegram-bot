import os
import asyncio
from aiohttp import web

from telegram import Update
from telegram.ext import Application, ApplicationBuilder, MessageHandler, filters, ContextTypes

# ------------------ СПАМ-СПИСОК ------------------

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


# ------------------ БОТ ------------------

async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text:
        return
    text = msg.text.lower()
    for spam in SPAM_WORDS:
        if spam in text:
            await msg.reply_text(REPLY_TEXT)
            return


async def start_bot():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("ERROR: BOT_TOKEN not set")
        return

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )
    app.add_handler(MessageHandler(filters.TEXT, check_spam))

    # Запуск бота без run_polling
    await app.initialize()
    await app.start()
    print("Telegram bot started!")

    # Telegram API требует, чтобы бот не выключался
    await asyncio.Event().wait()


# ------------------ ВЕБ-СЕРВЕР ДЛЯ RENDER ------------------

async def start_web():
    async def handle(request):
        return web.Response(text="OK")

    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 10000)))
    await site.start()
    print("Web server started!")


# ------------------ ОБЩИЙ ЗАПУСК ------------------

async def main():
    await asyncio.gather(
        start_bot(),
        start_web()
    )

if __name__ == "__main__":
    asyncio.run(main())
