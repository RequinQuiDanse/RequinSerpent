import glob
import numpy as np
from bot import bot, discord, commands
from discord import Embed, ui, app_commands
from googletrans import Translator, constants
from pprint import pprint
import random
import csv
import time


@bot.command()
async def parle(ctx):
    print(glob.glob("playlist/*.csv")) 
    await ctx.reply('Un flip oui chef!')