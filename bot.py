import telebot
from telebot import types
import requests
import time

# 🌐 بيانات الـ API الخاصة بموقع فولو عراق (foloiq)
API_URL = "https://foloiq.com/api/v2"
API_KEY = "5d97af2902dacc9a4e2d2bbd6885b99c"

# 📢 معرف قناة الاشتراك الإجباري
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
    "🎵 | متابعين حسابات مميزة | 1000 بـ 62,000 نقطة": {"id": 7963, "points": 62000},
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
    "🔴 | اشتراك بريميوم مدى الحياة | 1000 بـ 20,000 نقطة": {"id": 8373, "points": 20000},
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

# 💾 قواعد البيانات الوهمية لحفظ البيانات
USER_BALANCES = {}      # حفظ الرصيد
USER_DAILY_GIFT = {}    # حفظ توقيت الهدية اليومية
REFERRAL_USED = {}      # حفظ من أحال كل مستخدم (user_id -> referrer_id)
REFERRED_USERS = {}     # حفظ قائمة المُحالين لكل مشارك (referrer_id -> set of user_ids)

BOT_TOKEN = "8804286947:AAEydiGWGxA7ylGtCs7K5BmDImPfUI9dmww"
bot = telebot.TeleBot(BOT_TOKEN)

# --- دالة فحص الاشتراك الإجباري الصارمة ---
def check_is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception:
        return False

# --- واجهة الاشتراك الإجباري المخصصة ---
def force_sub_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("اضغط هنا للاشتراك بالقناة 📢", url="https://t.me/Sultan_Follow"))
    markup.row(types.InlineKeyboardButton("تم الاشتراك ✅", callback_data="verify_subscription"))
    return markup

# --- دالة لتوليد نص الترحيب الرئيسي المحدث بيوزر البوت الحالي ---
def get_welcome_text(user_id):
    balance = USER_BALANCES.get(user_id, 0)
    return (
        f"اهلاً بك في بوت السلطان للدعم - @tamgdbot\n"
        f"• البوت مختص لرشق جميع الخدمات والبرامج\n"
        f"سارع بتجربة أسرع وأفضل الخدمات 👋\n\n"
        f"🆔 | ايديك : {user_id}\n"
        f"💎 | عدد نقاطك : {balance} نقطة"
    )

# --- 1. القائمة الرئيسية الشفافة (Inline) ---
def main_inline_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("🛒 الخدمات", callback_data="main_services"))
    markup.row(types.InlineKeyboardButton("🎯 تمويل قناتك", callback_data="btn_under_dev"))
    markup.row(
        types.InlineKeyboardButton("💎 تجمع نقاط", callback_data="collect_menu"),
        types.InlineKeyboardButton("💳 استخدام كود", callback_data="btn_under_dev")
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

# --- 2. واجهة اختيار التطبيقات والبرامج ---
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
    markup.row(types.InlineKeyboardButton("رجوع ◀️", callback_data="back_to_main"))
    return markup

# --- قوائم الخدمات الفرعية للمنصات ---
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

# --- 3. معالجة أمر البداية /start مع دعم نظام الإحالة تلقائياً وحذف أزرار الكيبورد القديمة ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    text_args = message.text.split()

    # كود تنظيف وحذف أزرار الكيبورد القديمة الثابتة تلقائياً من شاشة المستخدم
    clean_msg = bot.send_message(message.chat.id, "جاري فتح لوحة التحكم...", reply_markup=types.ReplyKeyboardRemove())
    bot.delete_message(message.chat.id, clean_msg.message_id)

    # التحقق من الاشتراك الإجباري أولاً
    if not check_is_subscribed(user_id):
        bot.send_message(
            message.chat.id,
            f"⚠️ <b>عذراً عزيزي، يجب عليك الاشتراك في قناة البوت الرسمية لتتمكن من استخدامه!</b>\n\nاشترك في القناة: {CHANNEL_USERNAME} ثم اضغط على زر تفعيل الحساب بالأسفل 👇",
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
                USER_BALANCES[referrer_id] = USER_BALANCES.get(referrer_id, 0) + 200
                try:
                    bot.send_message(referrer_id, "🎯 دخل مستخدم جديد للبوت عن طريق رابط الإحالة الخاص بك!\n➕ تم إضافة 200 نقطة إلى حسابك.")
                except Exception:
                    pass
        except ValueError:
            pass

    bot.send_message(message.chat.id, get_welcome_text(user_id))
    bot.send_message(message.chat.id, "📋 القائمة الرئيسية :", reply_markup=main_inline_menu())

# --- 🛠 ميزة شحن وتحويل النقاط الحصرية للمالك فقط ---
@bot.message_handler(commands=['add'])
def add_points_admin(message):
    username = message.from_user.username

    # فحص حساب المالك عبر اليوزر المعتمد فقط لضمان الخصوصية والأمان
    if username == 'xc_1h':
        try:
            args = message.text.split()
            if len(args) == 3:
                target_id = int(args[1])
                points_to_add = int(args[2])

                if target_id not in USER_BALANCES:
                    USER_BALANCES[target_id] = 0

                USER_BALANCES[target_id] += points_to_add
                bot.send_message(message.chat.id, f"✅ تم تعديل النقاط بنجاح للمستخدم {target_id} بمقدار: ({points_to_add}) نقطة.", parse_mode="Markdown")

                try:
                    bot.send_message(target_id, f"💰 تم تحديث رصيد نقاطك من قبل الإدارة بمقدار: {points_to_add} نقطة! 🎉")
                except Exception:
                    pass
            else:
                bot.send_message(message.chat.id, "❌ الصيغة خاطئة! استخدم الأمر هكذا:\n/add [الآيدي] [عدد النقاط]", parse_mode="Markdown")
        except ValueError:
            bot.send_message(message.chat.id, "❌ خطأ! تأكد من كتابة الآيدي والنقاط بالأرقام فقط.")
    else:
        bot.send_message(message.chat.id, "❌ هذا الأمر مخصص للمالك والأدمن فقط!")

# --- 4. التحكم بالضغطات والتحديث بداخل الرسالة الشفافة ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # معالجة ضغطة التحقق من الاشتراك الإجباري بالقناة
    if call.data == "verify_subscription":
        if check_is_subscribed(user_id):
            bot.delete_message(chat_id, message_id)
            if user_id not in USER_BALANCES:
                USER_BALANCES[user_id] = 0
            bot.send_message(chat_id, get_welcome_text(user_id))
            bot.send_message(chat_id, "📋 القائمة الرئيسية :", reply_markup=main_inline_menu())
        else:
            bot.answer_callback_query(call.id, "❌ عزيزي، لم تشترك في القناة بعد! يرجى الانضمام أولاً.", show_alert=True)
        return

    # فحص القناة لجميع الأزرار والعمليات اللاحقة لضمان بقاء المستخدم بداخل القناة
    if not check_is_subscribed(user_id):
        bot.answer_callback_query(call.id, "⚠️ يجب عليك البقاء مشتركاً بالقناة لاستخدام البوت!", show_alert=True)
        bot.edit_message_text(
            f"⚠️ <b>يجب عليك الاشتراك في قناة البوت الرسمية أولاً:</b>\n\nالقناة الحالية: {CHANNEL_USERNAME}",
            chat_id, message_id, reply_markup=force_sub_menu(), parse_mode="HTML"
        )
        return

    if user_id not in USER_BALANCES:
        USER_BALANCES[user_id] = 0

    if call.data == "back_to_main":
        bot.edit_message_text(get_welcome_text(user_id), chat_id, message_id, reply_markup=main_inline_menu())

    elif call.data == "main_services" or call.data == "platforms_menu":
        services_text = "🔴 اهلاً بك في قسم الخدمات\n• اختر الخدمة التي تريدها 👇"
        bot.edit_message_text(services_text, chat_id, message_id, reply_markup=services_inline_menu())

    elif call.data == "main_account":
        account_text = f"👤 حسابك الشخصي:\n\n🆔 الآيدي: {user_id}\n💎 رصيد نقاطك: {USER_BALANCES[user_id]} نقطة"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_to_main"))
        bot.edit_message_text(account_text, chat_id, message_id, reply_markup=markup)

    elif call.data == "btn_under_dev":
        bot.answer_callback_query(call.id, "⚙️ هذا القسم قيد التحديث حالياً.", show_alert=True)

    elif call.data == "charge_points_menu":
        charge_text = (
            "🔹 | <b>اسعار نقاط بوت السلطان للدعم</b> 🔹\n\n"
            "- 1$ = 10,000 نقطة 💎\n"
            "- 2$ = 20,000 نقطة 💎\n"
            "- 3$ = 30,000 نقطة 💎\n"
            "- 4$ = 40,000 نقطة 💎\n"
            "- 5$ = 50,000 نقطة 💎\n"
            "- 10$ = 100,000 نقطة 💎\n"
            "- 20$ = 200,000 نقطة 💎\n"
            "- 50$ = 50,0000 نقطة 💎\n"
            "- 150$ = 1,500,000 نقطة 💎\n\n"
            "• يمكنك شحن حتى 100M نقطة 🤩\n"
            "-----------------------------\n"
            "• طرق الدفع : ↫ اسيا، زين كاش، زين العراق، ماستر كارد، ايتونز أمريكي \n"
            "( BTC | USDT $ TON )\n"
            "-----------------------------\n\n"
            "• للشحن يرجى التواصل مباشرة مع المالك عبر المعرف التالي:\n"
            "👉 @xc_1h\n\n"
            f"• قم بنسخ آيديك هذا وأرسله له ليتم الشحن لك فوراً:\n"
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
        markup.row(types.InlineKeyboardButton("🔗 مشاركة رابط الإحالة (+200 نقطة)", callback_data="referral_system"))
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
            f"• كل شخص يقوم بالدخول للبوت والضغط على (ابدأ / start) عبر رابطك لأول مرة، ستحصل تلقائياً على 200 نقطة! 🎉"
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
            bot.answer_callback_query(call.id, "🎁 مبروك! حصلت على 100 نقطة مجانية كهدية يومية.", show_alert=True)
            bot.edit_message_text(get_welcome_text(user_id), chat_id, message_id, reply_markup=main_inline_menu())
        else:
            remaining_time = int(86400 - (current_time - last_claim))
            hours = remaining_time // 3600
            minutes = (remaining_time % 3600) // 60
            bot.answer_callback_query(call.id, f"❌ لقد استلمت هديتك اليومية سابقاً!\nيرجى المحاولة بعد: {hours} ساعة و {minutes} دقيقة.", show_alert=True)

    # --- توجيه أزرار المنصات الأخرى ---
    elif call.data == "insta_menu":
        bot.edit_message_text("📊 قسم : انستغرام \n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=instagram_inline_menu())
    elif call.data == "tiktok_menu":
        bot.edit_message_text("📊 قسم : تيك توك \n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=tiktok_inline_menu())
    elif call.data == "tele_menu":
        bot.edit_message_text("📊 قسم : تلجرام \n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=telegram_inline_menu())
    elif call.data == "fb_menu":
        bot.edit_message_text("📊 قسم : فيس بوك \n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=facebook_inline_menu())
    elif call.data == "twitter_menu":
        bot.edit_message_text("📊 قسم : تويتر \n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=twitter_inline_menu())
    elif call.data == "threads_menu":
        bot.edit_message_text("📊 قسم : ثريدز \n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=threads_inline_menu())
    elif call.data == "spotify_menu":
        bot.edit_message_text("📊 قسم : سبوتي فاي \n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=spotify_inline_menu())
    elif call.data == "kick_menu":
        bot.edit_message_text("📊 قسم : كيك \n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=kick_inline_menu())
    elif call.data == "yt_menu":
        bot.edit_message_text("📊 قسم : يوتيوب \n| اختر الخدمة المطلوبة :", chat_id, message_id, reply_markup=youtube_inline_menu())

    elif call.data.startswith("ser_"):
        service_id = int(call.data.split("_")[1])
        service_info = SERVICES_BY_ID.get(service_id)

        if service_info:
            service_name = service_info["name"]
            bot.delete_message(chat_id, message_id)
            msg = bot.send_message(chat_id, f"🔗 أرسل الرابط المطلوب لخدمة:\n[{service_name}]:")
            bot.register_next_step_handler(msg, process_link, service_id)

# --- دالة معالجة فحص الطلب عبر الاتصال بالموقع ---
def process_check_order(message):
    user_id = message.from_user.id
    order_id = message.text

    if order_id.startswith("/"):
        bot.send_message(message.chat.id, "تم إلغاء عملية الفحص.")
        bot.send_message(message.chat.id, get_welcome_text(user_id))
        bot.send_message(message.chat.id, "📋 القائمة الرئيسية :", reply_markup=main_inline_menu())
        return

    if not order_id.isdigit():
        bot.send_message(message.chat.id, "❌ خطأ! رقم الطلب يجب أن يتكون من أرقام فقط.")
        bot.send_message(message.chat.id, get_welcome_text(user_id))
        bot.send_message(message.chat.id, "📋 القائمة الرئيسية :", reply_markup=main_inline_menu())
        return

    bot.send_message(message.chat.id, "⏳ جاري جلب حالة الطلب من الموقع...")

    api_data = {
        "key": API_KEY,
        "action": "status",
        "order": int(order_id)
    }

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
            status_en = result.get("status", "Unknown")
            status_ar = status_translations.get(status_en, status_en)
            remains = result.get("remains", "0")
            start_count = result.get("start_count", "0")

            info_text = (
                f"🔍 | تفاصيل حالة طلبك رقم: {order_id}\n\n"
                f"📊 حالة الطلب الحالية: {status_ar}\n"
                f"📈 العدد البدائي للمنشور: {start_count}\n"
                f"🔢 العدد المتبقي لإكمال الرشق: {remains}"
            )
            bot.send_message(message.chat.id, info_text)
        else:
            bot.send_message(message.chat.id, f"❌ لم يتم العثور على أي بيانات لهذا الطلب.\nالسبب: {result.get('error', 'رقم الطلب غير صحيح')}")
    except Exception:
        bot.send_message(message.chat.id, "❌ فشل الاتصال بالسيرفر، يرجى إعادة المحاولة لاحقاً.")

    bot.send_message(message.chat.id, get_welcome_text(user_id))
    bot.send_message(message.chat.id, "📋 القائمة الرئيسية :", reply_markup=main_inline_menu())

# --- استلام الرابط للخدمات ---
def process_link(message, service_id):
    link = message.text
    if link.startswith("/"):
        bot.send_message(message.chat.id, "تم إلغاء الطلب المفتوح.")
        bot.send_message(message.chat.id, get_welcome_text(message.from_user.id))
        bot.send_message(message.chat.id, "📋 القائمة الرئيسية :", reply_markup=main_inline_menu())
        return
    msg = bot.send_message(message.chat.id, "🔢 أرسل العدد المطلوب (مثال: 1000):")
    bot.register_next_step_handler(msg, process_quantity, service_id, link)

# --- استلام العدد وإرسال الطلب للسيرفر ---
def process_quantity(message, service_id, link):
    user_id = message.from_user.id
    quantity = message.text

    if quantity.startswith("/"):
        bot.send_message(message.chat.id, "تم إلغاء الطلب المفتوح.")
        bot.send_message(message.chat.id, get_welcome_text(user_id))
        bot.send_message(message.chat.id, "📋 القائمة الرئيسية :", reply_markup=main_inline_menu())
        return

    if not quantity.isdigit():
        bot.send_message(message.chat.id, "❌ خطأ! يجب إرسال العدد كأرقام فقط.")
        bot.send_message(message.chat.id, get_welcome_text(user_id))
        bot.send_message(message.chat.id, "📋 القائمة الرئيسية :", reply_markup=main_inline_menu())
        return

    qty = int(quantity)
    service_info = SERVICES_BY_ID[service_id]
    points_per_1000 = service_info["points"]
    cost = int((qty / 1000) * points_per_1000)

    if USER_BALANCES[user_id] < cost:
        bot.send_message(message.chat.id, f"❌ عذراً، نقاطك غير كافية لطلب هذه الخدمة!\n💰 التكلفة: {cost} نقطة.")
        bot.send_message(message.chat.id, get_welcome_text(user_id))
        bot.send_message(message.chat.id, "📋 القائمة الرئيسية :", reply_markup=main_inline_menu())
        return

    USER_BALANCES[user_id] -= cost
    bot.send_message(message.chat.id, f"⏳ جاري معالجة طلبك وإرساله للسيرفر...")

    api_data = {
        "key": API_KEY,
        "action": "add",
        "service": service_id,
        "link": link,
        "quantity": qty
    }

    try:
        response = requests.post(API_URL, data=api_data, timeout=10)
        result = response.json()

        if "order" in result:
            bot.send_message(message.chat.id, f"✅ تم إرسال طلبك بنجاح للموقع!\n🆔 رقم الطلب: {result['order']}\n📉 المخصوم: {cost} نقطة")
        else:
            USER_BALANCES[user_id] += cost
            bot.send_message(message.chat.id, f"❌ رفض الموقع الطلب بسبب:\n {result.get('error', 'خطأ غير معروف')}\n🔄 تم إعادة نقاطك.")
    except Exception:
        USER_BALANCES[user_id] += cost
        bot.send_message(message.chat.id, f"❌ فشل الاتصال بالموقع. تم إعادة نقاطك لحسابك.")

    bot.send_message(message.chat.id, get_welcome_text(user_id))
    bot.send_message(message.chat.id, "📋 القائمة الرئيسية :", reply_markup=main_inline_menu())

print("البوت يعمل الآن بنظام اشتراك إجباري صارم ومغلق لقناة @Sultan_Follow...")
bot.polling(none_stop=True)
