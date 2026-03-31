import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
#        MUTE COMMAND
# -----------------------------
@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, duration: int, *, reason="No reason provided"):
    if member == ctx.author:
        return await ctx.send("You can't mute yourself.")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You can't mute someone with a higher or equal role.")
    if member.top_role >= ctx.guild.me.top_role:
        return await ctx.send("I can't mute someone with a higher role than me.")

    try:
        await member.timeout_for(duration=duration*60, reason=reason)
        await ctx.send(f"{member} has been muted for {duration} minutes. Reason: {reason}")
    except Exception as e:
        await ctx.send(f"Failed to mute: {e}")

# -----------------------------
#       UNMUTE COMMAND
# -----------------------------
@bot.command()
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    try:
        await member.timeout_until(None)
        await ctx.send(f"{member} has been unmuted.")
    except Exception as e:
        await ctx.send(f"Failed to unmute: {e}")

# -----------------------------
#         BAN COMMAND
# -----------------------------
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    if member == ctx.author:
        return await ctx.send("You can't ban yourself.")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You can't ban someone with a higher or equal role.")
    if member.top_role >= ctx.guild.me.top_role:
        return await ctx.send("I can't ban someone with a higher role than me.")

    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned. Reason: {reason}")

# -----------------------------
#        UNBAN COMMAND
# -----------------------------
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: discord.User, *, reason="No reason provided"):
    await ctx.guild.unban(user, reason=reason)
    await ctx.send(f"{user} has been unbanned.")

# -----------------------------
#         BOT ONLINE
# -----------------------------
@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

# -----------------------------
#        RUN THE BOT
# -----------------------------
bot.run(os.getenv("TOKEN"))
