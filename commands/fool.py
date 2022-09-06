import random
from bot import bot, discord, commands
import requests
from bs4 import BeautifulSoup
import re

choices = [
    "4k",     "bellevid",  "spank",
    "anal",    "bj",  "hentai", "lesbian",
    "animalears", "blowjob",  "feet",   "holo",  "lewd",   "pussy",
    "boobs",   "belle",  "laugh", "wallpapers",
]

class nsfSelect(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = [
            discord.SelectOption(
                label='Aléatoire', description='⠀'),
        ]
        super().__init__(placeholder="Quel chose veux tu?",
                         min_values=1, max_values=1, options=options)
        for choix in choices:
            self.add_option(label=choix, description="⠀")

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Aléatoire":
            self.values[0] = random.choice(choices)
        r = requests.get(
            f"http://api.nekos.fun:8080/api/{self.values[0]}")
        soup = BeautifulSoup(r.content, "html.parser")
        #y = re.findall('message.*color', str(soup))
        img = str(soup).replace("{\"image\":\"", "").replace("\"}", "")
        #await self.ctx.channel.send(content=img)
        await interaction.response.edit_message(content = img, view = nsfView(self.ctx))

class nsfView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.add_item(nsfSelect(ctx))


@bot.tree.command(guild=discord.Object(id=769911179547246592), description="Nsf")
async def nsf(interaction: discord.Interaction):
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message(content="nsf", view=nsfView(ctx), ephemeral=True)

choices2 = [
    "anal",
    "ass",
    "boobs",
    "erokemo",
    "fourk",
    "gonewild",
    "hentaiass",
    "hentai",
    "hmidriff",
    "hentaithigh",
    "kitsune",
    "lewd",
    "nekofeet",
    "nekopussy",
    "nekotits",
    "pgif",
    "pussy",
    "thigh",
    "solo",
    "wallpaper"]


class nsfwSelect(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = [
            discord.SelectOption(
                label='Aléatoire', description='⠀'),
        ]
        super().__init__(placeholder="Quel chose veux tu?",
                         min_values=1, max_values=1, options = options)
        for choix in choices2:
            self.add_option(label=choix, description="⠀")

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Aléatoire":
            self.values[0] = random.choice(choices2)
        print(self.values[0])
        r = requests.get(f"https://nekobot.xyz/api/image?type={self.values[0]}")
        soup = BeautifulSoup(r.content, "html.parser")
        img = re.findall('message.*color', str(soup))
        img = str(img).replace("['message\":\"", "").replace("\",\"color']", "")
        #await self.ctx.channel.send(content=y)
        await interaction.response.edit_message(content = img, view = nsfView(self.ctx))

class nsfwView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.add_item(nsfwSelect(ctx))

@bot.tree.command(guild=discord.Object(id =769911179547246592), description="Nsfw (lent à repondre)")
async def nsfw(interaction: discord.Interaction):
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message(content="nsfw", view=nsfwView(ctx), ephemeral=True)
    