import telebot
from telebot import types
import requests
import time
import json
import os

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

# 💾 مسار ملف حفظ البيانات
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_data.json")

# 🎟️ أكواد النقاط - كل كود يشتغل لـ 5 أشخاص فقط
GIFT_CODES = {
    "0ki2er": {"points": 5000, "max_uses": 5, "used_by": []},
    "bym5a5": {"points": 5000, "max_uses": 5, "used_by": []},
    "cqx45": {"points": 5000, "max_uses": 5, "used_by": []},
    "imvde": {"points": 5000, "max_uses": 5, "used_by": []},
    "7s5ts4": {"points": 5000, "max_uses": 5, "used_by": []},
    "rqh73v": {"points": 5000, "max_uses": 5, "used_by": []},
    "i4z6": {"points": 5000, "max_uses": 5, "used_by": []},
    "u0qm5d": {"points": 5000, "max_uses": 5, "used_by": []},
    "8kkr": {"points": 5000, "max_uses": 5, "used_by": []},
    "8j3yc": {"points": 5000, "max_uses": 5, "used_by": []},
    "3dpi6": {"points": 5000, "max_uses": 5, "used_by": []},
    "7wxs1": {"points": 5000, "max_uses": 5, "used_by": []},
    "u2ao2": {"points": 5000, "max_uses": 5, "used_by": []},
    "y1zu": {"points": 5000, "max_uses": 5, "used_by": []},
    "f7apda": {"points": 5000, "max_uses": 5, "used_by": []},
    "cboy": {"points": 5000, "max_uses": 5, "used_by": []},
    "1dev5i": {"points": 5000, "max_uses": 5, "used_by": []},
    "j2nx": {"points": 5000, "max_uses": 5, "used_by": []},
    "cay89": {"points": 5000, "max_uses": 5, "used_by": []},
    "4uxnu": {"points": 5000, "max_uses": 5, "used_by": []},
    "bzqjmm": {"points": 5000, "max_uses": 5, "used_by": []},
    "0pfg7": {"points": 5000, "max_uses": 5, "used_by": []},
    "6s1tn9": {"points": 5000, "max_uses": 5, "used_by": []},
    "fmur": {"points": 5000, "max_uses": 5, "used_by": []},
    "50hu": {"points": 5000, "max_uses": 5, "used_by": []},
    "d8ry": {"points": 5000, "max_uses": 5, "used_by": []},
    "q8iidx": {"points": 5000, "max_uses": 5, "used_by": []},
    "2fsf": {"points": 5000, "max_uses": 5, "used_by": []},
    "jghc0j": {"points": 5000, "max_uses": 5, "used_by": []},
    "xfh0": {"points": 5000, "max_uses": 5, "used_by": []},
    "rys2lz": {"points": 5000, "max_uses": 5, "used_by": []},
    "wjv0": {"points": 5000, "max_uses": 5, "used_by": []},
    "w0hu1k": {"points": 5000, "max_uses": 5, "used_by": []},
    "pwnkq": {"points": 5000, "max_uses": 5, "used_by": []},
    "6rnm": {"points": 5000, "max_uses": 5, "used_by": []},
    "jkc0v0": {"points": 5000, "max_uses": 5, "used_by": []},
    "5x6rx": {"points": 5000, "max_uses": 5, "used_by": []},
    "4o49": {"points": 5000, "max_uses": 5, "used_by": []},
    "7dxd": {"points": 5000, "max_uses": 5, "used_by": []},
    "wrq3ax": {"points": 5000, "max_uses": 5, "used_by": []},
    "xmytba": {"points": 5000, "max_uses": 5, "used_by": []},
    "d7zp": {"points": 5000, "max_uses": 5, "used_by": []},
    "jzjuyf": {"points": 5000, "max_uses": 5, "used_by": []},
    "ipc5v": {"points": 5000, "max_uses": 5, "used_by": []},
    "x99i": {"points": 5000, "max_uses": 5, "used_by": []},
    "tgpmj": {"points": 5000, "max_uses": 5, "used_by": []},
    "p9ek5h": {"points": 5000, "max_uses": 5, "used_by": []},
    "3qmys7": {"points": 5000, "max_uses": 5, "used_by": []},
    "hjvjs": {"points": 5000, "max_uses": 5, "used_by": []},
    "2j6n": {"points": 5000, "max_uses": 5, "used_by": []},
    "e3z9u": {"points": 5000, "max_uses": 5, "used_by": []},
    "1qiadg": {"points": 5000, "max_uses": 5, "used_by": []},
    "tg5o": {"points": 5000, "max_uses": 5, "used_by": []},
    "hd3khm": {"points": 5000, "max_uses": 5, "used_by": []},
    "bhrr": {"points": 5000, "max_uses": 5, "used_by": []},
    "9e0q": {"points": 5000, "max_uses": 5, "used_by": []},
    "92wz": {"points": 5000, "max_uses": 5, "used_by": []},
    "qg5az": {"points": 5000, "max_uses": 5, "used_by": []},
    "2lm3d": {"points": 5000, "max_uses": 5, "used_by": []},
    "ku1hs9": {"points": 5000, "max_uses": 5, "used_by": []},
    "py58": {"points": 5000, "max_uses": 5, "used_by": []},
    "uc769b": {"points": 5000, "max_uses": 5, "used_by": []},
    "chups2": {"points": 5000, "max_uses": 5, "used_by": []},
    "tyhx2": {"points": 5000, "max_uses": 5, "used_by": []},
    "dk2e1w": {"points": 5000, "max_uses": 5, "used_by": []},
    "qqepv": {"points": 5000, "max_uses": 5, "used_by": []},
    "vlsvfa": {"points": 5000, "max_uses": 5, "used_by": []},
    "emw5": {"points": 5000, "max_uses": 5, "used_by": []},
    "55v6": {"points": 5000, "max_uses": 5, "used_by": []},
    "psyji": {"points": 5000, "max_uses": 5, "used_by": []},
    "y63d7": {"points": 5000, "max_uses": 5, "used_by": []},
    "c8u9k": {"points": 5000, "max_uses": 5, "used_by": []},
    "tsl16d": {"points": 5000, "max_uses": 5, "used_by": []},
    "oezto": {"points": 5000, "max_uses": 5, "used_by": []},
    "9p1syl": {"points": 5000, "max_uses": 5, "used_by": []},
    "9b94": {"points": 5000, "max_uses": 5, "used_by": []},
    "vot7": {"points": 5000, "max_uses": 5, "used_by": []},
    "og6kh1": {"points": 5000, "max_uses": 5, "used_by": []},
    "cxrih": {"points": 5000, "max_uses": 5, "used_by": []},
    "h3t5xt": {"points": 5000, "max_uses": 5, "used_by": []},
    "mwejx": {"points": 5000, "max_uses": 5, "used_by": []},
    "eb4u": {"points": 5000, "max_uses": 5, "used_by": []},
    "9bqd": {"points": 5000, "max_uses": 5, "used_by": []},
    "4zgcy": {"points": 5000, "max_uses": 5, "used_by": []},
    "bqw0t": {"points": 5000, "max_uses": 5, "used_by": []},
    "224xhc": {"points": 5000, "max_uses": 5, "used_by": []},
    "x801u": {"points": 5000, "max_uses": 5, "used_by": []},
    "5vg6": {"points": 5000, "max_uses": 5, "used_by": []},
    "yvib": {"points": 5000, "max_uses": 5, "used_by": []},
    "pjtu": {"points": 5000, "max_uses": 5, "used_by": []},
    "t2hs6": {"points": 5000, "max_uses": 5, "used_by": []},
    "cvkxh": {"points": 5000, "max_uses": 5, "used_by": []},
    "72zw": {"points": 5000, "max_uses": 5, "used_by": []},
    "wu9b7s": {"points": 5000, "max_uses": 5, "used_by": []},
    "pnrsd": {"points": 5000, "max_uses": 5, "used_by": []},
    "olmy": {"points": 5000, "max_uses": 5, "used_by": []},
    "txir": {"points": 5000, "max_uses": 5, "used_by": []},
    "7sl36w": {"points": 5000, "max_uses": 5, "used_by": []},
    "87kute": {"points": 5000, "max_uses": 5, "used_by": []},
    "m56wr": {"points": 5000, "max_uses": 5, "used_by": []},
    "60lj": {"points": 5000, "max_uses": 5, "used_by": []},
    "le8i8": {"points": 5000, "max_uses": 5, "used_by": []},
    "l5il": {"points": 5000, "max_uses": 5, "used_by": []},
    "55adcn": {"points": 5000, "max_uses": 5, "used_by": []},
    "rdxt0": {"points": 5000, "max_uses": 5, "used_by": []},
    "ag3w6": {"points": 5000, "max_uses": 5, "used_by": []},
    "fbadx": {"points": 5000, "max_uses": 5, "used_by": []},
    "72g9pd": {"points": 5000, "max_uses": 5, "used_by": []},
    "kqmot": {"points": 5000, "max_uses": 5, "used_by": []},
    "7j2nnk": {"points": 5000, "max_uses": 5, "used_by": []},
    "4dkgsq": {"points": 5000, "max_uses": 5, "used_by": []},
    "kottg0": {"points": 5000, "max_uses": 5, "used_by": []},
    "6ksw5": {"points": 5000, "max_uses": 5, "used_by": []},
    "3m8g": {"points": 5000, "max_uses": 5, "used_by": []},
    "daro": {"points": 5000, "max_uses": 5, "used_by": []},
    "87b27": {"points": 5000, "max_uses": 5, "used_by": []},
    "nlue": {"points": 5000, "max_uses": 5, "used_by": []},
    "otl83": {"points": 5000, "max_uses": 5, "used_by": []},
    "keyz": {"points": 5000, "max_uses": 5, "used_by": []},
    "ovqx5": {"points": 5000, "max_uses": 5, "used_by": []},
    "6hky9z": {"points": 5000, "max_uses": 5, "used_by": []},
    "ldmz": {"points": 5000, "max_uses": 5, "used_by": []},
    "87z9": {"points": 5000, "max_uses": 5, "used_by": []},
    "da0k": {"points": 5000, "max_uses": 5, "used_by": []},
    "xcvq3d": {"points": 5000, "max_uses": 5, "used_by": []},
    "r1xtoa": {"points": 5000, "max_uses": 5, "used_by": []},
    "yeapav": {"points": 5000, "max_uses": 5, "used_by": []},
    "jwrus": {"points": 5000, "max_uses": 5, "used_by": []},
    "9qveh0": {"points": 5000, "max_uses": 5, "used_by": []},
    "fz8fke": {"points": 5000, "max_uses": 5, "used_by": []},
    "2wbo": {"points": 5000, "max_uses": 5, "used_by": []},
    "r1b0": {"points": 5000, "max_uses": 5, "used_by": []},
    "p2jayl": {"points": 5000, "max_uses": 5, "used_by": []},
    "3ogj53": {"points": 5000, "max_uses": 5, "used_by": []},
    "cf10": {"points": 5000, "max_uses": 5, "used_by": []},
    "kkjn": {"points": 5000, "max_uses": 5, "used_by": []},
    "6jr3": {"points": 5000, "max_uses": 5, "used_by": []},
    "v73mp": {"points": 5000, "max_uses": 5, "used_by": []},
    "k4rt": {"points": 5000, "max_uses": 5, "used_by": []},
    "8noo": {"points": 5000, "max_uses": 5, "used_by": []},
    "8qxg": {"points": 5000, "max_uses": 5, "used_by": []},
    "u6hh": {"points": 5000, "max_uses": 5, "used_by": []},
    "lltze": {"points": 5000, "max_uses": 5, "used_by": []},
    "z4wwy5": {"points": 5000, "max_uses": 5, "used_by": []},
    "wk1rq": {"points": 5000, "max_uses": 5, "used_by": []},
    "ock4": {"points": 5000, "max_uses": 5, "used_by": []},
    "ct4h": {"points": 5000, "max_uses": 5, "used_by": []},
    "bkw9": {"points": 5000, "max_uses": 5, "used_by": []},
    "8br7": {"points": 5000, "max_uses": 5, "used_by": []},
    "ig6mjy": {"points": 5000, "max_uses": 5, "used_by": []},
    "cyxyk": {"points": 5000, "max_uses": 5, "used_by": []},
    "yhmp8": {"points": 5000, "max_uses": 5, "used_by": []},
    "nuraga": {"points": 5000, "max_uses": 5, "used_by": []},
    "ssu32f": {"points": 5000, "max_uses": 5, "used_by": []},
    "jqtk": {"points": 5000, "max_uses": 5, "used_by": []},
    "xopb5p": {"points": 5000, "max_uses": 5, "used_by": []},
    "q98v1t": {"points": 5000, "max_uses": 5, "used_by": []},
    "qthy4": {"points": 5000, "max_uses": 5, "used_by": []},
    "grwc": {"points": 5000, "max_uses": 5, "used_by": []},
    "pat7tg": {"points": 5000, "max_uses": 5, "used_by": []},
    "o549d2": {"points": 5000, "max_uses": 5, "used_by": []},
    "9iky8": {"points": 5000, "max_uses": 5, "used_by": []},
    "uyocwv": {"points": 5000, "max_uses": 5, "used_by": []},
    "v34t": {"points": 5000, "max_uses": 5, "used_by": []},
    "6176ud": {"points": 5000, "max_uses": 5, "used_by": []},
    "vkya1": {"points": 5000, "max_uses": 5, "used_by": []},
    "6o9zg": {"points": 5000, "max_uses": 5, "used_by": []},
    "uyz1": {"points": 5000, "max_uses": 5, "used_by": []},
    "xsjz8p": {"points": 5000, "max_uses": 5, "used_by": []},
    "x73wsk": {"points": 5000, "max_uses": 5, "used_by": []},
    "qebsl0": {"points": 5000, "max_uses": 5, "used_by": []},
    "ep4x2": {"points": 5000, "max_uses": 5, "used_by": []},
    "zh74v8": {"points": 5000, "max_uses": 5, "used_by": []},
    "krdph": {"points": 5000, "max_uses": 5, "used_by": []},
    "tki3": {"points": 5000, "max_uses": 5, "used_by": []},
    "karl": {"points": 5000, "max_uses": 5, "used_by": []},
    "10uwq": {"points": 5000, "max_uses": 5, "used_by": []},
    "h973": {"points": 5000, "max_uses": 5, "used_by": []},
    "ivpiz": {"points": 5000, "max_uses": 5, "used_by": []}
}

# ⚙️ نظام تخزين البيانات (حفظ دائم)
USER_BALANCES = {}
USER_DAILY_GIFT = {}
REFERRAL_USED = {}
REFERRED_USERS = {}

def load_data():
    global USER_BALANCES, USER_DAILY_GIFT, REFERRAL_USED, REFERRED_USERS, GIFT_CODES
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                USER_BALANCES = {int(k): v for k, v in data.get("balances", {}).items()}
                USER_DAILY_GIFT = {int(k): v for k, v in data.get("daily_gift", {}).items()}
                REFERRAL_USED = {int(k): int(v) for k, v in data.get("referral_used", {}).items()}
                REFERRED_USERS = {int(k): set(map(int, v)) for k, v in data.get("referred_users", {}).items()}
                
                # تحميل حالة الأكواد المستعملة لكي لا تضيع استخداماتها
                saved_codes = data.get("gift_codes", {})
                for code in GIFT_CODES:
                    if code in saved_codes:
                        GIFT_CODES[code]["used_by"] = saved_codes[code].get("used_by", [])
        except Exception as e:
            print(f"Error loading data: {e}")

def save_data():
    try:
        data = {
            "balances": {str(k): v for k, v in USER_BALANCES.items()},
            "daily_gift": {str(k): v for k, v in USER_DAILY_GIFT.items()},
            "referral_used": {str(k): str(v) for k, v in REFERRAL_USED.items()},
            "referred_users": {str(k): list(v) for k, v in REFERRED_USERS.items()},
            "gift_codes": GIFT_CODES
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

# استدعاء دالة التحميل الفوري قبل بدء تشغيل البوت
load_data()

# تحديث تلقائي للمستخدمين الذين تم إعطاؤهم نقاط مسبقاً عن طريق المطور
ADMIN_GIVEN = [
    (6062776882, 999999999), (6761049909, 999999999), (6801905753, 999999999),
    (6738914616, 999999999), (5011933081, 999999999), (7201777218, 999999999),
    (6850257404, 999999999), (6102607802, 999999999), (5726244675, 999999999)
]
for uid, pts in ADMIN_GIVEN:
    if uid not in USER_BALANCES:
        USER_BALANCES[uid] = pts
    elif USER_BALANCES[uid] < pts:
        USER_BALANCES[uid] = pts
save_data()

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
        types.InlineKeyboardButton("ℹ️ حول البوت", callback_data="main_about")
    )
    markup.row(types.InlineKeyboardButton("شحن نقاط للبوت 💰", callback_data="charge_points_menu"))
    return markup

# --- القوائم الفرعية للخدمات المنصات ---
def platforms_inline_menu():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("📸 انستغرام", callback_data="instagram_menu"), types.InlineKeyboardButton("🎵 تيك توك", callback_data="tiktok_menu"))
    markup.row(types.InlineKeyboardButton("✈️ تلجرام", callback_data="telegram_menu"), types.InlineKeyboardButton("📘 فيسبوك", callback_data="facebook_menu"))
    markup.row(types.InlineKeyboardButton("✖️ تويتر", callback_data="twitter_menu"), types.InlineKeyboardButton("🧵 ثريدز", callback_data="threads_menu"))
    markup.row(types.InlineKeyboardButton("🎧 سبوتيفاي", callback_data="spotify_menu"), types.InlineKeyboardButton("🟢 كيك", callback_data="kick_menu"))
    markup.row(types.InlineKeyboardButton("🔴 يوتيوب", callback_data="yt_menu"))
    markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_to_main"))
    return markup

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

def send_welcome(chat_id, user_id):
    bot.send_message(chat_id, get_welcome_text(user_id), reply_markup=main_inline_menu())

def edit_to_welcome(chat_id, message_id, user_id):
    bot.edit_message_text(get_welcome_text(user_id), chat_id, message_id, reply_markup=main_inline_menu())

# --- /start ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    text_args = message.text.split()
    
    # حذف الكيبورد القديم لضمان نظافة المحادثة
    clean_msg = bot.send_message(message.chat.id, "جاري فتح البوت...", reply_markup=types.ReplyKeyboardRemove())
    bot.delete_message(message.chat.id, clean_msg.message_id)

    # تسجيل مستخدم جديد بنقاط 0 تلقائياً وحفظ البيانات
    if user_id not in USER_BALANCES:
        USER_BALANCES[user_id] = 0
        save_data()

    # معالجة نظام رابط الإحالة بدقة عند الدخول أول مرة
    if len(text_args) > 1 and user_id not in REFERRAL_USED:
        try:
            referrer_id = int(text_args[1])
            if referrer_id != user_id and referrer_id in USER_BALANCES:
                REFERRAL_USED[user_id] = referrer_id
                if referrer_id not in REFERRED_USERS:
                    REFERRED_USERS[referrer_id] = set()
                REFERRED_USERS[referrer_id].add(user_id)
                
                # إضافة 1000 نقطة للمُحيل وحفظ التعديل
                USER_BALANCES[referrer_id] = USER_BALANCES.get(referrer_id, 0) + 1000
                save_data()
                
                try:
                    bot.send_message(referrer_id, f"🎯 دخل شخص من خلال رابط إحالتك!\n➕ تم إضافة 1000 نقطة إلى حسابك.")
                except Exception:
                    pass
        except ValueError:
            pass

    # التحقق من الاشتراك الإجباري
    if not check_is_subscribed(user_id):
        bot.send_message(message.chat.id, "⚠️ عذراً عزيزي، يجب عليك الاشتراك في قناة البوت أولاً لتتمكن من استخدامه!", reply_markup=force_sub_menu())
        return

    send_welcome(message.chat.id, user_id)

# --- كشف قائمة المتصدرين في الإحالات ---
@bot.message_handler(func=lambda message: message.text in [
    'اكثر مشاركين رابط الإحالة', 'اكثر مشاركين رابط الإحالة', 'أكثر مشاركين رابط الاحالة', '/اكثر مشاركين'
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
        text += f"{medals[i]} *الآيدي:* `{uid}`\n"
        text += f"   ↳ *عدد المشاركات:* {count} {word}\n"
        text += "━━━━━━━━━━━━━━━━\n"
        
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# --- معالجة الأزرار (Callbacks) ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # التحقق من الاشتراك الإجباري
    if call.data == "verify_subscription":
        if check_is_subscribed(user_id):
            bot.delete_message(chat_id, message_id)
            send_welcome(chat_id, user_id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك بالقناة بعد! يرجى الاشتراك أولاً.", show_alert=True)
        return

    if not check_is_subscribed(user_id):
        bot.answer_callback_query(call.id, "⚠️ يجب عليك الاشتراك في القناة أولاً!", show_alert=True)
        return

    if call.data == "back_to_main":
        edit_to_welcome(chat_id, message_id, user_id)
    elif call.data == "main_services":
        bot.edit_message_text("🛒 أهلاً بك في قسم الخدمات، اختر المنصة التي تريد رشقها من الأسفل 👇", chat_id, message_id, reply_markup=platforms_inline_menu())
    elif call.data == "platforms_menu":
        bot.edit_message_text("🛒 أهلاً بك في قسم الخدمات، اختر المنصة التي تريد رشقها من الأسفل 👇", chat_id, message_id, reply_markup=platforms_inline_menu())
    elif call.data == "instagram_menu":
        bot.edit_message_text("📸 قسم: انستغرام\n| اختر الخدمة المطلوبة:", chat_id, message_id, reply_markup=instagram_inline_menu())
    elif call.data == "tiktok_menu":
        bot.edit_message_text("🎵 قسم: تيك توك\n| اختر الخدمة المطلوبة:", chat_id, message_id, reply_markup=tiktok_inline_menu())
    elif call.data == "telegram_menu":
        bot.edit_message_text("✈️ قسم: تلجرام\n| اختر الخدمة المطلوبة:", chat_id, message_id, reply_markup=telegram_inline_menu())
    elif call.data == "facebook_menu":
        bot.edit_message_text("📘 قسم: فيس بوك\n| اختر الخدمة المطلوبة:", chat_id, message_id, reply_markup=facebook_inline_menu())
    elif call.data == "twitter_menu":
        bot.edit_message_text("✖️ قسم: تويتر\n| اختر الخدمة المطلوبة:", chat_id, message_id, reply_markup=twitter_inline_menu())
    elif call.data == "threads_menu":
        bot.edit_message_text("🧵 قسم: ثريدز\n| اختر الخدمة المطلوبة:", chat_id, message_id, reply_markup=threads_inline_menu())
    elif call.data == "spotify_menu":
        bot.edit_message_text("🎧 قسم: سبوتي فاي\n| اختر الخدمة المطلوبة:", chat_id, message_id, reply_markup=spotify_inline_menu())
    elif call.data == "kick_menu":
        bot.edit_message_text("🟢 قسم: كيك\n| اختر الخدمة المطلوبة:", chat_id, message_id, reply_markup=kick_inline_menu())
    elif call.data == "yt_menu":
        bot.edit_message_text("🔴 قسم: يوتيوب\n| اختر الخدمة المطلوبة:", chat_id, message_id, reply_markup=youtube_inline_menu())
        
    elif call.data.startswith("ser_"):
        service_id = int(call.data.split("_")[1])
        service_info = SERVICES_BY_ID.get(service_id)
        if service_info:
            service_name = service_info["name"]
            bot.delete_message(chat_id, message_id)
            msg = bot.send_message(chat_id, f"📥 لقد اخترت خدمة:\n【 {service_name} 】\n\n🔗 يرجى إرسال الرابط المطلوب الآن:")
            bot.register_next_step_handler(msg, process_link, service_id)
            
    elif call.data == "btn_under_dev":
        bot.answer_callback_query(call.id, "🛠️ هذه الميزة قيد التطوير والصيانة حالياً وسيتم إتاحتها قريباً!", show_alert=True)
        
    elif call.data == "main_account":
        acc_text = (
            f"🪪 | معلومات حسابك في البوت:\n\n"
            f"🆔 | ايديك: <code>{user_id}</code>\n"
            f"💎 | عدد نقاطك: {USER_BALANCES.get(user_id, 0)} نقطة\n"
            f"🔗 | عدد الأشخاص الذين دعوتهم: {len(REFERRED_USERS.get(user_id, set()))} عضو"
        )
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_to_main"))
        bot.edit_message_text(acc_text, chat_id, message_id, reply_markup=markup, parse_mode="HTML")
        
    elif call.data == "main_about":
        about_text = (
            "ℹ️ | حول بوت السلطان للدعم:\n\n"
            "• أسرع بوت رشق ودعم في التلجرام.\n"
            "• خدمات سريعة وتحديثات مستمرة لضمان أفضل جودة.\n"
            "• مطور البوت والمستودع الرسمي: @xc_1h"
        )
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_to_main"))
        bot.edit_message_text(about_text, chat_id, message_id, reply_markup=markup)
        
    elif call.data == "charge_points_menu":
        charge_text = (
            "💰 | أسعار شحن النقاط في بوت السلطان:\n\n"
            "- 1$ = 10000 نقطة 💎\n"
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
        markup.row(types.InlineKeyboardButton("📅 الهدية اليومية (+100 نقطة)", callback_data="daily_gift_system"))
        markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_to_main"))
        bot.edit_message_text(collect_text, chat_id, message_id, reply_markup=markup)
        
    elif call.data == "referral_system":
        bot_info = bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
        ref_text = (
            f"🔗 | رابط الإحالة الخاص بك:\n"
            f"<code>{ref_link}</code>\n\n"
            f"• شارك هذا الرابط مع أصدقائك أو مجموعاتك.\n"
            f"• كل شخص يقوم بالدخول للبوت والاشتراك بالقناة من خلال رابطك ستحصل على *1000 نقطة* مجاناً فورا! 🎉"
        )
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("🔙 رجوع لقسم تجميع النقاط", callback_data="collect_menu"))
        bot.edit_message_text(ref_text, chat_id, message_id, reply_markup=markup, parse_mode="HTML")
        
    elif call.data == "daily_gift_system":
        current_time = time.time()
        last_gift_time = USER_DAILY_GIFT.get(user_id, 0)
        
        # 24 ساعة تعادل 86400 ثانية
        if current_time - last_gift_time >= 86400:
            USER_DAILY_GIFT[user_id] = current_time
            USER_BALANCES[user_id] = USER_BALANCES.get(user_id, 0) + 100
            save_data() # حفظ فوري للنقاط الممنوحة بالهدية اليومية
            bot.answer_callback_query(call.id, "🎁 مبروك! حصلت على 100 نقطة هدية يومية.", show_alert=True)
            edit_to_welcome(chat_id, message_id, user_id)
        else:
            remaining_seconds = int(86400 - (current_time - last_gift_time))
            hours = remaining_seconds // 3600
            minutes = (remaining_seconds % 3600) // 60
            bot.answer_callback_query(
                call.id, 
                f"❌ لقد استلمت هديتك اليومية سابقاً!\nيرجى الانتظار: {hours} ساعة و {minutes} دقيقة.", 
                show_alert=True
            )
            
    elif call.data == "use_code_menu":
        bot.delete_message(chat_id, message_id)
        msg = bot.send_message(chat_id, "💳 يرجى إرسال كود الهدية المراد استخدامه:\n(تأكد من كتابة الكود بشكل صحيح)")
        bot.register_next_step_handler(msg, process_gift_code)

# --- استلام وفحص كود الهدية ---
def process_gift_code(message):
    user_id = message.from_user.id
    code_text = message.text.strip()

    if code_text.startswith("/"):
        bot.send_message(message.chat.id, "تم إلغاء العملية.")
        send_welcome(message.chat.id, user_id)
        return

    if code_text in GIFT_CODES:
        code_data = GIFT_CODES[code_text]
        
        if user_id in code_data["used_by"]:
            bot.send_message(message.chat.id, "❌ عذراً، لقد قمت باستخدام هذا الكود مسبقاً!")
            send_welcome(message.chat.id, user_id)
            return
            
        if len(code_data["used_by"]) >= code_data["max_uses"]:
            bot.send_message(message.chat.id, "❌ انتهت صلاحية هذا الكود (وصل للحد الأقصى من الاستخدام)!")
            send_welcome(message.chat.id, user_id)
            return
            
        # إضافة النقاط وتسجيل المستخدم في قائمة مستعملي الكود
        code_data["used_by"].append(user_id)
        USER_BALANCES[user_id] = USER_BALANCES.get(user_id, 0) + code_data["points"]
        save_data() # حفظ فوري لتعديل استخدام الكود وزيادة النقاط
        
        bot.send_message(message.chat.id, f"✅ تم تفعيل الكود بنجاح!\n➕ تم إضافة {code_data['points']} نقطة إلى حسابك.")
    else:
        bot.send_message(message.chat.id, "❌ هذا الكود غير صحيح أو غير موجود!")
        
    send_welcome(message.chat.id, user_id)

# --- فحص حالة الطلب من السيرفر ---
def process_check_order(message):
    user_id = message.from_user.id
    order_id = message.text.strip()

    if order_id.startswith("/"):
        bot.send_message(message.chat.id, "تم إلغاء فحص الطلب.")
        send_welcome(message.chat.id, user_id)
        return

    bot.send_message(message.chat.id, "⏳ جاري الاستعلام عن حالة الطلب من السيرفر...")
    
    api_data = {"key": API_KEY, "action": "status", "order": order_id}
    try:
        response = requests.post(API_URL, data=api_data, timeout=10)
        result = response.json()
        
        if "status" in result:
            status_map = {
                "Pending": "⏳ قيد الانتظار", "In progress": "🔄 جاري التنفيذ",
                "Completed": "✅ مكتمل", "Partial": "⚠️ مكتمل جزئياً", "Canceled": "❌ ملغي"
            }
            status_ar = status_map.get(result["status"], result["status"])
            
            res_text = (
                f"📊 تفاصيل الطلب رقم: `{order_id}`\n\n"
                f"📌 الحالة: *{status_ar}*\n"
                f"🔢 الكمية البدئية: {result.get('start_count', 0)}\n"
                f"📉 الكمية المتبقية: {result.get('remains', 0)}"
            )
            bot.send_message(message.chat.id, res_text, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, f"❌ لم نتمكن من العثور على بيانات لهذا الطلب.\nالسبب: {result.get('error', 'رقم الطلب غير صحيح')}")
    except Exception:
        bot.send_message(message.chat.id, "❌ فشل الاتصال بالسيرفر، يرجى المحاولة لاحقاً.")
        
    send_welcome(message.chat.id, user_id)

# --- استلام الرابط ---
def process_link(message, service_id):
    user_id = message.from_user.id
    link = message.text.strip()

    if link.startswith("/"):
        bot.send_message(message.chat.id, "تم إلغاء الطلب.")
        send_welcome(message.chat.id, user_id)
        return

    msg = bot.send_message(message.chat.id, "🔢 يرجى إرسال الكمية المطلوبة الآن:\n(مثال: 1000)")
    bot.register_next_step_handler(msg, process_quantity, service_id, link)

# --- استلام الكمية وإرسال الطلب للسيرفر ---
def process_quantity(message, service_id, link):
    user_id = message.from_user.id
    qty_text = message.text.strip()

    if qty_text.startswith("/"):
        bot.send_message(message.chat.id, "تم إلغاء الطلب.")
        send_welcome(message.chat.id, user_id)
        return

    try:
        qty = int(qty_text)
        if qty <= 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "❌ يرجى إرسال كمية صحيحة أكبر من صفر!")
        send_welcome(message.chat.id, user_id)
        return

    service_info = SERVICES_BY_ID.get(service_id)
    if not service_info:
        bot.send_message(message.chat.id, "❌ خطأ في النظام الداخلي للخدمة.")
        send_welcome(message.chat.id, user_id)
        return

    cost = int((qty / 1000) * service_info["points"])
    balance = USER_BALANCES.get(user_id, 0)

    if balance < cost:
        bot.send_message(message.chat.id, f"❌ عذراً، نقاطك غير كافية!\n💰 التكلفة: {cost} نقطة\n💎 رصيدك: {balance} نقطة")
        send_welcome(message.chat.id, user_id)
        return

    # خصم النقاط وحفظ البيانات قبل إرسال الطلب للـ API لضمان الأمان
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
            # إعادة النقاط في حال رفض السيرفر للطلب
            USER_BALANCES[user_id] += cost
            save_data()
            bot.send_message(message.chat.id, f"❌ رفض الموقع الطلب:\n{result.get('error', 'خطأ غير معروف')}\n🔄 تم إعادة نقاطك.")
    except Exception:
        # إعادة النقاط في حال حدوث خطأ اتصال بالسيرفر
        USER_BALANCES[user_id] += cost
        save_data()
        bot.send_message(message.chat.id, "❌ فشل الاتصال بالسيرفر لإتمام الطلب، تم إعادة نقاطك بالكامل.")

    send_welcome(message.chat.id, user_id)

# --- تشغيل البوت بشكل مستمر وضد الانقطاع ---
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(5)
