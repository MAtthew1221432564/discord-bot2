import discord
from discord.ext import commands
import datetime
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
# TIME PARSER (10s, 1m, 10m, 1h, 1w)
# -----------------------------
def parse_duration(duration_str):
    units = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800
    }

    try:
        unit = duration_str[-1].lower()
        value = int(duration_str[:-1])

        if unit not in units:
            return None

        return value * units[unit]

    except:
        return None


# -----------------------------
# BOT READY
# -----------------------------
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


# -----------------------------
# MUTE COMMAND
# -----------------------------
@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, duration: str, *, reason="No reason provided"):
    seconds = parse_duration(duration)

    if seconds is None:
        return await ctx.send("❌ Invalid duration. Use: `10s`, `1m`, `10m`, `1h`, `1w`.")

    try:
        until = discord.utils.utcnow() + datetime.timedelta(seconds=seconds)
        await member.timeout(until, reason=reason)
        await ctx.send(f"🔇 {member.mention} has been muted for **{duration}**. Reason: {reason}")

    except Exception as e:
        await ctx.send(f"❌ Failed to mute: {e}")


# -----------------------------
# UNMUTE COMMAND
# -----------------------------
@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    try:
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} has been unmuted.")
    except Exception as e:
        await ctx.send(f"❌ Failed to unmute: {e}")


# -----------------------------
# BAN COMMAND
# -----------------------------
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"⛔ {member.mention} has been banned. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Failed to ban: {e}")


# -----------------------------
# UNBAN COMMAND
# -----------------------------
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user: str):
    try:
        name, discriminator = user.split("#")
        for ban_entry in await ctx.guild.bans():
            banned_user = ban_entry.user
            if banned_user.name == name and banned_user.discriminator == discriminator:
                await ctx.guild.unban(banned_user)
                return await ctx.send(f"✅ Unbanned **{user}**")

        await ctx.send("❌ User not found in ban list.")

    except Exception as e:
        await ctx.send(f"❌ Failed to unban: {e}")


# -----------------------------
# KICK COMMAND
# -----------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} has been kicked. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Failed to kick: {e}")


# -----------------------------
# PURGE COMMAND (MAX 100 PER BATCH)
# -----------------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    if amount < 1:
        return await ctx.send("❌ You must delete at least 1 message.")

    # Discord only allows 100 per bulk delete, but discord.py loops automatically.
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Deleted **{len(deleted) - 1}** messages.", delete_after=3)
    except Exception as e:
        await ctx.send(f"❌ Failed to purge messages: {e}")


# -----------------------------
# RUN BOT
# -----------------------------
bot.run(os.getenv("TOKEN"))
