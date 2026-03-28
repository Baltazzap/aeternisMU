#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeternis Core - Official Discord Bot
Project: Aeternis MU Online
Version: 3.0 (Full System)
"""

import os
import discord
from dotenv import load_dotenv
from discord.ui import Button, View
from datetime import datetime, timedelta
import asyncio
import random

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
LOG_CHANNEL_ID = 1487390220830900344
GIVEAWAY_BANNER = "https://i.imgur.com/Nce6GzV.jpeg"

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
        "admin_panel_only": "Only administrators can create this panel!",
        
        "log_member_join": "Member Joined",
        "log_member_leave": "Member Left",
        "log_ticket_create": "Ticket Created",
        "log_ticket_close": "Ticket Closed",
        
        "btn_enter_giveaway": "Enter Giveaway",
        "btn_leave_giveaway": "Leave Giveaway",
        "giveaway_title": "Giveaway",
        "giveaway_prize": "Prize",
        "giveaway_end": "Ends",
        "giveaway_hosts": "Hosted by",
        "giveaway_participants": "Participants",
        "giveaway_entered": "You have entered the giveaway!",
        "giveaway_left": "You have left the giveaway!",
        "giveaway_already_entered": "You have already entered this giveaway!",
        "giveaway_not_entered": "You have not entered this giveaway!",
        "giveaway_ended": "Giveaway Ended",
        "giveaway_winner": "Winner",
        "giveaway_no_participants": "No participants in this giveaway!",
        "giveaway_created": "Giveaway created in {channel}!",
        "giveaway_ended_log": "Giveaway ended",
        "giveaway_created_log": "Giveaway created",
        "giveaway_winner_log": "Giveaway winner selected",
        "gw_command_usage": "Usage: !giveaway <duration> <winners> <prize>\nExample: !giveaway 1h 2 1000 Zen",
        "gw_invalid_duration": "Invalid duration! Use: 1h, 24h, 7d, etc.",
        "gw_invalid_winners": "Invalid number of winners! Use a number between 1 and 10.",
        "gw_no_prize": "Please specify a prize!"
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
        "admin_panel_only": "Только администраторы могут создавать эту панель!",
        
        "log_member_join": "Пользователь вошел",
        "log_member_leave": "Пользователь вышел",
        "log_ticket_create": "Тикет создан",
        "log_ticket_close": "Тикет закрыт",
        
        "btn_enter_giveaway": "Участвовать",
        "btn_leave_giveaway": "Отменить участие",
        "giveaway_title": "Розыгрыш",
        "giveaway_prize": "Приз",
        "giveaway_end": "Завершение",
        "giveaway_hosts": "Организатор",
        "giveaway_participants": "Участников",
        "giveaway_entered": "Вы участвуете в розыгрыше!",
        "giveaway_left": "Вы отменили участие в розыгрыше!",
        "giveaway_already_entered": "Вы уже участвуете в этом розыгрыше!",
        "giveaway_not_entered": "Вы не участвуете в этом розыгрыше!",
        "giveaway_ended": "Розыгрыш завершен",
        "giveaway_winner": "Победитель",
        "giveaway_no_participants": "Нет участников в этом розыгрыше!",
        "giveaway_created": "Розыгрыш создан в {channel}!",
        "giveaway_ended_log": "Розыгрыш завершен",
        "giveaway_created_log": "Розыгрыш создан",
        "giveaway_winner_log": "Победитель розыгрыша выбран",
        "gw_command_usage": "Использование: !giveaway <время> <победители> <приз>\nПример: !giveaway 1h 2 1000 Zen",
        "gw_invalid_duration": "Неверное время! Используйте: 1h, 24h, 7d и т.д.",
        "gw_invalid_winners": "Неверное число победителей! Используйте число от 1 до 10.",
        "gw_no_prize": "Укажите приз!"
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
intents.guilds = True

client = discord.Client(intents=intents)
active_giveaways = {}

# ============================================================
# ФУНКЦИИ ЛОГИРОВАНИЯ
# ============================================================

async def send_log(title, description, color=0x5865F2):
    try:
        log_channel = client.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            return
        embed = discord.Embed(title=title, description=description, color=color, timestamp=datetime.utcnow())
        embed.set_footer(text="Aeternis Core Log System")
        await log_channel.send(embed=embed)
    except Exception as e:
        print(f"Log error: {e}")

async def log_giveaway_action(action, details, color=0x5865F2):
    await send_log(action, details, color=color)

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
# КЛАССЫ ДЛЯ РОЗЫГРЫШЕЙ
# ============================================================

class GiveawayEnterButton(Button):
    def __init__(self, lang="en"):
        super().__init__(label=t("btn_enter_giveaway", lang), style=discord.ButtonStyle.success, custom_id="giveaway_enter")
        self.lang = lang
    
    async def callback(self, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user)
        message_id = interaction.message.id
        if message_id not in active_giveaways:
            await interaction.response.send_message("This giveaway is no longer active!", ephemeral=True)
            return
        giveaway = active_giveaways[message_id]
        if interaction.user.id in giveaway["participants"]:
            await interaction.response.send_message(t("giveaway_already_entered", lang), ephemeral=True)
            return
        giveaway["participants"].append(interaction.user.id)
        embed = interaction.message.embeds[0]
        embed.set_field_at(2, name=t("giveaway_participants", lang), value=str(len(giveaway["participants"])), inline=True)
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message(t("giveaway_entered", lang), ephemeral=True)

class GiveawayLeaveButton(Button):
    def __init__(self, lang="en"):
        super().__init__(label=t("btn_leave_giveaway", lang), style=discord.ButtonStyle.danger, custom_id="giveaway_leave")
        self.lang = lang
    
    async def callback(self, interaction: discord.Interaction):
        lang = get_user_lang(interaction.user)
        message_id = interaction.message.id
        if message_id not in active_giveaways:
            await interaction.response.send_message("This giveaway is no longer active!", ephemeral=True)
            return
        giveaway = active_giveaways[message_id]
        if interaction.user.id not in giveaway["participants"]:
            await interaction.response.send_message(t("giveaway_not_entered", lang), ephemeral=True)
            return
        giveaway["participants"].remove(interaction.user.id)
        embed = interaction.message.embeds[0]
        embed.set_field_at(2, name=t("giveaway_participants", lang), value=str(len(giveaway["participants"])), inline=True)
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message(t("giveaway_left", lang), ephemeral=True)

class GiveawayView(View):
    def __init__(self, lang="en"):
        super().__init__(timeout=None)
        self.add_item(GiveawayEnterButton(lang=lang))
        self.add_item(GiveawayLeaveButton(lang=lang))

# ============================================================
# ФУНКЦИИ РОЗЫГРЫШЕЙ
# ============================================================

def parse_duration(duration_str):
    try:
        if duration_str.endswith('h'):
            hours = int(duration_str[:-1])
            return datetime.utcnow() + timedelta(hours=hours)
        elif duration_str.endswith('d'):
            days = int(duration_str[:-1])
            return datetime.utcnow() + timedelta(days=days)
        elif duration_str.endswith('m'):
            minutes = int(duration_str[:-1])
            return datetime.utcnow() + timedelta(minutes=minutes)
        else:
            return None
    except:
        return None

def create_giveaway_embed(prize, end_time, winners, host, lang="en"):
    embed = discord.Embed(
        title=t("giveaway_title", lang),
        description=f"**{t('giveaway_prize', lang)}:** {prize}",
        color=0xFFD700,
        timestamp=datetime.utcnow()
    )
    embed.set_image(url=GIVEAWAY_BANNER)
    embed.add_field(name=t("giveaway_end", lang), value=f"<t:{int(end_time.timestamp())}:R>", inline=True)
    embed.add_field(name=t("giveaway_hosts", lang), value=host.mention, inline=True)
    embed.add_field(name=t("giveaway_participants", lang), value="0", inline=True)
    embed.set_footer(text=f"{t('footer', lang)} - {winners} winner(s)")
    return embed

async def end_giveaway(message_id):
    if message_id not in active_giveaways:
        return
    giveaway = active_giveaways[message_id]
    channel = giveaway["channel"]
    prize = giveaway["prize"]
    winners_count = giveaway["winners"]
    participants = giveaway["participants"]
    lang = giveaway["lang"]
    del active_giveaways[message_id]
    
    if len(participants) == 0:
        embed = discord.Embed(
            title=t("giveaway_ended", lang),
            description=f"**{t('giveaway_prize', lang)}:** {prize}\n\n{t('giveaway_no_participants', lang)}",
            color=0xFF0000,
            timestamp=datetime.utcnow()
        )
        embed.set_image(url=GIVEAWAY_BANNER)
        embed.set_footer(text=t("footer", lang))
        try:
            msg = await channel.fetch_message(message_id)
            await msg.edit(embed=embed, view=None)
        except:
            pass
        await log_giveaway_action(t("giveaway_ended_log", lang), f"Prize: {prize}\nResult: No participants", color=0xFF0000)
        return
    
    selected_winners = random.sample(participants, min(winners_count, len(participants)))
    winners_mention = ", ".join([f"<@{winner_id}>" for winner_id in selected_winners])
    
    embed = discord.Embed(
        title=t("giveaway_ended", lang),
        description=f"**{t('giveaway_prize', lang)}:** {prize}\n\n**{t('giveaway_winner', lang)}:**\n{winners_mention}",
        color=0x00FF00,
        timestamp=datetime.utcnow()
    )
    embed.set_image(url=GIVEAWAY_BANNER)
    embed.set_footer(text=f"{t('footer', lang)} - {len(selected_winners)} winner(s)")
    
    try:
        msg = await channel.fetch_message(message_id)
        await msg.edit(embed=embed, view=None)
        await channel.send(f"Congratulations to the winner(s): {winners_mention}!")
    except Exception as e:
        print(f"Error ending giveaway: {e}")
    
    await log_giveaway_action(
        t("giveaway_winner_log", lang),
        f"Prize: {prize}\nWinners: {winners_mention}\nTotal participants: {len(participants)}",
        color=0x00FF00
    )

async def scheduled_end_giveaway(message_id, end_time):
    wait_time = (end_time - datetime.utcnow()).total_seconds()
    if wait_time > 0:
        await asyncio.sleep(wait_time)
    await end_giveaway(message_id)

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
            await send_log(t("log_ticket_create", lang), f"User: {member.name}\nChannel: #{channel.name}", color=0x00FF00)
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
            await send_log(t("log_ticket_close", "en"), f"Closed by: {interaction.user.name}\nChannel: #{channel_name}", color=0xFF0000)
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
    embed = discord.Embed(title=t("welcome_title", lang), description=t("welcome_desc", lang), color=0xFFD700, timestamp=discord.utils.utcnow())
    embed.set_footer(text=t("footer", lang))
    embed.add_field(name=t("quick_start", lang), value=f"{t('verify', lang)}\n{t('language', lang)}\n{t('download', lang)}\n{t('connect', lang)}", inline=False)
    embed.add_field(name=t("links", lang), value=f"{t('website', lang)}\n{t('wiki', lang)}\n{t('donate', lang)}", inline=True)
    embed.add_field(name=t("server_info", lang), value="EXP: [X]x\nDrop: [X]x\nMax Lvl: [X]", inline=True)
    return embed

def create_roles_embed(lang="en"):
    embed = discord.Embed(title=t("roles_title", lang), description=t("roles_desc", lang), color=0x5865F2, timestamp=discord.utils.utcnow())
    embed.set_footer(text=t("footer", lang))
    embed.add_field(name=t("available_lang", lang), value="General - International\nEspañol - Spanish\nPortuguês - Portuguese\nРусский - Russian\nTürkçe - Turkish\nTiếng Việt - Vietnamese\nFilipino - Filipino", inline=False)
    embed.add_field(name=t("how_it_works", lang), value=t("how_it_works_val", lang), inline=True)
    embed.add_field(name=t("permissions", lang), value=t("permissions_val", lang), inline=True)
    return embed

def create_tickets_embed(lang="en"):
    embed = discord.Embed(title=t("tickets_title", lang), description=t("tickets_desc", lang), color=0x5865F2, timestamp=discord.utils.utcnow())
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
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name="Aeternis MU Online"))
    client.add_view(TicketPanelView())
    client.add_view(LangView())
    client.add_view(GiveawayView())
    print("Aeternis Core v3.0 (Full System) started")
    print(f"Bot: {client.user.name}")
    print(f"ID: {client.user.id}")
    print(f"Languages: EN / RU")
    print(f"Log Channel: {LOG_CHANNEL_ID}")
    print("-------------------------------")

@client.event
async def on_member_join(member):
    await send_log(t("log_member_join", "en"), f"User: {member.name}#{member.discriminator}\nID: {member.id}", color=0x00FF00)

@client.event
async def on_member_remove(member):
    await send_log(t("log_member_leave", "en"), f"User: {member.name}#{member.discriminator}\nID: {member.id}", color=0xFF0000)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    lang = get_user_lang(message.author)
    
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
    
    if message.content.startswith("!giveaway"):
        if not has_permission(message.author, admin_only=True):
            await message.reply(t("no_permission", lang), ephemeral=True)
            return
        args = message.content.split()
        if len(args) < 4:
            await message.reply(t("gw_command_usage", lang), ephemeral=True)
            return
        duration_str = args[1]
        try:
            winners_count = int(args[2])
            if winners_count < 1 or winners_count > 10:
                await message.reply(t("gw_invalid_winners", lang), ephemeral=True)
                return
        except:
            await message.reply(t("gw_invalid_winners", lang), ephemeral=True)
            return
        prize = " ".join(args[3:])
        if not prize:
            await message.reply(t("gw_no_prize", lang), ephemeral=True)
            return
        end_time = parse_duration(duration_str)
        if not end_time:
            await message.reply(t("gw_invalid_duration", lang), ephemeral=True)
            return
        embed = create_giveaway_embed(prize, end_time, winners_count, message.author, lang)
        view = GiveawayView(lang=lang)
        giveaway_msg = await message.channel.send(embed=embed, view=view)
        active_giveaways[giveaway_msg.id] = {
            "prize": prize,
            "end_time": end_time,
            "winners": winners_count,
            "host": message.author.id,
            "participants": [],
            "channel": message.channel,
            "lang": lang
        }
        await log_giveaway_action(
            t("giveaway_created_log", lang),
            f"Prize: {prize}\nDuration: {duration_str}\nWinners: {winners_count}\nChannel: #{message.channel.name}",
            color=0x00FF00
        )
        await message.delete()
        asyncio.create_task(scheduled_end_giveaway(giveaway_msg.id, end_time))

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
