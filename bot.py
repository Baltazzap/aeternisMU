import os
import discord
from dotenv import load_dotenv

# Загружаем переменные из файла .env (если он есть)
load_dotenv()

# Получаем токен из переменных окружения
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("Ошибка: Токен не найден! Проверьте файл .env или настройки хостинга.")
    exit()

# Настройка намерений (Intents) - обязательно для новых версий API
intents = discord.Intents.default()
intents.message_content = True  # На всякий случай, если потом понадобиется читать сообщения

# Создание клиента
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Бот успешно запущен!')
    print(f'👤 Логин: {client.user.name}')
    print(f'🆔 ID: {client.user.id}')
    print('---------------------------')

# Запуск бота
try:
    client.run(TOKEN)
except discord.LoginFailure:
    print("❌ Ошибка входа: Неверный токен дискорда.")
