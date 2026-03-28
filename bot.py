#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeternis Core - Official Discord Bot
Project: Aeternis MU Online
"""

import os
import discord
from dotenv import load_dotenv

# 1. Загрузка переменных окружения из файла .env
load_dotenv()

# 2. Получение токена
TOKEN = os.getenv('DISCORD_TOKEN')

# Проверка наличия токена
if not TOKEN:
    print("❌ ОШИБКА: Токен не найден! Проверьте файл .env")
    exit()

# 3. Настройка намерений (Intents)
# Это права доступа бота к данным сервера
intents = discord.Intents.default()
intents.message_content = True  # Для чтения сообщений (будет нужно для команд)
intents.members = True          # Для доступа к списку участников

# 4. Инициализация клиента
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """
    Срабатывает, когда бот успешно подключился к Discord.
    Здесь мы устанавливаем статус и активность.
    """
    
    # 🟢 Установка статуса и активности
    await client.change_presence(
        status=discord.Status.do_not_disturb,  # 🔴 Статус: Не беспокоить
        activity=discord.Activity(
            type=discord.ActivityType.watching, # 📺 Тип активности: Смотрит
            name="Aeternis MU Online"           # 📝 Текст активности
        )
    )
    
    # 🖨️ Вывод информации в консоль
    print("✅ Aeternis Core успешно запущен!")
    print(f"👤 Бот: {client.user.name}")
    print(f"🆔 ID: {client.user.id}")
    print(f"🔴 Статус: Не беспокоить (Do Not Disturb)")
    print("-------------------------------")

# 5. Запуск бота
if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except discord.LoginFailure:
        print("❌ ОШИБКА: Неверный токен Discord.")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
