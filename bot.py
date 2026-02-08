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
                 (user_id TEXT PRIMARY KEY, name TEXT, banned INTEGER, warns INTEGER, downloads INTEGER)''')
    conn.commit()
    conn.close()

def load_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (str(user_id),))
    row = c.fetchone()
    conn.close()
    if row:
        return {"name": row[1], "banned": bool(row[2]), "warns": row[3], "downloads": row[4]}
    return None

def save_user(user_id, user_data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)',
              (str(user_id), user_data["name"], int(user_data["banned"]), user_data["warns"], user_data["downloads"]))
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
        users[row[0]] = {"name": row[1], "banned": bool(row[2]), "warns": row[3], "downloads": row[4]}
    return users

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
            "downloads": 0
        })
        user_data = load_user(user_id)
    
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
