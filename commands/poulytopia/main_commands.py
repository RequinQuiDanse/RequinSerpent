from bot import bot, discord
from commands.poulytopia.sql_cmd import *
import requests
from datetime import datetime, timedelta

con = create_connection(path=path)
cur = con.cursor()


@bot.tree.command(
    guild=discord.Object(id=769911179547246592), description="Montre ton poulailler"
)
async def poulailler(interaction: discord.Interaction):
    """
    cmd to show your poulailler
    """
    now = datetime.now()
    await interaction.response.defer()
    fermier_id = interaction.user.id
    fermier_exist(cur, con, fermier_id, now)

    embed = discord.Embed(title="Ton poulailler")
    poulailler = get_poulailler(cur, fermier_id)
    poulailler_data = get_poulailler_data(cur, fermier_id)
    if len(poulailler) != 0:
        poule = poulailler[0]
        embed, file = create_embed(title=f"**{poule['poule_name']}**", poule=poule, poule_place=[
                                   0, poulailler_data['amount']], avatar=interaction.user.avatar, fermier_id=fermier_id)

        await interaction.followup.send(file=file, embed=embed, view=Poulailler_Buttons(poulailler, poulailler_data, fermier_id, interaction.user.avatar)
                                        )
    else:
        embed.add_field(name="Tu n'as aucune poule", value="Aucune ")
        await interaction.followup.send(embed=embed
                                        )


@bot.tree.command(
    guild=discord.Object(id=769911179547246592), description="Ajoute une nouvelle poule"
)
async def create_poulee(
    interaction: discord.Interaction,
    poule_name: str,
    price: int,
    production: int,
    picture: discord.Attachment,
):
    """
    cmd to add poule to sql
    """
    await interaction.response.defer()

    if interaction.user.id not in [533764434305351690, 379227572682227712]:
        return
    filename = picture.filename
    picture = requests.get(picture).content
    with open(f"commands/poulytopia/pictures/{filename}", "wb") as handler:
        handler.write(picture)

    res = create_poule(cur, con, poule_name, price, production, filename)
    if res != None:
        embed = discord.Embed(title=f"{poule_name}")
        embed.add_field(name="Prix de la poule:", value=f"**{price}**🥚")
        embed.add_field(
            name="Production journalière de la poule d'oeufs:",
            value=f"**{production}**🥚",
        )
        embed.set_image(url=f"attachment://{filename}")
        file = discord.File(
            f"commands/poulytopia/pictures/{filename}", filename=filename
        )
        await interaction.followup.send(
            content="La boule a bien été ajoutée :)", ephemeral=True, embed=embed, file=file
        )
    else:
        await interaction.followup.send(
            content="La poule a été renversée sur la route:(", ephemeral=True
        )


@bot.tree.command(
    guild=discord.Object(id=769911179547246592), description="Tirage quotidien de poule"
)
async def daily_poule(interaction: discord.Interaction):
    """
    cmd to daily chance to get a poule
    """
    now = datetime.now()
    await interaction.response.defer()
    fermier_id = interaction.user.id
    fermier_exist(cur, con, fermier_id, now)

    last_tirage = get_last_tirage(cur, fermier_id)
    if last_tirage != "0":
        last_tirage = datetime.strptime(last_tirage, "%Y-%m-%d %H:%M:%S.%f")
        diff = (now - last_tirage).total_seconds()
        if diff < 3600:
            return await interaction.followup.send(
                content=f"Le dernier tirage de date que de {round(diff/60)} minutes, attends encore :)",
                ephemeral=True,
            )

    register_tirage(cur, con, fermier_id, now)
    poule = get_random_poule(cur)

    embed, file = create_embed(
        title=f"**{poule['poule_name']}**", poule=poule, avatar=interaction.user.avatar, fermier_id=fermier_id)

    await interaction.followup.send(
        file=file, embed=embed, ephemeral=True, view=Daily_Button(poule, fermier_id)
    )


@bot.tree.command(
    guild=discord.Object(id=769911179547246592), description="Tirage quotidien de poule"
)
async def marketplace(interaction: discord.Interaction):
    """
    cmd to daily market
    """
    now = datetime.now()
    await interaction.response.defer()
    fermier_id = interaction.user.id
    fermier_exist(cur, con, fermier_id, now)

    last_market = get_last_market(cur)
    last_market = datetime.strptime(last_market, "%Y-%m-%d %H:%M:%S.%f")
    diff = (now - last_market).total_seconds()

    if diff > 86400:
        register_market(cur, con, now)

    market = get_market(cur)
    poule = market[0]
    embed, file = create_embed(
        title=f"**{poule['poule_name']}**", poule=poule, poule_place=[0, 5], fermier_id=fermier_id)

    await interaction.followup.send(
        file=file, embed=embed, ephemeral=True, view=Market_Buttons(market, fermier_id)
    )


class Poulailler_Buttons(discord.ui.View):
    """
    create all the buttons
    """

    def __init__(self, poulailler, poulailler_data, fermier_id, avatar):
        super().__init__()
        self.poulailler = poulailler
        self.poule_place = 0
        self.poulailler_data = poulailler_data
        self.fermier_id = fermier_id
        self.avatar = avatar

    @discord.ui.button(label="⬅", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        await interaction.response.defer()
        self.poule_place -= 1
        if self.poule_place < 0:
            self.poule_place = len(self.poulailler)-1
        poule = self.poulailler[self.poule_place]

        embed, file = create_embed(title=f"**{poule['poule_name']}**", poule=poule, poule_place=[
                                   self.poule_place, self.poulailler_data['amount']], avatar=interaction.user.avatar, fermier_id=self.fermier_id)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            attachments=[file],
            embed=embed,
            view=self,
        )

    @discord.ui.button(label="➡", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        await interaction.response.defer()
        self.poule_place += 1
        if self.poule_place >= len(self.poulailler):
            self.poule_place = 0
        poule = self.poulailler[self.poule_place]

        embed, file = create_embed(title=f"**{poule['poule_name']}**", poule=poule, poule_place=[
                                   self.poule_place, self.poulailler_data['amount']], avatar=interaction.user.avatar, fermier_id=self.fermier_id)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            attachments=[file],
            embed=embed,
            view=self,
        )

    @discord.ui.button(label="Vendre", style=discord.ButtonStyle.danger)
    async def sell(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        await interaction.response.defer()
        poule = self.poulailler[self.poule_place]
        sell_poule(cur, con, self.fermier_id, poule['poule_name'])
        gain_money(cur, con, self.fermier_id, poule['price'])
        actuel_money = get_my_money(cur, self.fermier_id)

        embed = discord.Embed(
            title=f"**Transaction effectuée**"
        )
        embed.add_field(
            name="Poule vendue:",
            value=f"**{poule['poule_name']}**",
        )
        embed.add_field(
            name="Oeufs gagné:",
            value=f"**{poule['price']}**🥚"
        )
        embed.add_field(
            name="Oeufs total:",
            value=f"{actuel_money}🥚"
        )
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=embed,
            attachments=[],
            view=None
        )

    @discord.ui.button(label="Récolte d'🥚", style=discord.ButtonStyle.green)
    async def take_oeufs(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        await interaction.response.defer()
        now = datetime.now()

        last_harvest = get_last_harvest(cur, self.fermier_id)
        last_harvest = datetime.strptime(last_harvest, "%Y-%m-%d %H:%M:%S.%f")
        diff = (now - last_harvest).total_seconds()
        hours = diff//3600
        oeufs_produits = 0
        if hours > 0:
            poule_prod = self.poulailler_data['production']
            oeufs_produits += poule_prod * hours
            now = now - timedelta(seconds=diff % 3600)
            register_harvest(cur, con, self.fermier_id, now)
        embed = discord.Embed(title=f"Résultat de la récolte d'oeufs")
        embed.add_field(name="Nombre d'oeufs récupérés:",
                        value=f"**{oeufs_produits}**🥚 produits en {round(hours)} heures et {round(diff%3600/60)}minutes")
        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=None, attachments=[]
                                                )

    @discord.ui.button(label=f"Monter de niveau", style=discord.ButtonStyle.green)
    async def lvl_upp(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        await interaction.response.defer()
        fermier_lvl = get_fermier_lvl(cur, self.fermier_id)
        embed = discord.Embed(title="Monter de niveau")
        embed.add_field(name="Prix", value=str(fermier_lvl*100)+"🥚")
        embed.add_field(name="Avantage",
                        value="Augmente de 1 la taille de ton poulailler")
        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=Lvl_Up_Button(fermier_lvl, self.fermier_id, self.avatar), attachments=[]
                                                )


class Daily_Button(discord.ui.View):
    """
    to gain a poule
    """

    def __init__(self, random_poule, fermier_id):
        super().__init__()
        self.poule = random_poule
        self.fermier_id = fermier_id

    @discord.ui.button(label="Prendre la poule", style=discord.ButtonStyle.green)
    async def prendre_poule(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        res = add_poule(cur, con, self.poule["poule_name"], self.fermier_id)
        if type(res) == str:
            embed, file = create_embed(title=f"Tu n'as plus de place dans le poulailler",
                                       poule=self.poule, avatar=interaction.user.avatar, fermier_id=self.fermier_id)
            return await interaction.followup.edit_message(
                message_id=interaction.message.id,
                attachments=[file],
                embed=embed,
                view=self,
            )

        embed, file = create_embed(
            title=f"Tu as gagné la poule {self.poule['poule_name']}:)", poule=self.poule, avatar=interaction.user.avatar, fermier_id=self.fermier_id)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            attachments=[file],
            embed=embed,
            view=None,
        )


class Market_Buttons(discord.ui.View):
    """
    to buy a poule
    """

    def __init__(self, market, fermier_id):
        super().__init__()
        self.market = market
        self.fermier_id = fermier_id
        self.poule_place = 0

    @discord.ui.button(label="Acheter la poule", style=discord.ButtonStyle.gray)
    async def buy_poulee(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        poule = self.market[self.poule_place]

        res = buy_poule(cur, con, self.fermier_id, poule)
        if type(res) == str:
            return await interaction.followup.edit_message(
                message_id=interaction.message.id,
                attachments=[],
                embed=None,
                view=None,
                content="Tu n'as plus de place dans le poulailler"
            )

        embed, file = create_embed(
            title=f"Tu as acheté la poule {poule['poule_name']}:)", poule=poule, avatar=interaction.user.avatar, fermier_id=self.fermier_id)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            attachments=[file],
            embed=embed,
            view=None,
        )

    @discord.ui.button(label="⬅", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        await interaction.response.defer()
        self.poule_place -= 1
        if self.poule_place < 0:
            self.poule_place = len(self.market)-1
        poule = self.market[self.poule_place]
        embed, file = create_embed(title=poule['poule_name'], poule=poule, poule_place=[
                                   self.poule_place, 5], fermier_id=self.fermier_id)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            attachments=[file],
            embed=embed,
            view=self,
        )

    @discord.ui.button(label="➡", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        await interaction.response.defer()
        self.poule_place += 1
        if self.poule_place >= len(self.market):
            self.poule_place = 0
        poule = self.market[self.poule_place]
        embed, file = create_embed(title=poule['poule_name'], poule=poule, poule_place=[
                                   self.poule_place, 5], fermier_id=self.fermier_id)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            attachments=[file],
            embed=embed,
            view=self,
        )


def create_embed(title, poule, fermier_id, poule_place=None, avatar=None):
    embed = discord.Embed(
        title=title
    )
    embed.add_field(name="Prix de la poule:",
                    value=f"**{poule['price']}**🥚")
    embed.add_field(
        name="Production journalière de la poule d'oeufs:",
        value=f"**{poule['production']}**🥚",
    )
    actuel_money = get_my_money(cur, fermier_id)

    poulailler_lvl = get_fermier_lvl(cur, fermier_id)

    embed.set_image(url=f"attachment://{poule['path']}")
    file = discord.File(
        f"commands/poulytopia/pictures/{poule['path']}",
        filename=poule["path"],
    )
    if avatar is not None:
        embed.set_thumbnail(url=avatar)
    if poule_place is not None:
        embed.set_footer(
            text=f"{poule_place[0]+1}/{poule_place[1]} poules      \n Niveau du poulailler:{poulailler_lvl}       Oeufs:{actuel_money}🥚")
    return embed, file


class Lvl_Up_Button(discord.ui.View):
    """
    to lv u^
    """

    def __init__(self, fermier_lvl, fermier_id, avatar):
        super().__init__()
        self.fermier_lvl = fermier_lvl
        self.fermier_id = fermier_id
        self.avatar = avatar

    @discord.ui.button(label="Monter de niveau", style=discord.ButtonStyle.gray)
    async def lvl_up(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        res = lvl_up_fermier(cur, con, self.fermier_lvl, self.fermier_id)
        if type(res) == str:
            return await interaction.followup.edit_message(
                message_id=interaction.message.id,
                attachments=[],
                embed=None,
                view=None,
                content="T'as pas assez d'oeufs bouffon"
            )

        actuel_money = get_my_money(cur, self.fermier_id)
        embed = discord.Embed(title="GG tu as monté de niveau ton poulailler")
        embed.add_field(name="Niveau actuelle", value=self.fermier_lvl+1)
        embed.add_field(name="Oeufs restant", value=actuel_money)
        embed.set_thumbnail(url=self.avatar)
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            attachments=[],
            embed=embed,
            view=None,
        )
