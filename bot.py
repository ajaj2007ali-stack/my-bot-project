import telebot
from telebot import types
import requests
import time
import json

# 🌐 بيانات الـ API
API_URL = "https://foloiq.com/api/v2"
API_KEY = "5d97af2902dacc9a4e2d2bbd6885b99c"

# 📢 قناة الاشتراك الإجباري
CHANNEL_USERNAME = "@Sultan_Follow"

# 📸 خدمات إنستغرام
INSTAGRAM_SERVICES = {
"📸 | متابعين انستغرام | 1000 بـ 15,000 نقطة": {"id": 8023, "points": 15000},
"📸 | متابعين حقيقي | 1000 بـ 20,000 نقطة": {"id": 7296, "points": 20000},
"📸 | لايكات ضمان مدى الحياة | 1000 بـ 3,000 نقطة": {"id": 8712, "points": 3000},
"📸 | لايكات نقص قليل | 1000 بـ 2,500 نقطة": {"id": 8603, "points": 2500},
"📸 | لايكات عرب 30 يوم | 1000 بـ 8,000 نقطة": {"id": 8559, "points": 8000},
"📸 | مشاهدات بدون ضمان | 1000 بـ 500 نقطة": {"id": 8194, "points": 500},
"📸 | مشاهدات ضمان 30 يوم | 1000 بـ 750 نقطة": {"id": 7035, "points": 750},
"📸 | عرض مشاهدات انستغرام | 1000 بـ 240 نقطة": {"id": 5912, "points": 240},
"📸 | عرض مشاهدات ضمان 7 ايام | 1000 بـ 500 نقطة": {"id": 4219, "points": 500}
}

# 🎵 خدمات تيك توك
TIKTOK_SERVICES = {
"🎵 | لايكات+مشاهدات ضمان شهر | 1000 بـ 4,000 نقطة": {"id": 8397, "points": 4000},
"🎵 | لايكات+مشاهدات 365 يوم | 1000 بـ 5,000 نقطة": {"id": 8401, "points": 5000},
"🎵 | لايكات ضمان شهر | 1000 بـ 6,000 نقطة": {"id": 8539, "points": 6000},
"🎵 | لايكات ضمان 7 ايام | 1000 بـ 9,000 نقطة": {"id": 8610, "points": 9000},
"🎵 | لايكات ضمان مدى الحياة | 1000 بـ 15,000 نقطة": {"id": 8541, "points": 15000},
"🎵 | مشاهدات ضمان 30 يوم | 1000 بـ 500 نقطة": {"id": 8845, "points": 500},
"🎵 | مشاهدات اعلان ممول | 1000 بـ 20,000 نقطة": {"id": 7285, "points": 20000},
"🎵 | مشاهدات ضمان 60 يوم | 1000 بـ 2,000 نقطة": {"id": 8706, "points": 2000},
"🎵 | مشاهدات بث | 1000 بـ 20,000 نقطة": {"id": 8735, "points": 20000},
"🎵 | مشاهدات بث عربي | 1000 بـ 30,000 نقطة": {"id": 8736, "points": 30000},
"🎵 | متابعين حقيقي 15 يوم | 1000 بـ 60,000 نقطة": {"id": 8103, "points": 60000},
"🎵 | متابعين حسابات مميزة | 1000 بـ 7963 نقطة": {"id": 7963, "points": 62000},
"🎵 | مشاركات بدون ضمان | 1000 بـ 15,000 نقطة": {"id": 8091, "points": 15000},
"🎵 | مشاركات ضمان | 1000 بـ 16,000 نقطة": {"id": 8092, "points": 16000},
"🎵 | حفظ بدون ضمان | 1000 بـ 500 نقطة": {"id": 8363, "points": 500},
"🎵 | حفظ ضمان مدى الحياة | 1000 بـ 5,000 نقطة": {"id": 8364, "points": 5000},
"🎵 | تعليقات عشوائية ضمان | 1000 بـ 35,000 نقطة": {"id": 8618, "points": 35000},
"🎵 | رشق سكور | 1000 بـ 19,000 نقطة": {"id": 7510, "points": 19000},
"🎵 | اعجابات ستوري | 1000 بـ 16,000 نقطة": {"id": 5419, "points": 16000}
}

# ✈️ خدمات تلجرام
TELEGRAM_SERVICES = {
"✈️ | مشتركون بوت ضمان 30 يوم | 1000 بـ 8,000 نقطة": {"id": 8511, "points": 8000},
"✈️ | مشتركون بوت 365 يوم | 1000 بـ 9,000 نقطة": {"id": 8515, "points": 9000},
"✈️ | اعضاء قناة مدى الحياة | 1000 بـ 8,500 نقطة": {"id": 8516, "points": 8500},
"✈️ | اعضاء مميزون 60 يوم | 1000 بـ 25,000 نقطة": {"id": 6625, "points": 25000},
"✈️ | اعضاء كروب | 1000 بـ 14,000 نقطة": {"id": 6156, "points": 14000},
"✈️ | مشاهدات منشور | 1000 بـ 500 نقطة": {"id": 4608, "points": 500},
"✈️ | مشاهدات 10 منشورات | 1000 بـ 2,000 نقطة": {"id": 4610, "points": 2000},
"✈️ | مشاهدة ستوري | 1000 بـ 7,000 نقطة": {"id": 5221, "points": 7000},
"✈️ | مشاهدات مستقبلية | 1000 بـ 5,000 نقطة": {"id": 7670, "points": 5000},
"✈️ | تصويت مسابقات | 1000 بـ 8,000 نقطة": {"id": 7386, "points": 8000}
}

# 📘 خدمات فيس بوك
FACEBOOK_SERVICES = {
"📘 | متابعين حساب شخصي حقيقي ضمان شهر | 1000 بـ 4,000 نقطة": {"id": 8642, "points": 4000},
"📘 | متابعين حساب شخصي ضمان سنة | 1000 بـ 5,000 نقطة": {"id": 8861, "points": 5000},
"📘 | مشتركين البيج + متابعين البيج | 1000 بـ 14,000 نقطة": {"id": 5808, "points": 14000},
"📘 | اعضاء مجموعة ضمان شهر | 1000 بـ 4,000 نقطة": {"id": 8724, "points": 4000},
"📘 | طلبات صداقة | 1000 بـ 25,000 نقطة": {"id": 8767, "points": 25000},
"📘 | مشاهدات الفيديو | 1000 بـ 30,000 نقطة": {"id": 5013, "points": 30000}
}

# ✖️ خدمات تويتر
TWITTER_SERVICES = {
"✖️ | متابعين ضمان شهر | 1000 بـ 40,000 نقطة": {"id": 8848, "points": 40000},
"✖️ | متابعين بوت بدون ضمان | 1000 بـ 17,000 نقطة": {"id": 8543, "points": 17000},
"✖️ | مشاهدات فيديو جودة عالية | 1000 بـ 500 نقطة": {"id": 8241, "points": 500},
"✖️ | لايكات ضمان 7 يوم | 1000 بـ 30,000 نقطة": {"id": 8763, "points": 30000}
}

# 🧵 خدمات ثريدز
THREADS_SERVICES = {
"🧵 | متابعين ضمان | 1000 بـ 55,000 نقطة": {"id": 3559, "points": 55000},
"🧵 | لايكات ضمان | 1000 بـ 160,000 نقطة": {"id": 3564, "points": 160000}
}

# 🎧 خدمات سبوتي فاي
SPOTIFY_SERVICES = {
"🎧 | متابعين حقيقي ضمان مدى الحياة | 1000 بـ 17,000 نقطة": {"id": 8662, "points": 17000},
"🎧 | مشاهدات مضمونة | 1000 بـ 13,000 نقطة": {"id": 8660, "points": 13000},
"🎧 | حفظ جودة مضمونة | 1000 بـ 16,000 نقطة": {"id": 8661, "points": 16000}
}

# 🟢 خدمات كيك
KICK_SERVICES = {
"🟢 | مشاهدات بث فوري | 1000 بـ 2,000 نقطة": {"id": 5461, "points": 2000},
"🟢 | مشاهدات فوري ضمان 150 دقيقة | 1000 بـ 20,000 نقطة": {"id": 5466, "points": 20000}
}

# 🔴 خدمات يوتيوب
YOUTUBE_SERVICES = {
"🔴 | اشتрак بريميوم مدى الحياة | 1000 بـ 20,000 نقطة": {"id": 8373, "points": 20000},
"🔴 | مشتركين يوتيوب حقيقي ضمان مدى الحياة | 1000 بـ 18,000 نقطة": {"id": 8750, "points": 18000},
"🔴 | مشاهدات حقيقية ضمان مدى الحياة | 1000 بـ 16,000 نقطة": {"id": 8855, "points": 16000},
"🔴 | لايكات + تعليقات ضمان 90 يوم | 1000 بـ 6,000 نقطة": {"id": 6163, "points": 6000},
"🔴 | لايكات ضمان 100 يوم | 1000 بـ 8,000 نقطة": {"id": 6995, "points": 8000},
"🔴 | مشاهدات بث | 1000 بـ 2,000 نقطة": {"id": 6058, "points": 2000},
"🔴 | مشاهدات يوتيوب تحقيق الارباح | 1000 بـ 105,000 نقطة": {"id": 7373, "points": 105000}
}

ALL_SERVICES = {
**INSTAGRAM_SERVICES, **TIKTOK_SERVICES, **TELEGRAM_SERVICES,
**FACEBOOK_SERVICES, **TWITTER_SERVICES, **THREADS_SERVICES,
**SPOTIFY_SERVICES, **KICK_SERVICES, **YOUTUBE_SERVICES
}
SERVICES_BY_ID = {data["id"]: {"name": name, "points": data["points"]} for name, data in ALL_SERVICES.items()}

# 💾 ملف حفظ البيانات
import os as _os
DATA_FILE = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "bot_data.json")

# 🎟️ أكواد النقاط - كل كود يشتغل لـ 5 أشخاص فقط
GIFT_CODES = {
    "p.m": {"points": 5000, "max_uses": 5, "used_by": []},
    "pl0": {"points": 5000, "max_uses": 5, "used_by": []},
    "pl9": {"points": 5000, "max_uses": 5, "used_by": []},
    "pmw": {"points": 5000, "max_uses": 5, "used_by": []},
    "poi": {"points": 5000, "max_uses": 5, "used_by": []},
    "yuo": {"points": 5000, "max_uses": 5, "used_by": []},
    "lki": {"points": 5000, "max_uses": 5, "used_by": []},
    "red": {"points": 5000, "max_uses": 5, "used_by": []},
    "bnj": {"points": 5000, "max_uses": 5, "used_by": []},
    "uhb": {"points": 5000, "max_uses": 5, "used_by": []},
    "fgj": {"points": 5000, "max_uses": 5, "used_by": []},
}

def load_data():
    global USER_BALANCES, USER_DAILY_GIFT, REFERRAL_USED, REFERRED_USERS
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        USER_BALANCES   = {int(k): v for k, v in data.get("balances", {}).items()}
        USER_DAILY_GIFT = {int(k): v for k, v in data.get("daily_gift", {}).items()}
        REFERRAL_USED   = {int(k): int(v) for k, v in data.get("referral_used", {}).items()}
        REFERRED_USERS  = {int(k): set(map(int, v)) for k, v in data.get("referred_users", {}).items()}
    except Exception:
        USER_BALANCES   = {}
        USER_DAILY_GIFT = {}
        REFERRAL_USED   = {}
        REFERRED_USERS  = {}

def save_data():
    data = {
        "balances":       {str(k): v for k, v in USER_BALANCES.items()},
        "daily_gift":     {str(k): v for k, v in USER_DAILY_GIFT.items()},
        "referral_used":  {str(k): str(v) for k, v in REFERRAL_USED.items()},
        "referred_users": {str(k): list(v) for k, v in REFERRED_USERS.items()},
        "gift_codes":     {k: {"points": v["points"], "max_uses": v["max_uses"], "used_by": v["used_by"]} for k, v in GIFT_CODES.items()}
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# تحميل البيانات عند بدء البوت
USER_BALANCES   = {}
USER_DAILY_GIFT = {}
REFERRAL_USED   = {}
REFERRED_USERS  = {}
# 🎟️ أكواد النقاط - كل كود يشتغل لـ 5 أشخاص فقط
GIFT_CODES = {
    "p.m": {"points": 5000, "max_uses": 5, "used_by": []},
    "pl0": {"points": 5000, "max_uses": 5, "used_by": []},
    "pl9": {"points": 5000, "max_uses": 5, "used_by": []},
    "pmw": {"points": 5000, "max_uses": 5, "used_by": []},
    "poi": {"points": 5000, "max_uses": 5, "used_by": []},
    "yuo": {"points": 5000, "max_uses": 5, "used_by": []},
    "lki": {"points": 5000, "max_uses": 5, "used_by": []},
    "red": {"points": 5000, "max_uses": 5, "used_by": []},
    "bnj": {"points": 5000, "max_uses": 5, "used_by": []},
    "uhb": {"points": 5000, "max_uses": 5, "used_by": []},
    "fgj": {"points": 5000, "max_uses": 5, "used_by": []},
}

load_data()

BOT_TOKEN = "8804286947:AAEydiGWGxA7ylGtCs7K5BmDImPfUI9dmww"
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# --- فحص الاشتراك ---
def check_is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

# --- واجهة الاشتراك الإجباري ---
def force_sub_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("اضغط هنا للاشتراك بالقناة 📢", url="https://t.me/Sultan_Follow"))
    markup.row(types.InlineKeyboardButton("تم الاشتراك ✅", callback_data="verify_subscription"))
    return markup

# رسالة ترحيب واحدة تحتوي على الأزرار مباشرة
def get_welcome_text(user_id):
    balance = USER_BALANCES.get(user_id, 0)
    return (
        f"اهلاً بك في بوت السلطان للدعم - @tamgdbot\n"
        f"• البوت مختص لرشق جميع الخدمات والبرامج\n"
        f"سارع بتجربة أسرع وأفضل الخدمات 👋\n\n"
        f"🆔 | ايديك : {user_id}\n"
        f"💎 | عدد نقاطك : {balance} نقطة"
    )

# --- القائمة الرئيسية ---
def main_inline_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("🛒 الخدمات", callback_data="main_services"))
    markup.row(types.InlineKeyboardButton("🎯 تمويل قناتك", callback_data="btn_under_dev"))
    markup.row(
        types.InlineKeyboardButton("💎 تجمع نقاط", callback_data="collect_menu"),
        types.InlineKeyboardButton("💳 استخدام كود", callback_data="use_code_menu")
    )
    markup.row(
        types.InlineKeyboardButton("📅 طلباتي", callback_data="btn_under_dev"),
        types.InlineKeyboardButton("🔍 فحص الطلب", callback_data="check_order_menu")
    )
    markup.row(
        types.InlineKeyboardButton("🪪 الحساب", callback_data="main_account"),
        types.InlineKeyboardButton("💰 شحن نقاط", callback_data="charge_points_menu")
    )
    markup.row(
        types.InlineKeyboardButton("🦾 تحديثات البوت", url="https://t.me/Sultan_Follow"),
        types.InlineKeyboardButton("🔺 شروط الاستخدام", callback_data="btn_under_dev")
    )
    return markup

# --- واجهة الخدمات ---
def services_inline_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("الخدمات المجانية 🎁", callback_data="btn_under_dev"))
    markup.row(
        types.InlineKeyboardButton("تلجرام ✈️", callback_data="tele_menu"),
        types.InlineKeyboardButton("انستغرام 📸", callback_data="insta_menu")
    )
    markup.row(
        types.InlineKeyboardButton("تيك توك 🎵", callback_data="tiktok_menu"),
        types.InlineKeyboardButton("فيس بوك 📘", callback_data="fb_menu")
    )
    markup.row(
        types.InlineKeyboardButton("يوتيوب 🔴", callback_data="yt_menu"),
        types.InlineKeyboardButton("تويتر ✖️", callback_data="twitter_menu")
    )
    markup.row(
        types.InlineKeyboardButton("ثريدز 🧵", callback_data="threads_menu"),
        types.InlineKeyboardButton("كيك 🟢", callback_data="kick_menu")
    )
    markup.row(
        types.InlineKeyboardButton("كواي 🟠", callback_data="btn_under_dev"),
        types.InlineKeyboardButton("سبوتي فاي 🎧", callback_data="spotify_menu")
    )
    markup.row(types.InlineKeyboardButton("قسم الإعلانات 📢", callback_data="btn_under_dev"))
    markup.row(types.InlineKeyboardButton("◀️ رجوع للقائمة الرئيسية", callback_data="back_to_main"))
    return markup

# --- قوائم الخدمات الفرعية ---
def instagram_inline_menu():
    markup = types.InlineKeyboardMarkup()
    for name, data in INSTAGRAM_SERVICES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"ser_{data['id']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع للمنصات", callback_data="platforms_menu"))
    return markup

def tiktok_inline_menu():
    markup = types.InlineKeyboardMarkup()
    for name, data in TIKTOK_SERVICES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"ser_{data['id']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع للمنصات", callback_data="platforms_menu"))
    return markup

def telegram_inline_menu():
    markup = types.InlineKeyboardMarkup()
    for name, data in TELEGRAM_SERVICES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"ser_{data['id']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع للمنصات", callback_data="platforms_menu"))
    return markup

def facebook_inline_menu():
    markup = types.InlineKeyboardMarkup()
    for name, data in FACEBOOK_SERVICES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"ser_{data['id']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع للمنصات", callback_data="platforms_menu"))
    return markup

def twitter_inline_menu():
    markup = types.InlineKeyboardMarkup()
    for name, data in TWITTER_SERVICES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"ser_{data['id']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع للمنصات", callback_data="platforms_menu"))
    return markup

def threads_inline_menu():
    markup = types.InlineKeyboardMarkup()
    for name, data in THREADS_SERVICES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"ser_{data['id']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع للمنصات", callback_data="platforms_menu"))
    return markup

def spotify_inline_menu():
    markup = types.InlineKeyboardMarkup()
    for name, data in SPOTIFY_SERVICES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"ser_{data['id']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع للمنصات", callback_data="platforms_menu"))
    return markup

def kick_inline_menu():
    markup = types.InlineKeyboardMarkup()
    for name, data in KICK_SERVICES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"ser_{data['id']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع للمنصات", callback_data="platforms_menu"))
    return markup

def youtube_inline_menu():
    markup = types.InlineKeyboardMarkup()
    for name, data in YOUTUBE_SERVICES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"ser_{data['id']}"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع للمنصات", callback_data="platforms_menu"))
    return markup

# دالة مساعدة لإرسال قائمة الترحيب
def send_welcome(chat_id, user_id):
    bot.send_message(chat_id, get_welcome_text(user_id), reply_markup=main_inline_menu())

# دالة مساعدة لتعديل الواجهة الحالية والعودة للرئيسية
def edit_to_welcome(chat_id, message_id, user_id):
    bot.edit_message_text(get_welcome_text(user_id), chat_id, message_id, reply_markup=main_inline_menu())

# --- /start ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    text_args = message.text.split()

    # مسح لوحة المفاتيح القديمة لتنظيف الشات
    clean_msg = bot.send_message(message.chat.id, "جاري فتح لوحة التحكم...", reply_markup=types.ReplyKeyboardRemove())
    bot.delete_message(message.chat.id, clean_msg.message_id)

    if not check_is_subscribed(user_id):
        bot.send_message(
            message.chat.id,
            f"⚠️ <b>عذراً عزيزي، يجب عليك الاشتراك في قناة البوت الرسمية لتتمكن من استخدامه!</b>\n\nاشترك في القناة: {CHANNEL_USERNAME} ثم اضغط على زر تم الاشتراك بالأسفل 👇",
            reply_markup=force_sub_menu(),
            parse_mode="HTML"
        )
        return

    is_new_user = user_id not in USER_BALANCES
    if is_new_user:
        USER_BALANCES[user_id] = 0

    if len(text_args) > 1 and is_new_user:
        try:
            referrer_id = int(text_args[1])
            if referrer_id != user_id and referrer_id in USER_BALANCES and user_id not in REFERRAL_USED:
                REFERRAL_USED[user_id] = referrer_id
                if referrer_id not in REFERRED_USERS:
                    REFERRED_USERS[referrer_id] = set()
                REFERRED_USERS[referrer_id].add(user_id)
                # 🛠️ هنا تم التعديل إلى 1000 نقطة
                USER_BALANCES[referrer_id] = USER_BALANCES.get(referrer_id, 0) + 1000
                save_data()
                try:
                    # 🛠️ هنا تم تعديل رسالة الإشعار لتصبح 1000 نقطة
                    bot.send_message(referrer_id, "🎯 دخل مستخدم جديد للبوت عن طريق رابط الإحالة الخاص بك!\n➕ تم إضافة 1000 نقطة إلى حسابك.")
                except Exception:
                    pass
        except ValueError:
            pass

    send_welcome(message.chat.id, user_id)

# --- شحن نقاط للمالك ---
@bot.message_handler(commands=['add'])
def add_points_admin(message):
    username = message.from_user.username
    if username == 'xc_1h':
        try:
            args = message.text.split()
            if len(args) == 3:
                target_id = int(args[1])
                points_to_add = int(args[2])
                if target_id not in USER_BALANCES:
                    USER_BALANCES[target_id] = 0
                USER_BALANCES[target_id] += points_to_add
                save_data()
                bot.send_message(message.chat.id, f"✅ تم تعديل النقاط بنجاح للمستخدم {target_id} بمقدار: ({points_to_add}) نقطة.")
                try:
                    bot.send_message(target_id, f"💰 تم تحديث رصيد نقاطك من قبل الإدارة بمقدار: {points_to_add} نقطة! 🎉")
                except Exception:
                    pass
            else:
                bot.send_message(message.chat.id, "❌ الصيغة خاطئة! استخدم:\n/add [الآيدي] [عدد النقاط]")
        except ValueError:
            bot.send_message(message.chat.id, "❌ خطأ! تأكد من كتابة الآيدي والنقاط بالأرقام فقط.")
    else:
        bot.send_message(message.chat.id, "❌ هذا الأمر مخصص للمالك فقط!")

# --- أمر أعلى 10 مشاركين ---
@bot.message_handler(func=lambda m: m.text and m.text.strip() in [
    '/top_referrals', 'اكثر مشاركين رابط الاحالة', 'أكثر مشاركين رابط الإحالة',
    'اكثر مشاركين رابط الإحالة', 'أكثر مشاركين رابط الاحالة', '/اكثر مشاركين'
])
def top_referrals(message):
    if not REFERRED_USERS:
        bot.send_message(message.chat.id, "📊 لا يوجد مشاركين بعد.")
        return

    sorted_referrers = sorted(
        REFERRED_USERS.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )[:10]

    total = sum(len(v) for v in REFERRED_USERS.values())
    text = f"🏆 أعلى 10 مشاركين لرابط الإحالة:\n"
    text += f"👥 إجمالي المشاركات: {total}\n"
    text += "━━━━━━━━━━━━━━━━\n"
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for i, (uid, referred_set) in enumerate(sorted_referrers):
        count = len(referred_set)
        word = "مشاركة" if count == 1 else "مشاركات"
        text += f"{medals[i]} الآيدي: `{uid}`\n"
        text += f"     ↳ عدد المشاركات: {count} {word}\n"
    text += "━━━━━━━━━━━━━━━━"

    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# --- معالجة الأزرار ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "verify_subscription":
        if check_is_subscribed(user_id):
            bot.delete_message(chat_id, message_id)
            if user_id not in USER_BALANCES:
                USER_BALANCES[user_id] = 0
            send_welcome(chat_id, user_id)
        else:
            bot.answer_callback_query(call.id, "❌ عزيزي، لم تشترك في القناة بعد!", show_alert=True)
        return

    if not check_is_subscribed(user_id):
        bot.answer_callback_query(call.id, "⚠️ يجب عليك البقاء مشتركاً بالقناة!", show_alert=True)
        bot.edit_message_text(
            f"⚠️ <b>يجب عليك الاشتراك في قناة البوت الرسمية أولاً:</b>\n\nالقناة: {CHANNEL_USERNAME}",
            chat_id, message_id, reply_markup=force_sub_menu(), parse_mode="HTML"
        )
        return

    if user_id not in USER_BALANCES:
        USER_BALANCES[user_id] = 0

    if call.data == "back_to_main":
        edit_to_welcome(chat_id, message_id, user_id)

    elif call.data == "main_services" or call.data == "platforms_menu":
        bot.edit_message_text(
            "🛒 اهلاً بك في قسم الخدمات\n• اختر المنصة التي تريدها 👇",
            chat_id, message_id, reply_markup=services_inline_menu()
        )

    elif call.data == "main_account":
        account_text = f"👤 حسابك الشخصي:\n\n🆔 الآيدي: {user_id}\n💎 رصيد نقاطك: {USER_BALANCES.get(user_id, 0)} نقطة"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_to_main"))
        bot.edit_message_text(account_text, chat_id, message_id, reply_markup=markup)

    elif call.data == "use_code_menu":
        bot.delete_message(chat_id, message_id)
        msg = bot.send_message(chat_id, "💳 أرسل الكود الذي تريد استخدامه:")
        bot.register_next_step_handler(msg, process_gift_code)

    elif call.data == "btn_under_dev":
        bot.answer_callback_query(call.id, "⚙️ هذا القسم قيد التحديث حالياً.", show_alert=True)

    elif call.data == "charge_points_menu":
        charge_text = (
            "🔹 | <b>اسعار نقاط بوت السلطان للدعم</b> 🔹\n\n"
            "- 1$ = 10000 نقطة 💎\n"
            "- 2$ = 20000 نقطة 💎\n"
            "- 3$ = 30000 نقطة 💎\n"
            "- 4$ = 40000 نقطة 💎\n"
            "- 5$ = 50000 نقطة 💎\n"
            "- 10$ = 100000 نقطة 💎\n"
            "- 20$ = 200000 نقطة 💎\n"
            "- 50$ = 500000 نقطة 💎\n"
            "- 150$ = 1500000 نقطة 💎\n"
            "• يمكنك شحن حتى 100M نقطة 🤩\n"
            "-----------------------------\n"
            "• طرق الدفع: اسيا، زين كاش، زين العراق، ماستر كارد، ايتونز أمريكي\n"
            "( BTC | USDT $ TON )\n"
            "-----------------------------\n\n"
            "• للشحن يرجى التواصل مباشرة مع المالك:\n"
            "👉 @xc_1h\n\n"
            f"• قم بنسخ آيديك وأرسله له:\n"
            f"<code>{user_id}</code>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_to_main"))
        bot.edit_message_text(charge_text, chat_id, message_id, reply_markup=markup, parse_mode="HTML")

    elif call.data == "check_order_menu":
        bot.delete_message(chat_id, message_id)
        msg = bot.send_message(chat_id, "🔍 يرجى إرسال رقم الطلب (Order ID) المراد فحصه:\nمثال: 457812")
        bot.register_next_step_handler(msg, process_check_order)

    elif call.data == "collect_menu":
        collect_text = (
            "💎 | قسم تجميع النقاط مجاناً\n\n"
            "• اختر الطريقة المناسبة لك لتجميع النقاط من الأسفل 👇"
        )
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("🔗 مشاركة رابط الإحالة (+1000 نقطة)", callback_data="referral_system"))
        markup.row(types.InlineKeyboardButton("🎁 الهدية اليومية المجانية", callback_data="daily_gift_system"))
        markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_to_main"))
        bot.edit_message_text(collect_text, chat_id, message_id, reply_markup=markup)

    elif call.data == "referral_system":
        bot_username = "tamgdbot"
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        ref_text = (
            f"🔗 | رابط الإحالة الخاص بك:\n\n"
            f"{ref_link}\n\n"
            f"• انسخ الرابط وقم بمشاركته مع أصدقائك وفي المجموعات.\n"
            f"• كل شخص يدخل للبوت عبر رابطك لأول مرة، ستحصل تلقائياً على 1000 نقطة! 🎉"
        )
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("🔙 رجوع لقسم التجميع", callback_data="collect_menu"))
        bot.edit_message_text(ref_text, chat_id, message_id, reply_markup=markup)

    elif call.data == "daily_gift_system":
        current_time = time.time()
        last_claim = USER_DAILY_GIFT.get(user_id, 0)

        if current_time - last_claim >= 86400:
            USER_DAILY_GIFT[user_id] = current_time
            USER_BALANCES[user_id] = USER_BALANCES.get(user_id, 0) + 100
            save_data()
            bot.answer_callback_query(call.id, "🎁 مبروك! حصلت على 100 نقطة مجانية كهدية يومية.", show_alert=True)
        else:
            remaining_time = int(86400 - (current_time - last_claim))
            hours = remaining_time // 3600
            minutes = (remaining_time % 3600) // 60
            bot.answer_callback_query(call.id, f"❌ لقد استلمت هديتك اليومية!\nيرجى المحاولة بعد: {hours} ساعة و {minutes} دقيقة.", show_alert=True)
        
        edit_to_welcome(chat_id, message_id, user_id)

    # --- توجيه المنصات ---
    elif call.data == "insta_menu":
        bot.edit_message_text("📸 قسم : انستغرام\n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=instagram_inline_menu())
    elif call.data == "tiktok_menu":
        bot.edit_message_text("🎵 قسم : تيك توك\n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=tiktok_inline_menu())
    elif call.data == "tele_menu":
        bot.edit_message_text("✈️ قسم : تلجرام\n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=telegram_inline_menu())
    elif call.data == "fb_menu":
        bot.edit_message_text("📘 قسم : فيس بوك\n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=facebook_inline_menu())
    elif call.data == "twitter_menu":
        bot.edit_message_text("✖️ قسم : تويتر\n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=twitter_inline_menu())
    elif call.data == "threads_menu":
        bot.edit_message_text("🧵 قسم : ثريدز\n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=threads_inline_menu())
    elif call.data == "spotify_menu":
        bot.edit_message_text("🎧 قسم : سبوتي فاي\n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=spotify_inline_menu())
    elif call.data == "kick_menu":
        bot.edit_message_text("🟢 قسم : كيك\n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=kick_inline_menu())
    elif call.data == "yt_menu":
        bot.edit_message_text("🔴 قسم : يوتيوب\n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=youtube_inline_menu())

    elif call.data.startswith("ser_"):
        service_id = int(call.data.split("_")[1])
        service_info = SERVICES_BY_ID.get(service_id)
        if service_info:
            service_name = service_info["name"]
            bot.delete_message(chat_id, message_id)
            msg = bot.send_message(chat_id, f"🔗 أرسل الرابط المطلوب لخدمة:\n[{service_name}]:")
            bot.register_next_step_handler(msg, process_link, service_id)

# --- معالجة الكود ---
def process_gift_code(message):
    user_id = message.from_user.id
    code = message.text.strip()

    if code.startswith("/"):
        bot.send_message(message.chat.id, "تم إلغاء العملية.")
        send_welcome(message.chat.id, user_id)
        return

    if code not in GIFT_CODES:
        bot.send_message(message.chat.id, "❌ الكود غير صحيح أو غير موجود!")
        send_welcome(message.chat.id, user_id)
        return

    code_data = GIFT_CODES[code]

    if user_id in code_data["used_by"]:
        bot.send_message(message.chat.id, "❌ لقد استخدمت هذا الكود مسبقاً!")
        send_welcome(message.chat.id, user_id)
        return

    if len(code_data["used_by"]) >= code_data["max_uses"]:
        bot.send_message(message.chat.id, "❌ انتهت استخدامات هذا الكود!")
        send_welcome(message.chat.id, user_id)
        return

    # إضافة النقاط لحساب المستخدم
    points = code_data["points"]
    GIFT_CODES[code]["used_by"].append(user_id)
    USER_BALANCES[user_id] = USER_BALANCES.get(user_id, 0) + points
    save_data()

    remaining = code_data["max_uses"] - len(GIFT_CODES[code]["used_by"])
    
    bot.send_message(message.chat.id, f"""✅ تم تفعيل الكود بنجاح!
💎 حصلت على {points} نقطة!
🔢 المتبقي من استخدامات الكود: {remaining}""")
    send_welcome(message.chat.id, user_id)

# --- فحص الطلب ---
def process_check_order(message):
    user_id = message.from_user.id
    order_id = message.text

    if order_id.startswith("/"):
        bot.send_message(message.chat.id, "تم إلغاء عملية الفحص.")
        send_welcome(message.chat.id, user_id)
        return

    if not order_id.isdigit():
        bot.send_message(message.chat.id, "❌ خطأ! رقم الطلب يجب أن يتكون من أرقام فقط.")
        send_welcome(message.chat.id, user_id)
        return

    bot.send_message(message.chat.id, "⏳ جاري جلب حالة الطلب من الموقع...")

    api_data = {"key": API_KEY, "action": "status", "order": int(order_id)}
    try:
        response = requests.post(API_URL, data=api_data, timeout=10)
        result = response.json()
        if "status" in result:
            status_translations = {
                "Pending": "قيد الانتظار ⏳",
                "In progress": "جاري التنفيذ ⚙️",
                "Completed": "مكتمل بنجاح ✅",
                "Partial": "مكتمل جزئياً ⚠️",
                "Canceled": "ملغي من الموقع ❌",
                "Processing": "جاري المعالجة 🔄"
            }
            status_ar = status_translations.get(result.get("status", ""), result.get("status", ""))
            info_text = (
                f"🔍 | تفاصيل حالة طلبك رقم: {order_id}\n\n"
                f"📊 حالة الطلب: {status_ar}\n"
                f"📈 العدد البدائي: {result.get('start_count', '0')}\n"
                f"🔢 المتبقي: {result.get('remains', '0')}"
            )
            bot.send_message(message.chat.id, info_text)
        else:
            bot.send_message(message.chat.id, f"❌ لم يتم العثور على بيانات لهذا الطلب.\nالسبب: {result.get('error', 'رقم الطلب غير صحيح')}")
    except Exception:
        bot.send_message(message.chat.id, "❌ فشل الاتصال بالسيرفر، يرجى المحاولة لاحقاً.")

    send_welcome(message.chat.id, user_id)

# --- استلام الرابط ---
def process_link(message, service_id):
    link = message.text
    if link.startswith("/"):
        bot.send_message(message.chat.id, "تم إلغاء الطلب.")
        send_welcome(message.chat.id, message.from_user.id)
        return
    msg = bot.send_message(message.chat.id, "🔢 أرسل العدد المطلوب (مثال: 1000):")
    bot.register_next_step_handler(msg, process_quantity, service_id, link)

# --- استلام العدد وإرسال الطلب للسيرفر ---
def process_quantity(message, service_id, link):
    user_id = message.from_user.id
    quantity = message.text

    if not quantity.isdigit():
        bot.send_message(message.chat.id, "❌ خطأ! يجب إرسال العدد كأرقام فقط.")
        send_welcome(message.chat.id, user_id)
        return

    qty = int(quantity)
    service_info = SERVICES_BY_ID[service_id]
    cost = int((qty / 1000) * service_info["points"])
    balance = USER_BALANCES.get(user_id, 0)

    if balance < cost:
        bot.send_message(message.chat.id, f"❌ عذراً، نقاطك غير كافية!\n💰 التكلفة: {cost} نقطة\n💎 رصيدك: {balance} نقطة")
        send_welcome(message.chat.id, user_id)
        return

    USER_BALANCES[user_id] = balance - cost
    save_data()
    bot.send_message(message.chat.id, "⏳ جاري معالجة طلبك وإرساله للسيرفر...")

    api_data = {"key": API_KEY, "action": "add", "service": service_id, "link": link, "quantity": qty}
    try:
        response = requests.post(API_URL, data=api_data, timeout=10)
        result = response.json()
        if "order" in result:
            bot.send_message(message.chat.id, f"✅ تم إرسال طلبك بنجاح!\n🆔 رقم الطلب: {result['order']}\n📉 المخصوم: {cost} نقطة")
        else:
            USER_BALANCES[user_id] += cost
            save_data()
            bot.send_message(message.chat.id, f"❌ رفض الموقع الطلب:\n{result.get('error', 'خطأ غير معروف')}\n🔄 تم إعادة نقاطك.")
    except Exception:
        USER_BALANCES[user_id] += cost
        save_data()
        bot.send_message(message.chat.id, "❌ فشل الاتصال بالموقع. تم إعادة نقاطك.")

    send_welcome(message.chat.id, user_id)

import time as _time
print("البوت يعمل الآن...")
while True:
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")
        print("إعادة المحاولة بعد 5 ثواني...")
        _time.sleep(5)
