import asyncio

from discord.ext import commands

from scraping.craigslist_urls import all_categories
from scraping.scrape import SearchQuery


# TODO: Implement disabling / enabling tracking and changing queries.
class Tracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.searches = dict()
        self.tracking = True

    @commands.command()
    async def search(self, ctx, *args):
        # Usage: -search <keyword> <category>
        if len(args) > 2 or len(args) < 1:
            await ctx.send("Usage: '-search <keyword> <category>'")
            return

        keyword = args[0]
        try:
            category = args[1]
        except IndexError:  # By default, will set category to 'all' if not specified
            category = 'all'

        await ctx.send('SEARCHING: Keyword = {}, Category = {}'.format(keyword, category))
        new_query = SearchQuery(keyword, category)
        await self.bot.wait_until_ready()

        while True:
            backlog = await new_query.run_search()
            while not backlog.empty():
                notification = backlog.get()
                await ctx.send(notification)
            await asyncio.sleep(60)


@commands.command()
async def help(ctx, *args):
    # Usage: -help            (to show commands)
    #        -help categories (to list all possible search categories)
    if len(args) and args[0] == 'categories':
        every_category = '```'
        for category in all_categories:
            every_category += "'{}' ".format(category)
        every_category += '```'
        await ctx.send(every_category)

    else:
        await ctx.send("```Commands:\n\n"
                       "-search <keyword> <category>\n"
                       "Tracks Craigslist for a given keyword under a given category.\n"
                       "If no categories are specified, the search will run on the default category (all).\n\n"
                       "For a list of categories, run: "
                       "-help categories```")


def setup(bot):
    bot.add_cog(Tracking(bot))
    bot.add_command(help)
