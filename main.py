import re
import asyncio
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# === BOT TOKEN ===
TOKEN = '7559696217:AAFesX46-0R3FwFcMCqJ9VtNo6EblreZtVE'

# === MANBA GURUHLAR ID’LARI
SOURCE_GROUPS = [
    -1001897186249,
    -1001580463680,
    -1001538155301,
    -1001586456059,
    -1001855230331
]

# === MAQSAD GURUHLAR
GROUP_UMUMIY = -1001963547587
GROUP_RUS = -1002608975373

# === Foydali funksiyalar
def escape_md(text):
    return re.sub(r'([\\()])', r'\\\1', text or '')

def is_russian(text):
    return bool(re.search(r'[А-Яа-яЁё]', text))

def mask_phone(text):
    return re.sub(r'\+?\d[\d\s\-()]{6,}', '*****', text)

# === /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot ishga tushdi.")

# === Asosiy handler
async def forward_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = msg.from_user
    chat = msg.chat

    if not msg.text or msg.photo or msg.sticker:
        return

    text = msg.text
    masked = mask_phone(text)
    rus = is_russian(text)
    target = GROUP_RUS if rus else GROUP_UMUMIY

    try:
        await msg.delete()
    except:
        pass

    info_msg = await context.bot.send_message(chat.id, "📨 Xabaringiz haydovchilarga yuborildi.")
    await asyncio.sleep(15)
    try:
        await info_msg.delete()
    except:
        pass

    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Foydalanuvchi"
    user_link = f"[{escape_md(full_name)}](tg://user?id={user.id})"
    phone = f"\n📞 Telefon: +{user.phone}" if getattr(user, 'phone', None) else ""

    if chat.username:
        group_text = f"[GURUHDAN KELDI](https://t.me/{chat.username})"
    else:
        group_text = "GURUHDAN KELDI"

    caption = f"{escape_md(masked)}\n\n👤 Yuboruvchi: {user_link}{phone}\n{group_text}"

    await context.bot.send_message(
        chat_id=target,
        text=caption,
        parse_mode="Markdown"
    )

# === Main funksiyasi
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Chat(SOURCE_GROUPS) & filters.TEXT, forward_handler))
    print("🚀 Bot ishga tushdi.")
    app.run_polling()

if __name__ == "__main__":
    main()
