from bot import bot, discord
from sql_cmd import *

cur = create_connection(path=path).cursor()

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Montre ton poulailler")
async def poulailler(interaction: discord.Interaction):
    """
    cmd to show your poulailler
    """
    embed = discord.Embed(title="Ton poulailler")
    poulailler = get_poulailler(cur, interaction.user.id) #{poule_name, price, production, file_name}
    embed.set_image(url= f"attachment://commands/poulytopia/pictures/{poulailler['file_name']}.png")
    embed.add_field(name = poulailler["poule_name"], value=f"prix={poulailler['prix']}, production = {poulailler['production']}")
    await interaction.response.send_message(content="Tes poules", embed=embed)

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Ajoute une nouvelle poule")
async def add_poule(interaction: discord.Interaction, poule_name:str, price:int, production:int, file_name:str):
    """
    cmd to add poule to sql
    """
    if interaction.user.id not in [533764434305351690, 379227572682227712]:
        return
    
    res = add_poule(poule_name, price, production, file_name)
    if res != None:
        await interaction.response.send_message(content="La boule a bien été ajoutée :)", ephemeral=True)
    else:
        await interaction.response.send_message(content="La poule a été renversée sur la route:(", ephemeral=True)



class Poulailler_Buttons(discord.ui.View):
    """
    create all the buttons
    """
    def __init__(self, poulailler):
        super().__init__()
        self.poulailler = poulailler

    @discord.ui.button(label='Next', style=discord.ButtonStyle.gray)
    async def next(self, interaction: discord.Interaction):

        embed = discord.Embed(title="")
        embed.set_image(url= f"attachment://photo-{self.idImage}.jpg")
        await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)
