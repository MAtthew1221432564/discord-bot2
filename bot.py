import discord
from discord.ext import commands
import asyncio
import re
from datetime import timedelta, datetime, timezone
import os

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Convert "10s", "5m", "2h", etc. into seconds
def convert_time(time_str):
    match = re.match(r"(\d+)(s|m|h|d|w)$", time_str)
    if not match:
        return None

    num = int(match.group(1))
    unit = match.group(2)

    if unit == "s":
        return num
    if unit == "m":
        return num * 60
    if unit == "h":
        return num * 60 * 60
    if unit == "d":
        return num * 60 * 60 * 24
    if unit == "w":
        return num * 60 * 60 * 24 * 7

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, duration=None):
    if duration is None:
        await ctx.send("You must include a time. Example: `!mute @user 10s`")
        return

    seconds = convert_time(duration)
    if seconds is None:
        await ctx.send("Invalid time format. Use: 10s, 1m, 10m, 1h, 1d, 1w")
        return

    try:
        end_time = datetime.now(timezone.utc) + timedelta(seconds=seconds)
        await member.timeout(end_time)
        await ctx.send(f"{member.mention} has been muted for **{duration}**")

        # Auto unmute
        await asyncio.sleep(seconds)
        await member.timeout(None)
        await ctx.send(f"{member.mention} has been automatically unmuted.")

    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    try:
        await member.timeout(None)
        await ctx.send(f"{member.mention} has been manually unmuted.")
    except:
        await ctx.send("Could not unmute this user.")

# Run bot (Railway loads TOKEN from environment)
bot.run(os.getenv("TOKEN"))
