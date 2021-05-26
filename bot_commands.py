from discord.ext import commands


@commands.command()
async def search(ctx, *args):
    # Usage: -search <keyword> <category>
    await ctx.send('SEARCHING: Keyword = {}, Category = {}'.format(args[0], args[1]))

    if len(args) != 2:
        await ctx.send("Usage: '-search <keyword> <category>'")

def setup(bot):
    bot.add_command(search)
