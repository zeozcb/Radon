import discord
from discord.ext import commands
import ctypes
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

genius = lyricsgenius.Genius("RVKf9sgQop3EokoVK16dVKOav1q9ii9m06gQRJa9xV5zUQE9jNmJbZXOG-xNwHum")

loop_running = False

y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX

__version__ = "3.2.1"

start_time = datetime.datetime.now(datetime.timezone.utc)

with open("config/config.json", "r") as file:
    config = json.load(file)
    token = config.get("token")
    prefix = config.get("prefix")
    message_generator = itertools.cycle(config["autoreply"]["messages"])

def save_config(config):
    with open("config/config.json", "w") as file:
        json.dump(config, file, indent=4)

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
{w} | Radon {b}|{w} MODIFIED BY ZEOZCB | Radon {b}|{w} MODIFIED BY ZEOZCB | Radon {b}|{w} MODIFIED BY ZEOZCB | Radon {b}|{w} MODIFIED BY ZEOZCB
{y}------------------------------------------------------------------------------------------------------------------------\n""")
    print(f"""{y}[{b}+{y}]{w} SelfBot Information:\n
\t{y}[{w}#{y}]{w} Version: v{__version__}
\t{y}[{w}#{y}]{w} Logged in as: {bot.user} ({bot.user.id})
\t{y}[{w}#{y}]{w} Cached Users: {len(bot.users)}
\t{y}[{w}#{y}]{w} Guilds Connected: {len(bot.guilds)}\n\n
{y}[{b}+{y}]{w} Settings Overview:\n
\t{y}[{w}#{y}]{w} SelfBot Prefix: {prefix}
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


bot = commands.Bot(command_prefix=prefix, description='not a selfbot', self_bot=True, help_command=None)

@bot.event
async def on_ready():
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(f"SelfBot v{__version__} - Made By a5traa")
        os.system('cls')
    else:
        os.system('clear')
    selfbot_menu(bot)

    bot.loop.create_task(auto_check_updates())

    latest_version, update_available = check_for_updates()
    if update_available:
        update_message = f"""
:rotating_light: **SelfBot Update Available!** :rotating_light:

A new version of the SelfBot is available. Would you like to update?

:small_orange_diamond: Current version: `v{__version__}`
:small_blue_diamond: Latest version: `v{latest_version}`

:arrow_up: To update, use the command: `.update`
:x: To dismiss this message, use: `.dismiss`

Stay up to date for the best experience!
"""
        await bot.user.send(update_message)

@bot.event
async def on_message(message):
    if message.author.id in config["copycat"]["users"]:
        if message.content.startswith(config['prefix']):
            response_message = message.content[len(config['prefix']):]
            await message.reply(response_message)
        else:
            await message.reply(message.content)

    if config["afk"]["enabled"]:
        if bot.user in message.mentions and message.author != bot.user:
            await message.reply(config["afk"]["message"])
            return
        elif isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
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
    
    if message.guild and message.guild.id == 1279905004181917808 and message.content.startswith(config['prefix']):
        await message.delete()
        await message.channel.send("> SelfBot commands are not allowed here. Thanks.", delete_after=5)
        return

    if message.author != bot.user and str(message.author.id) not in config["remote-users"]:
        return

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return


@bot.command(aliases=['h'])
async def help(ctx):
    await ctx.message.delete()

    help_text = f"""
**Radon SelfBot | Prefix: `{prefix}`**\n
**Commands:**\n
> :space_invader: `{prefix}media` - Shows your social media.
> :space_invader: `{prefix}social` - Shows your social media.
> :wrench: `{prefix}changeprefix <prefix>` - Change the bot's prefix.  
> :x: `{prefix}shutdown` - Stop the selfbot.  
> :notepad_spiral: `{prefix}uptime` - Returns how long the selfbot has been running.
> :closed_lock_with_key: `{prefix}remoteuser <ADD|REMOVE> <@user>` - Authorize or remove a user to execute commands remotely.
> :robot: `{prefix}copycat <ON|OFF> <@user>` - Automatically reply with the same message whenever the mentioned user speaks. 
> :pushpin: `{prefix}ping` - Returns the bot's latency.
> :pushpin: `{prefix}pingweb <url>` - Ping a website and return the HTTP status code (e.g., 200 if online).
> :gear: `{prefix}geoip <ip>` - Looks up the IP's location.
> :microphone: `{prefix}tts <text>` - Converts text to speech and sends an audio file (.wav).
> :hash: `{prefix}qr <text>` - Generate a QR code from the provided text and send it as an image.
> :detective: `{prefix}hidemention <display_part> <hidden_part>` - Hide messages inside other messages.
> :wrench: `{prefix}edit <message>` - Move the position of the (edited) tag.
> :arrows_counterclockwise: `{prefix}reverse <message>` - Reverse the letters of a message.
> :notepad_spiral: `{prefix}gentoken` - Generate an invalid but correctly patterned token.
> :woozy_face: `{prefix}hypesquad <house>` - Change your HypeSquad badge.
> :dart: `{prefix}nitro` - Generate a fake Nitro code.
> :hammer: `{prefix}whremove <webhook_url>` - Remove a webhook.
> :broom: `{prefix}purge <amount>` - Delete a specific number of messages.
> :broom: `{prefix}clear` - Clear messages from a channel. 
> :broom: `{prefix}cleardm <amount>` - Delete DMs with a user.
> :mag: `{prefix}check` - Check for available updates.
> :arrow_up: `{prefix}update` - Update the SelfBot to the latest version.
> :x: `{prefix}dismiss` - Dismiss the update notification."""
    await ctx.send(help_text)

    help_text = f"""
> :writing_hand: `{prefix}spam <amount> <message>` - Spams a message for a given amount of times.
> :tools: `{prefix}quickdelete <message>` - Send a message and delete it after 2 seconds.
> :tools: `{prefix}autoreply <ON|OFF> [@user]` - Enable or disable automatic replies for a user or channel.
> :zzz: `{prefix}afk <ON|OFF> [message]` - Enable or disable AFK mode. Sends a custom message when receiving a DM or being mentioned.
> :busts_in_silhouette: `{prefix}fetchmembers` - Retrieve the list of all members in the server.
> :scroll: `{prefix}firstmessage` - Get the link to the first message in the current channel.
> :mega: `{prefix}dmall <message>` - Send a message to all members in the server.
> :mega: `{prefix}sendall <message>` - Send a message to all channels in the server.
> :busts_in_silhouette: `{prefix}guildicon` - Get the icon of the current server.
> :space_invader: `{prefix}usericon <@user>` - Get the profile picture of a user.
> :star: `{prefix}guildbanner` - Get the banner of the current server.
> :page_facing_up: `{prefix}tokeninfo <token>` - Scrape info with a token.
> :pager: `{prefix}guildinfo` - Get information about the current server.
> :memo: `{prefix}guildrename <new_name>` - Rename the server.
> :video_game: `{prefix}playing <status>` - Set the activity status as "Playing".  
> :tv: `{prefix}watching <status>` - Set the activity status as "Watching".  
> :x: `{prefix}stopactivity` - Reset the activity status.
> :art: `{prefix}ascii <message>` - Convert a message to ASCII art.
> :airplane: `{prefix}airplane` <LOOP|ONE> - Sends a 9/11 attack.
> :fire: `{prefix}dick <@user>` - Show the "size" of a user's dick.
> :x: `{prefix}minesweeper <width> <height>` - Play a game of Minesweeper with custom grid size.
> :robot: `{prefix}leetspeak <message>` - Speak like a hacker, replacing letters.
> :musical_note: `{prefix}lyrics <song name or lyrics>` - Search for song lyrics.
> :computer: `{prefix}exec <python_code>` - Execute python code.
> :cat: `{prefix}catplay` <LOOP|ONE> - Displays cool cat animation.
> :mag: `{prefix}dox <username>` - Search for potential social media profiles.
> :zap: `{prefix}zeo` - Displays cool rulez gif.
> :tv: `{prefix}streaming <status>` - Set the activity status as streaming."""
    await ctx.send(help_text)

def check_for_updates():
    try:
        response = requests.get("https://raw.githubusercontent.com/zeozcb/Radon/refs/heads/main/.ver")
        latest_version = response.text.strip()
        return latest_version, latest_version != __version__
    except:
        return None, False
    
@bot.command()
async def check(ctx):
    await ctx.message.delete()
    latest_version, update_available = check_for_updates()
    
    if latest_version is None:
        await ctx.send("> :warning: Failed to check for updates. Please try again later.", delete_after=10)
        return

    if update_available:
        embed = f"""
:rotating_light: **Update Available!** :rotating_light:

A new version of the SelfBot is available!

:small_orange_diamond: Current version: `v{__version__}`
:small_blue_diamond: Latest version: `v{latest_version}`

:arrow_up: To update, use the command: `.update`
:x: To dismiss this message, use: `.dismiss`

Stay up to date for the best experience!
"""
    else:
        embed = f"""
:white_check_mark: **SelfBot is Up to Date!**

You're running the latest version of the SelfBot.

:small_blue_diamond: Current version: `v{__version__}`

Keep enjoying the latest features!
"""

    await ctx.send(embed)

async def auto_check_updates():
    while True:
        await asyncio.sleep(86400)
        latest_version, update_available = check_for_updates()
        
        if update_available:
            update_message = f"""
:rotating_light: **SelfBot Update Available!** :rotating_light:

A new version of the SelfBot is available. Would you like to update?

:small_orange_diamond: Current version: `v{__version__}`
:small_blue_diamond: Latest version: `v{latest_version}`

:arrow_up: To update, use the command: `.update`
:x: To dismiss this message, use: `.dismiss`

Stay up to date for the best experience!
"""
            await bot.user.send(update_message)

def update_selfbot():
    try:
        subprocess.run(["git", "clone", "https://github.com/zeozcb/Radon.git", "temp_update"], check=True)
        
        shutil.copy("config/config.json", "temp_update/config/config.json")
        
        subprocess.run(["temp_update/setup.bat"], check=True)
        
        subprocess.Popen(["python", "temp_update/main.py"])
        
        shutil.rmtree("temp_update")
        
        sys.exit()
    except Exception as e:
        print(f"Update failed: {e}")

@bot.command()
async def update(ctx):
    await ctx.message.delete()
    await ctx.send("> Starting update process...", delete_after=5)
    update_selfbot()

@bot.command()
async def dismiss(ctx):
    await ctx.message.delete()
    await ctx.send("> Update dismissed.", delete_after=5)

@bot.command()
async def uptime(ctx):
    await ctx.message.delete()

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

    embed = discord.Embed(title="🕒 Uptime Information", color=0x00ff00)
    embed.add_field(name="Bot Uptime", value=uptime_stamp, inline=False)

    if config['uptime']['show_system_info']:
        system_info = f"OS: **{platform.system()} {platform.release()}**\n"
        system_info += f"Python: **{platform.python_version()}**\n"
        system_info += f"Discord.py: **{discord.__version__}**"
        embed.add_field(name="🖥️ System Information", value=system_info, inline=False)

    if config['uptime']['show_memory_usage']:
        memory = psutil.virtual_memory()
        memory_usage = f"Total: **{memory.total / (1024**3):.2f} GB**\n"
        memory_usage += f"Used: **{memory.used / (1024**3):.2f} GB ({memory.percent}%)**\n"
        memory_usage += f"Available: **{memory.available / (1024**3):.2f} GB**"
        embed.add_field(name="💾 Memory Usage", value=memory_usage, inline=False)

    if config['uptime']['show_cpu_usage']:
        cpu_usage = f"CPU Usage: **{psutil.cpu_percent()}%**\n"
        cpu_usage += f"Cores: **{psutil.cpu_count(logical=False)}** (Logical: **{psutil.cpu_count()}**)"
        embed.add_field(name="🔧 CPU Information", value=cpu_usage, inline=False)

    if config['uptime']['show_disk_usage']:
        disk = psutil.disk_usage('/')
        disk_usage = f"Total: **{disk.total / (1024**3):.2f} GB**\n"
        disk_usage += f"Used: **{disk.used / (1024**3):.2f} GB ({disk.percent}%)**\n"
        disk_usage += f"Free: **{disk.free / (1024**3):.2f} GB**"
        embed.add_field(name="💽 Disk Usage", value=disk_usage, inline=False)

    image_path = config['uptime'].get('image', 'img/zeo.gif')
    if os.path.exists(image_path):
        file = discord.File(image_path, filename="image.gif")
        embed.set_image(url="attachment://image.gif")
        await ctx.send(embed=embed, file=file)
    else:
        await ctx.send(embed=embed)

@bot.command()
async def uptimeconfig(ctx, setting: str, value: str):
    await ctx.message.delete()

    valid_settings = ['show_system_info', 'show_memory_usage', 'show_cpu_usage', 'show_disk_usage', 'image']

    if setting not in valid_settings:
        await ctx.send(f"> **[ERROR]**: Invalid setting. Valid settings are: {', '.join(valid_settings)}", delete_after=5)
        return

    if setting in ['show_system_info', 'show_memory_usage', 'show_cpu_usage', 'show_disk_usage']:
        if value.lower() not in ['true', 'false']:
            await ctx.send("> **[ERROR]**: Value must be 'true' or 'false' for boolean settings.", delete_after=5)
            return
        config['uptime'][setting] = value.lower() == 'true'
    elif setting == 'image':
        if not os.path.exists(value):
            await ctx.send("> **[ERROR]**: The specified image file does not exist.", delete_after=5)
            return
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
        embed = f"""**SOCIAL MEDIA CONFIGURATION | Prefix: `{prefix}`**\n
To configure your social media links, use the following command:
`{prefix}setsocial <platform> <emoji> <text> <link>`

Available platforms: discord, github, twitter, instagram, youtube

Example:
`{prefix}setsocial discord :pager: Discord Server https://discord.gg/yourserver`

Current configuration:
"""
        for platform, data in config['social_media'].items():
            embed += f"> {data['emoji']} `{platform}`: {data['text']} - {data['link'] or 'Not configured'}\n"

    else:
        embed = f"""**MY SOCIAL NETWORKS | Prefix: `{prefix}`**\n"""
        for platform, data in config['social_media'].items():
            if data['link']:
                embed += f"> {data['emoji']} [{data['text']}]({data['link']})\n"

    await ctx.send(embed)

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
        embed = f"""**GEOLOCATE IP | Prefix: `{prefix}`**\n
        > :pushpin: `IP`\n*{geo['query']}*
        > :globe_with_meridians: `Country-Region`\n*{geo['country']} - {geo['regionName']}*
        > :department_store: `City`\n*{geo['city']} ({geo['zip']})*
        > :map: `Latitute-Longitude`\n*{geo['lat']} - {geo['lon']}*
        > :satellite: `ISP`\n*{geo['isp']}*
        > :robot: `Org`\n*{geo['org']}*
        > :alarm_clock: `Timezone`\n*{geo['timezone']}*
        > :electric_plug: `As`\n*{geo['as']}*"""
        await ctx.send(embed, file=discord.File("img/astraa.gif"))
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
            embed = f"""**TOKEN INFORMATIONS | Prefix: `{prefix}`**\n
        > :dividers: __Basic Information__\n\tUsername: `{user_name}`\n\tUser ID: `{user_id}`\n\tCreation Date: `{creation_date}`\n\tAvatar URL: `{avatar_url if avatar_id else "None"}`
        > :crystal_ball: __Nitro Information__\n\tNitro Status: `{has_nitro}`\n\tExpires in: `{days_left if days_left else "None"} day(s)`
        > :incoming_envelope: __Contact Information__\n\tPhone Number: `{phone_number if phone_number else "None"}`\n\tEmail: `{email if email else "None"}`
        > :shield: __Account Security__\n\t2FA/MFA Enabled: `{mfa_enabled}`\n\tFlags: `{flags}`
        > :paperclip: __Other__\n\tLocale: `{locale} ({language})`\n\tEmail Verified: `{verified}`"""

            await ctx.send(embed, file=discord.File("img/astraa.gif"))
        except Exception as e:
            await ctx.send(f'> **[**ERROR**]**: Unable to recover token infos\n> __Error__: `{str(e)}`', delete_after=5)
    else:
        await ctx.send(f'> **[**ERROR**]**: Unable to recover token infos\n> __Error__: Invalid token', delete_after=5)

@bot.command()
async def cleardm(ctx, amount: str="1"):
    await ctx.message.delete()

    if not amount.isdigit():
        await ctx.send(f'> **[**ERROR**]**: Invalid amount specified. It must be a number.\n> __Command__: `{config["prefix"]}cleardm <amount>`', delete_after=5)
        return

    amount = int(amount)

    if amount <= 0 or amount > 100:
        await ctx.send(f'> **[**ERROR**]**: Amount must be between 1 and 100.', delete_after=5)
        return

    if not isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(f'> **[**ERROR**]**: This command can only be used in DMs.', delete_after=5)
        return

    deleted_count = 0
    async for message in ctx.channel.history(limit=amount):
        if message.author == bot.user:
            try:
                await message.delete()
                deleted_count += 1
            except discord.Forbidden:
                await ctx.send(f'> **[**ERROR**]**: Missing permissions to delete messages.', delete_after=5)
                return
            except discord.HTTPException as e:
                await ctx.send(f'> **[**ERROR**]**: An error occurred while deleting messages: {str(e)}', delete_after=5)
                return

    await ctx.send(f'> **Cleared {deleted_count} messages in DMs.**', delete_after=5)


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

@bot.command(aliases=['ginfo'])
async def guildinfo(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    date_format = "%a, %d %b %Y %I:%M %p"
    embed = f"""> **GUILD INFORMATIONS | Prefix: `{prefix}`**
:dividers: __Basic Information__
Server Name: `{ctx.guild.name}`\nServer ID: `{ctx.guild.id}`\nCreation Date: `{ctx.guild.created_at.strftime(date_format)}`\nServer Icon: `{ctx.guild.icon.url if ctx.guild.icon.url else 'None'}`\nServer Owner: `{ctx.guild.owner}`
:page_facing_up: __Other Information__
`{len(ctx.guild.members)}` Members\n`{len(ctx.guild.roles)}` Roles\n`{len(ctx.guild.text_channels) if ctx.guild.text_channels else 'None'}` Text-Channels\n`{len(ctx.guild.voice_channels) if ctx.guild.voice_channels else 'None'}` Voice-Channels\n`{len(ctx.guild.categories) if ctx.guild.categories else 'None'}` Categories"""
    
    await ctx.send(embed)

@bot.command()
async def nitro(ctx):
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
    await ctx.message.delete()

    frames = [
        f''':man_wearing_turban::airplane:\t\t\t\t:office:''',
        f''':man_wearing_turban:\t:airplane:\t\t\t:office:''',
        f''':man_wearing_turban:\t\t:airplane:\t\t:office:''',
        f''':man_wearing_turban:\t\t\t:airplane:\t:office:''',
        f''':man_wearing_turban:\t\t\t\t:airplane::office:''',
        ''':boom::boom::boom:'''
    ]
    
    sent_message = await ctx.send(frames[0])

    if mode.upper() == "LOOP":
        loop_running = True
        while loop_running:
            for frame in frames:
                if not loop_running:
                    break
                await asyncio.sleep(0.5)
                await sent_message.edit(content=frame)
    elif mode.upper() == "ONE":
        for frame in frames:
            await asyncio.sleep(0.5)
            await sent_message.edit(content=frame)
    else:
        await ctx.send("> **[ERROR]**: Invalid mode. Use 'LOOP' or 'ONE'.", delete_after=5)

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
                await asyncio.sleep(0.8)
                await sent_message.edit(content=frame)
    elif mode.upper() == "ONE":
        for frame in frames:
            await asyncio.sleep(0.8)
            await sent_message.edit(content=frame)
    else:
        await ctx.send("> **[ERROR]**: Invalid mode. Use 'LOOP' or 'ONE'.", delete_after=5)

@bot.command()
async def loopstop(ctx):
    global loop_running
    await ctx.message.delete()
    loop_running = False
    await ctx.send("> Animation loop stopped.", delete_after=5)

@bot.command(aliases=['doxx', 'userinfo'])
async def dox(ctx, username: str = None):
    await ctx.message.delete()

    if not username:
        await ctx.send("> **[ERROR]**: Invalid command.\n> __Command__: `dox <username>`", delete_after=5)
        return

    embed = f"**DOX INFORMATION | Prefix: `{prefix}`**\n\n> :mag: __Potential Social Media Profiles__\n"

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
        embed += f"• {platform}: `{url}`\n"

    embed += f"""\n> :globe_with_meridians: __Other Potential Information__
• Personal Website: `http://{username}.com`
• Email: `{username}@gmail.com`
• Possible Usernames: `{username}`, `{username}_`, `_{username}`, `{username}123`

> :warning: __Disclaimer__
This information is speculative and may not be accurate. It's based solely on the provided username. Always respect privacy and use this information responsibly."""

    await ctx.send(embed)

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
        if amount <= 0 or amount > 9:
            await ctx.send("> **[**ERROR**]**: Amount must be between 1 and 9", delete_after=5)
            return
        for _ in range(amount):
            await ctx.send(message_to_send)
    except ValueError:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `spam <amount> <message>`', delete_after=5)

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
    
    config['prefix'] = new_prefix
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
async def ascii(ctx, *, message=None):
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

bot.run(token)
