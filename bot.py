# I M P O R T I N G    P L U G I N S

from sys import builtin_module_names
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from datetime import datetime
import asyncio
import pytz
import json
import os
import aiohttp
import requests
from dotenv import load_dotenv
load_dotenv()


# D E F I N I N G    I N T E N T S


DEVLOG_FILE = "devlog.json"
reaction_roles_file = "reaction_roles.json"
LOGS_PER_PAGE = 5
VALID_PROJECTS = ["dead_dreams_demo", "dead_dreams"]
intents = discord.Intents.default()
intents = discord.Intents.all()
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
HF_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"  # Stable Diffusion model
OPENAI_API_KEY = ""

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# P R E F I X

client = commands.Bot(command_prefix=",", help_command=None, intents=intents)


@client.event
async def on_ready():
    print("Bot is working.")
    activity = discord.Game("Dead Dreams Demo")
    await client.change_presence(activity=activity)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# C A L L I N G    J S O N    F I L E S

def load_warns():
    try:
        with open("warns.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
def log_warns(data):
    with open("warns.json", "w") as file:
        json.dump(data, file, indent=4)
    
def log_to_json(action, user, moderator, reason, comment=None):
    log_entry = {
        "action": action,
        "user": user,
        "moderator": moderator,
        "reason": reason,
        "comment": f"{comment}" if comment else "---",
        "timestamp": datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S %Z")
    }

    try:
        with open("mod_log.json", "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)

    with open("mod_log.json", "w") as file:
        json.dump(logs, file, indent=4)

def log_warn(user, moderator, reason,):
    log_entry = {
        "user": user,
        "moderator": moderator,
        "reason": reason,
        "timestamp": datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S %Z")
    }

    try:
        with open("mod_log.json", "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)

    with open("mod_log.json", "w") as file:
        json.dump(logs, file, indent=4)

def ensure_devlog_file():
    if not os.path.exists(DEVLOG_FILE) or os.stat(DEVLOG_FILE).st_size == 0:
        with open(DEVLOG_FILE, "w") as f:
            json.dump([], f, indent=4)


if not os.path.exists(DEVLOG_FILE):
    with open(DEVLOG_FILE, "w") as f:
        json.dump([], f, indent=4)

def load_reaction_roles():
    if os.path.exists(reaction_roles_file):
        with open(reaction_roles_file, "r") as file:
            return json.load(file)
    return {}

def save_reaction_roles(data):
    with open(reaction_roles_file, "w") as file:
        json.dump(data, file, indent=4)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#  H I    C O M M A N D S

@client.command()
async def hi(ctx):
    await ctx.send("Hello!")


@client.command(name="online", aliases=["working", "up", "on"])
async def online(ctx):
    await ctx.send("Hi, the bot is functioning correctly.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#  R U L E S    C O M M A N D

@client.command(name="rules", aliases=["rule", "RULES", "Rules", "RULE", "Rule"])
async def rules(ctx):
    embed = discord.Embed(
        title="Rules", description="**📌 Server Rules**", color=discord.Color.blue()
    )
    embed.set_author(name="NeoWave Studios")
    embed.add_field(
        name="📜 **__General Rules__**",
        value=(
            "\n"
            "1️⃣ **Respect Everyone** – No harassment, hate speech, racism, sexism, or personal attacks. Treat everyone with respect.\n"
            "2️⃣ **No NSFW Content** – This includes media, links, and discussions. Keep it clean.\n"
            "3️⃣ **No Spamming** – Avoid excessive messages, emojis, or mentions.\n"
            "4️⃣ **No Sharing Private Information** – Do not share personal details without consent.\n"
            "4️⃣ **Keep It Relevant** – Stay on topic in each channel. Random discussions go in designated channels.\n"
            "5️⃣ **No Drama or Toxicity** – Keep arguments private. Don't bring unnecessary negativity into the server.\n"
            "6️⃣ **No Doxxing or Personal Info** – Do not share anyone's personal details without consent.\n"
        ),
        inline=False,
    )
    embed.add_field(
        name="🚫 **__Security & Safety__**",
        value=(
            "\n"
            "7️⃣ **No Impersonation** – Don’t pretend to be staff, another user, or a well-known figure.\n"
            "8️⃣ **No Hacking, Piracy, or Illegal Activities** – Discussions or links related to hacking, pirated software, or anything illegal are strictly forbidden.\n"
            "9️⃣ **Follow Discord's [TOS](https://discord.com/terms) & [Guidlines](https://discord.com/guidelines)** - If Discord doesn’t allow it, we don’t either.\n"
        ),
        inline=False,
    )
    embed.add_field(
        name="⚖ **__Moderation & Conduct__**",
        value=(
            "🔹 **Listen to Mods & Admins** – If a mod asks you to stop doing something, listen to them. Repeated violations may lead to bans.\n"
            "🔹 **Use Common Sense** – If you think something might break the rules, it probably does. Don’t test the limits."
        ),
        inline=False,
    )
    embed.set_footer(text="Enjoy your experience in our server!")
    await ctx.send(embed=embed)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# P U R G E    C O M M A N D

@client.command(name="clear", aliases=["delete", "remove", "purge", "del"])
@commands.has_permissions(manage_messages=True)
async def Clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
    log_to_json("Clear", "N/A", str(ctx.author), "Cleared messages", f(amount, "messages"))


current_time = datetime.now(pytz.timezone("Asia/Kolkata"))
time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# K I C K    C O M M A N D

@client.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if reason == None:
        reason = "---"
    embed = discord.Embed(title="USER KICKED", color=discord.Color.blue())
    embed.set_author(name=member.name, icon_url=member.avatar)
    embed.add_field(
        name="Details",
        value=(
            f"**User Kicked:** {member.mention}\n"
            f"**Moderator:** {ctx.author.mention}\n"
            f"**Reason provided:** {reason}\n"
            f"**Kicked on:** {time}"
        ),
        inline=False,
    )
    await ctx.guild.kick(member)
    kick_log = client.get_channel(1114105865402859530)
    await kick_log.send(embed=embed)
    log_to_json("Kick", str(member), str(ctx.author), reason)

@client.command(name="Time")
async def time(ctx):
    await ctx.send(time)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# B A N    C O M M A N D

@client.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if reason == None:
        reason = "---"
    embed = discord.Embed(title="USER BANNED", color=discord.Color.blue())
    embed.set_author(name=member.name, icon_url=member.avatar)
    embed.add_field(
        name="Details",
        value=(
            f"**User Banned:** {member.mention}\n"
            f"**Moderator:** {ctx.author.mention}\n"
            f"**Reason provided:** {reason}\n"
            f"**Banned on:** {time}"
        ),
        inline=False,
    )

    await member.ban(reason=reason)
    ban_log = client.get_channel(1114105865402859530)
    await ban_log.send(embed=embed)
    log_to_json("Ban", str(member), str(ctx.author), reason)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# M U T E    C O M M A N D

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, duration: int = None, *, reason="No reason provided"):
    """Mutes a user with an optional duration (in minutes)."""
    
    muted_role = discord.utils.get(ctx.guild.roles, name="mute")
    
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted", reason="Mute role for muting users")
        
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False, speak=False)
    
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted. Reason: {reason}")

    log_channel = client.get_channel(1114105865402859530)
    if log_channel:
        embed = discord.Embed(title="User Muted", color=discord.Color.red())
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Duration", value=f"{duration} minutes" if duration else "Permanent", inline=False)
        await log_channel.send(embed=embed)
        log_to_json("Mute", str(member), str(ctx.author), reason, duration)


    if duration:
        await asyncio.sleep(duration * 60)
        await member.remove_roles(muted_role)
        await ctx.send(f"{member.mention} has been automatically unmuted.")
        log_to_json("Unmute (Auto)", str(member), "Bot", "Time elapsed, Hence unmuted", f(duration, "minutes"))

        if log_channel:
            embed = discord.Embed(title="🔊 User Unmuted (Auto)", color=discord.Color.green())
            embed.add_field(name="User", value=member.mention, inline=True)
            embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
            await log_channel.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    """Unmutes a user manually."""
    muted_role = discord.utils.get(ctx.guild.roles, name="mute")

    if not muted_role or muted_role not in member.roles:
        await ctx.send(f"{member.mention} is not muted.")
        return

    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} has been unmuted.")

    log_channel = client.get_channel(1114105865402859530)
    if log_channel:
        embed = discord.Embed(title="User Unmuted", color=discord.Color.green())
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
        await log_channel.send(embed=embed)
        log_to_json("Unmute (Manual)", str(member), str(ctx.author), "Manual unmute")

@mute.error
@unmute.error
async def error_handler(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need `Manage Messages` permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: `,mute @user [duration in minutes] [reason]` OR `,unmute @user`")
    else:
        await ctx.send("Hmm... This does not seem to work. Try again later or contact the bot developer.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# W A R N    C O M M A N D

@client.command(name="warn")
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    warns_data = load_warns()
    user_id = str(member.id)

    warning_entry = {
        "reason": reason,
        "moderator": str(ctx.author),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if user_id in warns_data:
        warns_data[user_id].append(warning_entry)
    else:
        warns_data[user_id] = [warning_entry]

    log_warns(warns_data)
    await ctx.send(f"{member.mention} has been warned by {ctx.author.mention}. Reason: {reason}.")

# Check warns command
@client.command(name="warns")
async def check_warns(ctx, member: discord.Member):
    warns_data = load_warns()
    user_id = str(member.id)

    if user_id in warns_data:
        embed = discord.Embed(title=f"Warnings for {member.name}", color=discord.Color.orange())
        for idx, warning in enumerate(warns_data[user_id], start=1):
            embed.add_field(
                name=f"Warning {idx}",
                value=f"**Reason:** {warning['reason']}\n**Moderator:** {warning['moderator']}\n**Date:** {warning['timestamp']}",
                inline=False
            )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{member.mention} has no warnings.")


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# M E M E    C O M M A N D 
 
@client.command(name="meme", aliases=["MEME", "memer", "emem", "meem", "emme"])
async def meme(ctx):
    async def fetch_meme():
        url = "https://meme-api.com/gimme"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    meme_data = await fetch_meme()
    if meme_data is None:
        await ctx.send("Failed to fetch a meme. Please try again later!")
        return

    meme_url = meme_data["url"]
    meme_title = meme_data["title"]
    meme_author = meme_data["author"]
    meme_subreddit = meme_data["subreddit"]
    meme_postlink = meme_data["postLink"]

    # Create an embed for the meme
    embed = discord.Embed(title=meme_title, color=discord.Color.blue())
    embed.set_image(url=meme_url)
    embed.set_footer(
        text=f"u/{meme_author} | r/{meme_subreddit}"
    )

    # Define the "More" button
    class MoreMemeView(View):
        @discord.ui.button(label="More", style=discord.ButtonStyle.primary)
        async def more_button(self, interaction: discord.Interaction, button: Button):
            meme_data = await fetch_meme()
            if meme_data is None:
                await interaction.response.send_message(
                    "Failed to fetch a meme. Please try again later!", ephemeral=True
                )
                return

            # Update the embed with a new meme
            new_embed = discord.Embed(
                title=meme_data["title"], color=discord.Color.blue()
            )
            new_embed.set_image(url=meme_data["url"])
            new_embed.set_footer(
                text=f"u/{meme_data['author']} | r/{meme_data['subreddit']}"
            )
            await interaction.response.edit_message(embed=new_embed, view=self)

    # Send the initial embed with the "More" button
    await ctx.send(embed=embed, view=MoreMemeView())

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# G A M E S    C O M M A N D

@client.command(
    name="games", aliases=["Games", "GAMES", "Game", "game", "GAME", "gamelist"]
)
async def games(ctx):
    embed = discord.Embed(
        title="Games",
        description="These are all the games we have released/plan to release.",
        color=discord.Color.blue(),
    )
    embed.set_author(name="NeoWave Studios")
    embed.add_field(
        name="__1. Dead Dreams__",
        value=(
            "Genre: Horror\n"
            "Status: UnReleased\n"
            "Release Date: TBA (Demo: Early 2025)\n"
            "Condition: Under Development\n"
            "Description:\n\n"
            "Dead Dreams is our current project, which is a FNAF fan game. It features two styles of gameplay - The regular FNAF style sections (You have cameras, you close doors, etc.), and the Free Roam section, which is the main feature of this game. The game will feature its own unique storyline, as well as wide variety of mechanics.\n"
        ),
    )
    embed.set_footer(
        text="Thanks for reading! Please support us by playing our games and giving us feedbacks."
    )
    await ctx.send(embed=embed)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# D E V L O G

#Ensure the devlog file exists and is valid
def ensure_devlog_file():
    if not os.path.exists(DEVLOG_FILE) or os.stat(DEVLOG_FILE).st_size == 0:
        with open(DEVLOG_FILE, "w") as f:
            json.dump({}, f, indent=4)


#Get current IST time
def get_current_time():
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist).strftime("%Y-%m-%d")


#Command to add a devlog
@client.command()
async def devlog(
    ctx,
    action: str = None,
    project: str = None,
    number: str = None,
    heading: str = None,
    *,
    details: str = None,
):
    """Handles devlog actions (Adding new logs)."""

    developer_role = discord.utils.get(ctx.guild.roles, name="Developer")
    if developer_role not in ctx.author.roles:
        await ctx.send("🚫 You need the 'Developer' role to use this command.")
        return

    if (
        action != "add"
        or project not in VALID_PROJECTS
        or not number
        or not heading
        or not details
    ):
        await ctx.send(
            "⚠️ **Invalid usage!** Use:\n`,devlog add <bot/game> <number> <heading> <details>`"
        )
        return

    ensure_devlog_file()

    with open(DEVLOG_FILE, "r") as f:
        logs = json.load(f)

    if project not in logs:
        logs[project] = []

    logs[project].append(
        {
            "number": number,
            "heading": heading,
            "details": details,
            "author": ctx.author.name,
            "timestamp": get_current_time(),
        }
    )

    with open(DEVLOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

    await ctx.send(f"✅ **Devlog {number} added successfully for {project}!**")


#Pagination
class DevlogView(discord.ui.View):
    def __init__(self, logs, project, page, total_pages):
        super().__init__()
        self.logs = logs
        self.project = project
        self.page = page
        self.total_pages = total_pages

    async def update_embed(self, interaction):
        start_idx = (self.page - 1) * LOGS_PER_PAGE
        end_idx = start_idx + LOGS_PER_PAGE
        logs_to_display = self.logs[::-1][start_idx:end_idx]

        embed = discord.Embed(
            title=f"🛠️ {self.project.upper()} Development Logs (Page {self.page}/{self.total_pages})",
            color=discord.Color.blue(),
        )

        for log in logs_to_display:
            embed.add_field(
                name=f"📌 {log['number']} - {log['heading']} ({log['timestamp']})",
                value=f"**Details:**\n{log['details']}\n\n**Author:** {log['author']}",
                inline=False,
            )

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀️ Prev", style=discord.ButtonStyle.primary)
    async def prev_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.page > 1:
            self.page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label="Next ▶️", style=discord.ButtonStyle.primary)
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.page < self.total_pages:
            self.page += 1
            await self.update_embed(interaction)


#Command to view paginated devlogs (With Buttons)
@client.command()
async def devlogs(ctx, project: str = None):
    """Displays development logs for a specific project with pagination buttons."""

    if project not in VALID_PROJECTS:
        await ctx.send(
            f"⚠️ **Invalid project!** Choose from: {', '.join(VALID_PROJECTS)}\nUsage: `,devlogs fluorez` or `,devlogs dead_dreams`"
        )
        return

    ensure_devlog_file()

    with open(DEVLOG_FILE, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            await ctx.send("⚠️ Error: Devlog file is corrupted! Resetting...")
            with open(DEVLOG_FILE, "w") as reset_file:
                json.dump({}, reset_file, indent=4)
            return

    if project not in logs or not logs[project]:
        await ctx.send(f"📭 No devlogs available for **{project}**!")
        return

    total_pages = max(1, (len(logs[project]) + LOGS_PER_PAGE - 1) // LOGS_PER_PAGE)

    view = DevlogView(logs[project], project, 1, total_pages)

    # Initial Embed
    start_idx = 0
    end_idx = LOGS_PER_PAGE
    logs_to_display = logs[project][::-1][start_idx:end_idx]

    embed = discord.Embed(
        title=f"🛠️ {project.upper()} Development Logs (Page 1/{total_pages})",
        color=discord.Color.blue(),
    )

    for log in logs_to_display:
        embed.add_field(
            name=f"📌 {log['number']} - {log['heading']} ({log['timestamp']})",
            value=f"**Details:**\n{log['details']}\n\n**Author:** {log['author']}",
            inline=False,
        )

    await ctx.send(embed=embed, view=view)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# R E A C T I O N    R O L E S    C O M M A N D

reaction_roles = load_reaction_roles()

@client.command()
@commands.has_permissions(manage_roles=True)
async def reactionrole(ctx, channel: discord.TextChannel, emoji: str, role: discord.Role, title: str, *, description: str):
    """Command to send an embed for reaction roles."""
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    embed.set_footer(text="React below to get the role!")

    message = await channel.send(embed=embed)
    await message.add_reaction(emoji)

    # Store reaction-role mapping in JSON
    reaction_roles[str(message.id)] = {"emoji": emoji, "role_id": role.id}
    save_reaction_roles(reaction_roles)

    await ctx.send(f"✅ Reaction role set! Users can react to `{emoji}` in {channel.mention} to get `{role.name}`.")

@client.event
async def on_raw_reaction_add(payload):
    """Gives role when a user reacts."""
    if str(payload.message_id) in reaction_roles:
        data = reaction_roles[str(payload.message_id)]
        if str(payload.emoji) == data["emoji"]:
            guild = client.get_guild(payload.guild_id)
            role = guild.get_role(data["role_id"])
            member = guild.get_member(payload.user_id)

            if role and member and not member.bot:
                await member.add_roles(role)
                print(f"✅ Gave {role.name} to {member.display_name}")

@client.event
async def on_raw_reaction_remove(payload):
    """Removes role when a user removes reaction."""
    if str(payload.message_id) in reaction_roles:
        data = reaction_roles[str(payload.message_id)]
        if str(payload.emoji) == data["emoji"]:
            guild = client.get_guild(payload.guild_id)
            role = guild.get_role(data["role_id"])
            member = guild.get_member(payload.user_id)

            if role and member and not member.bot:
                await member.remove_roles(role)
                print(f"❌ Removed {role.name} from {member.display_name}")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# P O I N T L A U G H    C O M M A N D

@client.command()
async def pointlaugh(ctx, member: discord.Member = None):
    target = member.mention if member else ctx.author.mention
    await ctx.send(f"*points and laughs at* {target} :joy: :rofl:")

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# F I L T E R    C R I N G E    W O R D S

cringe_words = ["uwu", "owo", "meow", "rawr", "x3", ">:3", "pwease", "sowwy"]
restricted_words= ["bakchod", "fuck", "kamine", "nigga", "kamina", "madarchod", "faggot", "bsdk", "chamaar", "bastard", "motherfucker", "bhosdike", "fucker", "nigger", "whore", "asshole", "slut", "chamar", "fucking", "fag", "cock"]

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if any(word in message.content.lower() for word in cringe_words):
        await message.reply(f"stop embarrassing yourself.")
    if any(word in message.content.lower() for word in restricted_words):
        await message.reply(f"Stop using such language in this server. <@&{922188455570706482}>")
    if sum(1 for c in message.content if c.isupper()) > len(message.content) * 0.7 and len(message.content) > 5:
        await message.reply("STOP. SHOUTING.")

    await client.process_commands(message)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# H E L P    C O M M A N D

class HelpDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="General", description="Basic commands", emoji="📜"
            ),
            discord.SelectOption(
                label="Studio", description="Studio commands", emoji="💼"
            ),
            discord.SelectOption(
                label="Fun", description="Meme and game commands", emoji="🎮"
            ),
            discord.SelectOption(
                label="Moderation", description="Admin commands", emoji="🛠️"
            ),
            discord.SelectOption(
                label="Server Utilities", description="Server commands", emoji="🛠️"
            ),
        ]
        super().__init__(placeholder="Choose a category...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]

        if category == "General":
            embed = discord.Embed(
                title="📜 Studio commands", color=discord.Color.blue()
            )
            embed.add_field(
                name="Syntax",
                value="**Prefix is `,`**\n**Syntax: `,<command>`**",
                inline=False,
            )
            embed.add_field(
                name="1. Rules",
                value="Shows the list of rules.\n**Aliases:** `rules, rule`\n**Usage:** `,rules`",
                inline=False,
            )
        elif category == "Studio":
            embed = discord.Embed(
                title="💼 General Commands", color=discord.Color.yellow()
            )
            embed.add_field(
                name="Syntax",
                value="**Prefix is `,`**\n**Syntax: `,<command>`**",
                inline=False,
            )
            embed.add_field(
                name="1. Devlogs",
                value="Shows the list of devlogs.\n**Usage:** `,devlogs <project>`",
                inline=False,
            )
            embed.add_field(
                name="2. Games",
                value="Shows a list of our projects.\n**Aliases:** `games, gamelist`\n**Usage:** `,games`",
                inline=False,
            )

        elif category == "Fun":
            embed = discord.Embed(title="🎮 Fun Commands", color=discord.Color.green())
            embed.add_field(
                name="Syntax",
                value="**Prefix is `,`**\n**Syntax: `,<command>`**",
                inline=False,
            )
            embed.add_field(
                name="1. Meme",
                value="Fetches a random meme from Reddit.\n**Aliases:** `meme, meem, emem`\n**Usage:** `,meme`",
                inline=False,
            )
            embed.add_field(
                name="2. PointLaugh",
                value="Points and laughs the mentioned member, duh.\n**Usage:** `,pointlaugh <member>`",
                inline=False,
            )

        elif category == "Moderation":
            embed = discord.Embed(
                title="🛠️ Moderation Commands", color=discord.Color.red()
            )
            embed.add_field(
                name="Syntax",
                value="**Prefix is `,`**\n**Syntax: `,<command>`**",
                inline=False,
            )
            embed.add_field(
                name="1. Purge",
                value="Deletes a specified number of messages.\n**Aliases:** `clear, delete, remove, purge`\n**Usage:** `,purge <number>`\n**Permissions:** `Manage Messages`",
                inline=False,
            )
            embed.add_field(
                name="2. Kick",
                value="Kicks a user from the server.\n**Usage:** `,kick <member> <reason>`\n**Permissions:** `Kick Members`",
                inline=False,
            )
            embed.add_field(
                name="3. Ban",
                value="Bans a user from the server.\n**Usage:** `,ban <member> <reason>`\n**Permissions:** `Ban Members`",
                inline=False,
            )
            embed.add_field(
                name="4. Mute",
                value="Mutes a user in the server.\n**Usage:** `,mute <member> <duration_minutes> <reason>`\n**Permissions:** `Manage Messages`",
                inline=False,
            )
            embed.add_field(
                name="5.Unmute",
                value="Unmutes a user in the server.\n**Usage:** `,unmute <member>`\n**Permissions:** `Manage Messages`",
                inline=False,
            )

        elif category == "Server Utilities":
            embed = discord.Embed(
                title="🛠️ Moderation Commands", color=discord.Color.red()
            )
            embed.add_field(
                name="Syntax",
                value="**Prefix is `,`**\n**Syntax: `,<command>`**",
                inline=False,
            )
            embed.add_field(
                name="1. Devlog",
                value="**Adds a devlogs to the list.**\n**Syntax**:`,devlog add <project name> <devlog number> <title> <description>`\n**Role:** `Developer`",
                inline=False,
            )
            embed.add_field(
                name="2. Reaction Roles",
                value="**Adds an embed for reaction roles to a specified channel.**\n**Syntax**:`,reactionrole <#channel> <:emoji:> <@role> <title> <description>`\n**Permissions:** `Manage Roles`",
                inline=False,
            )
            

        embed.set_footer(text="Select a category from the dropdown menu below.")

        await interaction.response.edit_message(embed=embed)


class HelpView(View):
    def __init__(self):
        super().__init__()
        self.add_item(HelpDropdown())


@client.command(
    name="help", aliases=["HELP", "Help", "commands", "Commands", "COMMANDS"]
)
async def help(ctx):
    embed = discord.Embed(
        title="📖 Help Menu",
        description="Use the dropdown below to view different command categories.",
        color=discord.Color.blue(),
    )
    embed.set_author(name="NeoWave Studios")
    embed.set_footer(text="Select a category from the dropdown menu.")

    await ctx.send(embed=embed, view=HelpView())

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CLIENT_ID = os.getenv('CLIENT_ID')
client.run(CLIENT_ID)
