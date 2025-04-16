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

- **Fun and Games**
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
   - **Automated:** Run `setup.bat`, then launch the created file.
   - **Manual:**
     ```bash
     git clone https://github.com/zeozcb/Radon.git
     cd Radon
     python -m pip install -r requirements.txt
     python main.py
     ```

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

- **Contribute:** Open issues or create pull requests on GitHub.
- **Support:** Join our Discord Server for help and updates.

## License

Radon is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Radon is a fork of Discord-SelfBot by @AstraaDev, which was based on the original SelfBot by @humza1400. All credits belongs to them.
