import asyncio
import threading
from queue import Queue

from discord.ext import commands

from scraping.craigslist_urls import all_categories
from scraping.scrape import SearchQuery


# TODO: Implement disabling / enabling tracking and changing queries.
class Tracking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.searches = dict()  # Keeps track of all keywords, and a tuple containing both the search query
                                # and its notification backlog.
        self.tracking = threading.Event()  # Using threading to prevent busy-waiting when stopping tracking.
        self.tracking.set()

    @commands.command()
    async def stop(self, ctx):
        self.tracking.clear()
        await ctx.send("Stopped tracking Craigslist.\n"
                       "To re-enable tracking, use command '-track'")

    @commands.command()
    async def track(self, ctx):
        self.tracking.set()
        await ctx.send("Tracking Craigslist.\n"
                       "To temporarily disable tracking, use command '-stop'")
        for keywords in self.searches:
            search_query = self.searches[keywords][0]
            await self.periodic_tasks(ctx, search_query)

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
        self.searches.update({keyword: (new_query, Queue())})

        await self.bot.wait_until_ready()
        await self.periodic_tasks(ctx, new_query)

    # Tracks Craigslist every 120 seconds for a specific search query.
    async def periodic_tasks(self, ctx, search_query):
        existing_backlog = self.searches[search_query.get_keyword()][1]

        while self.tracking.is_set():
            if not existing_backlog.empty():
                backlog = existing_backlog
            else:
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
        await ctx.send("Commands:\n\n"
                       "-search <keyword> <category>\n"
                       "Tracks Craigslist for a given keyword under a given category.\n"
                       "If no categories are specified, the search will run on the default category (all).\n\n"
                       "For a list of categories, run: "
                       "-help categories")


def setup(bot):
    bot.add_cog(Tracking(bot))
    bot.add_command(help)
