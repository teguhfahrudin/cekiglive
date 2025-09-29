import os
import time
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

def cek_instagram(username: str) -> str:
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text
        if "Sorry, this page isn't available." in html or "Page Not Found" in html:
            return f"{username}: ❌ Tidak ditemukan"
        elif 'property="og:type" content="profile"' in html or "profilePage_" in html:
            return f"{username}: ✅ Ada (profil aktif)"
        else:
            return f"{username}: ❓ Ambigu / butuh login"
    except Exception as e:
        return f"{username}: ⚠️ Error ({e})"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim list username IG (max 10 per pesan).")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usernames = update.message.text.split()
    if len(usernames) > 10:
        await update.message.reply_text("Maksimal 10 username sekali cek.")
        return

    for i, u in enumerate(usernames, start=1):
        hasil = cek_instagram(u.strip())
        await update.message.reply_text(hasil)

        time.sleep(2)  # jeda antar akun
        if i % 5 == 0:
            await update.message.reply_text("⏳ Jeda 10 detik...")
            time.sleep(10)

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    import telegram
    print("python-telegram-bot version:", telegram.__version__)  # debug
    main()
