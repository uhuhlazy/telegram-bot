import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# ---------- СПАМ-СЛОВА ----------

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
    "перейди","перейди по ссылке","ссылка","по ссылке",
]

REPLY_TEXT = (
    "Ваше сообщение было автоматически помечено как спам. "
    "Дальнейшая переписка по данному вопросу не ведется."
)

# ---------- ОБРАБОТЧИК СПАМА ----------

async def check_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text:
        return

    text = msg.text.lower()

    for word in SPAM_WORDS:
        if word in text:
            await msg.reply_text(REPLY_TEXT)
            return

# ---------- ТУПОЙ HTTP-СЕРВЕР ДЛЯ RENDER ----------

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OK\n")

    # глушим лишние логи
    def log_message(self, format, *args):
        return


def start_http_server():
    port = int(os.environ.get("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"HTTP server listening on 0.0.0.0:{port}")
    server.serve_forever()

# ---------- ЗАПУСК БОТА ----------

def main():
    # поднимаем HTTP-сервер в отдельном потоке
    threading.Thread(target=start_http_server, daemon=True).start()

    token = os.environ.get("BOT_TOKEN")
    print("BOT_TOKEN length:", len(token) if token else "None")

    if not token:
        print("ERROR: BOT_TOKEN not set")
        return

    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_spam))

    print("Telegram bot starting polling...")
    # ВАЖНО: тут БЕЗ asyncio.run, просто обычный run_polling
    app.run_polling()


if __name__ == "__main__":
    main()

