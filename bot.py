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

        # Auto unmute after time expires
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