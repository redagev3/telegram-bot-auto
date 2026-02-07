import subprocess
import os
import time
from datetime import datetime

# Конфиг
REPO_PATH = "."
GIT_USER = "redagev3"
GIT_EMAIL = "katqw3@gmail.com"
GIT_TOKEN = "YOUR_GITHUB_TOKEN"  # Замени на свой токен

def setup_git():
    """Настраиваем Git"""
    os.system(f'git config user.name "{GIT_USER}"')
    os.system(f'git config user.email "{GIT_EMAIL}"')

def auto_push():
    """Автоматически пушит изменения"""
    while True:
        try:
            # Проверяем изменения
            result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            
            if result.stdout.strip():  # Если есть изменения
                print(f"[{datetime.now()}] Найдены изменения, пушим...")
                
                os.system("git add .")
                os.system(f'git commit -m "Auto update {datetime.now()}"')
                os.system("git push")
                
                print(f"[{datetime.now()}] ✅ Успешно запушено!")
            
            # Проверяем каждые 5 минут
            time.sleep(300)
        
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(60)

if __name__ == "__main__":
    setup_git()
    auto_push()
