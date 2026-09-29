import os
import sys

print("================================")
print("KVAZAR START TEST")
print("================================")

print("Python:", sys.version)
print("Рабочая папка:", os.getcwd())
print("BOT_TOKEN найден:", bool(os.getenv("BOT_TOKEN")))

print("Проверяю импорт discord...")

try:
    import discord
    print("discord.py: OK")
    print("Версия:", discord.__version__)
except Exception as e:
    print("discord.py ERROR:")
    print(repr(e))
    raise

print("Проверка завершена успешно.")
print("================================")
print("PROCESS ALIVE")
print("================================")

# Чтобы процесс не завершился сразу
import time

while True:
    time.sleep(60)
