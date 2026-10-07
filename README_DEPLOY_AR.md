# نشر بوت الاذكار ليعمل 24 ساعة بلا حاسوب

Telegram لا يستضيف البوتات. البوت يحتاج دارا تحرسه مثل Render المجاني.
بهذا يبقى يعمل حتى بعد اطفاء حاسوبك وكانه عند Telegram.

## الخطوات

1- اذهب الى BotFather في Telegram واصنع بوتا جديدا وانسخ التوكن الجديد ولا تنشره
2- ارفع مجلد telegram_bot الى GitHub
3- ادخل موقع Render واختر New ثم Background Worker واربط مستودعك
4- Build: pip install -r telegram_bot/requirements.txt
   Start: python telegram_bot/bot.py
5- اضف متغير البيئة BOT_TOKEN والصق فيه التوكن
6- اضغط Deploy وانتظر ثم جرب في Telegram ارسل /start لبوتك
7- للتذكير التلقائي ارسل /remind مرة واحدة في البوت

## تجربة محلية

pip install -r telegram_bot/requirements.txt
set BOT_TOKEN=التوكن (ويندوز) ثم python telegram_bot/bot.py

## الاوامر

/start - الازرار
/random - ذكر عشوائي
/remind - تفعيل رسائل الصباح 7:00 والمساء 18:00
