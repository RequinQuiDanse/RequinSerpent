import re
from bs4 import BeautifulSoup
import requests
from bot import bot, discord, commands


class vidsButton(discord.ui.View):
    def __init__(self, query=str):
        super().__init__()
        self.add_item(discord.ui.Button(
            label='vids', url='https://inhumanity.com/plug/'+query))


@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Envoie une video x random et louche")
async def vids(interaction: discord.Interaction):

    ctx = await commands.Context.from_interaction(interaction)
    r = requests.get("https://inhumanity.com/random/")
    soup = BeautifulSoup(r.content, "html.parser")

    x = soup.find_all(class_="row meta")
    y = re.findall("https://inhumanity.com/plug/.*", str(x))
    result = re.findall('\d+', str(y))

    await ctx.channel.send(
        "vids", view=vidsButton(result[0])
    )