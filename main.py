import os

from discord.ext import commands
from dotenv import load_dotenv

'''
For future reference, here's the documentation.
https://discordpy.readthedocs.io/en/stable/api.html#client
'''

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='-')
bot.remove_command('help')


@bot.event
async def on_ready():
    print('{} has connected to Discord.'.format(bot.user.name), flush=True)

if __name__ == '__main__':
    bot.load_extension('bot_commands')

bot.run(TOKEN)
