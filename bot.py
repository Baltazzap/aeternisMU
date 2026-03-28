#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeternis Core - Official Discord Bot
Project: Aeternis MU Online
Version: 5.0 (English Only)
"""

import os
import discord
import re
from dotenv import load_dotenv
from discord.ui import Button, View
from discord import app_commands
from datetime import datetime, timedelta
from collections import defaultdict, deque
import asyncio
import random

# ============================================================
# CONFIGURATION
# ============================================================

OWNER_IDS = [314805583788244993]

ADMIN_ROLE_IDS = [
    1487181204816920769, 1487360978181160980, 1487360985688969296,
    1487360986947129385, 1487360987131547688, 1487360987727138939,
]

TICKET_CATEGORY_ID = 1487369421440946236
LOG_CHANNEL_ID = 1487390220830900344
MUTE_ROLE_ID = 1487360998946898002
WELCOME_CHANNEL_ID = 1487367796009472070
RULES_CHANNEL_ID = 1487367826275831838
GIVEAWAY_THUMBNAIL = "https://i.imgur.com/7K8oSFK.png"

# ⚙️ AUTOMOD SETTINGS
AUTOMOD_CONFIG = {
    "flood_limit": 5,
    "flood_time": 5,
    "duplicate_check": True,
    "anti_invite": True,
    "warn_dm": True
}

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
tree = app_commands.CommandTree(client)
active_giveaways = {}

# ============================================================
# 🛡️ AUTOMOD SYSTEM
# ============================================================

user_message_times = defaultdict(lambda: deque(maxlen=10))
user_last_message = {}

DISCORD_INVITE_REGEX = re.compile(r'(https?:\/\/)?(www\.)?(discord\.gg|discord\.com\/invite|discordapp\.com\/invite)\/[a-zA-Z0-9-]+', re.IGNORECASE)

async def apply_mute(member, reason):
    try:
        mute_role = member.guild.get_role(MUTE_ROLE_ID)
        if mute_role and mute_role not in member.roles:
            await member.add_roles(mute_role)
            if AUTOMOD_CONFIG["warn_dm"]:
                try:
                    await member.send(f"🔇 You have been muted for violating server rules.\n\n**Reason:** {reason}")
                except discord.Forbidden:
                    pass
            await send_log(
                "AutoMod Action",
                f"**User:** {member.mention} (ID: {member.id})\n**Action:** Muted\n**Reason:** {reason}",
                color=0xFF0000
            )
            return True
    except Exception as e:
        print(f"Mute error: {e}")
    return False

async def check_automod(message):
    if message.author.bot or has_permission(message.author, admin_only=True):
        return
    now = datetime.utcnow()
    user_id = message.author.id
    
    if AUTOMOD_CONFIG["anti_invite"] and DISCORD_INVITE_REGEX.search(message.content):
        try:
            await message.delete()
        except:
            pass
        await apply_mute(message.author, "Posted Discord invite link")
        warn_msg = await message.channel.send(f"{message.author.mention} ⚠️ Posting Discord invite links is not allowed.")
        asyncio.create_task(auto_delete_warn(warn_msg))
        return True
    
    if AUTOMOD_CONFIG["flood_limit"] > 0:
        times = user_message_times[user_id]
        times.append(now)
        if len(times) >= AUTOMOD_CONFIG["flood_limit"]:
            time_diff = (now - times[0]).total_seconds()
            if time_diff <= AUTOMOD_CONFIG["flood_time"]:
                try:
                    await message.delete()
                except:
                    pass
                await apply_mute(message.author, "Flooding chat (spam)")
                warn_msg = await message.channel.send(f"{message.author.mention} ⚠️ Please slow down! You are sending messages too fast.")
                asyncio.create_task(auto_delete_warn(warn_msg))
                return True
    
    if AUTOMOD_CONFIG["duplicate_check"]:
        last_msg = user_last_message.get(user_id)
        if last_msg and message.content.strip() == last_msg.strip():
            try:
                await message.delete()
            except:
                pass
            warn_msg = await message.channel.send(f"{message.author.mention} ⚠️ Please do not send duplicate messages.")
            asyncio.create_task(auto_delete_warn(warn_msg))
            return True
        user_last_message[user_id] = message.content
    return False

async def auto_delete_warn(message, delay=5):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass

# ============================================================
# 👋 WELCOME SYSTEM
# ============================================================

async def send_welcome_message(member):
    try:
        welcome_channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if not welcome_channel:
            return
        
        rules_mention = f"<#{RULES_CHANNEL_ID}>"
        
        embed = discord.Embed(
            title="⚔️ New Warrior Joined",
            description=f"**{member.mention}** has joined the battle!\n\nPlease read the rules before playing:\n📜 {rules_mention}",
            color=0x5865F2,
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Aeternis MU Online")
        
        await welcome_channel.send(embed=embed)
        
    except Exception as e:
        print(f"Welcome message error: {e}")

# ============================================================
# 🧹 CLEAR COMMAND
# ============================================================

@tree.command(name="clear", description="Clear messages in channel")
@app_commands.describe(amount="Number of messages to delete (1-100)")
@app_commands.checks.has_any_role(*ADMIN_ROLE_IDS)
async def clear_command(interaction: discord.Interaction, amount: int):
    if not has_permission(interaction.user, admin_only=True):
        await interaction.response.send_message("🚫 You don't have permission to use this command.", ephemeral=True)
        return
    
    if amount < 1 or amount > 100:
        await interaction.response.send_message("❌ Please specify a number between 1 and 100.", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        deleted = await interaction.channel.purge(limit=amount + 1, check=lambda m: not m.pinned)
        count = len(deleted) - 1
        
        await interaction.followup.send(f"✅ Successfully deleted **{count}** messages.", ephemeral=True)
        
        await send_log(
            "Messages Cleared",
            f"Cleared {count} messages in #{interaction.channel.name}\n**Moderator:** {interaction.user.mention}",
            color=0x00FF00
        )
        
    except discord.HTTPException as e:
        await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Unexpected error: {e}", ephemeral=True)

@clear_command.error
async def clear_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingAnyRole):
        await interaction.response.send_message("🚫 You don't have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)

# ============================================================
# LOGGING FUNCTIONS
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
# PERMISSION CHECKS
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
# 🎁 GIVEAWAY SYSTEM
# ============================================================

class GiveawayEnterButton(Button):
    def __init__(self):
        super().__init__(label="Enter Giveaway", style=discord.ButtonStyle.success, custom_id="giveaway_enter", emoji="🎁")
    
    async def callback(self, interaction: discord.Interaction):
        message_id = interaction.message.id
        if message_id not in active_giveaways:
            await interaction.response.send_message("This giveaway is no longer active!", ephemeral=True)
            return
        giveaway = active_giveaways[message_id]
        if interaction.user.id in giveaway["participants"]:
            await interaction.response.send_message("You have already entered this giveaway!", ephemeral=True)
            return
        giveaway["participants"].append(interaction.user.id)
        embed = interaction.message.embeds[0]
        embed.set_field_at(3, name="📃 Participants", value=f"**{len(giveaway['participants'])}**", inline=True)
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message("✅ You have entered the giveaway!", ephemeral=True)

class GiveawayView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GiveawayEnterButton())

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

def create_giveaway_embed(prize, end_time, winners, host):
    divider = "━━━━━━━━━━━━━━━━━━━━"
    embed = discord.Embed(
        title="🎉 NEW GIVEAWAY",
        description=f"{divider}\n**🎁 Prize**\n> {prize}\n{divider}",
        color=0xFFD700,
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=GIVEAWAY_THUMBNAIL)
    embed.add_field(name="⏳ Ends", value=f"<t:{int(end_time.timestamp())}:F>\n<t:{int(end_time.timestamp())}:R>", inline=True)
    embed.add_field(name="👑 Creator", value=f"{host.mention}", inline=True)
    embed.add_field(name="✨ Winners", value=f"**{winners}**", inline=True)
    embed.add_field(name="📃 Participants", value="**0**", inline=True)
    embed.add_field(name="🧾 Rules", value="- React to enter\n- Must be in server\n- Winner announced automatically", inline=False)
    embed.set_footer(text="Aeternis Core - MU Online | Giveaway System")
    return embed

async def end_giveaway(message_id):
    if message_id not in active_giveaways:
        return
    giveaway = active_giveaways[message_id]
    channel = giveaway["channel"]
    prize = giveaway["prize"]
    winners_count = giveaway["winners"]
    participants = giveaway["participants"]
    del active_giveaways[message_id]
    divider = "━━━━━━━━━━━━━━━━━━━━"
    
    if len(participants) == 0:
        embed = discord.Embed(
            title="❌ Giveaway Ended",
            description=f"{divider}\n**🎁 Prize**\n> {prize}\n{divider}\n\n😔 No participants in this giveaway!\n\nTry joining the next giveaway!",
            color=0xFF6B6B,
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=GIVEAWAY_THUMBNAIL)
        embed.set_footer(text="Aeternis Core - MU Online")
        try:
            msg = await channel.fetch_message(message_id)
            await msg.edit(embed=embed, view=None)
        except:
            pass
        await log_giveaway_action("Giveaway ended", f"Prize: {prize}\nResult: No participants", color=0xFF6B6B)
        return
    
    selected_winners = random.sample(participants, min(winners_count, len(participants)))
    winners_mention = ", ".join([f"<@{winner_id}>" for winner_id in selected_winners])
    embed = discord.Embed(
        title="❌ Giveaway Ended",
        description=f"{divider}\n**🎁 Prize**\n> {prize}\n{divider}\n\n**🥇 Winner:**\n{winners_mention}\n\n🎉 Congratulations! Create a support ticket.",
        color=0x00FFA3,
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=GIVEAWAY_THUMBNAIL)
    embed.add_field(name="📊 Statistics", value=f"- Total participants: **{len(participants)}**\n- Winners selected: **{len(selected_winners)}**\n- Fair random selection: Yes", inline=False)
    embed.set_footer(text="Aeternis Core - MU Online | Results Verified")
    try:
        msg = await channel.fetch_message(message_id)
        await msg.edit(embed=embed, view=None)
        await channel.send(f"🎉 Congratulations: {winners_mention}!")
    except Exception as e:
        print(f"Error ending giveaway: {e}")
    await log_giveaway_action("Giveaway winner selected", f"Prize: {prize}\nWinners: {winners_mention}\nParticipants: {len(participants)}", color=0x00FFA3)

async def scheduled_end_giveaway(message_id, end_time):
    wait_time = (end_time - datetime.utcnow()).total_seconds()
    if wait_time > 0:
        await asyncio.sleep(wait_time)
    await end_giveaway(message_id)

@tree.command(name="giveaway", description="Create a new giveaway")
@app_commands.describe(duration="Duration (e.g., 1h, 24h, 7d)", winners="Number of winners (1-10)", prize="Prize description")
@app_commands.checks.has_any_role(*ADMIN_ROLE_IDS)
async def giveaway_command(interaction: discord.Interaction, duration: str, winners: int, prize: str):
    if not has_permission(interaction.user, admin_only=True):
        await interaction.response.send_message("🚫 Insufficient permissions!", ephemeral=True)
        return
    if winners < 1 or winners > 10:
        await interaction.response.send_message("❌ Invalid number of winners! Use a number between 1 and 10.", ephemeral=True)
        return
    end_time = parse_duration(duration)
    if not end_time:
        await interaction.response.send_message("❌ Invalid duration! Use: 1h, 24h, 7d, etc.", ephemeral=True)
        return
    embed = create_giveaway_embed(prize, end_time, winners, interaction.user)
    view = GiveawayView()
    giveaway_msg = await interaction.channel.send(embed=embed, view=view)
    active_giveaways[giveaway_msg.id] = {"prize": prize, "end_time": end_time, "winners": winners, "host": interaction.user.id, "participants": [], "channel": interaction.channel}
    await log_giveaway_action("Giveaway created", f"Prize: {prize}\nDuration: {duration}\nWinners: {winners}\nChannel: #{interaction.channel.name}", color=0x00FF00)
    await interaction.response.send_message("✅ Giveaway created successfully!", ephemeral=True)
    asyncio.create_task(scheduled_end_giveaway(giveaway_msg.id, end_time))

@giveaway_command.error
async def giveaway_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingAnyRole):
        await interaction.response.send_message("🚫 Insufficient permissions!", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)

# ============================================================
# 🎫 TICKET SYSTEM
# ============================================================

class TicketCreateButton(Button):
    def __init__(self):
        super().__init__(label="Create Ticket", style=discord.ButtonStyle.primary, custom_id="ticket_create")
    
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        for channel in guild.text_channels:
            if channel.name.startswith(f"ticket-{member.name}") and channel.category and channel.category.id == TICKET_CATEGORY_ID:
                await interaction.response.send_message("You already have an open ticket! Please close it before creating a new one.", ephemeral=True)
                return
        overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), member: discord.PermissionOverwrite(read_messages=True, send_messages=True)}
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
                await interaction.response.send_message("❌ Ticket category not found!", ephemeral=True)
                return
            channel = await guild.create_text_channel(name=f"ticket-{member.name}", category=category, overwrites=overwrites, topic=f"Ticket for {member.mention} | Created: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            embed = discord.Embed(title="🎫 Support Ticket", description=f"**Welcome, {member.mention}!**\n\nPlease describe your issue in detail.\n\nA staff member will assist you shortly.", color=0x5865F2, timestamp=datetime.utcnow())
            embed.set_footer(text=f"Ticket ID: {channel.id} - Aeternis Core - MU Online")
            view = TicketControlView()
            await channel.send(embed=embed, view=view)
            await channel.send(f"{member.mention}")
            await interaction.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)
            await send_log("Ticket Created", f"User: {member.name}\nChannel: #{channel.name}", color=0x00FF00)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error creating ticket: {e}", ephemeral=True)

class TicketCloseButton(Button):
    def __init__(self):
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="ticket_close")
    
    async def callback(self, interaction: discord.Interaction):
        if not has_permission(interaction.user, admin_only=False):
            await interaction.response.send_message("🚫 Insufficient permissions!", ephemeral=True)
            return
        confirm_view = ConfirmCloseView()
        await interaction.response.send_message("⚠️ Are you sure you want to close this ticket?", view=confirm_view, ephemeral=True)

class ConfirmCloseButton(Button):
    def __init__(self, confirm=True):
        style = discord.ButtonStyle.success if confirm else discord.ButtonStyle.secondary
        label = "✅ Confirm" if confirm else "❌ Cancel"
        super().__init__(label=label, style=style, custom_id=f"ticket_close_{'yes' if confirm else 'no'}")
        self.confirm = confirm
    
    async def callback(self, interaction: discord.Interaction):
        if self.confirm:
            channel_name = interaction.channel.name
            await send_log("Ticket Closed", f"Closed by: {interaction.user.name}\nChannel: #{channel_name}", color=0xFF0000)
            await interaction.channel.delete()
        else:
            await interaction.response.edit_message(content="❌ Closing cancelled.", view=None)

class ConfirmCloseView(View):
    def __init__(self):
        super().__init__(timeout=30)
        self.add_item(ConfirmCloseButton(confirm=True))
        self.add_item(ConfirmCloseButton(confirm=False))

class TicketControlView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketCloseButton())

class TicketPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketCreateButton())

# ============================================================
# 🌍 LANGUAGE ROLES SYSTEM
# ============================================================

LANGUAGE_ROLES = {
    "general": 1487363000322232390,
    "es": 1487363000980476095,
    "pt": 1487363006374350908,
    "ru": 1487363006869405696,
    "tr": 1487363006894706791,
    "vn": 1487371357573480540,
    "ph": 1487371358085316698,
}

class LangButton(Button):
    def __init__(self, label, emoji, role_id, style=discord.ButtonStyle.secondary):
        super().__init__(label=label, emoji=emoji, style=style, custom_id=f"lang_{role_id}")
        self.role_id = role_id
    
    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        role = guild.get_role(self.role_id)
        if not role:
            await interaction.response.send_message("❌ Role not found!", ephemeral=True)
            return
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"❌ Role **{role.name}** removed!", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"✅ Role **{role.name}** added!", ephemeral=True)

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

# ============================================================
# EMBED CREATION
# ============================================================

def create_welcome_embed():
    embed = discord.Embed(title="WELCOME TO AETERNIS", description="*The Eternal Battle Begins Here*\n\n**Greetings, Warrior!**\n\nYou have entered the realm of **Aeternis**, where legends are forged and eternity awaits.", color=0xFFD700, timestamp=discord.utils.utcnow())
    embed.set_footer(text="Aeternis Core - MU Online")
    embed.add_field(name="QUICK START", value="**1. Verify** — Read rules and verify\n**2. Language** — Choose your language\n**3. Download** — Get the client\n**4. Connect** — Join the battle", inline=False)
    embed.add_field(name="IMPORTANT LINKS", value="🌐 Website\n📖 Wiki/Guide\n🛒 Donate Shop", inline=True)
    embed.add_field(name="SERVER INFO", value="⚔️ EXP: [X]x\n💎 Drop: [X]x\n🛡️ Max Lvl: [X]", inline=True)
    return embed

def create_roles_embed():
    embed = discord.Embed(title="🌍 Language Selection", description="**Select your language to access regional channels!**\n\nClick the buttons below to add or remove language roles.", color=0x5865F2, timestamp=discord.utils.utcnow())
    embed.set_footer(text="Aeternis Core - MU Online")
    embed.add_field(name="📋 Available Languages", value="🌍 **General** — International\n🇪🇸 **Español** — Spanish\n🇵🇹 **Português** — Portuguese\n🇷🇺 **Русский** — Russian\n🇹🇷 **Türkçe** — Turkish\n🇻🇳 **Tiếng Việt** — Vietnamese\n🇵🇭 **Filipino** — Filipino", inline=False)
    embed.add_field(name="⚙️ How it works", value="Click a button to **add** the role.\nClick again to **remove** it.", inline=True)
    embed.add_field(name="🔒 Permissions", value="Roles grant access to language-specific channels.", inline=True)
    return embed

def create_tickets_embed():
    embed = discord.Embed(title="🎫 Support Center", description="**Need help? Create a ticket!**\n\nOur staff will assist you with:\n- 🐛 Bug Reports\n- 💰 Donation Issues\n- 📋 Account Problems\n- ❓ General Questions", color=0x5865F2, timestamp=discord.utils.utcnow())
    embed.set_footer(text="Aeternis Core - MU Online")
    embed.add_field(name="⏱️ Response Time", value="Usually within 24 hours", inline=True)
    embed.add_field(name="🌍 Languages", value="EN / RU / ES / PT / TR / VN / PH", inline=True)
    embed.add_field(name="📋 Rules", value="Be respectful", inline=True)
    return embed

# ============================================================
# BOT EVENTS
# ============================================================

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name="Aeternis MU Online"))
    await tree.sync()
    client.add_view(TicketPanelView())
    client.add_view(LangView())
    client.add_view(GiveawayView())
    print("Aeternis Core v5.0 (English Only) started")
    print(f"Bot: {client.user.name}")
    print(f"ID: {client.user.id}")
    print(f"Log Channel: {LOG_CHANNEL_ID}")
    print(f"Welcome Channel: {WELCOME_CHANNEL_ID}")
    print(f"Rules Channel: {RULES_CHANNEL_ID}")
    print(f"Mute Role ID: {MUTE_ROLE_ID}")
    print(f"Slash Commands: /giveaway, /clear")
    print("-------------------------------")

@client.event
async def on_member_join(member):
    await send_welcome_message(member)
    await send_log("Member Joined", f"User: {member.name}\nID: {member.id}", color=0x00FF00)

@client.event
async def on_member_remove(member):
    await send_log("Member Left", f"User: {member.name}\nID: {member.id}", color=0xFF0000)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if await check_automod(message):
        return
    
    if message.content.strip() == "!welcome":
        embed = create_welcome_embed()
        await message.channel.send(embed=embed)
        try:
            await message.delete()
        except:
            pass
    
    if message.content.strip() == "!roles":
        embed = create_roles_embed()
        view = LangView()
        await message.channel.send(embed=embed, view=view)
        try:
            await message.delete()
        except:
            pass
    
    if message.content.strip() == "!tickets":
        if not has_permission(message.author, admin_only=False):
            await message.reply("🚫 Only administrators can create this panel!", ephemeral=True)
            return
        embed = create_tickets_embed()
        view = TicketPanelView()
        await message.channel.send(embed=embed, view=view)
        try:
            await message.delete()
        except:
            pass
    
    if message.content.strip() == "!close":
        if not has_permission(message.author, admin_only=False):
            await message.reply("🚫 Insufficient permissions!", ephemeral=True)
            return
        if message.channel.category and message.channel.category.id == TICKET_CATEGORY_ID:
            confirm_view = ConfirmCloseView()
            await message.channel.send("⚠️ Are you sure you want to close this ticket?", view=confirm_view)
            try:
                await message.delete()
            except:
                pass

# ============================================================
# STARTUP
# ============================================================

if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except discord.LoginFailure:
        print("ERROR: Invalid Discord token.")
    except Exception as e:
        print(f"Critical error: {e}")
