from bot import bot, discord, commands
@bot.command()
async def supp(ctx, amount=0):
    """supp <nombre> de messages"""
    await ctx.channel.purge(limit=amount+1)