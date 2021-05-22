import os

import discord
from dotenv import load_dotenv

'''
For future reference, here's the documentation.
https://discordpy.readthedocs.io/en/stable/api.html#client
'''

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = discord.Client()

