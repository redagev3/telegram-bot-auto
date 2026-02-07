# -*- coding: utf-8 -*-
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
TOKEN = "8355969427:AAE90WG33-Jdrm5Pg915ZziUeZg3kyCblSg"
CHANNEL_ID = -1003288178338
WHITELIST = [8160020054]
ADMINS = [8160020054]
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

USERS = load_users()

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
        
        if user_id not in USERS:
            USERS[user_id] = {
                "name": user_name,
                "banned": False,
                "warns": 0,
                "downloads": 0
            }
            save_users(USERS)
        
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
    
    if user_id not in USERS:
        USERS[user_id] = {
            "name": user_name,
            "banned": False,
            "warns": 0,
            "downloads": 0
        }
        save_users(USERS)
    
    if USERS.get(user_id, {}).get("banned"):
        await update.message.reply_text("🚫 Ты забанен и не можешь использовать бота")
        return

    if context.user_data.get('admin_mode') and int(user_id) in ADMINS:
        if text == "👥 Список пользователей":
            user_list = "👥 Список пользователей:\n\n"
            for uid, user_info in USERS.items():
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
                if target_id in USERS:
                    USERS[target_id]["banned"] = True
                    save_users(USERS)
                    await update.message.reply_text(f"🚫 Пользователь {USERS[target_id]['name']} забанен!")
                else:
                    await update.message.reply_text("❌ Пользователь не найден")
                context.user_data['admin_action'] = None
            except:
                await update.message.reply_text("❌ Неверный ID")
            return
        
        elif action == 'unban':
            try:
                target_id = str(int(text))
                if target_id in USERS:
                    USERS[target_id]["banned"] = False
                    save_users(USERS)
                    await update.message.reply_text(f"✅ Пользователь {USERS[target_id]['name']} разбанен!")
                else:
                    await update.message.reply_text("❌ Пользователь не найден")
                context.user_data['admin_action'] = None
            except:
                await update.message.reply_text("❌ Неверный ID")
            return
        
        elif action == 'warn':
            try:
                target_id = str(int(text))
                if target_id in USERS:
                    USERS[target_id]["warns"] = USERS[target_id].get("warns", 0) + 1
                    warns = USERS[target_id]["warns"]
                    save_users(USERS)
                    await update.message.reply_text(f"⚠️ Предупреждение выдано ({warns}/3)")
                    
                    if warns >= 3:
                        USERS[target_id]["banned"] = True
                        save_users(USERS)
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
            
            caption_text = f"👤 Ваш профиль:\n\n📆 Последний вход: {current_time}\n\n🔑 ID: {user_id}\n💎 Никнейм: @{update.message.from_user.username or 'не указан'}\n📥 Скачиваний: {USERS.get(user_id, {}).get('downloads', 0)}{role_text}"
            
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
            
            text_msg = f"👤 Ваш профиль:\n\n📆 Последний вход: {current_time}\n\n🔑 ID: {user_id}\n💎 Никнейм: @{update.message.from_user.username or 'не указан'}\n📥 Скачиваний: {USERS.get(user_id, {}).get('downloads', 0)}{role_text}"
            
            await update.message.reply_text(
                text_msg,
                reply_markup=reply_markup
            )

    elif text == "💾 Сливы":
        if USERS.get(user_id, {}).get("banned"):
            await update.message.reply_text("🚫 Ты забанен и не можешь скачивать файлы")
            return
        
        if int(user_id) in WHITELIST:
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
        
        is_subscribed = False
        try:
            member = await context.bot.get_chat_member(CHANNEL_ID, int(user_id))
            if member.status in ["member", "administrator", "creator"]:
                is_subscribed = True
            print(f"User {user_id} subscription status: {member.status}")
        except Exception as e:
            print(f"Subscription check error for user {user_id}: {e}")
            is_subscribed = False
        
        if not is_subscribed:
            keyboard = [[KeyboardButton("⬅️ Назад")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(
                "❌ Ты не подписан на канал!\n\nПодпишись: https://t.me/bitocer\n\nПосле подписки попробуй снова",
                reply_markup=reply_markup
            )
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
            if user_id in USERS:
                USERS[user_id]["downloads"] = USERS[user_id].get("downloads", 0) + 1
                save_users(USERS)
            
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
