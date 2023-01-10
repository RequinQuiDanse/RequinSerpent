import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = discord.ext.commands.Bot(command_prefix=',', intents=intents)

