from bot import bot, discord
from commands.poulytopia.sql_cmd import *
import requests
from datetime import datetime
con = create_connection(path=path)
cur = con.cursor()

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Montre ton poulailler")
async def poulailler(interaction: discord.Interaction):
    """
    cmd to show your poulailler
    """
    fermier_id = interaction.user.id
    fermier_exist(cur, con, fermier_id)
    
    embed = discord.Embed(title="Ton poulailler")
    poulailler = get_poulailler(cur, fermier_id) #{poule_name, price, production, file_name}
    if len(poulailler) != 0:
        embed.set_image(url= f"attachment://commands/poulytopia/pictures/{poulailler['file_name']}.png")
        embed.add_field(name = poulailler["poule_name"], value=f"prix={poulailler['prix']}, production = {poulailler['production']}")
    else:
        embed.add_field(name="Tu n'as aucune poule", value="Aucune ")
    await interaction.response.send_message(content="Tes poules", embed=embed)

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Ajoute une nouvelle poule")
async def create_poulee(interaction: discord.Interaction, poule_name:str, price:int, production:int, file_name:str, picture:discord.Attachment):
    """
    cmd to add poule to sql
    """

    if interaction.user.id not in [533764434305351690, 379227572682227712]:
        return
    
    picture = requests.get(picture).content
    with open(f'commands/poulytopia/pictures/{file_name}.png', 'wb') as handler:
        handler.write(picture)

    res = create_poule(cur, con, poule_name, price, production, file_name)
    if res != None:
        await interaction.response.send_message(content="La boule a bien été ajoutée :)", ephemeral=True)
    else:
        await interaction.response.send_message(content="La poule a été renversée sur la route:(", ephemeral=True)

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Tirage quotidien de poule")
async def daily_poule(interaction: discord.Interaction):
    """
    cmd to daily chance to get a poule
    """
    fermier_id = interaction.user.id
    fermier_exist(cur, con, fermier_id)

    now = datetime.now()
    last_tirage = get_last_tirage(cur, fermier_id).fetchone()[0]
    last_tirage = datetime.strptime(last_tirage, "%Y-%m-%d %H:%M:%S.%f")
    if last_tirage!='0':
        diff = (now - last_tirage).total_seconds() 
        if diff < 3600:
            await interaction.response.send_message(content=f"Le dernier tirage de date que de {round(diff)} secondes, attends encore :)", ephemeral=True)
            return
    
    register_tirage(cur, con, fermier_id, now)
    random_poule = get_random_poule(cur)
    await interaction.response.send_message(content=random_poule, ephemeral=True)


# class Poulailler_Buttons(discord.ui.View):
#     """
#     create all the buttons
#     """
#     def __init__(self, poulailler):
#         super().__init__()
#         self.poulailler = poulailler

#     @discord.ui.button(label='Next', style=discord.ButtonStyle.gray)
#     async def next(self, interaction: discord.Interaction):

#         embed = discord.Embed(title="")
#         embed.set_image(url= f"attachment://photo-{self.idImage}.jpg")
#         await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)
