#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeternis Core - Official Discord Bot
Project: Aeternis MU Online
Version: 3.0 (Logging System)
"""

import os
import discord
from dotenv import load_dotenv
from discord.ui import Button, View, Modal, TextInput
from datetime import datetime

# ============================================================
# КОНФИГУРАЦИЯ
# ============================================================

OWNER_IDS = [314805583788244993]

ADMIN_ROLE_IDS = [
    1487181204816920769, 1487360978181160980, 1487360985688969296,
    1487360986947129385, 1487360987131547688, 1487360987727138939,
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

TICKET_CATEGORY_ID = 1487369421440946236

# КАНАЛ ЛОГИРОВАНИЯ
LOG_CHANNEL_ID = 1487390220830900344

# ============================================================
# СИСТЕМА ЛОКАЛИЗАЦИИ
# ============================================================

TEXTS = {
    "en": {
        "welcome_title": "WELCOME TO AETERNIS",
        "welcome_desc": "The Eternal Battle Begins Here\n\nGreetings, Warrior!\n\nYou have entered the realm of Aeternis, where legends are forged and eternity awaits.",
        "quick_start": "QUICK START",
        "verify": "1. Verify - Read rules & verify",
        "language": "2. Language - Choose your language",
        "download": "3. Download - Get the client",
        "connect": "4. Connect - Join the battle",
        "links": "IMPORTANT LINKS",
        "website": "Website",
        "wiki": "Wiki/Guide",
        "donate": "Donate Shop",
        "server_info": "SERVER INFO",
        "footer": "Aeternis Core - MU Online",
        
        "roles_title": "Language Selection",
        "roles_desc": "Select your language to access regional channels.\n\nClick the buttons below to add or remove language roles.",
        "available_lang": "Available Languages",
        "how_it_works": "How it works",
        "how_it_works_val": "Click a button to add the role.\nClick again to remove it.",
        "permissions": "Permissions",
        "permissions_val": "Roles grant access to language-specific channels.",
        
        "tickets_title": "Support Center",
        "tickets_desc": "Need help? Create a ticket!\n\nOur staff will assist you with:\n- Bug Reports\n- Donation Issues\n- Account Problems\n- General Questions",
        "response_time": "Response Time",
        "response_time_val": "Usually within 24 hours",
        "languages": "Languages",
        "languages_val": "EN / RU / ES / PT / TR / VN / PH",
        "rules": "Rules",
        "rules_val": "Be respectful",
        
        "btn_create_ticket": "Create Ticket",
        "btn_close_ticket": "Close Ticket",
        "btn_confirm": "Confirm",
        "btn_cancel": "Cancel",
        "btn_general": "General",
        "btn_ru": "Russian",
        
        "ticket_welcome": "Support Ticket",
        "ticket_welcome_desc": "Welcome, {mention}!\n\nPlease describe your issue in detail.\n\nA staff member will assist you shortly.",
        "ticket_created": "Ticket created: {channel}",
        "ticket_exists": "You already have an open ticket! Please close it before creating a new one.",
        "ticket_closed": "Ticket closed.",
        "close_confirm": "Are you sure you want to close this ticket?",
        "close_cancelled": "Closing cancelled.",
        "no_permission": "Insufficient permissions!",
        "category_not_found": "Ticket category not found!",
        "error_creating": "Error creating ticket: {error}",
        
        "role_added": "Role **{role}** added!",
        "role_removed": "Role **{role}** removed!",
        "role_not_found": "Role not found!",
        
        "admin_panel_only": "Only administrators can create this panel!"
    },
    "ru": {
        "welcome_title": "ДОБРО ПОЖАЛОВАТЬ В AETERNIS",
        "welcome_desc": "Вечная Битва Начинается Здесь\n\nПриветствуем, Воин!\n\nВы вошли в мир Aeternis, где куются легенды и ждет вечность.",
        "quick_start": "БЫСТРЫЙ СТАРТ",
        "verify": "1. Верификация - Прочти правила",
        "language": "2. Язык - Выбери свой язык",
        "download": "3. Скачать - Загрузи клиент",
        "connect": "4. Подключение - Вступай в битву",
        "links": "ВАЖНЫЕ ССЫЛКИ",
        "website": "Сайт",
        "wiki": "Вики/Гайды",
        "donate": "Донат Шоп",
        "server_info": "ИНФОРМАЦИЯ СЕРВЕРА",
        "footer": "Aeternis Core - MU Online",
        
        "roles_title": "Выбор Языка",
        "roles_desc": "Выберите свой язык для доступа к региональным каналам.\n\nНажмите на кнопки ниже, чтобы добавить или удалить языковые роли.",
        "available_lang": "Доступные Языки",
        "how_it_works": "Как это работает",
        "how_it_works_val": "Нажмите чтобы добавить роль.\nНажмите снова чтобы удалить.",
        "permissions": "Права доступа",
        "permissions_val": "Роли дают доступ к языковым каналам.",
        
        "tickets_title": "Центр Поддержки",
        "tickets_desc": "Нужна помощь? Создайте тикет!\n\nНаши сотрудники помогут вам с:\n- Сообщения об ошибках\n- Проблемы с донатом\n- Проблемы аккаунта\n- Общие вопросы",
        "response_time": "Время ответа",
        "response_time_val": "Обычно в течение 24 часов",
        "languages": "Языки",
        "languages_val": "EN / RU / ES / PT / TR / VN / PH",
        "rules": "Правила",
        "rules_val": "Будьте уважительны",
        
        "btn_create_ticket": "Создать Тикет",
        "btn_close_ticket": "Закрыть Тикет",
        "btn_confirm": "Подтвердить",
        "btn_cancel": "Отмена",
        "btn_general": "General",
        "btn_ru": "Русский",
        
        "ticket_welcome": "Тикет Поддержки",
        "ticket_welcome_desc": "Добро пожаловать, {mention}!\n\nПожалуйста, подробно опишите вашу проблему.\n\nСотрудник скоро вам поможет.",
        "ticket_created": "Тикет создан: {channel}",
        "ticket_exists": "У вас уже есть открытый тикет! Закройте его перед созданием нового.",
        "ticket_closed": "Тикет закрыт.",
        "close_confirm": "Вы уверены, что хотите закрыть этот тикет?",
        "close_cancelled": "Закрытие отменено.",
        "no_permission": "Недостаточно прав!",
        "category_not_found": "Категория тикетов не найдена!",
        "error_creating": "Ошибка создания тикета: {error}",
        
        "role_added": "Роль **{role}** добавлена!",
        "role_removed": "Роль **{role}** удалена!",
        "role_not_found": "Роль не найдена!",
        
        "admin_panel_only": "Только администраторы могут создавать эту панель!"
    }
}

def get_user_lang(member):
    if not isinstance(member, discord.Member):
        return "en"
    if any(role.id == LANGUAGE_ROLES["ru"] for role in member.roles):
        return "ru"
    return "en"

def t(key, lang="en"):
    return TEXTS.get(lang, TEXTS["en"]).get(key, TEXTS["en"].get(key, key))

# ============================================================

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("ERROR: Token not found! Check .env file")
    exit()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.message_content = True
intents.guilds = True
intents.bans = True

client = discord.Client(intents=intents)

# ============================================================
# ФУНКЦИИ ЛОГИРОВАНИЯ
# ============================================================

async def send_log(title, description, color=0x5865F2):
    """Отправляет лог в канал логирования"""
    try:
        log_channel = client.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            return
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="Aeternis Core Log System")
        
        await log_channel.send(embed=embed)
    except Exception as e:
        print(f"Log error: {e}")

async def log_member_join(member):
    """Лог входа участника"""
    title = "Member Joined"
    desc = (
        f"**User:** {member.name}#{member.discriminator}\n"
        f"**ID:** {member.id}\n"
        f"**Account Created:** {member.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        f"**Mention:** {member.mention}"
    )
    await send_log(title, desc, color=0x00FF00)

async def log_member_leave(member):
    """Лог выхода участника"""
    title = "Member Left"
    desc = (
        f"**User:** {member.name}#{member.discriminator}\n"
        f"**ID:** {member.id}\n"
        f"**Joined Server:** {member.joined_at.strftime('%d.%m.%Y %H:%M') if member.joined_at else 'Unknown'}\n"
        f"**Roles:** {', '.join([r.name for r in member.roles[1:]]) if member.roles[1:] else 'None'}"
    )
    await send_log(title, desc, color=0xFF0000)

async def log_message_edit(before, after):
    """Лог редактирования сообщения"""
    if before.content == after.content:
        return
    
    title = "Message Edited"
    desc = (
        f"**Author:** {before.author.name}#{before.author.discriminator}\n"
        f"**Channel:** {before.channel.mention}\n"
        f"**Message ID:** {before.id}\n\n"
        f"**Before:**\n```{before.content[:1000]}```\n\n"
        f"**After:**\n```{after.content[:1000]}```"
    )
    await send_log(title, desc, color=0xFFA500)

async def log_message_delete(message):
    """Лог удаления сообщения"""
    title = "Message Deleted"
    desc = (
        f"**Author:** {message.author.name}#{message.author.discriminator}\n"
        f"**Channel:** {message.channel.mention}\n"
        f"**Message ID:** {message.id}\n"
        f"**Content:**\n```{message.content[:1000] if message.content else 'No content'}```"
    )
    await send_log(title, desc, color=0xFF0000)

async def log_role_create(role):
    """Лог создания роли"""
    title = "Role Created"
    desc = (
        f"**Role:** {role.name}\n"
        f"**ID:** {role.id}\n"
        f"**Color:** #{role.color.value:06X}\n"
        f"**Hoisted:** {role.hoist}\n"
        f"**Mentionable:** {role.mentionable}"
    )
    await send_log(title, desc, color=0x00FF00)

async def log_role_delete(role):
    """Лог удаления роли"""
    title = "Role Deleted"
    desc = (
        f"**Role:** {role.name}\n"
        f"**ID:** {role.id}\n"
        f"**Color:** #{role.color.value:06X}"
    )
    await send_log(title, desc, color=0xFF0000)

async def log_member_ban(guild, user):
    """Лог бана участника"""
    title = "Member Banned"
    desc = (
        f"**User:** {user.name}#{user.discriminator}\n"
        f"**ID:** {user.id}\n"
        f"**Guild:** {guild.name}"
    )
    await send_log(title, desc, color=0xFF0000)

async def log_member_unban(guild, user):
    """Лог разбана участника"""
    title = "Member Unbanned"
    desc = (
        f"**User:** {user.name}#{user.discriminator}\n"
        f"**ID:** {user.id}\n"
        f"**Guild:** {guild.name}"
    )
    await send_log(title, desc, color=0x00FF00)

async def log_channel_create(channel):
    """Лог создания канала"""
    title = "Channel Created"
    desc = (
        f"**Channel:** {channel.name}\n"
        f"**ID:** {channel.id}\n"
        f"**Type:** {channel.type}\n"
        f"**Category:** {channel.category.name if channel.category else 'None'}"
    )
    await send_log(title, desc, color=0x00FF00)

async def log_channel_delete(channel):
    """Лог удаления канала"""
    title = "Channel Deleted"
    desc = (
        f"**Channel:** {channel.name}\n"
        f"**ID:** {channel.id}\n"
        f"**Type:** {channel.type}"
    )
    await send_log(title, desc, color=0xFF0000)

async def log_member_update(before, after):
    """Лог изменения участника (роли, ник)"""
    changes = []
    
    if before.nick != after.nick:
        changes.append(f"**Nickname:** {before.nick} -> {after.nick}")
    
    if before.roles != after.roles:
        added = set(after.roles) - set(before.roles)
        removed = set(before.roles) - set(after.roles)
        if added:
            changes.append(f"**Roles Added:** {', '.join([r.name for r in added])}")
        if removed:
            changes.append(f"**Roles Removed:** {', '.join([r.name for r in removed])}")
    
    if not changes:
        return
    
    title = "Member Updated"
    desc = (
        f"**User:** {after.name}#{after.discriminator}\n"
        f"**ID:** {after.id}\n\n" + "\n".join(changes)
    )
    await send_log(title, desc, color=0xFFA500)

async def log_voice_state_update(member, before, after):
    """Лог голосовых действий"""
    if before.channel is None and after.channel is not None:
        title = "Voice Channel Join"
        desc = (
            f"**User:** {member.name}#{member.discriminator}\n"
            f"**Channel:** {after.channel.name}"
        )
        await send_log(title, desc, color=0x00FF00)
    elif before.channel is not None and after.channel is None:
        title = "Voice Channel Leave"
        desc = (
            f"**User:** {member.name}#{member.discriminator}\n"
            f"**Channel:** {before.channel.name}"
        )
        await send_log(title, desc, color=0xFF0000)
    elif before.channel != after.channel:
        title = "Voice Channel Move"
        desc = (
            f"**User:** {member.name}#{member.discriminator}\n"
            f"**From:** {before.channel.name}\n"
            f"**To:** {after.channel.name}"
        )
        await send_log(title, desc, color=0xFFA500)

async def log_command_usage(user, command, channel):
    """Лог использования команд"""
    title = "Command Used"
    desc = (
        f"**User:** {user.name}#{user.discriminator}\n"
        f"**ID:** {user.id}\n"
        f"**Command:** {command}\n"
        f"**Channel:** {channel.mention}"
    )
    await send_log(title, desc, color=0x5865F2)

async def log_ticket_create(user, channel):
    """Лог создания тикета"""
    title = "Ticket Created"
    desc = (
        f"**User:** {user.name}#{user.discriminator}\n"
        f"**ID:** {user.id}\n"
        f"**Ticket:** {channel.mention}\n"
        f"**Ticket ID:** {channel.id}"
    )
    await send_log(title, desc, color=0x00FF00)

async def log_ticket_close(user, channel_name):
    """Лог закрытия тикета"""
    title = "Ticket Closed"
    desc = (
        f"**Closed By:** {user.name}#{user.discriminator}\n"
        f"**Ticket:** #{channel_name}"
    )
    await send_log(title, desc, color=0xFF0000)

# ============================================================
# ПРОВЕРКА ПРАВ
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
# КЛАССЫ ДЛЯ ТИКЕТОВ
# ============================================================

class TicketCreateButton(Button):
    def __init__(self, lang="en"):
        super().__init__(label=t("btn_create_ticket", lang), style=discord.ButtonStyle.primary, custom_id="ticket_create")
        self.lang = lang
    
    async def callback(self, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user)
        guild = interaction.guild
        member = interaction.user
        
        for channel in guild.text_channels:
            if channel.name.startswith(f"ticket-{member.name}") and channel.category and channel.category.id == TICKET_CATEGORY_ID:
                await interaction.response.send_message(t("ticket_exists", lang), ephemeral=True)
                return
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        
        for role_id in ADMIN_ROLE_IDS:
            role = guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        for owner_id in OWNER_IDS:
            owner = guild.get_member(owner_id)
            if owner:
                overwrites[owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        try:
            category = guild.get_channel(TICKET_CATEGORY_ID)
            if not category:
                await interaction.response.send_message(t("category_not_found", lang), ephemeral=True)
                return
            
            channel = await guild.create_text_channel(
                name=f"ticket-{member.name}",
                category=category,
                overwrites=overwrites,
                topic=f"Ticket for {member.mention} | Created: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
            
            embed = discord.Embed(
                title=t("ticket_welcome", lang),
                description=t("ticket_welcome_desc", lang).format(mention=member.mention),
                color=0x5865F2,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text=f"Ticket ID: {channel.id} - {t('footer', lang)}")
            
            view = TicketControlView(lang=lang)
            await channel.send(embed=embed, view=view)
            await channel.send(f"{member.mention}")
            
            await interaction.response.send_message(t("ticket_created", lang).format(channel=channel.mention), ephemeral=True)
            
            # Логирование
            await log_ticket_create(member, channel)
            
        except Exception as e:
            await interaction.response.send_message(t("error_creating", lang).format(error=e), ephemeral=True)

class TicketCloseButton(Button):
    def __init__(self, lang="en"):
        super().__init__(label=t("btn_close_ticket", lang), style=discord.ButtonStyle.danger, custom_id="ticket_close")
        self.lang = lang
    
    async def callback(self, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user)
        if not has_permission(interaction.user, admin_only=False):
            await interaction.response.send_message(t("no_permission", lang), ephemeral=True)
            return
        
        confirm_view = ConfirmCloseView(lang=lang)
        await interaction.response.send_message(t("close_confirm", lang), view=confirm_view, ephemeral=True)

class ConfirmCloseButton(Button):
    def __init__(self, confirm=True, lang="en"):
        style = discord.ButtonStyle.success if confirm else discord.ButtonStyle.secondary
        label = t("btn_confirm", lang) if confirm else t("btn_cancel", lang)
        super().__init__(label=label, style=style, custom_id=f"ticket_close_{'yes' if confirm else 'no'}")
        self.confirm = confirm
        self.lang = lang
    
    async def callback(self, interaction: discord.Interaction):
        if self.confirm:
            channel_name = interaction.channel.name
            await log_ticket_close(interaction.user, channel_name)
            await interaction.channel.delete()
        else:
            await interaction.response.edit_message(content=t("close_cancelled", self.lang), view=None)

class ConfirmCloseView(View):
    def __init__(self, lang="en"):
        super().__init__(timeout=30)
        self.add_item(ConfirmCloseButton(confirm=True, lang=lang))
        self.add_item(ConfirmCloseButton(confirm=False, lang=lang))

class TicketControlView(View):
    def __init__(self, lang="en"):
        super().__init__(timeout=None)
        self.add_item(TicketCloseButton(lang=lang))

class TicketPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketCreateButton())

# ============================================================
# КЛАССЫ ДЛЯ ЯЗЫКОВЫХ РОЛЕЙ
# ============================================================

class LangButton(Button):
    def __init__(self, label, emoji, role_id, style=discord.ButtonStyle.secondary, lang="en"):
        if label == "General":
            label = t("btn_general", lang)
        elif label == "Русский":
            label = t("btn_ru", lang)
            
        super().__init__(label=label, emoji=emoji, style=style, custom_id=f"lang_{role_id}")
        self.role_id = role_id
        self.lang = lang
    
    async def callback(self, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user)
        member = interaction.user
        guild = interaction.guild
        role = guild.get_role(self.role_id)
        
        if not role:
            await interaction.response.send_message(t("role_not_found", lang), ephemeral=True)
            return
        
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(t("role_removed", lang).format(role=role.name), ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(t("role_added", lang).format(role=role.name), ephemeral=True)

class LangView(View):
    def __init__(self, lang="en"):
        super().__init__(timeout=None)
        self.add_item(LangButton(label="General", emoji="🌍", role_id=LANGUAGE_ROLES["general"], style=discord.ButtonStyle.primary, lang=lang))
        self.add_item(LangButton(label="Español", emoji="🇪🇸", role_id=LANGUAGE_ROLES["es"], lang=lang))
        self.add_item(LangButton(label="Português", emoji="🇵🇹", role_id=LANGUAGE_ROLES["pt"], lang=lang))
        self.add_item(LangButton(label="Русский", emoji="🇷🇺", role_id=LANGUAGE_ROLES["ru"], lang=lang))
        self.add_item(LangButton(label="Türkçe", emoji="🇹🇷", role_id=LANGUAGE_ROLES["tr"], lang=lang))
        self.add_item(LangButton(label="Tiếng Việt", emoji="🇻🇳", role_id=LANGUAGE_ROLES["vn"], lang=lang))
        self.add_item(LangButton(label="Filipino", emoji="🇵🇭", role_id=LANGUAGE_ROLES["ph"], lang=lang))

# ============================================================
# СОЗДАНИЕ EMBED
# ============================================================

def create_welcome_embed(lang="en"):
    embed = discord.Embed(
        title=t("welcome_title", lang),
        description=t("welcome_desc", lang),
        color=0xFFD700,
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text=t("footer", lang))
    
    embed.add_field(name=t("quick_start", lang), value=f"{t('verify', lang)}\n{t('language', lang)}\n{t('download', lang)}\n{t('connect', lang)}", inline=False)
    embed.add_field(name=t("links", lang), value=f"{t('website', lang)}\n{t('wiki', lang)}\n{t('donate', lang)}", inline=True)
    embed.add_field(name=t("server_info", lang), value="EXP: [X]x\nDrop: [X]x\nMax Lvl: [X]", inline=True)
    return embed

def create_roles_embed(lang="en"):
    embed = discord.Embed(
        title=t("roles_title", lang),
        description=t("roles_desc", lang),
        color=0x5865F2,
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text=t("footer", lang))
    
    embed.add_field(
        name=t("available_lang", lang),
        value=(
            "General - International\n"
            "Español - Spanish\n"
            "Português - Portuguese\n"
            "Русский - Russian\n"
            "Türkçe - Turkish\n"
            "Tiếng Việt - Vietnamese\n"
            "Filipino - Filipino"
        ),
        inline=False
    )
    embed.add_field(name=t("how_it_works", lang), value=t("how_it_works_val", lang), inline=True)
    embed.add_field(name=t("permissions", lang), value=t("permissions_val", lang), inline=True)
    return embed

def create_tickets_embed(lang="en"):
    embed = discord.Embed(
        title=t("tickets_title", lang),
        description=t("tickets_desc", lang),
        color=0x5865F2,
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text=t("footer", lang))
    
    embed.add_field(name=t("response_time", lang), value=t("response_time_val", lang), inline=True)
    embed.add_field(name=t("languages", lang), value=t("languages_val", lang), inline=True)
    embed.add_field(name=t("rules", lang), value=t("rules_val", lang), inline=True)
    return embed

# ============================================================
# СОБЫТИЯ БОТА
# ============================================================

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.do_not_disturb,
        activity=discord.Activity(type=discord.ActivityType.watching, name="Aeternis MU Online")
    )
    
    client.add_view(TicketPanelView())
    client.add_view(LangView())
    
    print("Aeternis Core v3.0 (Logging System) started")
    print(f"Bot: {client.user.name}")
    print(f"ID: {client.user.id}")
    print(f"Log Channel: {LOG_CHANNEL_ID}")
    print("-------------------------------")

@client.event
async def on_member_join(member):
    await log_member_join(member)

@client.event
async def on_member_remove(member):
    await log_member_leave(member)

@client.event
async def on_message_edit(before, after):
    await log_message_edit(before, after)

@client.event
async def on_message_delete(message):
    await log_message_delete(message)

@client.event
async def on_guild_role_create(role):
    await log_role_create(role)

@client.event
async def on_guild_role_delete(role):
    await log_role_delete(role)

@client.event
async def on_member_ban(guild, user):
    await log_member_ban(guild, user)

@client.event
async def on_member_unban(guild, user):
    await log_member_unban(guild, user)

@client.event
async def on_guild_channel_create(channel):
    await log_channel_create(channel)

@client.event
async def on_guild_channel_delete(channel):
    await log_channel_delete(channel)

@client.event
async def on_member_update(before, after):
    await log_member_update(before, after)

@client.event
async def on_voice_state_update(member, before, after):
    await log_voice_state_update(member, before, after)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    lang = get_user_lang(message.author)
    
    # Логирование команд
    if message.content.startswith("!"):
        await log_command_usage(message.author, message.content.split()[0], message.channel)
    
    if message.content.strip() == "!welcome":
        embed = create_welcome_embed(lang)
        await message.channel.send(embed=embed)
        try:
            await message.delete()
        except:
            pass
    
    if message.content.strip() == "!roles":
        embed = create_roles_embed(lang)
        view = LangView(lang=lang)
        await message.channel.send(embed=embed, view=view)
        try:
            await message.delete()
        except:
            pass
    
    if message.content.strip() == "!tickets":
        if not has_permission(message.author, admin_only=False):
            await message.reply(t("admin_panel_only", lang), ephemeral=True)
            return
        
        embed = create_tickets_embed(lang)
        view = TicketPanelView()
        await message.channel.send(embed=embed, view=view)
        try:
            await message.delete()
        except:
            pass
    
    if message.content.strip() == "!close":
        if not has_permission(message.author, admin_only=False):
            await message.reply(t("no_permission", lang), ephemeral=True)
            return
        
        if message.channel.category and message.channel.category.id == TICKET_CATEGORY_ID:
            confirm_view = ConfirmCloseView(lang=lang)
            await message.channel.send(t("close_confirm", lang), view=confirm_view)
            try:
                await message.delete()
            except:
                pass

# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except discord.LoginFailure:
        print("ERROR: Invalid Discord token.")
    except Exception as e:
        print(f"Critical error: {e}")
