<p align="center">
  <img src="https://i.imgur.com/L8wQHUu.gif" alt="Radon Logo" width="200">
</p>

<h1 align="center">Radon - Discord SelfBot</h1>
<p align="center">
  <a href="https://github.com/zeozcb/Radon/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-important">
  </a>
  <a href="https://github.com/zeozcb/Radon">
    <img src="https://img.shields.io/github/repo-size/zeozcb/Radon.svg?label=Repo%20size&style=flat-square">
  </a>
  <a href="https://github.com/zeozcb/Radon/issues">
    <img src="https://img.shields.io/github/issues/zeozcb/Radon.svg?label=Issues&style=flat-square">
  </a>
  <a href="https://github.com/zeozcb/Radon/stargazers">
    <img src="https://img.shields.io/github/stars/zeozcb/Radon.svg?label=Stars&style=flat-square">
  </a>
</p>

<p align="center">
  Radon is a powerful and feature-rich Discord SelfBot designed for Windows, Linux, and macOS, written in Python.
</p>

> ⚠️ **WARNING:** Using self-bots is against TOS and can ban your account. This project is for educational purposes only. Use at your own risk.

This SelfBot offers a wide array of commands to enhance your Discord experience. It boasts an intuitive interface, comprehensive help documentation, and regular updates to maintain functionality and efficiency. While some unnecessary commands have been removed, we welcome suggestions for new features via issues or our Discord server.

## What's New!

Just added a bunch of cool stuff to Radon:
- **Auto-Update System** - Radon now checks for updates daily and lets you know when there's something new
- **One-Click Updates** - Just type `.update` and you're good to go
- **Dismiss Updates** - Not ready to update? Just use `.dismiss` to hide the notification
- **Manual Update Check** - Type `.check` whenever you want to see if there's a new version

I've also fixed some bugs and made everything run smoother. Let me know if you find any issues!

---

## Features

<details>
  <summary>Click to expand the list of commands</summary>

- **General**
  - `media`, `social`: Display your social media links
  - `changeprefix <prefix>`: Change the bot's command prefix
  - `shutdown`: Stop the selfbot
  - `uptime`: Show how long the selfbot has been running
  - `remoteuser <ADD|REMOVE> <@user>`: Manage remote command execution
  - `ping`: Check the bot's latency
  - `check`: Check for available updates
  - `update`: Update the SelfBot to the latest version
  - `dismiss`: Dismiss the update notification
  - `reload`: Restart the bot

- **User Interaction**
  - `copycat <ON|OFF> <@user>`: Mirror messages from a specific user
  - `hidemention <display_part> <hidden_part>`: Hide messages within other messages
  - `edit <message>`: Reposition the (edited) tag
  - `reverse <message>`: Reverse the letters of a message
  - `spam <amount> <message>`: Send a message multiple times
  - `quickdelete <message>`: Send and quickly delete a message
  - `autoreply <ON|OFF> [@user]`: Set up automatic replies
  - `afk <ON|OFF> [message]`: Enable/disable AFK mode with custom messages

- **Server Management**
  - `fetchmembers`: List all server members
  - `dmall <message>`: Message all server members
  - `sendall <message>`: Send a message to all server channels
  - `guildicon`: Get the server's icon
  - `guildbanner`: Get the server's banner
  - `guildinfo`: Display server information
  - `guildrename <new_name>`: Rename the server

- **User Profile**
  - `usericon <@user>`: Get a user's profile picture
  - `hypesquad <house>`: Change your HypeSquad badge
  - `playing <status>`: Set "Playing" status
  - `watching <status>`: Set "Watching" status
  - `streaming <status>`: Set "Streaming" status
  - `stopactivity`: Reset activity status
  - `profile [show|edit]`: Manage your custom profile

- **Utility**
  - `pingweb <url>`: Check a website's status
  - `geoip <ip>`: Look up an IP's location
  - `tts <text>`: Convert text to speech
  - `qr <text>`: Generate a QR code
  - `gentoken`: Generate a mock Discord token
  - `nitro`: Generate a fake Nitro code
  - `whremove <webhook_url>`: Remove a webhook
  - `purge <amount>`: Delete multiple messages
  - `clear`: Clear channel messages
  - `cleardm <amount>`: Delete DMs with a user
  - `firstmessage`: Get the first message in a channel
  - `tokeninfo <token>`: Retrieve token information
  - `ascii <message>`: Convert text to ASCII art
  - `lyrics <song name or lyrics>`: Search for song lyrics
  - `exec <python_code>`: Execute Python code
  - `dox <username>`: Search for potential social media profiles
  - `uptimeconfig <setting> <value>`: Configure uptime settings
  - `setsocial <platform> <emoji> <text> <link>`: Set social media links

- **Fun**
  - `airplane <LOOP|ONE>`: Display a 9/11 attack animation
  - `dick <@user>`: Show a user's "dick size"
  - `minesweeper <width> <height>`: Play Minesweeper
  - `leetspeak <message>`: Convert text to leetspeak
  - `catplay <LOOP|ONE>`: Show a cat animation
  - `zeo`: Display a cool "rulez" gif
  - `loopstop`: Stop any running loop animations

</details>

---

## Installation and Setup

1. **Configure `config/config.json`**:
   ```json
   {
     "token": "YOUR-DISCORD-TOKEN",
     "prefix": "YOUR-PREFERRED-PREFIX",
     "remote-users": ["USER-ID-1", "USER-ID-2"],
     "autoreply": {
       "messages": ["https://github.com/zeozcb/Radon"],
       "channels": ["CHANNEL-ID-1", "CHANNEL-ID-2"],
       "users": ["USER-ID-1", "USER-ID-2"]
     },
     "afk": {
       "enabled": false,
       "message": "I'm currently AFK. I'll respond when I return!"
     },
     "copycat": {
       "users": []
     }
   }

2. **Install Radon:**
   - **Easiest way:** Download EXE or download install.bat, GIT, Python 3.12 and run bat!
   - **Manual way:**
     ```bash
     git clone https://github.com/zeozcb/Radon.git
     cd Radon
     py -m pip install -r requirements.txt
     py main.py
     ```

## Auto-Update System

I've added a new update system that makes keeping Radon up-to-date super easy:

- Radon checks for updates once a day
- When there's a new version, you'll see a message like this:
 🚨 SelfBot Update Available! 🚨
  A new version of the SelfBot is available. Would you like to update?
  🔸 Current version: v1.0.0
  🔹 Latest version: v1.1.0
  ⬆️ To update, use the command: .update
  ❌ To dismiss this message, use: .dismiss
  Stay up to date for the best experience!
- Just type `.update` to automatically download and install the latest version
- If you want to check for updates manually, use `.check`
- Not ready to update? Use `.dismiss` to hide the notification

## Remote Command Execution

Radon allows remote command execution for users listed in the `remote-users` array in `config/config.json`.

**Usage:**
1. Add user IDs to `remote-users` in the config file.
2. Use `*remoteuser ADD @user(s)` to add users to the list.
3. From another account, use `*help` (replace * with your prefix) to execute commands if you're on the list.
4. Remove users with `*remoteuser REMOVE @user(s)`.

## Autoreply Feature

Set up automatic responses for specific channels or users.

**Usage:**
- `autoreply ON`: Enable autoreply in the current channel.
- `autoreply OFF`: Disable autoreply in the current channel.
- `autoreply ON @user`: Enable autoreply for a specific user.
- `autoreply OFF @user`: Disable autoreply for a specific user.

Configure autoreply messages and targets in `config/config.json`.

## Contribution and Support

- **Found a bug?** Open an issue on GitHub
- **Have a cool idea?** Create a pull request or suggest it in an issue
- **Need help?** Join our Discord Server for support and updates

## License

Radon is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Radon is a fork of Discord-SelfBot by @AstraaDev, which was based on the original SelfBot by @humza1400. Thanks to them for their awesome work!

---

Made by zeozcb - Star the repo if you like it!
