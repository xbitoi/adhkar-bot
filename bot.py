# -*- coding: utf-8 -*-
"""بوت اذكار وادعية - يعمل بالازرار + رسائل تلقائية. التوكن من متغير البيئة BOT_TOKEN فقط."""
import os
import logging
import random
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

try:
    from adhkar import ADHKAR_SABAH, ADHKAR_MASAA, ADHKAR_NAWM, ADIYA
except ImportError:
    from telegram_bot.adhkar import ADHKAR_SABAH, ADHKAR_MASAA, ADHKAR_NAWM, ADIYA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("اذكار الصباح", callback_data="sabah"),
         InlineKeyboardButton("اذكار المساء", callback_data="masaa")],
        [InlineKeyboardButton("اذكار النوم", callback_data="nawm"),
         InlineKeyboardButton("ادعية", callback_data="duaa")],
        [InlineKeyboardButton("ذكر عشوائي", callback_data="random")],
    ])

def format_list(items, title):
    lines = [f"{title}\n"]
    for i, d in enumerate(items, 1):
        if isinstance(d, dict):
            lines.append(f"{i}- {d['text']}\nفضل: {d.get('fadl','')}\n")
        else:
            lines.append(f"{i}- {d}\n")
    return "\n".join(lines)

async def send_long(message, text):
    # Telegram حد 4096 حرف
    for i in range(0, len(text), 4000):
        await message.reply_text(text[i:i+4000])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "السلام عليكم ورحمة الله\nانا بوت الاذكار والادعية\nاختر من الازرار او ارسل /random لذكر عشوائي",
        reply_markup=main_keyboard()
    )

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data == "sabah":
        await send_long(q.message, format_list(ADHKAR_SABAH, "اذكار الصباح"))
    elif data == "masaa":
        await send_long(q.message, format_list(ADHKAR_MASAA, "اذكار المساء"))
    elif data == "nawm":
        await send_long(q.message, format_list(ADHKAR_NAWM, "اذكار النوم"))
    elif data == "duaa":
        await send_long(q.message, format_list(ADIYA[:10], "ادعية مختارة"))
    elif data == "random":
        pool = ADHKAR_SABAH + ADHKAR_MASAA + [{"text": d} if isinstance(d, str) else d for d in ADIYA]
        pick = random.choice(pool)
        txt = pick["text"] if isinstance(pick, dict) else str(pick)
        await q.message.reply_text(f"ذكر لك:\n{txt}", reply_markup=main_keyboard())
    await q.message.reply_text("اختر مجددا:", reply_markup=main_keyboard())

async def random_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_items = ADHKAR_SABAH + ADHKAR_MASAA + ADHKAR_NAWM
    pick = random.choice(all_items + [{"text": d, "fadl": "دعاء"} for d in ADIYA])
    await update.message.reply_text(f"{pick['text']}\n\nفضل: {pick.get('fadl','')}")

async def morning_job(context: ContextTypes.DEFAULT_TYPE):
    # ترسل لاول دردشة معروفة - الافضل: البوت يرسل لمن ضغط /start فقط اذا حفظنا chat_id
    # نبقيها بسيطة: لا شيء هنا الا لمن فعل التذكير
    pass

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # تذكير صباحي 7:00 ومسائي 18:00 بتوقيت الدار البيضاء
    # نحذف القديم ثم نضيف
    for job in context.job_queue.get_jobs_by_name(str(chat_id)):
        job.schedule_removal()
    t_morning = datetime.time(hour=7, minute=0)
    t_evening = datetime.time(hour=18, minute=0)
    context.job_queue.run_daily(
        lambda ctx: ctx.bot.send_message(chat_id=chat_id, text="اصبحنا واصبح الملك لله\n" + random.choice(ADHKAR_SABAH)["text"]),
        time=t_morning, name=str(chat_id)
    )
    context.job_queue.run_daily(
        lambda ctx: ctx.bot.send_message(chat_id=chat_id, text="امسينا وامسى الملك لله\n" + random.choice(ADHKAR_MASAA)["text"]),
        time=t_evening, name=str(chat_id)
    )
    await update.message.reply_text("تم تفعيل التذكير الصباحي والمسائي لك باذن الله")

def main():
    token = os.environ.get("BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit("ضع التوكن في متغير البيئة BOT_TOKEN ثم شغل البوت")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("random", random_cmd))
    app.add_handler(CommandHandler("remind", subscribe))
    app.add_handler(CallbackQueryHandler(on_button))
    logger.info("البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
