#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeternis Core - Official Discord Bot
Project: Aeternis MU Online
"""

import os
import discord
from dotenv import load_dotenv
from discord.ui import Button, View, Modal, TextInput
from datetime import datetime

# ============================================================
# ⚙️ КОНФИГУРАЦИЯ
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

LANGUAGE_ROLES = {
    "general": 1487363000322232390,
    "es": 1487363000980476095,
    "pt": 1487363006374350908,
    "ru": 1487363006869405696,
    "tr": 1487363006894706791,
    "vn": 1487371357573480540,
    "ph": 1487371358085316698,
}

# 🎫 КАТЕГОРИЯ ТИКЕТОВ
TICKET_CATEGORY_ID = 1487369421440946236

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
# 🎫 КЛАССЫ ДЛЯ ТИКЕТОВ
# ============================================================

class TicketCreateButton(Button):
    """Кнопка создания тикета"""
    
    def __init__(self):
        super().__init__(label="🎫 Create Ticket", style=discord.ButtonStyle.primary, custom_id="ticket_create")
    
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        
        # Проверка: есть ли уже открытый тикет у пользователя
        for channel in guild.text_channels:
            if channel.name.startswith(f"ticket-{member.name}") and channel.category.id == TICKET_CATEGORY_ID:
                await interaction.response.send_message(
                    "❌ У вас уже есть открытый тикет! Пожалуйста, закройте его перед созданием нового.",
                    ephemeral=True
                )
                return
        
        # Создание канала
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        
        # Добавляем права для админов
        for role_id in ADMIN_ROLE_IDS:
            role = guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        # Добавляем права для владельца
        for owner_id in OWNER_IDS:
            owner = guild.get_member(owner_id)
            if owner:
                overwrites[owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        try:
            category = guild.get_channel(TICKET_CATEGORY_ID)
            if not category:
                await interaction.response.send_message("❌ Категория тикетов не найдена!", ephemeral=True)
                return
            
            channel = await guild.create_text_channel(
                name=f"ticket-{member.name}",
                category=category,
                overwrites=overwrites,
                topic=f"Тикет для {member.mention} | Создан: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
            
            # Отправляем приветственное сообщение в тикет
            embed = discord.Embed(
                title="🎫 Support Ticket",
                description=(
                    f"**Welcome, {member.mention}!**\n"
                    "Добро пожаловать в службу поддержки!\n\n"
                    "Please describe your issue in detail.\n"
                    "Опишите вашу проблему подробно.\n\n"
                    "A staff member will assist you shortly.\n"
                    "Сотрудник скоро вам поможет."
                ),
                color=0x5865F2,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=f"Ticket ID: {channel.id} • Aeternis Core")
            
            view = TicketControlView()
            await channel.send(embed=embed, view=view)
            await channel.send(f"👋 {member.mention}, welcome to your ticket!")
            
            await interaction.response.send_message(
                f"✅ Тикет создан: {channel.mention}",
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Ошибка создания тикета: {e}", ephemeral=True)


class TicketCloseButton(Button):
    """Кнопка закрытия тикета"""
    
    def __init__(self):
        super().__init__(label="🔒 Close Ticket", style=discord.ButtonStyle.danger, custom_id="ticket_close")
    
    async def callback(self, interaction: discord.Interaction):
        if not has_permission(interaction.user, admin_only=False):
            await interaction.response.send_message("❌ Недостаточно прав!", ephemeral=True)
            return
        
        confirm_view = ConfirmCloseView()
        await interaction.response.send_message(
            "⚠️ Вы уверены, что хотите закрыть этот тикет?",
            view=confirm_view,
            ephemeral=True
        )


class ConfirmCloseButton(Button):
    """Кнопка подтверждения закрытия"""
    
    def __init__(self, confirm=True):
        style = discord.ButtonStyle.success if confirm else discord.ButtonStyle.secondary
        label = "✅ Confirm" if confirm else "❌ Cancel"
        super().__init__(label=label, style=style, custom_id=f"ticket_close_{'yes' if confirm else 'no'}")
    
    async def callback(self, interaction: discord.Interaction):
        if self.custom_id == "ticket_close_yes":
            await interaction.channel.delete()
        else:
            await interaction.response.edit_message(content="❌ Закрытие отменено.", view=None)


class ConfirmCloseView(View):
    """View для подтверждения закрытия"""
    
    def __init__(self):
        super().__init__(timeout=30)
        self.add_item(ConfirmCloseButton(confirm=True))
        self.add_item(ConfirmCloseButton(confirm=False))


class TicketControlView(View):
    """View управления тикетом"""
    
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketCloseButton())


class TicketPanelView(View):
    """View для панели тикетов"""
    
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketCreateButton())


# ============================================================
# 📜 EMBED ДЛЯ ПАНЕЛИ ТИКЕТОВ
# ============================================================

def create_ticket_embed():
    """Создаёт Embed для панели тикетов"""
    
    embed = discord.Embed(
        title="🎫 Support Center | Центр Поддержки",
        description=(
            "**Need help? Create a ticket!**\n"
            "Нужна помощь? Создайте тикет!\n\n"
            "Our staff will assist you with:\n"
            "Наши сотрудники помогут вам с:\n"
            "• 🐛 Bug Reports\n"
            "• 💰 Donation Issues\n"
            "• 📋 Account Problems\n"
            "• ❓ General Questions"
        ),
        color=0x5865F2,
        timestamp=discord.utils.utcnow()
    )
    
    embed.set_footer(text="Aeternis Core • MU Online")
    
    embed.add_field(
        name="⏱️ Response Time",
        value="Usually within 24 hours\nОбычно в течение 24 часов",
        inline=True
    )
    
    embed.add_field(
        name="🌍 Languages",
        value="EN / ES / PT / RU / TR / VN / PH",
        inline=True
    )
    
    embed.add_field(
        name="📋 Rules",
        value="Be respectful | Будьте уважительны",
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
    
    # Регистрация персистентных View
    client.add_view(TicketPanelView())
    client.add_view(TicketControlView())
    
    print("✅ Aeternis Core успешно запущен!")
    print(f"👤 Бот: {client.user.name}")
    print(f"🆔 ID: {client.user.id}")
    print(f"🔴 Статус: Не беспокоить")
    print(f"👑 Владельцев: {len(OWNER_IDS)}")
    print(f"🛡️ Админ-ролей: {len(ADMIN_ROLE_IDS)}")
    print(f"🎫 Категория тикетов: {TICKET_CATEGORY_ID}")
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
        
        from discord.ui import Button, View
        
        class LangButton(Button):
            def __init__(self, label, emoji, role_id, style=discord.ButtonStyle.secondary):
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
                    await interaction.response.send_message(f"❌ Роль **{role.name}** удалена.", ephemeral=True)
                else:
                    await member.add_roles(role)
                    await interaction.response.send_message(f"✅ Роль **{role.name}** добавлена!", ephemeral=True)
        
        class LangView(View):
            def __init__(self):
                super().__init__(timeout=None)
                self.add_item(LangButton(label="General", emoji="🌍", role_id=LANGUAGE_ROLES["general"], style=discord.ButtonStyle.primary))
                self.add_item(LangButton(label="Español", emoji="🇪🇸", role_id=LANGUAGE_ROLES["es"]))
                self.add_item(LangButton(label="Português", emoji="🇵🇹", role_id=LANGUAGE_ROLES["pt"]))
                self.add_item(LangButton(label="Русский", emoji="🇷🇺", role_id=LANGUAGE_ROLES["ru"]))
                self.add_item(LangButton(label="Türkçe", emoji="🇹🇷", role_id=LANGUAGE_ROLES["tr"]))
                self.add_item(LangButton(label="Tiếng Việt", emoji="🇻🇳", role_id=LANGUAGE_ROLES["vn"]))
                self.add_item(LangButton(label="Filipino", emoji="🇵🇭", role_id=LANGUAGE_ROLES["ph"]))
        
        embed = discord.Embed(
            title="🌍 Language Selection | Выбор Языка",
            description=(
                "**Select your language to access regional channels!**\n"
                "**Выберите свой язык для доступа к региональным каналам!**\n\n"
                "Click the buttons below to add or remove language roles."
            ),
            color=0x5865F2,
            timestamp=discord.utils.utcnow()
        )
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
        
        await message.channel.send(embed=embed, view=LangView())
        try:
            await message.delete()
        except:
            pass
    
    # Команда !tickets
    if message.content.strip() == "!tickets":
        if not isinstance(message.author, discord.Member):
            return
        
        # Проверка прав (только админы и владелец могут создавать панель)
        if not has_permission(message.author, admin_only=False):
            await message.reply("🚫 Только администраторы могут создавать панель тикетов!", ephemeral=True)
            return
        
        embed = create_ticket_embed()
        view = TicketPanelView()
        
        await message.channel.send(embed=embed, view=view)
        
        try:
            await message.delete()
        except:
            pass
    
    # Команда !close (альтернатива кнопке)
    if message.content.strip() == "!close":
        if not isinstance(message.author, discord.Member):
            return
        
        if not has_permission(message.author, admin_only=False):
            await message.reply("🚫 Недостаточно прав!", ephemeral=True)
            return
        
        if message.channel.category and message.channel.category.id == TICKET_CATEGORY_ID:
            confirm_view = ConfirmCloseView()
            await message.channel.send(
                "⚠️ Вы уверены, что хотите закрыть этот тикет?",
                view=confirm_view
            )
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
