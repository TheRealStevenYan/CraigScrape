import asyncio
import threading
from queue import LifoQueue

from discord.ext import commands

from scraping.craigslist_urls import all_categories
from scraping.scrape import SearchQuery


class Tracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.searches = dict()  # Keeps track of all keywords, and a tuple containing both the search query
                                # and its notification backlog. [keyword, (search_query, backlog)]
        self.tracking = threading.Event()  # Using threading to prevent busy-waiting when stopping tracking.
        self.tracking.set()

    @commands.command()
    async def stop(self, ctx):
        # Usage: -stop
        self.tracking.clear()
        await ctx.send("Stopped tracking Craigslist.\n"
                       "To re-enable tracking, use command '-track'")

    @commands.command()
    async def track(self, ctx):
        # Usage: -track
        self.tracking.set()
        await ctx.send("Tracking Craigslist.\n"
                       "To temporarily disable tracking, use command '-stop'")
        for keywords in self.searches:
            search_query = self.searches[keywords][0]
            await self.periodic_tasks(ctx, search_query)

    @commands.command()
    async def all_searches(self, ctx):
        all_searches = "**Currently tracking the following:**\n"
        for searches in self.searches:
            all_searches += "{}\n".format(searches)
        await ctx.send(all_searches)

    @commands.command()
    async def remove(self, ctx, *args):
        # Usage: -remove <keyword>
        if len(args) != 1 or self.tracking.is_set():
            await ctx.send("Usage: 'remove <keyword>\n"
                           "Please disable tracking before removing search queries.")
            return

        keyword = args[0]
        try:
            self.searches.pop(keyword)
            await ctx.send("Successfully removed search: {}".format(keyword))
        except KeyError:
            await ctx.send("{} is not being tracked at the moment. Remove unsuccessful.".format(keyword))

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

        await ctx.send("SEARCHING: Keyword = {}, Category = {}\n"
                       "To temporarily disable tracking, use command '-stop'".format(keyword, category))

        new_query = SearchQuery(keyword, category)
        self.searches.update({keyword: (new_query, LifoQueue())})

        await self.bot.wait_until_ready()
        await self.periodic_tasks(ctx, new_query)

    # Tracks Craigslist every 120 seconds for a specific search query.
    async def periodic_tasks(self, ctx, search_query):
        backlog = self.searches[search_query.get_keyword()][1]

        while self.tracking.is_set():
            if backlog.empty():
                backlog = await search_query.run_search()

            while not backlog.empty() and self.tracking.is_set():
                notification = backlog.get()
                await ctx.send(notification)
            if backlog.empty():
                await asyncio.sleep(120)

        # If Craigslist tracking is disabled, the current state of the backlog is saved.
        self.searches.update({search_query.get_keyword() : (search_query, backlog)})


@commands.command()
async def help(ctx, *args):
    # Usage: -help            (to show commands)
    #        -help categories (to list all possible search categories)
    if len(args) and args[0] == 'categories':
        every_category = ""
        for category in all_categories:
            every_category += "'{}' ".format(category)
        await ctx.send(every_category)

    else:
        await ctx.send("**Commands:**\n\n"
                       "**-search <keyword> <category>**\n"
                       "Tracks Craigslist for a given keyword under a given category.\n"
                       "If no categories are specified, the search will run on the default category (all). Run:\n\n"
                       "**-help categories**\n"
                       "For getting a list of all possible searchable categories.\n\n"
                       "**-remove <keyword>**\n"
                       "Will stop tracking Craigslist for the given keyword. Before removing a keyword, remember to "
                       "temporarily disable automatic tracking with the following:\n\n"
                       "**-stop**\n"
                       "To temporarily automatic disable tracking.\n\n"
                       "**-track**\n"
                       "Will re-enable automatic tracking.\n\n"
                       "**-all_searches**\n"
                       "Lists out every keyword currently being tracked.\n\n")


def setup(bot):
    bot.add_cog(Tracking(bot))
    bot.add_command(help)
