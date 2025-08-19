# 🤖 Discord Bot

A modular **Discord Bot** built with [discord.py](https://discordpy.readthedocs.io/) and [Flask](https://flask.palletsprojects.com/) for uptime health checks.

---

## 🚀 Features

- Modular commands & events (Cogs)
- Role management (assign/remove)
- Moderation (bad word filter, logs)
- Fun commands (polls, reply, DM)
- Flask server for Render/UptimeRobot pings
- Logs stored in `discord.log`

---

## ⚙️ Setup

1. Clone repo:

   ```bash
   git clone <repo-url>
   cd discord-bot
   ```

2. Install deps:

   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env`:

   ```env
   DISCORD_TOKEN=your-token
   PREFIX=#
   ANNOUNCE_CHANNEL_ID=1234567890
   HOST=0.0.0.0
   PORT=1234
   ```

4. Run:

   ```bash
   python main.py
   ```

---

## 📜 Commands

- `!hello` → Greet user
- `!assign @user Role` → Assign role (Admin)
- `!remove @user Role` → Remove role (Admin)
- `!secret` → Hidden command (Admin)
- `!dm msg` → Send DM to yourself
- `!reply` → Reply to last message
- `!poll Question` → Create 👍👎 poll
- `!ping` → Check bot latency
- `!invite` → Generates server invite link
- `!serverinfo` → Displays server information
- `!userinfo` → Displays user information
- `!` → Show command list

---

## 📚 Notes

- **Cogs** = modular structure for commands/events
- **Flask** = uptime check endpoint
- **Logs** → written to `discord.log` only
