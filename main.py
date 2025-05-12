# RADON / https://github.com/zeozcb/Radon

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import json
import os
import random
import requests
import asyncio
import string
import time
import datetime
from colorama import Fore
import platform
import psutil
import itertools
from gtts import gTTS
import io
import qrcode
import pyfiglet
import aiohttp
import lyricsgenius
import contextlib
import subprocess
import sys
import shutil
import inspect
import cpuinfo
import GPUtil
import socket
import uuid
import re

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_PATH)

genius = lyricsgenius.Genius("RVKf9sgQop3EokoVK16dVKOav1q9ii9m06gQRJa9xV5zUQE9jNmJbZXOG-xNwHum")

try:
    with open(os.path.join(BASE_PATH, '.ver'), 'r') as ver_file:
        current_version = ver_file.read().strip()
except FileNotFoundError:
    current_version = "Unknown"

loop_running = False
status_animation_running = False
has_nitro = False

y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX

update_message_sent = False
latest_version = None
update_available = False

start_time = datetime.datetime.now(datetime.timezone.utc)

config_path = os.path.join(BASE_PATH, "config", "config.json")

def load_config():
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)
    except UnicodeDecodeError:
        try:
            with open(config_path, "r", encoding="utf-8-sig") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error reading config file: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"Unexpected error reading config file: {e}")
        sys.exit(1)

config = load_config()

def create_message_generator():
    messages = config["autoreply"]["messages"]
    while True:
        for message in messages:
            yield message

message_generator = create_message_generator()

if "tokens" in config and len(config["tokens"]) > 0:
    token = config["tokens"][0]["token"]
    prefix = config["tokens"][0]["prefix"]
else:
    token = None
    prefix = "."

if "autoreply" not in config or "messages" not in config["autoreply"]:
    config["autoreply"] = {"messages": ["Hello! I'm currently AFK.", "Hi there! I'm currently AFK."], "channels": [], "users": []}

def save_config(config):
    try:
        with open(config_path, "w", encoding="utf-8") as file:
            json.dump(config, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving config file: {e}")

def get_emoji(emoji_name, default_emoji):
    if config.get('nitro_emotes', False):
        custom_emoji = discord.utils.get(bot.emojis, name=emoji_name)
        return str(custom_emoji) if custom_emoji else default_emoji
    elif not has_nitro and bot.get_guild(1359951405057704150):
        custom_emoji = discord.utils.get(bot.get_guild(1359951405057704150).emojis, name=emoji_name)
        return str(custom_emoji) if custom_emoji else default_emoji
    return default_emoji

if 'nitro_emotes' not in config:
    config['nitro_emotes'] = False
    save_config(config)

if 'advertise_delay' not in config:
    config['advertise_delay'] = {
        'min': 2,
        'max': 4
    }
    save_config(config)

def selfbot_menu(bot):
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    print(f"""\n{Fore.RESET}
                                            ██████╗  █████╗ ██████╗  ██████╗ ███╗   ██╗
                                            ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗████╗  ██║
                                            ██████╔╝███████║██║  ██║██║   ██║██╔██╗ ██║
                                            ██╔══██╗██╔══██║██║  ██║██║   ██║██║╚██╗██║
                                            ██║  ██║██║  ██║██████╔╝╚██████╔╝██║ ╚████║
                                            ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝\n""".replace('█', f'{b}█{y}'))
    print(f"""{y}------------------------------------------------------------------------------------------------------------------------
{w} Radon {b}|{w} MODIFIED BY ZEOZCB Radon {b}|{w} MODIFIED BY ZEOZCB Radon {b}|{w} MODIFIED BY ZEOZCB Radon {b}|{w} MODIFIED BY ZEOZCB
{y}------------------------------------------------------------------------------------------------------------------------\n""")
    print(f"""{y}[{b}+{y}]{w} SelfBot Information:\n
\t{y}[{w}#{y}]{w} Version: v{current_version}
\t{y}[{w}#{y}]{w} Logged in as: {bot.user} ({bot.user.id})
\t{y}[{w}#{y}]{w} Cached Users: {len(bot.users)}
\t{y}[{w}#{y}]{w} Guilds Connected: {len(bot.guilds)}\n\n
{y}[{b}+{y}]{w} Settings Overview:\n
\t{y}[{w}#{y}]{w} SelfBot Prefix: {bot.command_prefix}
\t{y}[{w}#{y}]{w} Remote Users Configured:""")
    if config["remote-users"]:
        for i, user_id in enumerate(config["remote-users"], start=1):
            print(f"\t\t{y}[{w}{i}{y}]{w} User ID: {user_id}")
    else:
        print(f"\t\t{y}[{w}-{y}]{w} No remote users configured.")
    print(f"""
\t{y}[{w}#{y}]{w} Active Autoreply Channels: {len(config["autoreply"]["channels"])}
\t{y}[{w}#{y}]{w} Active Autoreply Users: {len(config["autoreply"]["users"])}\n
\t{y}[{w}#{y}]{w} AFK Status: {'Enabled' if config["afk"]["enabled"] else 'Disabled'}
\t{y}[{w}#{y}]{w} AFK Message: "{config["afk"]["message"]}"\n
\t{y}[{w}#{y}]{w} Total Commands Loaded: 43\n\n
{y}[{Fore.GREEN}!{y}]{w} SelfBot is now online and ready!""")


bot = commands.Bot(command_prefix=prefix, description='crook', self_bot=True, help_command=None)

@bot.event
async def on_ready():
    global update_message_sent, latest_version, update_available, has_nitro
    if platform.system() == "Windows":
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(f"SelfBot v{current_version} - Made By zeozcb | Radon")
    
    latest_version, update_available = check_for_updates()
    update_message_sent = False

    bot.loop.create_task(auto_check_updates())

    has_nitro = await check_nitro_status()

    selfbot_menu(bot)

    if update_available:
        update_message = f"""
:rotating_light: **SelfBot Update Available!** :rotating_light:

A new version of the SelfBot is available. Would you like to update?

:small_orange_diamond: Current version: `v{current_version}`
:small_blue_diamond: Latest version: `v{latest_version}`

:arrow_up: To update, use the command: `.update`
:x: To dismiss this message, use: `.dismiss`

Stay up to date for the best experience!
"""
        print(update_message)

async def check_nitro_status():
    headers = {'Authorization': token}
    async with aiohttp.ClientSession() as session:
        async with session.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers) as r:
            if r.status == 200:
                json = await r.json()
                return len(json) > 0
    return False

@bot.command()
async def nitro(ctx, action: str = None):
    await ctx.message.delete()
    
    if action is None:
        await ctx.send(f"> **[ERROR]**: Invalid command.\n> __Command__: `{prefix}nitro <enable|disable>`", delete_after=5)
        return
    
    if action.lower() not in ['enable', 'disable']:
        await ctx.send(f"> **[ERROR]**: Invalid action. Use 'enable' or 'disable'.\n> __Command__: `{prefix}nitro <enable|disable>`", delete_after=5)
        return
    
    if action.lower() == 'enable':
        if has_nitro:
            config['nitro_emotes'] = True
            save_config(config)
            await ctx.send("> Nitro emotes enabled. You can now use custom emotes in any server.", delete_after=5)
        else:
            await ctx.send("> You need to join the official SelfBot server to use emotes without Nitro. Use `.server` to get an invite.", delete_after=5)
    else:
        config['nitro_emotes'] = False
        save_config(config)
        await ctx.send("> Nitro emotes disabled. Custom emotes will only work in the official SelfBot server.", delete_after=5)

@bot.command()
async def server(ctx):
    await ctx.message.delete()
    await ctx.send("> Join the official SelfBot server: https://discord.gg/8bTgaSkU5r", delete_after=10)

@bot.event
async def on_message(message):
    global update_message_sent, latest_version, update_available

    if message.author != bot.user and str(message.author.id) not in config["remote-users"]:
        return

    if message.author == bot.user and (config.get('nitro_emotes', False) or (not has_nitro and message.guild and message.guild.id == 1359951405057704150)):
        content = message.content
        emote_pattern = r'<a?:(\w+):(\d+)>'
        emotes = re.findall(emote_pattern, content)
        
        for name, id in emotes:
            if has_nitro:
                continue
            elif message.guild and message.guild.id == 1359951405057704150:
                content = content.replace(f'<a:{name}:{id}>', f'<:{name}:{id}>')
            else:
                content = content.replace(f'<a:{name}:{id}>', f':{name}:')
                content = content.replace(f'<:{name}:{id}>', f':{name}:')
        
        if content != message.content:
            await message.delete()
            await message.channel.send(content)
            return

    if message.author == bot.user and message.content.startswith(bot.command_prefix):
        if update_available and not update_message_sent:
            update_message = f"""
:rotating_light: **SelfBot Update Available!** :rotating_light:

A new version of the SelfBot is available. Would you like to update?

:small_orange_diamond: Current version: `v{current_version}`
:small_blue_diamond: Latest version: `v{latest_version}`

:arrow_up: To update, use the command: `.update`
:x: To dismiss this message, use: `.dismiss`

Stay up to date for the best experience!
"""
            await message.channel.send(update_message)
            update_message_sent = True

    if message.author.id in config.get("copycat", {}).get("users", []) and message.author != bot.user:
        if message.content.startswith(bot.command_prefix):
            response_message = message.content[len(bot.command_prefix):]
            await message.reply(response_message)
        else:
            await message.reply(message.content)

    if config["afk"]["enabled"] and message.author != bot.user:
        if bot.user in message.mentions:
            await message.reply(config["afk"]["message"])
            return
        elif isinstance(message.channel, discord.DMChannel):
            await message.reply(config["afk"]["message"])
            return

    if message.author != bot.user:
        if str(message.author.id) in config["autoreply"]["users"]:
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return
        elif str(message.channel.id) in config["autoreply"]["channels"]:
            autoreply_message = next(message_generator)
            await message.reply(autoreply_message)
            return
    
    if message.guild and message.guild.id == 1359951405057704150 and message.content.startswith(bot.command_prefix):
        await message.delete()
        await message.channel.send("> SelfBot commands are not allowed here. Thanks.", delete_after=5)
        return

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.errors.NotFound):
        return
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CommandInvokeError):
        original = error.original
        if isinstance(original, discord.errors.NotFound):
            return
        await ctx.send(f"> **[ERROR]**: {str(original)}", delete_after=5)
    else:
        await ctx.send(f"> **[ERROR]**: {str(error)}", delete_after=5)

async def safe_delete(message):
    try:
        await message.delete()
    except discord.errors.NotFound:
        pass


@bot.command(aliases=['h'])
async def help(ctx, option: str = None, *, query: str = None):
    try:
        await ctx.message.delete()
    except discord.errors.NotFound:
        pass
    
    command_categories = {
        "general": {
            "help": "Displays this help message",
            "ping": "Check the bot's latency",
            "uptime": "Shows the bot's uptime and system info",
            "uptimeconfig": "Configure what information is shown in uptime command",
            "changeprefix": "Change the bot's command prefix",
            "shutdown": "Shut down the selfbot",
            "reload": "Reload the selfbot",
            "check": "Check for selfbot updates",
            "update": "Update the selfbot to the latest version",
            "dismiss": "Dismiss update notification",
            "server": "Get an invite to the official server",
            "nitro": "Configure nitro emote settings",
        },
        "messaging": {
            "quickdelete": "Send a message that deletes after 2 seconds",
            "hidemention": "Hide a message behind a mention",
            "edit": "Send a message that can be edited",
            "clear": "Send a message that clears the chat visually",
            "emojify": "Convert text to emoji characters",
            "reverse": "Reverse the given text",
            "leetspeak": "Convert text to leet speak",
            "uwuify": "UwU-ify your message",
            "retardify": "Make your text look retarded",
            "femboyify": "Make your text look like it's from a femboy",
            "ascii": "Convert text to ASCII art",
            "mock": "MoCk TeXt LiKe ThIs",
            "tts": "Send a text-to-speech message as an audio file",
        },
        "social": {
            "media": "Show your social media links",
            "social": "Alias for media command",
            "setsocial": "Set your social media details",
            "dox": "Look up a username across platforms (informational only)",
            "geoip": "Look up location from an IP address",
        },
        "utility": {
            "qr": "Generate a QR code from text",
            "pingweb": "Check if a website is online",
            "remoteuser": "Add or remove users who can control your selfbot",
            "copycat": "Copy messages from a specific user",
            "autoreply": "Set up automatic replies to users or in channels",
            "afk": "Toggle AFK mode with custom message",
            "firstmessage": "Get a link to the first message in a channel",
            "usericon": "Get a user's avatar",
            "guildicon": "Get the server's icon",
            "guildbanner": "Get the server's banner",
            "guildrename": "Rename a server (if you have permission)",
            "guildinfo": "Get information about the current server",
            "tokeninfo": "Get information from a Discord token",
            "gentoken": "Generate a fake Discord token",
            "hypesquad": "Change your HypeSquad house",
        },
        "fun": {
            "airplane": "Show 9/11 animation",
            "catplay": "Show a cat animation",
            "coinflip": "Flip a coin",
            "magicball": "Ask the magic 8-ball a question",
            "roll": "Roll dice (e.g., 2d6)",
            "minesweeper": "Play minesweeper in Discord",
            "dick": "Show the size of someone's 'member'",
            "animatestatus": "Create an animated custom status",
            "stopanimation": "Stop any running animation",
            "loopstop": "Stop any animation loop",
            "nitrogen": "Generate a fake Nitro gift link",
        },
        "trolling": {
            "discordupdate": "Send a fake Discord update message",
            "terminate": "Send a fake account termination message",
            "raidalert": "Send a fake raid alert message",
            "nitroexpire": "Send a fake Nitro expiration notice",
            "ownertransfer": "Send a fake ownership transfer message",
            "staffwarning": "Send a fake Discord staff warning",
            "serverdelete": "Send a fake server deletion message",
            "fakehack": "Pretend to hack someone",
            "fakeban": "Send a fake ban message",
            "fakemute": "Send a fake mute message",
            "fakenitro": "Send a fake Nitro gift",
            "fakeverify": "Send a fake account verification message",
            "fakepayment": "Send a fake payment confirmation",
            "fakegiveaway": "Start a fake giveaway",
            "ghostping": "Ghost ping a user",
        },
        "spam": {
            "spam": "Send multiple messages",
            "sendall": "Send a message to all channels in a server",
            "dmall": "DM all members in a server",
            "advertise": "Advertise in specific channels across servers",
            "setdelay": "Set delay for the advertise command",
        },
        "status": {
            "playing": "Set your status to playing a game",
            "streaming": "Set your status to streaming",
            "stopactivity": "Stop any activity status",
        },
        "server": {
            "fetchmembers": "Get a list of all members in the server",
            "purge": "Delete multiple messages (requires permissions)",
            "whremove": "Delete a webhook",
        },
        "python": {
            "exec": "Execute Python code",
        },
        "other": {
            "lyrics": "Search for song lyrics",
            "zeo": "Send a gif",
        }
    }
    
    if option and option.lower() == "small":
        command_list = []
        for category, commands in command_categories.items():
            for cmd, desc in commands.items():
                command_list.append(f"{prefix}{cmd}")
        
        chunks = [command_list[i:i+20] for i in range(0, len(command_list), 20)]
        for chunk in chunks:
            await ctx.send(f"```{', '.join(chunk)}```")
        return
    
    elif option and option.lower() == "search":
        if not query:
            await ctx.send(f"> **[ERROR]**: Please provide a search query.\n> __Command__: `{prefix}help search <query>`", delete_after=5)
            return
        
        search_results = []
        query = query.lower()
        
        if query in command_categories:
            await ctx.send(f"**Commands in category '{query}':**")
            commands_text = ""
            for cmd, desc in command_categories[query].items():
                commands_text += f"> `{prefix}{cmd}` - {desc}\n"
            
            chunks = [commands_text[i:i+1900] for i in range(0, len(commands_text), 1900)]
            for chunk in chunks:
                await ctx.send(chunk)
            return
        
        for category, commands in command_categories.items():
            for cmd, desc in commands.items():
                if query in cmd.lower() or query in desc.lower():
                    search_results.append(f"> `{prefix}{cmd}` - {desc} **[{category}]**")
        
        if search_results:
            await ctx.send(f"**Search results for '{query}':**")
            chunks = [search_results[i:i+15] for i in range(0, len(search_results), 15)]
            for chunk in chunks:
                await ctx.send("\n".join(chunk))
        else:
            await ctx.send(f"> No commands found matching '{query}'.")
        return
    
    help_intro = f"""```yaml
Radon SelfBot | Prefix: {prefix}
```
> Use `{prefix}help small` for a compact command list
> Use `{prefix}help search <query>` to search for specific commands

"""
    await ctx.send(help_intro)
    
    for category, commands in command_categories.items():
        category_name = category.upper()
        help_text = f"**{category_name} COMMANDS:**\n"
        
        for cmd, desc in commands.items():
            help_text += f"> `{prefix}{cmd}` - {desc}\n"
        
        if len(help_text) > 2000:
            chunks = [help_text[i:i+1900] for i in range(0, len(help_text), 1900)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(help_text)

def check_for_updates():
    try:
        response = requests.get("https://raw.githubusercontent.com/zeozcb/Radon/refs/heads/main/.ver")
        latest_version = response.text.strip()
        return latest_version, latest_version != current_version
    except:
        return None, False

async def send_error(ctx, message, delete_after=5):
    await ctx.message.delete()
    await ctx.send(f"> **[ERROR]**: {message}", delete_after=delete_after)

@bot.command()
async def discordupdate(ctx):
    await ctx.message.delete()
    
    update_version = f"{random.randint(100, 999)}.{random.randint(10, 99)}"
    features = [
        "Redesigned user interface",
        "Enhanced voice chat quality",
        "New emoji reactions",
        "Improved server performance",
        "Advanced security features",
        "New Nitro perks",
        "Expanded server limits",
        "New message formatting options",
        "Integrated AI assistant",
        "Enhanced screen sharing"
    ]
    
    selected_features = random.sample(features, 3)
    feature_text = "\n".join([f"• {feature}" for feature in selected_features])
    
    countdown = 10
    
    discord_message = f"""
```yaml
Discord Update v{update_version}
```
**A new Discord update is available and will be installed automatically.**

**New Features:**
{feature_text}

**Update will begin in {countdown} seconds.**
Please save any unsent messages.

*Discord Client Update • Today at {datetime.datetime.now().strftime("%I:%M %p")}*
"""
    
    message = await ctx.send(discord_message)
    
    for i in range(countdown-1, -1, -1):
        await asyncio.sleep(1)
        discord_message = f"""
```yaml
Discord Update v{update_version}
```
**A new Discord update is available and will be installed automatically.**

**New Features:**
{feature_text}

**Update will begin in {i} seconds.**
Please save any unsent messages.

*Discord Client Update • Today at {datetime.datetime.now().strftime("%I:%M %p")}*
"""
        await message.edit(content=discord_message)
    
    discord_message = f"""
```yaml
Discord Update v{update_version} - Installing...
```
**Discord is now updating. The application will restart automatically when complete.**

**Progress: 0%**
`[                    ]`

*Discord Client Update • Today at {datetime.datetime.now().strftime("%I:%M %p")}*
"""
    await message.edit(content=discord_message)
    
    for i in range(5, 101, 5):
        await asyncio.sleep(1)
        progress_bar = "["
        filled = int(i/5)
        progress_bar += "=" * filled + " " * (20 - filled) + "]"
        discord_message = f"""
```yaml
Discord Update v{update_version} - Installing...
```
**Discord is now updating. The application will restart automatically when complete.**

**Progress: {i}%**
`{progress_bar}`

*Discord Client Update • Today at {datetime.datetime.now().strftime("%I:%M %p")}*
"""
        await message.edit(content=discord_message)
    
    discord_message = f"""
```diff
+ Discord Update Complete
```
**Update has been installed successfully!**

Discord will restart in a few seconds to apply changes.

*Discord Client Update • Today at {datetime.datetime.now().strftime("%I:%M %p")}*
"""
    await message.edit(content=discord_message)

@bot.command()
async def terminate(ctx, user: discord.User = None):
    await ctx.message.delete()
    
    if not user:
        user = ctx.author
    
    violations = [
        "Sending unsolicited advertisements",
        "Sharing content that violates Terms of Service",
        "Engaging in harassment or bullying",
        "Sharing illegal content",
        "Using self-bots or automated scripts",
        "Participating in raids or server attacks",
        "Creating spam accounts",
        "Selling or purchasing accounts",
        "Distributing malware or phishing links",
        "Abusing Discord's API"
    ]
    
    selected_violation = random.choice(violations)
    case_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    discord_message = f"""
```diff
- Account Termination Notice
```
**Dear {user.name},**

We're writing to inform you that your Discord account has been terminated for violating our Terms of Service and Community Guidelines.

**Violation:** {selected_violation}

**Case ID:** {case_id}

This decision is final and your account will no longer be accessible. All data associated with this account will be deleted in accordance with our Privacy Policy.

*Discord Trust & Safety Team • Today at {datetime.datetime.now().strftime("%I:%M %p")}*
"""
    
    await ctx.send(discord_message)

@bot.command()
async def raidalert(ctx):
    await ctx.message.delete()
    
    alert_messages = [
        "⚠️ **SERVER RAID IN PROGRESS** ⚠️",
        "🚨 **RAID ALERT - EMERGENCY PROTOCOLS ACTIVATED** 🚨",
        "⚠️ **SERVER UNDER ATTACK - RAID DETECTED** ⚠️",
        "🚨 **EMERGENCY: COORDINATED RAID DETECTED** 🚨",
        "⚠️ **WARNING: SERVER RAID DETECTED** ⚠️"
    ]
    
    raid_message = f"{random.choice(alert_messages)}\n\n**A coordinated raid has been detected on this server!**\n\n• **Raid bots detected:** {random.randint(15, 150)}\n• **Attack type:** {random.choice(['Spam', 'Mass mentions', 'Invite spam', 'NSFW content', 'Phishing links'])}\n• **Severity level:** {random.choice(['HIGH', 'CRITICAL', 'SEVERE'])}\n\n**Emergency protocols have been activated:**\n• Server lockdown initiated\n• Verification level increased\n• Auto-moderation enhanced\n• Raid accounts being banned\n\n**DO NOT** click any links until the raid is contained.\n\n*Discord Security System • {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    
    message = await ctx.send(raid_message)
    
    for _ in range(5):
        await asyncio.sleep(1)
        await message.edit(content=raid_message.replace("🚨", "⚠️") if "🚨" in raid_message else raid_message.replace("⚠️", "🚨"))
        raid_message = message.content

@bot.command()
async def nitroexpire(ctx, user: discord.User = None):
    await ctx.message.delete()
    
    if not user:
        user = ctx.author
    
    days_left = random.randint(1, 3)
    expiry_date = (datetime.datetime.now() + datetime.timedelta(days=days_left)).strftime("%B %d, %Y")
    
    nitro_message = f"**Discord Nitro Expiration Notice**\n\n**Hey {user.name},**\n\nYour Discord Nitro subscription is about to expire in **{days_left} days** on **{expiry_date}**.\n\nWhen your subscription ends, you'll lose access to:\n• Custom animated emojis and stickers\n• Higher quality screen sharing\n• Larger file upload limit (100MB)\n• Server boosting capabilities\n• Custom profile banner\n• Animated avatar\n• Custom tag\n\n**Don't lose your perks!** Renew your subscription now to maintain all benefits.\n\n**Renewal Options**\n• Monthly: $9.99/month\n• Yearly: $99.99/year (Save 16%)\n\n*Discord Billing • Today at {datetime.datetime.now().strftime('%I:%M %p')}*"
    
    await ctx.send(nitro_message)

@bot.command()
async def ownertransfer(ctx, user: discord.User = None):
    await ctx.message.delete()
    
    if not user:
        await ctx.send("> **[ERROR]**: Please mention a user to transfer ownership to.", delete_after=5)
        return
    
    if not ctx.guild:
        await ctx.send("> **[ERROR]**: This command can only be used in a server.", delete_after=5)
        return
    
    transfer_message = f"**Server Ownership Transfer**\n\n**Server ownership has been transferred**\n\n**Previous owner:** {ctx.author.mention}\n**New owner:** {user.mention}\n\nThis action has been logged and cannot be undone. The new owner now has full control of the server settings, permissions, and management.\n\n*Discord System • Today at {datetime.datetime.now().strftime('%I:%M %p')}*"
    
    await ctx.send(transfer_message)

@bot.command()
async def staffwarning(ctx, user: discord.User = None):
    await ctx.message.delete()
    
    if not user:
        user = ctx.author
    
    violations = [
        "Use of automated user accounts (self-bots)",
        "Distribution of unauthorized Discord modifications",
        "Facilitating transactions for prohibited services",
        "Sharing exploits or vulnerabilities",
        "Organizing or participating in raids",
        "Evading user blocks or server bans",
        "Selling or purchasing accounts or servers",
        "Excessive API abuse"
    ]
    
    selected_violation = random.choice(violations)
    case_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    discord_message = f"""
```fix
Discord Staff Warning
```
**Attention {user.name},**

Our systems have detected activity on your account that violates Discord's Terms of Service. This is an official warning from Discord Staff.

**Detected Violation:** {selected_violation}

**Case ID:** {case_id}

Continued violations may result in permanent termination of your Discord account without further notice. This warning has been logged and will remain on your account record.

*Discord Trust & Safety Team • Today at {datetime.datetime.now().strftime("%I:%M %p")}*
"""
    
    await ctx.send(discord_message)

@bot.command()
async def serverdelete(ctx):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[ERROR]**: This command can only be used in a server.", delete_after=5)
        return
    
    countdown = 10
    
    discord_message = f"""
```diff
- ⚠️ SERVER DELETION INITIATED ⚠️
```
**This server will be permanently deleted in {countdown} seconds.**

**All channels, roles, and server data will be permanently lost.**

This action was initiated by a server administrator and cannot be canceled.

*Discord System • Today at {datetime.datetime.now().strftime("%I:%M %p")}*
"""
    
    message = await ctx.send(discord_message)
    
    for i in range(countdown-1, -1, -1):
        await asyncio.sleep(1)
        discord_message = f"""
```diff
- ⚠️ SERVER DELETION INITIATED ⚠️
```
**This server will be permanently deleted in {i} seconds.**

**All channels, roles, and server data will be permanently lost.**

This action was initiated by a server administrator and cannot be canceled.

*Discord System • Today at {datetime.datetime.now().strftime("%I:%M %p")}*
"""
        await message.edit(content=discord_message)
    
    discord_message = f"""
```diff
- ⚠️ SERVER DELETION COMPLETE ⚠️
```
**This server has been scheduled for deletion.**

All members will be removed and all data will be purged from Discord's servers within the next few minutes.

Thank you for using Discord.

*Discord System • Today at {datetime.datetime.now().strftime("%I:%M %p")}*
"""
    await message.edit(content=discord_message)

@bot.command()
async def stopanimation(ctx):
    global status_animation_running
    await ctx.message.delete()
    
    if not status_animation_running:
        await ctx.send("> No status animation is currently running.", delete_after=5)
        return
    
    status_animation_running = False
    await ctx.send("> Status animation stopped.", delete_after=5)
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command()
async def fakehack(ctx, user: discord.User = None):
    await ctx.message.delete()
    
    if not user:
        await ctx.send("> **[ERROR]**: Please mention a user to hack.", delete_after=5)
        return
    
    progress_message = await ctx.send(f"```\nHacking {user.name}#{user.discriminator}...\n```")
    
    steps = [
        f"Accessing Discord servers... [▓▓░░░░░░░░] 20%",
        f"Bypassing authentication... [▓▓▓▓░░░░░░] 40%",
        f"Retrieving user data... [▓▓▓▓▓▓░░░░] 60%",
        f"Decrypting passwords... [▓▓▓▓▓▓▓▓░░] 80%",
        f"Downloading personal information... [▓▓▓▓▓▓▓▓▓▓] 100%"
    ]
    
    for step in steps:
        await asyncio.sleep(1.5)
        await progress_message.edit(content=f"```\nHacking {user.name}#{user.discriminator}...\n{step}\n```")
    
    await asyncio.sleep(1)
    
    email = f"{user.name.lower()}{random.randint(100, 999)}@{'gmail.com' if random.random() > 0.5 else 'yahoo.com'}"
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
    ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    phone = f"+1 ({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    result = f"""```
HACK COMPLETE! User: {user.name}#{user.discriminator}

[Personal Information]
Email: {email}
Password: {password}
IP Address: {ip}
Phone Number: {phone}
Discord Token: {user.id}.{''.join(random.choices(string.ascii_letters + string.digits, k=27))}

[Message History]
- "Purry Forn free without registration"
- "hot femboys kissing each other"
- "femboy meeting 2025"

[Payment Information]
Credit Card: **** **** **** {random.randint(1000, 9999)}
Expiration: {random.randint(1, 12)}/{random.randint(23, 28)}
CVV: {random.randint(100, 999)}

All data has been saved to your device.
```"""
    
    await progress_message.edit(content=result)
    
    await asyncio.sleep(3)
    await progress_message.edit(content="```\nJust kidding! This is a prank command. No actual hacking occurred.\n```")

@bot.command()
async def fakeban(ctx, user: discord.User = None, *, reason: str = "No reason provided"):
    await ctx.message.delete()
    
    if not user:
        await ctx.send("> **[ERROR]**: Please mention a user to ban.", delete_after=5)
        return
    
    if not ctx.guild:
        await ctx.send("> **[ERROR]**: This command can only be used in a server.", delete_after=5)
        return
    
    ban_message = f"**:hammer: User Banned**\n\n{user.mention} has been banned from {ctx.guild.name}.\n\n**User ID:** {user.id}\n**Moderator:** {ctx.author.mention}\n**Reason:** {reason}\n\n**Ban ID:** {''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
    
    await ctx.send(ban_message)

@bot.command()
async def fakemute(ctx, user: discord.User = None, duration: str = "1h"):
    await ctx.message.delete()
    
    if not user:
        await ctx.send("> **[ERROR]**: Please mention a user to mute.", delete_after=5)
        return
    
    if not ctx.guild:
        await ctx.send("> **[ERROR]**: This command can only be used in a server.", delete_after=5)
        return
    
    mute_message = f"**:mute: User Muted**\n\n{user.mention} has been muted for {duration}.\n\n**User ID:** {user.id}\n**Moderator:** {ctx.author.mention}\n**Duration:** {duration}\n\n**Mute expires:** {(datetime.datetime.now() + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')}"
    
    await ctx.send(mute_message)

@bot.command()
async def fakenitro(ctx):
    await ctx.message.delete()
    
    codes = [
        "discord.gift/xnHs7KBHJnA8jJAK",
        "discord.gift/PkDn7cBN9qLpJsQx",
        "discord.gift/MnB7cVqLpDkJnSx9",
        "discord.gift/BcN7VqLpDkJnSx9M"
    ]
    
    nitro_message = f"**You've been gifted a subscription!**\n\nYou've been gifted Discord Nitro for 1 Month!\n\n**Claim your gift:**\n{random.choice(codes)}\n\n*Expires in 48 hours*"
    
    await ctx.send(nitro_message)

@bot.command()
async def fakeverify(ctx, user: discord.User = None):
    await ctx.message.delete()
    
    if not user:
        user = ctx.author
    
    verify_message = f"**:white_check_mark: Account Verified**\n\n{user.mention}'s account has been successfully verified.\n\n**User ID:** {user.id}\n**Verification Level:** Level 2\n**Verification Method:** Phone Number\n\n*Discord Security • Today at {datetime.datetime.now().strftime('%I:%M %p')}*"
    
    await ctx.send(verify_message)

@bot.command()
async def fakepayment(ctx, amount: str = "9.99"):
    await ctx.message.delete()
    
    transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    payment_message = f"**:credit_card: Payment Successful**\n\nYour payment of **${amount}** has been processed successfully.\n\n**Transaction ID:** {transaction_id}\n**Payment Method:** Credit Card (****{random.randint(1000, 9999)})\n**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n*Discord Billing • Today at {datetime.datetime.now().strftime('%I:%M %p')}*"
    
    await ctx.send(payment_message)

@bot.command()
async def fakegiveaway(ctx, *, prize: str = "Discord Nitro"):
    await ctx.message.delete()
    
    duration = random.choice(["1 hour", "6 hours", "12 hours", "1 day", "3 days"])
    winners = random.randint(1, 5)
    
    giveaway_message = f"**:tada: GIVEAWAY :tada:**\n\n**{prize}**\n\nReact with :tada: to enter!\nTime remaining: **{duration}**\n\n**Hosted by:** {ctx.author.mention}\n**Winners:** {winners}\n**Ends:** <t:{int(time.time() + 3600)}:R>\n\n*Giveaway ID: {''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}*"
    
    message = await ctx.send(giveaway_message)
    await message.add_reaction("🎉")

@bot.command()
async def reload(ctx):
    await ctx.message.delete()
    
    try:
        start_script_path = os.path.join(BASE_PATH, 'start.sh')
        
        if not os.path.exists(start_script_path):
            with open(start_script_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write(f"cd {BASE_PATH}\n")
                f.write("python main.py\n")
            os.chmod(start_script_path, 0o755)
            
        subprocess.Popen(["bash", start_script_path])
        
        await ctx.send("> Reloading the bot. Please wait...", delete_after=5)
        
        await asyncio.sleep(2)
        
        await bot.close()
        sys.exit()
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while reloading: `{str(e)}`", delete_after=5)

@bot.command()
async def check(ctx):
    await ctx.message.delete()
    latest_version, update_available = check_for_updates()
    
    if latest_version is None:
        await ctx.send("> :warning: Failed to check for updates. Please try again later.", delete_after=10)
        return

    if update_available:
        message = f"""```diff
+ Update Available!
```
:rotating_light: **A new version of the SelfBot is available!** :rotating_light:

:small_orange_diamond: Current version: `v{current_version}`
:small_blue_diamond: Latest version: `v{latest_version}`

:arrow_up: To update, use the command: `.update`
:x: To dismiss this message, use: `.dismiss`

Stay up to date for the best experience!
"""
    else:
        message = f"""```diff
+ SelfBot is Up to Date!
```
:white_check_mark: **You're running the latest version of the SelfBot.**

:small_blue_diamond: Current version: `v{current_version}`

Keep enjoying the latest features!
"""

    await ctx.send(message)

async def auto_check_updates():
    while True:
        await asyncio.sleep(86400)
        latest_version, update_available = check_for_updates()
        
        if update_available:
            update_message = f"""
:rotating_light: **SelfBot Update Available!** :rotating_light:

A new version of the SelfBot is available. Would you like to update?

:small_orange_diamond: Current version: `v{current_version}`
:small_blue_diamond: Latest version: `v{latest_version}`

:arrow_up: To update, use the command: `.update`
:x: To dismiss this message, use: `.dismiss`

Stay up to date for the best experience!
"""
            print(update_message)

def update_selfbot():
    try:
        temp_update_path = os.path.join(BASE_PATH, "temp_update")
        subprocess.run(["git", "clone", "https://github.com/zeozcb/Radon.git", temp_update_path], check=True)
        
        shutil.copy2(os.path.join(BASE_PATH, "config", "config.json"), 
                     os.path.join(temp_update_path, "config", "config.json"))
        
        setup_script = os.path.join(temp_update_path, "setup.sh")
        if os.path.exists(setup_script):
            subprocess.run(["bash", setup_script], check=True)
        else:
            with open(setup_script, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("pip install -r requirements.txt\n")
            os.chmod(setup_script, 0o755)
            subprocess.run(["bash", setup_script], check=True)
        
        subprocess.Popen(["python", os.path.join(temp_update_path, "main.py")])
        
        shutil.rmtree(temp_update_path)
        
        sys.exit()
    except Exception as e:
        print(f"Update failed: {e}")

@bot.command()
async def update(ctx):
    global update_message_sent
    await ctx.message.delete()
    await ctx.send("> Starting update process...", delete_after=5)
    update_selfbot()
    update_message_sent = False

@bot.command()
async def dismiss(ctx):
    global update_message_sent, update_available
    await ctx.message.delete()
    
    if update_available:
        config['dismissed_version'] = latest_version
        save_config(config)
        update_available = False
        update_message_sent = False
        await ctx.send("> Update dismissed. You won't be notified about this version again.", delete_after=5)
    else:
        await ctx.send("> There's no pending update to dismiss.", delete_after=5)

def check_for_updates():
    try:
        response = requests.get("https://raw.githubusercontent.com/zeozcb/Radon/refs/heads/main/.ver")
        latest_version = response.text.strip()
        update_available = latest_version != current_version and latest_version != config.get('dismissed_version')
        return latest_version, update_available
    except:
        return None, False

@bot.command()
async def uptime(ctx):
    try:
        await ctx.message.delete()
    except discord.errors.NotFound:
        pass

    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."

    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)

    try:
        message = "**UPTIME INFORMATION**\n"
        message += f"Prefix: {prefix}\n\n"

        if config['uptime'].get('show_system_info', True):
            message += f"{get_emoji('computer', ':computer:')} **System Information**\n"
            message += f"OS: `{platform.system()} {platform.release()} ({platform.version()})`\n"
            message += f"Architecture: `{platform.machine()}`\n"
            message += f"Processor: `{cpuinfo.get_cpu_info()['brand_raw']}`\n"
            message += f"Python Version: `{platform.python_version()}`\n"
            message += f"Discord.py Version: `{discord.__version__}`\n\n"

        if config['uptime'].get('show_memory_usage', True):
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            message += f"{get_emoji('floppy_disk', ':floppy_disk:')} **Memory Information**\n"
            message += f"Total: `{get_size(mem.total)}`\n"
            message += f"Available: `{get_size(mem.available)}`\n"
            message += f"Used: `{get_size(mem.used)} ({mem.percent}%)`\n"
            message += f"Swap: `{get_size(swap.total)} (Used: {get_size(swap.used)})`\n\n"

        if config['uptime'].get('show_cpu_usage', True):
            message += f"{get_emoji('gear', ':gear:')} **CPU Information**\n"
            message += f"Physical Cores: `{psutil.cpu_count(logical=False)}`\n"
            message += f"Logical Cores: `{psutil.cpu_count(logical=True)}`\n"
            message += f"Max Frequency: `{psutil.cpu_freq().max:.2f}Mhz`\n"
            message += f"Current Frequency: `{psutil.cpu_freq().current:.2f}Mhz`\n"
            message += f"CPU Usage: `{psutil.cpu_percent()}%`\n\n"

        if config['uptime'].get('show_disk_usage', True):
            message += f"{get_emoji('cd', ':cd:')} **Disk Information**\n"
            partitions = psutil.disk_partitions()
            for partition in partitions:
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    message += f"Disk {partition.device}:\n"
                    message += f"  Total: `{get_size(partition_usage.total)}`\n"
                    message += f"  Used: `{get_size(partition_usage.used)} ({partition_usage.percent}%)`\n"
                except PermissionError:
                    continue
            message += "\n"

        if config['uptime'].get('show_network_info', True):
            message += f"{get_emoji('satellite', ':satellite:')} **Network Information**\n"
            if_addrs = psutil.net_if_addrs()
            for interface_name, interface_addresses in if_addrs.items():
                for addr in interface_addresses:
                    if str(addr.family) == 'AddressFamily.AF_INET':
                        message += f"{interface_name}:\n"
                        message += f"  IP Address: `{addr.address}`\n"
            message += f"Hostname: `{socket.gethostname()}`\n"
            message += f"MAC Address: `{':'.join(re.findall('..', '%012x' % uuid.getnode()))}`\n\n"

        if config['uptime'].get('show_gpu_info', True):
            message += f"{get_emoji('joystick', ':joystick:')} **GPU Information**\n"
            gpus = GPUtil.getGPUs()
            for i, gpu in enumerate(gpus):
                message += f"GPU {i}:\n"
                message += f"  Name: `{gpu.name}`\n"
                message += f"  Load: `{gpu.load*100}%`\n"
                message += f"  Memory: `{gpu.memoryUsed}MB / {gpu.memoryTotal}MB`\n"
                message += f"  Temperature: `{gpu.temperature} °C`\n"
            if not gpus:
                message += "No GPU information available\n"
            message += "\n"

        if config['uptime'].get('show_bot_info', True):
            message += f"{get_emoji('robot', ':robot:')} **Bot Information**\n"
            message += f"Bot Uptime: `{uptime_stamp}`\n"
            message += f"Guilds: `{len(bot.guilds)}`\n"
            message += f"Users: `{len(set(bot.get_all_members()))}`\n"
            message += f"Channels: `{len(set(bot.get_all_channels()))}`\n"
            message += f"Emojis: `{len(bot.emojis)}`\n"

        if config['uptime'].get('image'):
            message += f"\n\n{config['uptime']['image']}"

        await ctx.send(message)

    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while sending uptime information: {str(e)}", delete_after=10)

@bot.command()
async def uptimeconfig(ctx, setting: str = None, *, value: str = None):
    await ctx.message.delete()

    valid_settings = [
        'show_system_info', 'show_memory_usage', 'show_cpu_usage', 'show_disk_usage',
        'show_network_info', 'show_gpu_info', 'show_bot_info', 'image'
    ]

    if not setting:
        current_config = "\n".join([f"> {s}: `{config['uptime'].get(s, 'Not set')}`" for s in valid_settings])
        await ctx.send(f"**Current Uptime Configuration | Prefix: `{prefix}`**\n\n{current_config}\n\nUse `{prefix}uptimeconfig <setting> <value>` to change a setting.")
        return

    if setting not in valid_settings:
        await ctx.send(f"> **[ERROR]**: Invalid setting. Valid settings are: {', '.join(valid_settings)}", delete_after=5)
        return

    if not value:
        await ctx.send(f"> **[ERROR]**: You must provide a value for the setting.", delete_after=5)
        return

    if setting != 'image':
        if value.lower() not in ['true', 'false']:
            await ctx.send("> **[ERROR]**: Value must be 'true' or 'false' for boolean settings.", delete_after=5)
            return
        config['uptime'][setting] = value.lower() == 'true'
    else:
        config['uptime']['image'] = value

    save_config(config)
    await ctx.send(f"> Uptime configuration updated. Setting '{setting}' set to '{value}'.", delete_after=5)

@bot.command()
async def ping(ctx):
    await ctx.message.delete()

    before = time.monotonic()
    message_to_send = await ctx.send("Pinging...")

    await message_to_send.edit(content=f"`{int((time.monotonic() - before) * 1000)} ms`")

@bot.command(aliases=['social'])
async def media(ctx):
    await ctx.message.delete()

    if not any(platform['link'] for platform in config['social_media'].values()):
        message = f"""```yaml
SOCIAL MEDIA CONFIGURATION | Prefix: {prefix}
```

To configure your social media links, use the following command:
`{prefix}setsocial <platform> <emoji> <text> <link>`

Available platforms: discord, github, twitter, instagram, youtube

Example:
`{prefix}setsocial discord :pager: Discord Server https://discord.gg/yourserver`

Current configuration:
"""
        for platform, data in config['social_media'].items():
            message += f"> {data['emoji']} `{platform}`: {data['text']} - {data['link'] or 'Not configured'}\n"

    else:
        message = f"""```yaml
MY SOCIAL NETWORKS | Prefix: {prefix}
```
"""
        for platform, data in config['social_media'].items():
            if data['link']:
                message += f"> {data['emoji']} [{data['text']}]({data['link']})\n"

    await ctx.send(message)

@bot.command()
async def setsocial(ctx, platform: str, emoji: str, text: str, link: str):
    await ctx.message.delete()

    if platform not in config['social_media']:
        await ctx.send(f"> **[ERROR]**: Invalid platform. Available platforms: {', '.join(config['social_media'].keys())}", delete_after=5)
        return

    config['social_media'][platform] = {
        "emoji": emoji,
        "text": text,
        "link": link
    }
    save_config(config)

    await ctx.send(f"> Social media link for {platform} has been updated.", delete_after=5)

@bot.command()
async def geoip(ctx, ip: str=None):
    await ctx.message.delete()

    if not ip:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `geoip <ip>`", delete_after=5)
        return

    try:
        r = requests.get(f'http://ip-api.com/json/{ip}')
        geo = r.json()
        message = f"""```yaml
GEOLOCATE IP | Prefix: {prefix}
```

> :pushpin: `IP`
*{geo['query']}*
> :globe_with_meridians: `Country-Region`
*{geo['country']} - {geo['regionName']}*
> :department_store: `City`
*{geo['city']} ({geo['zip']})*
> :map: `Latitute-Longitude`
*{geo['lat']} - {geo['lon']}*
> :satellite: `ISP`
*{geo['isp']}*
> :robot: `Org`
*{geo['org']}*
> :alarm_clock: `Timezone`
*{geo['timezone']}*
> :electric_plug: `As`
*{geo['as']}*"""
        await ctx.send(message)
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to geolocate ip\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command()
async def tts(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `tts <message>`", delete_after=5)
        return

    content = content.strip()

    tts = gTTS(text=content, lang="en")
    
    f = io.BytesIO()
    tts.write_to_fp(f)
    f.seek(0)

    await ctx.send(file=discord.File(f, f"{content[:10]}.wav"))

@bot.command(aliases=['qrcode'])
async def qr(ctx, *, text: str="https://discord.gg/PKR7nM9j9U"):
    qr = qrcode.make(text)
    
    img_byte_arr = io.BytesIO()
    qr.save(img_byte_arr)
    img_byte_arr.seek(0)

    await ctx.send(file=discord.File(img_byte_arr, "qr_code.png"))

@bot.command()
async def pingweb(ctx, website_url: str=None):
    await ctx.message.delete()

    if not website_url:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `pingweb <url>`", delete_after=5)
        return

    try:
        r = requests.get(website_url).status_code
        if r == 404:
            await ctx.send(f'> Website **down** *({r})*')
        else:
            await ctx.send(f'> Website **operational** *({r})*')
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to ping website\n> __Error__: `{str(e)}`', delete_after=5)

@bot.command()
async def gentoken(ctx, user: str=None):
    await ctx.message.delete()

    code = "ODA"+random.choice(string.ascii_letters)+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))+"."+random.choice(string.ascii_letters).upper()+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))+"."+''.join(random.choice(string.ascii_letters + string.digits) for _ in range(27))
    
    if not user:
        await ctx.send(''.join(code))
    else:
        await ctx.send(f"> {user}'s token is: ||{''.join(code)}||")

@bot.command()
async def quickdelete(ctx, *, message: str=None):
    await ctx.message.delete()
    
    if not message:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `quickdelete <message>`', delete_after=2)
        return
        
    await ctx.send(message, delete_after=2)

@bot.command(aliases=['uicon'])
async def usericon(ctx, user: discord.User = None):
    await ctx.message.delete()

    if not user:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `usericon <@user>`', delete_after=5)
        return
    
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    await ctx.send(f"> {user.mention}'s avatar:\n{avatar_url}")

@bot.command(aliases=['tinfo'])
async def tokeninfo(ctx, usertoken: str=None):
    await ctx.message.delete()

    if not usertoken:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `tokeninfo <token>`', delete_after=5)
        return

    headers = {'Authorization': usertoken, 'Content-Type': 'application/json'}
    languages = {
        'da': 'Danish, Denmark',
        'de': 'German, Germany',
        'en-GB': 'English, United Kingdom',
        'en-US': 'English, United States',
        'es-ES': 'Spanish, Spain',
        'fr': 'French, France',
        'hr': 'Croatian, Croatia',
        'lt': 'Lithuanian, Lithuania',
        'hu': 'Hungarian, Hungary',
        'nl': 'Dutch, Netherlands',
        'no': 'Norwegian, Norway',
        'pl': 'Polish, Poland',
        'pt-BR': 'Portuguese, Brazilian, Brazil',
        'ro': 'Romanian, Romania',
        'fi': 'Finnish, Finland',
        'sv-SE': 'Swedish, Sweden',
        'vi': 'Vietnamese, Vietnam',
        'tr': 'Turkish, Turkey',
        'cs': 'Czech, Czechia, Czech Republic',
        'el': 'Greek, Greece',
        'bg': 'Bulgarian, Bulgaria',
        'ru': 'Russian, Russia',
        'uk': 'Ukrainian, Ukraine',
        'th': 'Thai, Thailand',
        'zh-CN': 'Chinese, China',
        'ja': 'Japanese',
        'zh-TW': 'Chinese, Taiwan',
        'ko': 'Korean, Korea'
    }

    try:
        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: An error occurred while sending request\n> __Error__: `{str(e)}`', delete_after=5)
        return

    if res.status_code == 200:
        res_json = res.json()
        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
        user_id = res_json['id']
        avatar_id = res_json['avatar']
        avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif'
        phone_number = res_json['phone']
        email = res_json['email']
        mfa_enabled = res_json['mfa_enabled']
        flags = res_json['flags']
        locale = res_json['locale']
        verified = res_json['verified']
        days_left = ""
        language = languages.get(locale)
        creation_date = datetime.datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')
        has_nitro = False

        try:
            nitro_res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
            nitro_res.raise_for_status()
            nitro_data = nitro_res.json()
            has_nitro = bool(len(nitro_data) > 0)
            if has_nitro:
                d1 = datetime.datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                d2 = datetime.datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                days_left = abs((d2 - d1).days)
        except requests.exceptions.RequestException as e:
            pass

        try:
            message = f"""```ini
[TOKEN INFORMATIONS | Prefix: {prefix}]
```

> :dividers: __Basic Information__
Username: `{user_name}`
User ID: `{user_id}`
Creation Date: `{creation_date}`
Avatar URL: `{avatar_url if avatar_id else "None"}`

> :crystal_ball: __Nitro Information__
Nitro Status: `{has_nitro}`
Expires in: `{days_left if days_left else "None"} day(s)`

> :incoming_envelope: __Contact Information__
Phone Number: `{phone_number if phone_number else "None"}`
Email: `{email if email else "None"}`

> :shield: __Account Security__
2FA/MFA Enabled: `{mfa_enabled}`
Flags: `{flags}`

> :paperclip: __Other__
Locale: `{locale} ({language})`
Email Verified: `{verified}`"""

            await ctx.send(message)
        except Exception as e:
            await ctx.send(f'> **[**ERROR**]**: Unable to recover token infos\n> __Error__: `{str(e)}`', delete_after=5)
    else:
        await ctx.send(f'> **[**ERROR**]**: Unable to recover token infos\n> __Error__: Invalid token', delete_after=5)

@bot.command(aliases=['ginfo'])
async def guildinfo(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    date_format = "%a, %d %b %Y %I:%M %p"
    message = f"""```ini
[GUILD INFORMATIONS | Prefix: {prefix}]
```

:dividers: __Basic Information__
Server Name: `{ctx.guild.name}`
Server ID: `{ctx.guild.id}`
Creation Date: `{ctx.guild.created_at.strftime(date_format)}`
Server Icon: `{ctx.guild.icon.url if ctx.guild.icon else 'None'}`
Server Owner: `{ctx.guild.owner}`

:page_facing_up: __Other Information__
`{len(ctx.guild.members)}` Members
`{len(ctx.guild.roles)}` Roles
`{len(ctx.guild.text_channels) if ctx.guild.text_channels else 'None'}` Text-Channels
`{len(ctx.guild.voice_channels) if ctx.guild.voice_channels else 'None'}` Voice-Channels
`{len(ctx.guild.categories) if ctx.guild.categories else 'None'}` Categories"""
    
    await ctx.send(message)

@bot.command()
async def nitrogen(ctx):
    await ctx.message.delete()

    await ctx.send(f"https://discord.gift/{''.join(random.choices(string.ascii_letters + string.digits, k=16))}")

@bot.command()
async def whremove(ctx, webhook: str=None):
    await ctx.message.delete()

    if not webhook:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}whremove <webhook>`', delete_after=5)
        return
    
    try:
        requests.delete(webhook.rstrip())
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to delete webhook\n> __Error__: `{str(e)}`', delete_after=5)
        return
    
    await ctx.send(f'> Webhook has been deleted!')

@bot.command(aliases=['hide'])
async def hidemention(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}hidemention <message>`', delete_after=5)
        return
    
    await ctx.send(content + ('||\u200b||' * 200) + '@everyone')

@bot.command()
async def edit(ctx, *, content: str=None):
    await ctx.message.delete()
    
    if not content:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `{prefix}edit <message>`', delete_after=5)
        return
    
    text = await ctx.send(content)

    await text.edit(content=f"\u202b{content}")

@bot.command(aliases=['911'])
async def airplane(ctx, mode: str = "ONE"):
    global loop_running
    await safe_delete(ctx.message)

    frames = [
        f''':man_wearing_turban::airplane:\t\t\t\t:office:''',
        f''':man_wearing_turban:\t:airplane:\t\t\t:office:''',
        f''':man_wearing_turban:\t\t:airplane:\t\t:office:''',
        f''':man_wearing_turban:\t\t\t:airplane:\t:office:''',
        f''':man_wearing_turban:\t\t\t\t:airplane::office:''',
        ''':boom::boom::boom:'''
    ]
    
    try:
        sent_message = await ctx.send(frames[0])

        if mode.upper() == "LOOP":
            loop_running = True
            while loop_running:
                for frame in frames:
                    if not loop_running:
                        break
                    await asyncio.sleep(0.2)
                    await sent_message.edit(content=frame)
        elif mode.upper() == "ONE":
            for frame in frames:
                await asyncio.sleep(0.5)
                await sent_message.edit(content=frame)
        else:
            await ctx.send("> **[ERROR]**: Invalid mode. Use 'LOOP' or 'ONE'.", delete_after=5)
    except discord.errors.NotFound:
        loop_running = False

@bot.command(aliases=['kitty'])
async def catplay(ctx, mode: str = "ONE"):
    global loop_running
    await ctx.message.delete()

    frames = [
        "ฅ^•ﻌ•^ฅ",
        "ฅ^≧◡≦^ฅ",
        "ฅ^•ω•^ฅ",
        "ฅ^ω^ฅ",
        "ฅ^•ﻌ•^ฅ ♪",
        "ฅ^≧◡≦^ฅ ♫",
        "ฅ^•ω•^ฅ ♪♫",
        "ฅ^ω^ฅ ♫♪"
    ]
    
    sent_message = await ctx.send(frames[0])

    if mode.upper() == "LOOP":
        loop_running = True
        while loop_running:
            for frame in frames:
                if not loop_running:
                    break
                await asyncio.sleep(0.2)
                await sent_message.edit(content=frame)
    elif mode.upper() == "ONE":
        for frame in frames:
            await asyncio.sleep(0.8)
            await sent_message.edit(content=frame)
    else:
        await ctx.send("> **[ERROR]**: Invalid mode. Use 'LOOP' or 'ONE'.", delete_after=5)

@bot.command()
async def animatestatus(ctx, frame_time: float = None, *, frames: str = None):
    global status_animation_running
    await ctx.message.delete()

    if status_animation_running:
        await ctx.send("> An animation is already running. Use `.stopanimation` to stop it first.", delete_after=5)
        return

    if frame_time is None or frames is None:
        help_message = f"""
**Animate Status Command | Prefix: `{prefix}`**

Usage: `{prefix}animatestatus <frame_time> <frame1>|<frame2>|<frame3>...`

Parameters:
• `frame_time`: Time in seconds between each frame (e.g., 2.0)
• `frames`: Status messages separated by `|`

Example:
`{prefix}animatestatus 2.0 Hello|World|Discord|SelfBot`

This will change your status every 2 seconds between "Hello", "World", "Discord", and "SelfBot".

To stop the animation, use: `{prefix}stopanimation`
"""
        await ctx.send(help_message, delete_after=30)
        return

    if not frames:
        await ctx.send(f"> **[ERROR]**: Invalid command.\n> __Command__: `{prefix}animatestatus <frame_time> <frame1>|<frame2>|<frame3>...`", delete_after=5)
        return

    frame_list = frames.split('|')
    if len(frame_list) < 2:
        await ctx.send(f"> **[ERROR]**: Please provide at least two frames separated by '|'.", delete_after=5)
        return

    status_animation_running = True
    await ctx.send(f"> Status animation started with {len(frame_list)} frames and {frame_time} seconds per frame.", delete_after=5)

    while status_animation_running:
        for frame in frame_list:
            if not status_animation_running:
                break
            await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=frame))
            await asyncio.sleep(frame_time)

    await bot.change_presence(status=discord.Status.online, activity=None)  

@bot.command(aliases=['8ball'])
async def magicball(ctx, *, question: str = None):
    await ctx.message.delete()
    
    if not question:
        await ctx.send("> **[ERROR]**: Please ask a question.\n> __Command__: `8ball <question>`", delete_after=5)
        return
    
    responses = [
        "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
        "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
        "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
        "Don't count on it.", "My reply is no.", "My sources say no.",
        "Outlook not so good.", "Very doubtful."
    ]
    
    response = random.choice(responses)
    await ctx.send(f"> **Question:** {question}\n> **Magic 8-Ball says:** {response}")

@bot.command(aliases=['flip', 'coin'])
async def coinflip(ctx):
    await ctx.message.delete()
    
    result = random.choice(['Heads', 'Tails'])
    await ctx.send(f"> The coin landed on: **{result}**!")

@bot.command(aliases=['dice'])
async def roll(ctx, dice: str = "1d6"):
    await ctx.message.delete()
    
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send("> **[ERROR]**: Format has to be in NdN!\n> __Example__: `roll 3d6`", delete_after=5)
        return

    results = [random.randint(1, limit) for _ in range(rolls)]
    await ctx.send(f"> 🎲 Rolling {dice}:\n> Results: {', '.join(map(str, results))}\n> Total: {sum(results)}")

@bot.command()
async def emojify(ctx, *, text: str):
    await ctx.message.delete()
    
    emojis = {
        'a': '🅰️', 'b': '🅱️', 'c': '©️', 'd': '🇩', 'e': '3️⃣', 'f': '🎏',
        'g': '🇬', 'h': '♓', 'i': 'ℹ️', 'j': '🗾', 'k': '🇰', 'l': '🇱',
        'm': 'Ⓜ️', 'n': '🇳', 'o': '🅾️', 'p': '🅿️', 'q': '🇶', 'r': '®️',
        's': '💲', 't': '✝️', 'u': '⛎', 'v': '♈', 'w': '〰️', 'x': '❌',
        'y': '🌱', 'z': '💤'
    }
    
    emojified = ''.join(emojis.get(char.lower(), char) for char in text)
    await ctx.send(emojified)

@bot.command()
async def mock(ctx, *, text: str):
    await ctx.message.delete()
    
    mocked = ''.join(char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(text))
    await ctx.send(f"{mocked} 🥴")

@bot.command()
async def uwuify(ctx, *, text: str):
    await ctx.message.delete()
    
    uwu_text = text.replace('r', 'w').replace('l', 'w').replace('R', 'W').replace('L', 'W')
    uwu_text = uwu_text.replace('th', 'd').replace('Th', 'D')
    uwu_text += " " + random.choice(["uwu", "owo", ">w<", "^w^"])
    
    await ctx.send(uwu_text)

@bot.command()
async def retardify(ctx, *, text: str):
    await ctx.message.delete()
    
    retardified = ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))
    retardified = retardified.replace('l', 'w').replace('r', 'w')
    
    await ctx.send(f"{retardified} 🥴")

@bot.command()
async def femboyify(ctx, *, text: str):
    await ctx.message.delete()
    
    femboy_prefixes = ["uwu", "owo", ">w<", "^-^", "nya~"]
    femboy_suffixes = ["❤️", "💖", "🌸", "✨", "🎀"]
    
    femboyified = text.lower()
    femboyified = femboyified.replace('r', 'w').replace('l', 'w')
    femboyified = femboyified.replace('th', 'd')
    femboyified = f"{random.choice(femboy_prefixes)} {femboyified} {random.choice(femboy_suffixes)}"
    
    await ctx.send(femboyified)

@bot.command()
async def ghostping(ctx, user: discord.User):
    await ctx.message.delete()
    
    message = await ctx.send(f"{user.mention}")
    await asyncio.sleep(0.1)
    await message.delete()

@bot.command()
async def loopstop(ctx):
    global loop_running
    await ctx.message.delete()
    
    if loop_running:
        loop_running = False
        await ctx.send("> Animation loop stopped.", delete_after=5)
    else:
        await ctx.send("> No animation loop is currently running.", delete_after=5)

@bot.command(aliases=['doxx', 'userinfo'])
async def dox(ctx, username: str = None):
    await ctx.message.delete()

    if not username:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `dox <username>`", delete_after=5)
        return

    message = f"""```css
[DOX INFORMATION | Prefix: {prefix}]
```

> :mag: __Potential Social Media Profiles__
"""

    platforms = [
        ("Instagram", f"https://www.instagram.com/{username}/"),
        ("Twitter", f"https://twitter.com/{username}"),
        ("Facebook", f"https://www.facebook.com/{username}"),
        ("LinkedIn", f"https://www.linkedin.com/in/{username}/"),
        ("GitHub", f"https://github.com/{username}"),
        ("YouTube", f"https://www.youtube.com/user/{username}"),
        ("Twitch", f"https://www.twitch.tv/{username}"),
        ("Reddit", f"https://www.reddit.com/user/{username}")
    ]

    for platform, url in platforms:
        message += f"• {platform}: `{url}`\n"

    message += f"""\n> :globe_with_meridians: __Other Potential Information__
• Personal Website: `http://{username}.com`
• Email: `{username}@gmail.com`
• Possible Usernames: `{username}`, `{username}_`, `_{username}`, `{username}123`

> :warning: __Disclaimer__
This information is speculative and may not be accurate. It's based solely on the provided username. Always respect privacy and use this information responsibly."""

    await ctx.send(message)

@bot.command(aliases=['mine'])
async def minesweeper(ctx, size: int=5):
    await ctx.message.delete()

    size = max(min(size, 8), 2)
    bombs = [[random.randint(0, size - 1), random.randint(0, size - 1)] for _ in range(size - 1)]
    is_on_board = lambda x, y: 0 <= x < size and 0 <= y < size
    has_bomb = lambda x, y: [i for i in bombs if i[0] == x and i[1] == y]
    m_numbers = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]
    m_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    message_to_send = "**Click to play**:\n"

    for y in range(size):
        for x in range(size):
            tile = "||{}||".format(chr(11036))
            if has_bomb(x, y):
                tile = "||{}||".format(chr(128163))
            else:
                count = 0
                for xmod, ymod in m_offsets:
                    if is_on_board(x + xmod, y + ymod) and has_bomb(x + xmod, y + ymod):
                        count += 1
                if count != 0:
                    tile = "||{}||".format(m_numbers[count - 1])
            message_to_send += tile
        message_to_send += "\n"

    await ctx.send(message_to_send)

@bot.command(aliases=['leet'])
async def leetspeak(ctx, *, content: str):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `leetspeak <message>`", delete_after=5)
        return

    content = content.replace('a', '4').replace('A', '4').replace('e', '3').replace('E', '3').replace('i', '1').replace('I', '1').replace('o', '0').replace('O', '0').replace('t', '7').replace('T', '7').replace('b', '8').replace('B', '8')
    await ctx.send(content)

@bot.command()
async def dick(ctx, user: str=None):
    await ctx.message.delete()

    if not user:
        user = ctx.author.display_name

    size = random.randint(1, 15)
    dong = "=" * size

    await ctx.send(f"> **{user}**'s Dick size\n8{dong}D")

@bot.command()
async def zeo(ctx):
    await ctx.message.delete()
    
    gif_link = "https://cdn.discordapp.com/attachments/759677090085208086/1200480224819826809/standard.gif?ex=67fde315&is=67fc9195&hm=fc83d3d42bb9066a13e7f0a98c7f0ff6c8ceae9d6d974e0452f316b32747797a&"
    
    await ctx.send(gif_link)

@bot.command()
async def exec(ctx, *, code: str):
    await ctx.message.delete()

    if not code:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `exec <python_code>`", delete_after=5)
        return

    str_obj = io.StringIO()

    try:
        with contextlib.redirect_stdout(str_obj):
            exec_result = eval(code)
            if inspect.isawaitable(exec_result):
                exec_result = await exec_result

        output = str_obj.getvalue()

        if output or exec_result:
            await ctx.send(f"```py\n{output}\n{exec_result}\n```")
        else:
            await ctx.send("> Code executed successfully, but there was no output.")
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while executing the code:\n```py\n{str(e)}\n```")
    finally:
        str_obj.close()

@bot.command()
async def reverse(ctx, *, content: str=None):
    await ctx.message.delete()

    if not content:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `reverse <message>`", delete_after=5)
        return

    content = content[::-1]
    await ctx.send(content)

@bot.command(aliases=['fetch'])
async def fetchmembers(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(f'> **[**ERROR**]**: This command can only be used in a server.', delete_after=5)
        return
    
    members = ctx.guild.members
    member_data = []

    for member in members:
        member_info = {
            "name": member.name,
            "id": str(member.id),
            "avatar_url": str(member.avatar.url) if member.avatar else str(member.default_avatar.url),
            "discriminator": member.discriminator,
            "status": str(member.status),
            "joined_at": str(member.joined_at)
        }
        member_data.append(member_info)

    with open("members_list.json", "w", encoding="utf-8") as f:
        json.dump(member_data, f, indent=4)

    await ctx.send("> List of members:", file=discord.File("members_list.json"))

    os.remove("members_list.json")

@bot.command()
async def spam(ctx, amount: int=1, *, message_to_send: str="https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()

    try:
        if amount <= 0 or amount > 50:
            await ctx.send("> **[**ERROR**]**: Amount must be between 1 and 50", delete_after=5)
            return
        
        status_msg = await ctx.send(f"> Sending {amount} messages... Please wait.")
        
        sent_count = 0
        for i in range(amount):
            try:
                await ctx.send(message_to_send)
                sent_count += 1
                
                if (i + 1) % 5 == 0:
                    await status_msg.edit(content=f"> Progress: {i+1}/{amount} messages sent")
                
                if amount <= 10:
                    await asyncio.sleep(0.5)
                elif amount <= 25:
                    await asyncio.sleep(random.uniform(0.7, 1.2))
                else:
                    await asyncio.sleep(random.uniform(1.0, 1.5))
                    
            except discord.errors.HTTPException as e:
                if e.code == 429:
                    retry_after = e.retry_after
                    await status_msg.edit(content=f"> Rate limited! Waiting {retry_after:.2f}s before continuing... ({i+1}/{amount})")
                    await asyncio.sleep(retry_after + 0.5)
                else:
                    await status_msg.edit(content=f"> Error sending message {i+1}: {str(e)}")
                    await asyncio.sleep(1)
        
        await status_msg.edit(content=f"> Successfully sent {sent_count}/{amount} messages.")
        await asyncio.sleep(3)
        await status_msg.delete()
        
    except ValueError:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `spam <amount> <message>`', delete_after=5)
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: An unexpected error occurred: {str(e)}', delete_after=5)

@bot.command(aliases=['gicon'])
async def guildicon(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    await ctx.send(f"> **{ctx.guild.name} icon :**\n{ctx.guild.icon.url if ctx.guild.icon else '*NO ICON*'}")

@bot.command(aliases=['gbanner'])
async def guildbanner(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    await ctx.send(f"> **{ctx.guild.name} banner :**\n{ctx.guild.banner.url if ctx.guild.banner else '*NO BANNER*'}")

@bot.command(aliases=['grename'])
async def guildrename(ctx, *, name: str=None):
    await ctx.message.delete()

    if not name:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `guildrename <name>`", delete_after=5)
        return

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.guild.me.guild_permissions.manage_guild:
        await ctx.send(f'> **[**ERROR**]**: Missing permissions', delete_after=5)
        return
    
    try:
        await ctx.guild.edit(name=name)
        await ctx.send(f"> Server renamed to '{name}'")
    except Exception as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to rename the server\n> __Error__: `{str(e)}`, delete_after=5')

@bot.command()
async def purge(ctx, num_messages: int=1):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("> **[**ERROR**]**: You do not have permission to delete messages", delete_after=5)
        return
    
    if 1 <= num_messages <= 100:
        deleted_messages = await ctx.channel.purge(limit=num_messages)
        await ctx.send(f"> **{len(deleted_messages)}** messages have been deleted", delete_after=5)
    else:
        await ctx.send("> **[**ERROR**]**: The number must be between 1 and 100", delete_after=5)

@bot.command(aliases=['song', 'track'])
async def lyrics(ctx, *, query: str):
    await ctx.message.delete()

    if not query:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `lyrics <song name or lyrics>`", delete_after=5)
        return

    try:
        song = genius.search_song(query)
        if song:
            title = song.title
            artist = song.artist

            spotify_link = None
            for annotation in song.song_art_image_thumbnail_url:
                if 'open.spotify.com' in annotation:
                    spotify_link = annotation
                    break

            youtube_link = f"https://www.youtube.com/results?search_query={title.replace(' ', '+')}+{artist.replace(' ', '+')}"

            message = f"> **{title}** by **{artist}**\n> Genius: {song.url}\n> Spotify: {spotify_link if spotify_link else 'Not found'}\n> YouTube Search: {youtube_link}\n\n# :warning: Note that this function is in BETA and may work bad"
            await ctx.send(message)
        else:
            await ctx.send("> **[ERROR]**: No lyrics found for this query.", delete_after=5)
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while fetching lyrics. `{e}`", delete_after=5)

@bot.command(aliases=['autor'])
async def autoreply(ctx, command: str, user: discord.User=None):
    await ctx.message.delete()

    if command not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid input. Use `ON` or `OFF`.\n> __Command__: `autoreply ON|OFF [@user]`", delete_after=5)
        return

    if command.upper() == "ON":
        if user:
            if str(user.id) not in config["autoreply"]["users"]:
                config["autoreply"]["users"].append(str(user.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(f"> **Autoreply enabled for user {user.mention}.**", delete_after=5)
        else:
            if str(ctx.channel.id) not in config["autoreply"]["channels"]:
                config["autoreply"]["channels"].append(str(ctx.channel.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send("> **Autoreply has been enabled in this channel**", delete_after=5)
    elif command.upper() == "OFF":
        if user:
            if str(user.id) in config["autoreply"]["users"]:
                config["autoreply"]["users"].remove(str(user.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send(f"> **Autoreply disabled for user {user.mention}**", delete_after=5)
        else:
            if str(ctx.channel.id) in config["autoreply"]["channels"]:
                config["autoreply"]["channels"].remove(str(ctx.channel.id))
                save_config(config)
                selfbot_menu(bot)
            await ctx.send("> **Autoreply has been disabled in this channel**", delete_after=5)

@bot.command(aliases=['remote'])
async def remoteuser(ctx, action: str, users: discord.User=None):
    await ctx.message.delete()

    if not users:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `remoteuser ADD|REMOVE <@user(s)>`", delete_after=5)
        return

    if action not in ["ADD", "REMOVE"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ADD` or `REMOVE`.\n> __Command__: `remoteuser ADD|REMOVE <@user(s)>`", delete_after=5)
        return
    
    if action.upper() == "ADD":
        for user in users:
            if str(user.id) not in config["remote-users"]:
                config["remote-users"].append(str(user.id))

        save_config(config)
        selfbot_menu(bot)

        await ctx.send(f"> **Success**: {len(users)} user(s) added to remote-users", delete_after=5)
    elif action.upper() == "REMOVE":
        for user in users:
            if str(user.id) in config["remote-users"]:
                config["remote-users"].remove(str(user.id))

        save_config(config)
        selfbot_menu(bot)

        await ctx.send(f"> **Success**: {len(users)} user(s) removed from remote-users", delete_after=5)

@bot.command()
async def afk(ctx, status: str, *, message: str=None):
    await ctx.message.delete()

    if status not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `afk ON|OFF <message>`", delete_after=5)
        return

    if status.upper() == "ON":
        if not config["afk"]["enabled"]:
            config["afk"]["enabled"] = True
            if message:
                config["afk"]["message"] = message
            save_config(config)
            selfbot_menu(bot)
            await ctx.send(f"> **AFK mode enabled.** Message: `{config['afk']['message']}`", delete_after=5)
        else:
            await ctx.send("> **[**ERROR**]**: AFK mode is already enabled", delete_after=5)
    elif status.upper() == "OFF":
        if config["afk"]["enabled"]:
            config["afk"]["enabled"] = False
            save_config(config)
            selfbot_menu(bot)
            await ctx.send("> **AFK mode disabled.** Welcome back!", delete_after=5)
        else:
            await ctx.send("> **[**ERROR**]**: AFK mode is not currently enabled", delete_after=5)

@bot.command(aliases=["prefix"])
async def changeprefix(ctx, *, new_prefix: str=None):
    await ctx.message.delete()

    if not new_prefix:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `changeprefix <prefix>`", delete_after=5)
        return
    
    if "tokens" in config and len(config["tokens"]) > 0:
        config["tokens"][0]["prefix"] = new_prefix
    save_config(config)
    selfbot_menu(bot)
    
    bot.command_prefix = new_prefix

    await ctx.send(f"> Prefix updated to `{new_prefix}`", delete_after=5)

@bot.command(aliases=["logout"])
async def shutdown(ctx):
    await ctx.message.delete()

    msg = await ctx.send("> Shutting down...")
    await asyncio.sleep(2)

    await msg.delete()
    await bot.close()

@bot.command()
async def clear(ctx):
    await ctx.message.delete()

    await ctx.send('ﾠﾠ' + '\n' * 200 + 'ﾠﾠ')

@bot.command()
async def sendall(ctx, *, message="https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return
    
    channels = ctx.guild.text_channels
    success_count = 0
    failure_count = 0
    
    try:        
        for channel in channels:
            try:
                await channel.send(message)
                success_count += 1
            except Exception as e:
                failure_count += 1
        await ctx.send(f"> {success_count} message(s) sent successfully, {failure_count} failed to send", delete_after=5)
    except Exception as e:
        await ctx.send(f"> **[**ERROR**]**: An error occurred: `{e}`", delete_after=5)

@bot.command(aliases=["copycatuser", "copyuser"])
async def copycat(ctx, action: str=None, user: discord.User=None):
    await ctx.message.delete()
    
    if action not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `copycat ON|OFF <@user>`", delete_after=5)
        return
    
    if not user:
        await ctx.send(f"> **[**ERROR**]**: Please specify a user to copy.\n> __Command__: `copycat ON|OFF <@user>`", delete_after=5)
        return
    
    if action == "ON":
        if user.id not in config['copycat']['users']:
            config['copycat']['users'].append(user.id)
            save_config(config)
            await ctx.send(f"> Now copying `{str(user)}`", delete_after=5)
        else:
            await ctx.send(f"> `{str(user)}` is already being copied.", delete_after=5)
    
    elif action == "OFF":
        if user.id in config['copycat']['users']:
            config['copycat']['users'].remove(user.id)
            save_config(config)
            await ctx.send(f"> Stopped copying `{str(user)}`", delete_after=5)
        else:
            await ctx.send(f"> `{str(user)}` was not being copied.", delete_after=5)

@bot.command()
async def firstmessage(ctx):
    await ctx.message.delete()
    
    try:
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            link = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message.id}"
            await ctx.send(f"> Here is the link to the first message: {link}", delete_after=5)
            break
        else:
            await ctx.send("> **[ERROR]**: No messages found in this channel.", delete_after=5)
    
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while fetching the first message. `{e}`", delete_after=5)

@bot.command()
async def ascii(ctx, *, message: str=None):
    await ctx.message.delete()
    
    if not message:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `ascii <message>`", delete_after=5)
        return
    
    try:
        ascii_art = pyfiglet.figlet_format(message)
        await ctx.send(f"```\n{ascii_art}\n```", delete_after=5)
    except Exception as e:
        await ctx.send(f"> **[ERROR]**: An error occurred while generating the ASCII art. `{e}`", delete_after=5)

@bot.command()
async def advertise(ctx, *, message: str = None):
    await ctx.message.delete()
    
    if not message:
        await ctx.send("> **[ERROR]**: Please provide a message to advertise.\n> __Command__: `advertise <message>`", delete_after=5)
        return
        
    target_channels = ['public-games', 'public-condos']
    success_count = 0
    fail_count = 0
    
    min_delay = config['advertise_delay']['min']
    max_delay = config['advertise_delay']['max']
    
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if any(target in channel.name.lower() for target in target_channels):
                try:
                    await channel.send(message)
                    success_count += 1
                    await asyncio.sleep(random.uniform(min_delay, max_delay))
                except Exception:
                    fail_count += 1
                    continue
    
    status_msg = f"> Advertisement sent to {success_count} channels (Failed: {fail_count})"
    await ctx.send(status_msg, delete_after=5)

@bot.command()
async def setdelay(ctx, min_delay: float = None, max_delay: float = None):
    await ctx.message.delete()
    
    if min_delay is None or max_delay is None:
        current_min = config['advertise_delay']['min']
        current_max = config['advertise_delay']['max']
        await ctx.send(f"> Current advertise delay: `{current_min}s - {current_max}s`\n> To change: `{prefix}setdelay <min_seconds> <max_seconds>`", delete_after=5)
        return
        
    if min_delay < 0 or max_delay < 0:
        await ctx.send("> **[ERROR]**: Delay values cannot be negative.", delete_after=5)
        return
        
    if min_delay > max_delay:
        await ctx.send("> **[ERROR]**: Minimum delay cannot be greater than maximum delay.", delete_after=5)
        return
        
    config['advertise_delay']['min'] = min_delay
    config['advertise_delay']['max'] = max_delay
    save_config(config)
    
    await ctx.send(f"> Advertise delay set to: `{min_delay}s - {max_delay}s`", delete_after=5)

@bot.command()
async def playing(ctx, *, status: str=None):
    await ctx.message.delete()

    if not status:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `playing <status>`", delete_after=5)
        return
    
    await bot.change_presence(activity=discord.Game(name=status))
    await ctx.send(f"> Successfully set the game status to `{status}`", delete_after=5)

@bot.command()
async def streaming(ctx, *, status: str=None):
    await ctx.message.delete()

    if not status:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `streaming <status>`", delete_after=5)
        return
    
    await bot.change_presence(activity=discord.Streaming(name=status, url=f"https://www.twitch.tv/{status}"))
    await ctx.send(f"> Successfully set the streaming status to `{status}`", delete_after=5)

@bot.command(aliases=["stopstreaming", "stopstatus", "stoplistening", "stopplaying", "stopwatching"])
async def stopactivity(ctx):
    await ctx.message.delete()

    await bot.change_presence(activity=None, status=discord.Status.dnd)

@bot.command()
async def dmall(ctx, *, message: str="https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    members = [m for m in ctx.guild.members if not m.bot]
    total_members = len(members)
    estimated_time = round(total_members * 4.5)

    await ctx.send(f">Starting DM process for `{total_members}` members.\n> Estimated time: `{estimated_time} seconds` (~{round(estimated_time / 60, 2)} minutes)", delete_after=10)

    success_count = 0
    fail_count = 0

    for member in members:
        try:
            await member.send(message)
            success_count += 1
        except Exception:
            fail_count += 1

        await asyncio.sleep(random.uniform(3, 6))

    await ctx.send(f"> **[**INFO**]**: DM process completed.\n> Successfully sent: `{success_count}`\n> Failed: `{fail_count}`", delete_after=10)

@bot.command(aliases=['hs'])
async def hypesquad(ctx, house: str=None):
    await ctx.message.delete()

    if not house:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `hypesquad <house>`', delete_after=5)
        return

    headers = {'Authorization': token, 'Content-Type': 'application/json'}

    try:
        r = requests.get('https://discord.com/api/v8/users/@me', headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: Invalid status code\n> __Error__: `{str(e)}`', delete_after=5)
        return

    headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'}
    payload = {}
    if house == "bravery":
        payload = {'house_id': 1}
    elif house == "brilliance":
        payload = {'house_id': 2}
    elif house == "balance":
        payload = {'house_id': 3}
    else:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Error__: Hypesquad house must be one of the following: `bravery`, `brilliance`, `balance`', delete_after=5)
        return

    try:
        r = requests.post('https://discordapp.com/api/v6/hypesquad/online', headers=headers, json=payload, timeout=10)
        r.raise_for_status()

        if r.status_code == 204:
            await ctx.send(f'> Hypesquad House changed to `{house}`!')

    except requests.exceptions.RequestException as e:
        await ctx.send(f'> **[**ERROR**]**: Unable to change Hypesquad house\n> __Error__: `{str(e)}`', delete_after=5)

bot.run(token)
