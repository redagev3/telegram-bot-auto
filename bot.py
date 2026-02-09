# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime

load_dotenv()
TOKEN = "8355969427:AAE90WG33-Jdrm5Pg915ZziUeZg3kyCblSg"
CHANNEL_ID = -1003288178338
WHITELIST = [8160020054]
ADMINS = [8160020054]
DB_FILE = "users.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id TEXT PRIMARY KEY, name TEXT, banned INTEGER, warns INTEGER, downloads INTEGER, has_access INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS keys
                 (key_id INTEGER PRIMARY KEY AUTOINCREMENT, key_text TEXT UNIQUE, used INTEGER, used_by TEXT)''')
    conn.commit()
    conn.close()

def load_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (str(user_id),))
    row = c.fetchone()
    conn.close()
    if row:
        return {"name": row[1], "banned": bool(row[2]), "warns": row[3], "downloads": row[4], "has_access": bool(row[5])}
    return None

def save_user(user_id, user_data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?)',
              (str(user_id), user_data["name"], int(user_data["banned"]), user_data["warns"], user_data["downloads"], int(user_data.get("has_access", False))))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    rows = c.fetchall()
    conn.close()
    users = {}
    for row in rows:
        users[row[0]] = {"name": row[1], "banned": bool(row[2]), "warns": row[3], "downloads": row[4], "has_access": bool(row[5])}
    return users

import random
import string

KEYS_LIST = [
    "BOT-K7F3P9Q2R5W8X1Z4", "BOT-A2B5C8D1E4F7G0H3",
    "BOT-J6K9L2M5N8P1Q4S7", "BOT-T3V6Y9B2E5H8K1N4",
    "BOT-R7U0X3Z6C9F2I5L8", "BOT-O1S4V7Y0B3E6H9K2",
    "BOT-M5P8S1V4Y7B0E3H6", "BOT-G9J2M5P8S1V4Y7B",
    "BOT-D0F3I6L9O2R5U8X1", "BOT-Q4T7W0Z3C6F9I2L5",
    "BOT-N8R1U4X7Z0C3F6I9", "BOT-H2K5N8Q1T4W7Z0C3",
    "BOT-E6I9L2O5R8U1X4Z7", "BOT-B3F6I9L2O5R8U1X",
    "BOT-Y7A0D3G6J9M2P5S8", "BOT-W4Z7C0F3I6L9O2R",
    "BOT-U1X4Z7C0F3I6L9O2", "BOT-S5V8Y2B5E8H1K4N7",
    "BOT-P9M2Q5T8W1Z4C7F0", "BOT-L3O6R9U2X5Z8C1F",
    "BOT-J7H0K3N6Q9T2W5Z8", "BOT-G1D4G7J0M3P6S9V2",
    "BOT-E8B1E4H7K0N3Q6T9", "BOT-C5Z8C1F4I7L0O3R6",
    "BOT-A2Y5B8E1H4K7N0Q3", "BOT-X9W2Z5C8F1I4L7O0",
    "BOT-V6T9W2Z5C8F1I4L", "BOT-R3Q6T9W2Z5C8F1I",
    "BOT-O0N3Q6T9W2Z5C8F", "BOT-M7K0N3Q6T9W2Z5C",
    "BOT-J4H7K0N3Q6T9W2Z", "BOT-G1E4H7K0N3Q6T9W",
    "BOT-D8B1E4H7K0N3Q6T", "BOT-A5Y8B1E4H7K0N3Q",
    "BOT-X2V5Y8B1E4H7K0N", "BOT-U9S2V5Y8B1E4H7K",
    "BOT-R6P9S2V5Y8B1E4H", "BOT-O3M6P9S2V5Y8B1E",
    "BOT-L0J3M6P9S2V5Y8B", "BOT-I7G0J3M6P9S2V5Y",
    "BOT-F4D7G0J3M6P9S2V", "BOT-C1A4D7G0J3M6P9S",
    "BOT-Z8X1A4D7G0J3M6P", "BOT-W5U8X1A4D7G0J3M",
    "BOT-T2R5U8X1A4D7G0J", "BOT-Q9O2R5U8X1A4D7G",
    "BOT-N6L9O2R5U8X1A4D", "BOT-K3I6L9O2R5U8X1A",
    "BOT-H0F3I6L9O2R5U8X", "BOT-E7C0F3I6L9O2R5U",
    "BOT-B4Z7C0F3I6L9O2R", "BOT-Y1W4Z7C0F3I6L9O",
    "BOT-V8T1W4Z7C0F3I6L", "BOT-S5Q8T1W4Z7C0F3I",
    "BOT-P2N5Q8T1W4Z7C0F", "BOT-M9K2N5Q8T1W4Z7C",
    "BOT-J6H9K2N5Q8T1W4Z", "BOT-G3E6H9K2N5Q8T1W",
    "BOT-D0B3E6H9K2N5Q8T", "BOT-A7X0B3E6H9K2N5Q",
    "BOT-X4U7X0B3E6H9K2N", "BOT-U1R4U7X0B3E6H9K",
    "BOT-R8O1R4U7X0B3E6H", "BOT-O5L8O1R4U7X0B3E",
    "BOT-L2I5L8O1R4U7X0B", "BOT-I9F2I5L8O1R4U7X",
    "BOT-F6C9F2I5L8O1R4U", "BOT-C3Z6C9F2I5L8O1R",
    "BOT-Z0W3Z6C9F2I5L8O", "BOT-W7T0W3Z6C9F2I5L",
    "BOT-T4Q7T0W3Z6C9F2I", "BOT-Q1N4Q7T0W3Z6C9F",
    "BOT-N8K1N4Q7T0W3Z6C", "BOT-K5H8K1N4Q7T0W3Z",
    "BOT-H2E5H8K1N4Q7T0W", "BOT-E9B2E5H8K1N4Q7T",
    "BOT-B6X9B2E5H8K1N4Q", "BOT-Y3U6X9B2E5H8K1N",
    "BOT-V0R3U6X9B2E5H8K", "BOT-S7O0R3U6X9B2E5H",
    "BOT-P4L7O0R3U6X9B2E", "BOT-M1I4L7O0R3U6X9B",
    "BOT-J8F1I4L7O0R3U6X", "BOT-G5C8F1I4L7O0R3U",
    "BOT-D2Z5C8F1I4L7O0R", "BOT-A9W2Z5C8F1I4L7O",
    "BOT-X6T9W2Z5C8F1I4L", "BOT-U3Q6T9W2Z5C8F1I",
    "BOT-R0N3Q6T9W2Z5C8F", "BOT-O7K0N3Q6T9W2Z5C",
    "BOT-L4H7K0N3Q6T9W2Z", "BOT-I1E4H7K0N3Q6T9W",
    "BOT-F8B1E4H7K0N3Q6T", "BOT-C5Y8B1E4H7K0N3Q",
    "BOT-Z2V5Y8B1E4H7K0N", "BOT-W9S2V5Y8B1E4H7K",
    "BOT-T6P9S2V5Y8B1E4H", "BOT-Q3M6P9S2V5Y8B1E",
    "BOT-N0J3M6P9S2V5Y8B", "BOT-K7G0J3M6P9S2V5Y"
]

def check_key(key_text):
    return key_text in KEYS_LIST

def add_key(key_text):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO keys (key_text, used, used_by) VALUES (?, 0, NULL)', (key_text,))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

init_db()

FILES = {
    "system1": {
        "name": "🎮 [A-Chassis 1.7.1 Sochi County Full FIX]",
        "url": "https://drive.google.com/file/d/1mPeBydKjNz_C9ARvmHQFAFZ-NYqICxtH/view?usp=sharing",
        "description": "Профессиональная система для Roblox Studio"
    },
    "system2": {
        "name": "🎮 Пак машин из Sochi County (Не которые оживлены) (Chassis новый)",
        "url": "https://drive.google.com/file/d/1Iubaw3PRbWMQ50w0jKODwTwFvEvruCp8/view?usp=sharing",
        "description": "Продвинутая система с интеграциями"
    },
    "system3": {
        "name": "🎮 Префикс + Галочка для своей игры",
        "url": "https://drive.google.com/file/d/1r9Lvq7sasuHDB3x6WlqoorEbJir5b4VI/view?usp=sharing",
        "description": "Легкая и быстрая система"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = str(update.message.from_user.id)
        user_name = update.message.from_user.first_name
        
        user_data = load_user(user_id)
        if not user_data:
            save_user(user_id, {
                "name": user_name,
                "banned": False,
                "warns": 0,
                "downloads": 0
            })
        
        keyboard = [
            [KeyboardButton("👤 Профиль")],
            [KeyboardButton("💾 Сливы")],
            [KeyboardButton("📞 Поддержка")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🎉 Добро пожаловать!\n\nВыбери раздел:",
            reply_markup=reply_markup
        )
    except Exception as e:
        print(f"Error in start: {e}")

async def adminpanel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(update.message.from_user.id)
    
    if user_id not in ADMINS:
        return
    
    keyboard = [
        [KeyboardButton("👥 Список пользователей")],
        [KeyboardButton("🚫 Забанить")],
        [KeyboardButton("✅ Разбанить")],
        [KeyboardButton("⚠️ Предупреждение")],
        [KeyboardButton("📢 Отправить уведомление")],
        [KeyboardButton("🔑 Создать ключ")],
        [KeyboardButton("⬅️ Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🎛️ Админ-панель",
        reply_markup=reply_markup
    )
    context.user_data['admin_mode'] = True

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)
    user_name = update.message.from_user.first_name
    
    user_data = load_user(user_id)
    if not user_data:
        save_user(user_id, {
            "name": user_name,
            "banned": False,
            "warns": 0,
            "downloads": 0,
            "has_access": False
        })
        user_data = load_user(user_id)
    
    # Проверка ввода ключа
    if context.user_data.get('waiting_for_key'):
        # Сначала проверяем кнопку Назад
        if text == "⬅️ Назад":
            context.user_data['waiting_for_key'] = False
            keyboard = [
                [KeyboardButton("👤 Профиль")],
                [KeyboardButton("💾 Сливы")],
                [KeyboardButton("📞 Поддержка")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(
                "🎉 Добро пожаловать!\n\nВыбери раздел:",
                reply_markup=reply_markup
            )
            return
        
        # Потом проверяем ключ
        if check_key(text):
            user_data["has_access"] = True
            save_user(user_id, user_data)
            context.user_data['waiting_for_key'] = False
            
            keyboard = [
                [KeyboardButton("👤 Профиль")],
                [KeyboardButton("💾 Сливы")],
                [KeyboardButton("📞 Поддержка")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(
                "✅ Ключ активирован! Теперь у тебя есть доступ к файлам.",
                reply_markup=reply_markup
            )
            return
        else:
            await update.message.reply_text("❌ Неверный ключ. Попробуй еще раз:")
            return
    
    if user_data.get("banned"):
        await update.message.reply_text("🚫 Ты забанен и не можешь использовать бота")
        return

    if context.user_data.get('admin_mode') and int(user_id) in ADMINS:
        if text == "👥 Список пользователей":
            user_list = "👥 Список пользователей:\n\n"
            all_users = get_all_users()
            for uid, user_info in all_users.items():
                status = "🚫 Забанен" if user_info.get("banned") else "✅ Активен"
                warns = user_info.get("warns", 0)
                user_list += f"ID: {uid}\nИмя: {user_info['name']}\nСтатус: {status}\nПредупреждений: {warns}\n\n"
            await update.message.reply_text(user_list)
            return
        
        elif text == "🚫 Забанить":
            await update.message.reply_text("Отправь ID пользователя:")
            context.user_data['admin_action'] = 'ban'
            return
        
        elif text == "✅ Разбанить":
            await update.message.reply_text("Отправь ID пользователя:")
            context.user_data['admin_action'] = 'unban'
            return
        
        elif text == "⚠️ Предупреждение":
            await update.message.reply_text("Отправь ID пользователя:")
            context.user_data['admin_action'] = 'warn'
            return
        
        elif text == "📢 Отправить уведомление":
            await update.message.reply_text("Напиши текст уведомления:")
            context.user_data['admin_action'] = 'notify'
            return
        
        elif text == "🔑 Создать ключ":
            import random
            import string
            key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if add_key(key):
                await update.message.reply_text(f"✅ Ключ создан: `{key}`")
            else:
                await update.message.reply_text("❌ Ошибка при создании ключа")
            return
        
        elif text == "⬅️ Назад":
            context.user_data['admin_mode'] = False
            keyboard = [
                [KeyboardButton("👤 Профиль")],
                [KeyboardButton("💾 Сливы")],
                [KeyboardButton("📞 Поддержка")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("🎉 Добро пожаловать!\n\nВыбери раздел:", reply_markup=reply_markup)
            return
        
        action = context.user_data.get('admin_action')
        if action == 'ban':
            try:
                target_id = str(int(text))
                target_data = load_user(target_id)
                if target_data:
                    target_data["banned"] = True
                    save_user(target_id, target_data)
                    await update.message.reply_text(f"🚫 Пользователь {target_data['name']} забанен!")
                else:
                    await update.message.reply_text("❌ Пользователь не найден")
                context.user_data['admin_action'] = None
            except:
                await update.message.reply_text("❌ Неверный ID")
            return
        
        elif action == 'unban':
            try:
                target_id = str(int(text))
                target_data = load_user(target_id)
                if target_data:
                    target_data["banned"] = False
                    save_user(target_id, target_data)
                    await update.message.reply_text(f"✅ Пользователь {target_data['name']} разбанен!")
                else:
                    await update.message.reply_text("❌ Пользователь не найден")
                context.user_data['admin_action'] = None
            except:
                await update.message.reply_text("❌ Неверный ID")
            return
        
        elif action == 'warn':
            try:
                target_id = str(int(text))
                target_data = load_user(target_id)
                if target_data:
                    target_data["warns"] = target_data.get("warns", 0) + 1
                    warns = target_data["warns"]
                    save_user(target_id, target_data)
                    await update.message.reply_text(f"⚠️ Предупреждение выдано ({warns}/3)")
                    
                    if warns >= 3:
                        target_data["banned"] = True
                        save_user(target_id, target_data)
                        await update.message.reply_text(f"🚫 Пользователь автоматически забанен!")
                else:
                    await update.message.reply_text("❌ Пользователь не найден")
                context.user_data['admin_action'] = None
            except:
                await update.message.reply_text("❌ Неверный ID")
            return

    if text == "👤 Профиль":
        try:
            current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
            
            role_text = ""
            if int(user_id) in ADMINS:
                role_text = "\n🎖️ Роль: 👑 Админ"
            
            keyboard = [[KeyboardButton("⬅️ Назад")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            
            downloads = user_data.get('downloads', 0)
            caption_text = f"👤 Ваш профиль:\n\n📆 Последний вход: {current_time}\n\n🔑 ID: {user_id}\n💎 Никнейм: @{update.message.from_user.username or 'не указан'}\n📥 Скачиваний: {downloads}{role_text}"
            
            await update.message.reply_photo(
                photo="https://drive.google.com/uc?id=1lLD2UGFbJaGM1fBQ7Vz0a5-l_mP5ciDQ&export=view",
                caption=caption_text,
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"Error loading profile photo: {e}")
            current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
            role_text = ""
            if int(user_id) in ADMINS:
                role_text = "\n🎖️ Роль: 👑 Админ"
            
            keyboard = [[KeyboardButton("⬅️ Назад")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            
            downloads = user_data.get('downloads', 0)
            text_msg = f"👤 Ваш профиль:\n\n📆 Последний вход: {current_time}\n\n🔑 ID: {user_id}\n💎 Никнейм: @{update.message.from_user.username or 'не указан'}\n📥 Скачиваний: {downloads}{role_text}"
            
            await update.message.reply_text(
                text_msg,
                reply_markup=reply_markup
            )

    elif text == "💾 Сливы":
        if user_data.get("banned"):
            await update.message.reply_text("🚫 Ты забанен и не можешь скачивать файлы")
            return
        
        if user_data.get("has_access"):
            keyboard = []
            for file_id, file_info in FILES.items():
                keyboard.append([KeyboardButton(file_info["name"])])
            keyboard.append([KeyboardButton("⬅️ Назад")])
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

            await update.message.reply_text(
                "💾 Доступные файлы:",
                reply_markup=reply_markup
            )
            context.user_data["in_files"] = True
            return
        
        keyboard = [[KeyboardButton("⬅️ Назад")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🔑 У тебя нет доступа!\n\nВведи ключ доступа:",
            reply_markup=reply_markup
        )
        context.user_data['waiting_for_key'] = True

    elif text in [file_info["name"] for file_info in FILES.values()]:
        file_info = None
        for f_info in FILES.values():
            if f_info["name"] == text:
                file_info = f_info
                break

        if file_info:
            user_data["downloads"] = user_data.get("downloads", 0) + 1
            save_user(user_id, user_data)
            
            keyboard = [[KeyboardButton("⬅️ Назад")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(
                f"{file_info['name']}\n\n{file_info['description']}\n\nСсылка: {file_info['url']}",
                reply_markup=reply_markup
            )

    elif text == "📞 Поддержка":
        try:
            keyboard = [[KeyboardButton("⬅️ Назад")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            
            await update.message.reply_photo(
                photo="https://drive.google.com/uc?id=1hzzbSlEKxu39ve_GrtjaHiiPCKFZEP1p&export=view",
                caption="📞 Поддержка\n\nНапиши @Durovgentlemen если есть вопросы",
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"Error loading support photo: {e}")
            keyboard = [[KeyboardButton("⬅️ Назад")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(
                "📞 Поддержка\n\nНапиши @Durovgentlemen если есть вопросы",
                reply_markup=reply_markup
            )

    elif text == "⬅️ Назад":
        keyboard = [
            [KeyboardButton("👤 Профиль")],
            [KeyboardButton("💾 Сливы")],
            [KeyboardButton("📞 Поддержка")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🎉 Добро пожаловать!\n\nВыбери раздел:",
            reply_markup=reply_markup
        )
        context.user_data["in_files"] = False
        context.user_data['admin_mode'] = False

def main():
    try:
        app = Application.builder().token(TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("adminpanel", adminpanel))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

        print("✅ Бот запущен...")
        app.run_polling(allowed_updates=["message"], drop_pending_updates=True)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
