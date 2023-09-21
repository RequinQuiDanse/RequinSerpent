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
async def create_poulee(interaction: discord.Interaction, poule_name:str, price:int, production:int, picture:discord.Attachment):
    """
    cmd to add poule to sql
    """
    await interaction.response.defer()

    if interaction.user.id not in [533764434305351690, 379227572682227712]:
        return
    filename = picture.filename
    picture = requests.get(picture).content
    with open(f'commands/poulytopia/pictures/{filename}', 'wb') as handler:
        handler.write(picture)

    res = create_poule(cur, con, poule_name, price, production, filename)
    if res != None:
        await interaction.followup.send(content="La boule a bien été ajoutée :)", ephemeral=True)
    else:
        await interaction.followup.send(content="La poule a été renversée sur la route:(", ephemeral=True)

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
        if diff < 10:
            await interaction.response.send_message(content=f"Le dernier tirage de date que de {round(diff)} secondes, attends encore :)", ephemeral=True)
            return
    
    register_tirage(cur, con, fermier_id, now)
    random_poule = get_random_poule(cur)

    embed = discord.Embed(title=f"Tu as gagné la poule {random_poule[0]}:)").set_image(url = f"attachment://{random_poule[3]}")
    print(random_poule[3])
    file = discord.File(f"commands/poulytopia/pictures/{random_poule[3]}", filename=random_poule[3])

    await interaction.response.send_message(file=file, embed=embed, ephemeral=True, view=Daily_Button(random_poule))


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

class Daily_Button(discord.ui.View):
    """
    to gain a poule
    """
    def __init__(self, random_poule):
        super().__init__()
        self.poule_name = random_poule[0]
        self.poule_price = random_poule[1]
        self.poule_production = random_poule[2]
        self.poule_path = random_poule[3]

    @discord.ui.button(label='Next', style=discord.ButtonStyle.gray)
    async def prendre_poule(self, interaction: discord.Interaction):

        embed = discord.Embed(title=f"Tu as gagné la poule {self.poule_name}:)")
        embed.set_image(url= f"commands/poulytopia/pictures/{self.poule_path}")
        await interaction.response.edit_message(attachments=[discord.File(f"commands/poulytopia/pictures/{self.poule_path}")], embed = embed)
