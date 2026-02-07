import subprocess
import sys

# Запускаем только основной бот
process = subprocess.Popen([sys.executable, "bot.py"])
process.wait()
