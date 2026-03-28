#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeternis Core - Official Discord Bot
Project: Aeternis MU Online
"""

import os
import discord
from dotenv import load_dotenv
from discord.ui import Button, View

# ============================================================
# ⚙️ КОНФИГУРАЦИЯ ПРАВ ДОСТУПА
# ============================================================

OWNER_IDS = [
    314805583788244993,
]

ADMIN_ROLE_IDS = [
    1487181204816920769,
    1487360978181160980,
    1487360985688969296,
    1487360986947129385,
    1487360987131547688,
    1487360987727138939,
]

# ============================================================
# 🌍 ЯЗЫКОВЫЕ РОЛИ (ID)
# ============================================================

LANGUAGE_ROLES = {
    "general": 1487363000322232390,      # 🌍 General
    "es": 1487363000980476095,           # 🇪🇸 Español
    "pt": 1487363006374350908,           # 🇵🇹 Português
    "ru": 1487363006869405696,           # 🇷🇺 Русский
    "tr": 1487363006894706791,           # 🇹🇷 Türkçe
    "vn": 1487371357573480540,           # 🇻🇳 Tiếng Việt
    "ph": 1487371358085316698,           # 🇵🇭 Filipino
}

# ============================================================

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("❌ ОШИБКА: Токен не найден! Проверьте файл .env")
    exit()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


# ============================================================
# 🔐 ФУНКЦИИ ПРОВЕРКИ ПРАВ
# ============================================================

def is_owner(user):
    return user.id in OWNER_IDS


def is_admin(member):
    if not isinstance(member, discord.Member):
        return False
    return any(role.id in ADMIN_ROLE_IDS for role in member.roles)


def has_permission(member, admin_only=False):
    if is_owner(member.user if hasattr(member, 'user') else member):
        return True
    if not admin_only and is_admin(member):
        return True
    return False

# ============================================================
# 🎛️ КЛАССЫ КНОПОК И VIEW (PERSISTENT)
# ============================================================

class LanguageRoleButton(Button):
    """Кнопка для выбора языковой роли"""
    
    def __init__(self, label, emoji, role_id, style=discord.ButtonStyle.secondary):
        # custom_id должен быть уникальным и постоянным для работы после перезагрузки
        super().__init__(label=label, emoji=emoji, style=style, custom_id=f"lang_{role_id}")
        self.role_id = role_id
    
    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        
        role = guild.get_role(self.role_id)
        if not role:
            await interaction.response.send_message("❌ Роль не найдена!", ephemeral=True)
            return
        
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(
                f"❌ Роль **{role.name}** удалена.",
                ephemeral=True
            )
        else:
            await member.add_roles(role)
            await interaction.response.send_message(
                f"✅ Роль **{role.name}** добавлена!",
                ephemeral=True
            )


class LanguageRoleView(View):
    """View с кнопками выбора языковых ролей (Вечный)"""
    
    def __init__(self):
        # timeout=None делает кнопки активными бесконечно (после перезагрузки тоже)
        super().__init__(timeout=None)
        
        self.add_item(LanguageRoleButton(label="General", emoji="🌍", role_id=LANGUAGE_ROLES["general"], style=discord.ButtonStyle.primary))
        self.add_item(LanguageRoleButton(label="Español", emoji="🇪🇸", role_id=LANGUAGE_ROLES["es"]))
        self.add_item(LanguageRoleButton(label="Português", emoji="🇵🇹", role_id=LANGUAGE_ROLES["pt"]))
        self.add_item(LanguageRoleButton(label="Русский", emoji="🇷🇺", role_id=LANGUAGE_ROLES["ru"]))
        self.add_item(LanguageRoleButton(label="Türkçe", emoji="🇹🇷", role_id=LANGUAGE_ROLES["tr"]))
        self.add_item(LanguageRoleButton(label="Tiếng Việt", emoji="🇻🇳", role_id=LANGUAGE_ROLES["vn"]))
        self.add_item(LanguageRoleButton(label="Filipino", emoji="🇵🇭", role_id=LANGUAGE_ROLES["ph"]))


# ============================================================
# 📜 СОЗДАНИЕ EMBED СООБЩЕНИЯ
# ============================================================

def create_roles_embed():
    """Создаёт красивое Embed для выбора ролей"""
    
    embed = discord.Embed(
        title="🌍 Language Selection | Выбор Языка",
        description=(
            "**Select your language to access regional channels!**\n"
            "**Выберите свой язык для доступа к региональным каналам!**\n\n"
            "Click the buttons below to add or remove language roles.\n"
            "Нажмите на кнопки ниже, чтобы добавить или удалить языковые роли."
        ),
        color=0x5865F2,  # Discord Blurple
        timestamp=discord.utils.utcnow()
    )
    
    # ❌ Превью картинки убрано по запросу
    
    embed.set_footer(text="Aeternis Core • MU Online")
    
    embed.add_field(
        name="📋 Available Languages",
        value=(
            "🌍 **General** — International channels\n"
            "🇪🇸 **Español** — Spanish channels\n"
            "🇵🇹 **Português** — Portuguese channels\n"
            "🇷🇺 **Русский** — Russian channels\n"
            "🇹🇷 **Türkçe** — Turkish channels\n"
            "🇻🇳 **Tiếng Việt** — Vietnamese channels\n"
            "🇵🇭 **Filipino** — Filipino channels"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚙️ How it works",
        value="Click a button to **add** the role.\nClick again to **remove** it.",
        inline=True
    )
    
    embed.add_field(
        name="🔒 Permissions",
        value="Roles grant access to language-specific channels.",
        inline=True
    )
    
    return embed

# ============================================================
# 🎯 СОБЫТИЯ БОТА
# ============================================================

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.do_not_disturb,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Aeternis MU Online"
        )
    )
    
    # 🔥 РЕГИСТРАЦИЯ ПЕРСИСТЕНТНОГО VIEW
    # Это заставляет Discord "вспомнить" кнопки после перезагрузки бота
    client.add_view(LanguageRoleView())
    
    print("✅ Aeternis Core успешно запущен!")
    print(f"👤 Бот: {client.user.name}")
    print(f"🆔 ID: {client.user.id}")
    print(f"🔴 Статус: Не беспокоить")
    print(f"👑 Владельцев: {len(OWNER_IDS)}")
    print(f"🛡️ Админ-ролей: {len(ADMIN_ROLE_IDS)}")
    print(f"🔘 Персистентные кнопки: Активны")
    print("-------------------------------")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Команда !roles
    if message.content.strip() == "!roles":
        if not isinstance(message.author, discord.Member):
            return
        
        embed = create_roles_embed()
        view = LanguageRoleView()
        
        await message.channel.send(embed=embed, view=view)
        
        try:
            await message.delete()
        except:
            pass


# ============================================================
# 🚀 ЗАПУСК
# ============================================================

if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except discord.LoginFailure:
        print("❌ ОШИБКА: Неверный токен Discord.")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
