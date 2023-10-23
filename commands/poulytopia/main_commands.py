from bot import bot, discord
from commands.poulytopia.sql_cmd import *
from commands.poulytopia.poule_prime import photoButton
from commands import puissance4
import requests
from datetime import datetime, timedelta
from random import randint
from unidecode import unidecode
con = create_connection(path=path)
cur = con.cursor()


@bot.tree.command(description="Montre ton poulailler"
)
async def poulailler(interaction: discord.Interaction, nom_du_fermier:str = None):
    """
    cmd to show your poulailler
    """
    now = datetime.now()
    await interaction.response.defer()
    if nom_du_fermier != None:
        # fermier_id = int(fermier_id.replace("<@", "").replace(">", ""))
        guild = bot.get_guild(interaction.guild.id)
        user = guild.get_member_named(nom_du_fermier)
        if user == None:
            user = guild.get_member(int(nom_du_fermier.replace("<@", "").replace(">", "")))
        avatar = user.avatar
        fermier_id = user.id
        
        embed = discord.Embed(title="Poulailler")
        poulailler = get_poulailler(cur, fermier_id)
        poulailler_data = get_poulailler_data(cur, fermier_id)
        if len(poulailler) != 0:
            poule = poulailler[0]
            embed, file = create_embed(title=f"**{poule['poule_name']}**", poule=poule, poule_place=[
                                    0, poulailler_data['amount']], avatar=avatar, fermier_id=fermier_id)

            await interaction.followup.send(file=file, embed=embed, view=Poulailler_Visite(poulailler, poulailler_data, fermier_id, avatar)
                                            )
        else:
            embed.add_field(name="Aucune poule", value="Aucune ")
            await interaction.followup.send(embed=embed
                                            )
    else:
        fermier_id = interaction.user.id
        avatar= interaction.user.avatar

        fermier_exist(cur, con, fermier_id, now)

        embed = discord.Embed(title="Poulailler")
        poulailler = get_poulailler(cur, fermier_id)
        poulailler_data = get_poulailler_data(cur, fermier_id)
        if len(poulailler) != 0:
            poule = poulailler[0]
            embed, file = create_embed(title=f"**{poule['poule_name']}**", poule=poule, poule_place=[
                                    0, poulailler_data['amount']], avatar=avatar, fermier_id=fermier_id)

            await interaction.followup.send(file=file, embed=embed, view=Poulailler_Buttons(poulailler, poulailler_data, fermier_id, avatar)
                                            )
        else:
            embed.add_field(name="Aucune poule", value="Aucune ")
            await interaction.followup.send(embed=embed
                                            )


@bot.tree.command(
    guild=discord.Object(id=769911179547246592), description="Ajoute une nouvelle poule"
)
async def create_poulee(
    interaction: discord.Interaction,
    poule_name: str,
    picture: discord.Attachment,
    tier: int = 1,
    family: str = None,
    price: int = None,
    production: int = None,
):
    """
    cmd to add poule to sql
    """
    await interaction.response.defer()

    if tier == 2:
        price = 350
        production = 10
    if price == None:
        price = round(randint(50, 250), -1)
    
    if production == None:
        production = randint(1,7)

    if interaction.user.id not in [533764434305351690, 379227572682227712]:
        return
    filename = unidecode(poule_name.casefold().replace(" ", "_")+".png")

    picture = requests.get(picture).content
    with open(f"commands/poulytopia/pictures/{filename}", "wb") as handler:
        handler.write(picture)

    res = create_poule(cur, con, poule_name, price, production, filename, tier, family)
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
    description="Tirage quotidien de poule"
)
async def tirage(interaction: discord.Interaction):
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
        if diff < 86400:
            return await interaction.followup.send(
                content=f"Prochain tirage à 18h, attends encore :)",
                ephemeral=True,
            )

    register_tirage(cur, con, fermier_id, now)
    poule = get_random_poule(cur, fermier_id)

    embed, file = create_embed(
        title=f"**{poule['poule_name']}**", poule=poule, avatar=interaction.user.avatar, fermier_id=fermier_id)

    await interaction.followup.send(
        file=file, embed=embed, ephemeral=True, view=Daily_Button(poule, fermier_id)
    )


@bot.tree.command(
    description="Marché quotidien de poule"
)
async def magazin(interaction: discord.Interaction):
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
        if self.fermier_id != interaction.user.id:
            return
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
        if self.fermier_id != interaction.user.id:
            return
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

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.blurple)
    async def edit(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        await interaction.response.defer()

        poule = self.poulailler[self.poule_place]
        path = poule["path"]
        new_path = path[:-4:]+"_edit"+str(randint(0,1000))+path[-4::]
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            view=photoButton(path=path, new_path = new_path, poule=poule, fermier_id = self.fermier_id, cur=cur, con=con, trade_id=poule['trade_id']),
        )

    @discord.ui.button(label="Vendre", style=discord.ButtonStyle.danger)
    async def sell(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        await interaction.response.defer()
        poule = self.poulailler[self.poule_place]
        sell_poule(cur, con, self.fermier_id, poule['poule_name'])
        price = randint(round(poule['price']*0.75), round(poule['price']*1.25))
        gain_money(cur, con, self.fermier_id, price)
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
            value=f"**{price}**🥚"
        )
        embed.add_field(
            name="Oeufs total:",
            value=f"{actuel_money}🥚"
        )
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=embed,
            attachments=[],
            view=BackToPoulailler(self.fermier_id),
        )

    @discord.ui.button(label="Récolte d'🥚", style=discord.ButtonStyle.green)
    async def take_oeufs(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        await interaction.response.defer()
        now = datetime.now()

        oeufs_produits, taxes = get_last_harvest(cur, con, self.fermier_id, now)

        embed = discord.Embed(title=f"Résultat de la récolte d'oeufs")
        embed.add_field(name="Nombre d'oeufs produits:",
                        value=f"**{oeufs_produits}**🥚")
        embed.add_field(name="Prix de l'entretien du poulailler:",
                        value=f"**{taxes}**🥚")
        embed.add_field(name="Nombre d'oeufs récupérés:",
                        value=f"**{round(oeufs_produits-taxes)}**🥚")
        embed.set_footer(text="Le coût de l'entretien du poulailler dépend de la taille du poulailler.\n Pour plus de détail: y=⁅(𝑥/8)^2 𝑥⋅c⁆ avec x le niveau du poulailler et c le nb d'heures depuis dernier entretien")
        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed,
                                                 view=None, attachments=[]
                                                )

    @discord.ui.button(label=f"Monter de niveau", style=discord.ButtonStyle.green)
    async def lvl_upp(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        await interaction.response.defer()
        fermier_lvl = get_fermier_lvl(cur, self.fermier_id)
        embed = discord.Embed(title="Monter de niveau")
        embed.add_field(name="Prix", value=str(fermier_lvl*100)+"🥚")
        embed.add_field(name="Avantage",
                        value="Augmente de 1 la taille de ton poulailler")
        embed.add_field(name="Désavantage:",
                        value=f"Prix entretien sur 24h:\nMaintenant: {round(24 * fermier_lvl * (int(fermier_lvl/8)**2))}🥚\nAprès:{round(24 * (fermier_lvl+1) * (int((fermier_lvl+1)/8)**2))}🥚")
        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=Lvl_Up_Button(fermier_lvl, self.fermier_id, self.avatar), attachments=[]
                                                )
    @discord.ui.button(label="Améliorer la production de la poule", style=discord.ButtonStyle.green)
    async def upgrade(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        await interaction.response.defer()

        poule = self.poulailler[self.poule_place]
        production = poule["production"]
        embed = discord.Embed(title="Améliorer la production")
        embed.add_field(name="Prix", value=str(production*115)+"🥚")
        embed.add_field(name="Avantage",
                        value="Améliore définitivement de 1 la production de ta poule")
        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=Lvl_Up_Poule_Button(self.fermier_id, self.avatar, poule), attachments=[]
                                                )

    @discord.ui.button(label=f"Statistiques", style=discord.ButtonStyle.green)
    async def stats(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        await interaction.response.defer()

        embed = embed_for_stats(self.fermier_id, interaction.user.avatar)

        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=BackToPoulailler(self.fermier_id), attachments=[])

@bot.tree.command(
    description="Permet de parier des poules sur un puissance 4"
)
async def parier(interaction: discord.Interaction, adversaire:str):
    """"""
    await interaction.response.defer()
    now = datetime.now()
    fermier_id = interaction.user.id
    fermier_exist(cur, con, fermier_id, now)

    last_parie = get_last_pari(cur, fermier_id)
    if last_parie != "0":
        last_parie = datetime.strptime(last_parie, "%Y-%m-%d %H:%M:%S.%f")
        diff = (now - last_parie).total_seconds()
        if diff < 86400:
            return await interaction.followup.send(
                content=f"Un seul pari par jour, prochain pari à 18h :)",
                ephemeral=True,
            )

    guild = bot.get_guild(interaction.guild.id)
    adversaire_ = guild.get_member_named(adversaire)
    if adversaire_ == None:
        adversaire_ = guild.get_member(int(adversaire.replace("<@", "").replace(">", "")))

    embed = discord.Embed(title=f"{interaction.user.name} défie {adversaire_.name}", description=f"{adversaire_.name} va-t-il se défiler??")
    await interaction.followup.send(embed=embed, view = ChooseWhichPari([interaction.user, adversaire_]))

@bot.tree.command(
    description="Classement des meilleurs poulaillers"
)
async def poulaillers_classement(interaction: discord.Interaction):
    """
    cmd to classment
    """
    await interaction.response.defer()

    fermier_data = get_fermiers_data(cur)
    embed = discord.Embed(title="Classement des fermiers")
    print(fermier_data)
    i = 1
    guild = bot.get_guild(interaction.guild.id.id)
    print(guild)
    for fermier in fermier_data:
        try:
            user = guild.get_member(fermier['fermier_id'])
            print(user)
            embed.add_field(name=f"{i}. "+user.name, value=f"Niveau: {fermier['level']}, Oeufs: {fermier['oeufs']}")
            i+=1
        except:
            pass

    await interaction.followup.send(
        embed=embed, ephemeral=False
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
        if self.fermier_id != interaction.user.id:
            return
        await interaction.response.defer()
        now = datetime.now()
        res = add_poule(cur, con, self.poule["poule_name"], self.fermier_id, now, self.poule["path"], self.poule["production"])
        if type(res) == str:
            embed, file = create_embed(title=f"Poulailller plus place! Lvl up vite pour récupérer ta poule",
                                       poule=self.poule, avatar=interaction.user.avatar, fermier_id=self.fermier_id)
            return await interaction.followup.edit_message(
                message_id=interaction.message.id,
                attachments=[file],
                embed=embed,
                view=self,
            )

        embed, file = create_embed(
            title=f"Tu as gagné {self.poule['poule_name']} :)", poule=self.poule, avatar=interaction.user.avatar, fermier_id=self.fermier_id)

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
        if self.fermier_id != interaction.user.id:
            return
        await interaction.response.defer()
        poule = self.market[self.poule_place]
        now = datetime.now()
        res = buy_poule(cur, con, self.fermier_id, poule, now, poule['path'])
        if type(res) == str:
            return await interaction.followup.edit_message(
                message_id=interaction.message.id,
                attachments=[],
                embed=None,
                view=BackToPoulailler(self.fermier_id),
                content=res
            )

        embed, file = create_embed(
            title=f"Tu as acheté la poule {poule['poule_name']} :)", poule=poule, avatar=interaction.user.avatar, fermier_id=self.fermier_id)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            attachments=[file],
            embed=embed,
            view=None,
        )

    @discord.ui.button(label="⬅", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
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
        if self.fermier_id != interaction.user.id:
            return
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


def create_embed(title, poule, fermier_id, poule_place=None, avatar=None, path=None):
    if path==None:
        path=poule["path"]

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
    
    embed.set_image(url=f"attachment://{path}")
    file = discord.File(
        f"commands/poulytopia/pictures/{path}",
        filename=path,
    )
    if poule['family'] != None:
        embed.add_field(name=f"Famille {poule['family']}", value='')
    if avatar is not None:
        embed.set_thumbnail(url=avatar)
    if poule_place is not None:
        embed.set_footer(
            text=f"{poule_place[0]+1}/{poule_place[1]} poules      \n Niveau du poulailler:{poulailler_lvl}       Oeufs:{actuel_money}🥚")
    return embed, file


def embed_for_stats(fermier_id, avatar):
    fermier_lvl = get_fermier_lvl(cur, fermier_id)
    poulailler_data = get_poulailler_data(cur, fermier_id)
    embed = discord.Embed(title="Stats du poulailler")
    embed.add_field(name="Nombre de poules", value=str(poulailler_data['amount'])+"🐔")
    embed.add_field(name="Valeur des poules", value=str(poulailler_data['value'])+"🥚")
    embed.add_field(name="Production des poules sur 24 heures", value=str(poulailler_data['production']*24)+"🥚")
    embed.add_field(name="Prix de l'entretien des poules sur 24 heures", value=str(round(24 * fermier_lvl * (int(fermier_lvl/8)**2)))+"🥚")
    embed.add_field(name="Poules familialles", value=poulailler_data['family_amount'])
    print(poulailler_data["families"])
    families = {}
    for el in poulailler_data['families']:
        if not el in families.keys():
            families[el] = 1
        else:
            families[el] += 1
    families_string = ""
    for el in families.items():
        families_string += f"{el[0][0]}: {el[1]}\n"
    embed.add_field(name = "Compte des familles", value=families_string)
    embed.set_thumbnail(url=avatar)
    return embed

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
        if self.fermier_id != interaction.user.id:
            return
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

class Lvl_Up_Poule_Button(discord.ui.View):
    """
    to lv u^
    """

    def __init__(self, fermier_id, avatar, poule):
        super().__init__()
        self.fermier_id = fermier_id
        self.avatar = avatar
        self.poule = poule

    @discord.ui.button(label="Améliorer la poule", style=discord.ButtonStyle.gray)
    async def lvl_up_poule(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.fermier_id != interaction.user.id:
            return
        await interaction.response.defer()
        production = self.poule['production']
        if get_fermier_oeufs(cur, self.fermier_id) < production*115:
            return await interaction.followup.edit_message(
                message_id=interaction.message.id,
                content="T'as pas assez d'argent boursemolle",
                embed=None,
                attachments=[],
                view=BackToPoulailler(self.fermier_id),
            )
        else:
            lose_money(cur, con, self.fermier_id, production*115)
            augmente_production_poule(cur, con, self.poule["trade_id"])

            embed = discord.Embed(
                title=f"Poule améliorée"
            )
            embed.add_field(
                name="Nouvelle production:",
                value=f"**{self.poule['production']+1}**",
            )
            await interaction.followup.edit_message(
                message_id=interaction.message.id,
                embed=embed,
                attachments=[],
                view=BackToPoulailler(self.fermier_id),
            )


class BackToPoulailler(discord.ui.View):
    """
    """
    def __init__(self, fermier_id):
        super().__init__()
        self.poulailler = get_poulailler(cur, fermier_id)
        self.poulailler_data = get_poulailler_data(cur, fermier_id)
        self.fermier_id = fermier_id

    @discord.ui.button(label="Poulailler", style=discord.ButtonStyle.green)
    async def back_to_poulailler(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        if self.fermier_id != interaction.user.id:
            return
        poulailler = get_poulailler(cur, self.fermier_id)
        poulailler_data = get_poulailler_data(cur, self.fermier_id)
        poule = poulailler[0]
        avatar = interaction.user.avatar
        embed, file = create_embed(title=f"**{poule['poule_name']}**", poule=poule, poule_place=[
                                    0, poulailler_data['amount']], avatar=avatar, fermier_id=self.fermier_id)
        await interaction.followup.edit_message(message_id=interaction.message.id, attachments=[file], embed=embed, view=Poulailler_Buttons(poulailler, poulailler_data, self.fermier_id, avatar)
                                        )
        

class Poulailler_Visite(discord.ui.View):
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
                                   self.poule_place, self.poulailler_data['amount']], avatar=self.avatar, fermier_id=self.fermier_id)

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
                                   self.poule_place, self.poulailler_data['amount']], avatar=self.avatar, fermier_id=self.fermier_id)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            attachments=[file],
            embed=embed,
            view=self,
        )

    @discord.ui.button(label=f"Statistiques", style=discord.ButtonStyle.green)
    async def stats(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        await interaction.response.defer()
        embed = embed_for_stats(self.fermier_id, self.avatar)
        await interaction.followup.edit_message(message_id=interaction.message.id, embed=embed, view=BackToPoulailler(self.fermier_id), attachments=[])

class PariSelect(discord.ui.Select):
    """
    create a select with the list of poules of the user
    """
    def __init__(self, adversaires, bet_poule:list):
        self.adversaires = adversaires
        self.bet_poule = bet_poule
        user_poulailler = get_poulailler(cur, adversaires[len(bet_poule)].id)
        user_poulailler_clear = []
        for el in user_poulailler:
            if el not in user_poulailler_clear:
                user_poulailler_clear.append(el)    

        options = [
            discord.SelectOption(
                label=poule['poule_name'], description=f"prix: {poule['price']}; prod: {poule['production']}")
                for poule in user_poulailler_clear
        ]
        text = ['Choisis la poule que tu paries', 'choisis la poule que tu veux gagner']
        super().__init__(placeholder=text[len(bet_poule)],
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.adversaires[0].id:
            return
        self.bet_poule.append(self.values[0])
        if len(self.bet_poule) == 2:

            embed = discord.Embed(title=f"{self.adversaires[0].name} défie {self.adversaires[1].name}", description=f"{self.adversaires[1].name}, acceptes tu le défi??")
            embed.add_field(name=f"Poule que {self.adversaires[0].name} pari:", value=self.bet_poule[0])
            embed.add_field(name=f"Poule que {self.adversaires[0].name} veut gagner:", value=self.bet_poule[1])
            await interaction.response.edit_message(embed=embed, view=AcceptPari(self.adversaires, self.bet_poule))
        else:
            await interaction.response.edit_message(view=ParierSelectView(self.adversaires, self.bet_poule))

class ParierSelectView(discord.ui.View):
    def __init__(self, adversaires, bet_poule):
        super().__init__()
        self.add_item(PariSelect(adversaires, bet_poule))

class AcceptPari(discord.ui.View):
    """
    """
    def __init__(self, adversaires, poule_bet):
        super().__init__()
        self.adversaires = adversaires
        self.poule_bet = poule_bet

    @discord.ui.button(label="Accepter le défi ⚠", style=discord.ButtonStyle.green)
    async def accept_defi(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.adversaires[1].id:
            return
        
        register_pari(cur, con, self.adversaires[0].id, datetime.now())
        register_pari(cur, con, self.adversaires[1].id, datetime.now())
        plateau = f"**🔴 {self.adversaires[0].name} VERSUS {self.adversaires[1].name} 🟡**\n\n"
        plateau += f"\t{puissance4.LETTERS}\n\t{puissance4.BLACK_CASE*7}\n\t{puissance4.BLACK_CASE*7}\n\t{puissance4.BLACK_CASE*7}\n\t{puissance4.BLACK_CASE*7}\n\t{puissance4.BLACK_CASE*7}\n\t{puissance4.BLACK_CASE*7}"
    
        await interaction.response.edit_message(content = plateau, embed = None, view=puissance4.Power4_Buttons(self.adversaires[0].id, self.adversaires[1].id, self.adversaires[0].name, self.adversaires[1].name, self.poule_bet)
                                        )

class ArgentSelect(discord.ui.Select):
    """
    create a select with the list of poules of the user
    """
    def __init__(self, adversaires):
        self.adversaires = adversaires

        options = [
            discord.SelectOption(
                label=i*100)
                for i in range(24)
        ]

        super().__init__(placeholder='Choisis l\'argent que tu paris',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.adversaires[0].id:
            return
        
        bet = int(self.values[0])
        user_money = get_my_money(cur, self.adversaires[0].id)
        adversaire_money = get_my_money(cur, self.adversaires[1].id)
        if not (user_money >= bet and adversaire_money >= bet):
            await interaction.response.edit_message(content="Vous n'avez pas assez d'argent pour parier des oeufs", view=None, embed=None)

        embed = discord.Embed(title=f"{self.adversaires[0].name} défie {self.adversaires[1].name}", description=f"{self.adversaires[1].name}, acceptes tu le défi??")
        embed.add_field(name=f"Le pari est de {bet}🥚 qui seront remportés par le vainqueur", value='')

        await interaction.response.edit_message(embed=embed, view=AcceptPari(self.adversaires, bet))


class ParierArgentSelectView(discord.ui.View):
    def __init__(self, adversaires):
        super().__init__()
        self.add_item(ArgentSelect(adversaires))

class ChooseWhichPari(discord.ui.View):
    """
    """
    def __init__(self, adversaires):
        super().__init__()
        self.adversaires = adversaires

    @discord.ui.button(label="Parier une poule", style=discord.ButtonStyle.green)
    async def defi_poule(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.adversaires[0].id:
            return

    
        embed = discord.Embed(title=f"{self.adversaires[0].name} défie {self.adversaires[1].name}", description=f"{self.adversaires[1].name} va-t-il se défiler??")
        await interaction.followup.send(embed=embed, view = ParierSelectView(self.adversaires, []))

        
    @discord.ui.button(label="Parier un tirage gratuit", style=discord.ButtonStyle.green)
    async def defi_tirage(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.adversaires[0].id:
            return

        embed = discord.Embed(title=f"{self.adversaires[0].name} défie {self.adversaires[1].name}", description=f"{self.adversaires[1].name}, acceptes tu le défi??")
        embed.add_field(name=f"Le gagnant remporte un tirage gratuit. Le perdant ne perd rien.", value="")
        await interaction.response.edit_message(embed=embed, view=AcceptPari(self.adversaires, "tirage"))
                
    @discord.ui.button(label="Parier des oeufs", style=discord.ButtonStyle.green)
    async def defi_argent(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.adversaires[0].id:
            return

        embed = discord.Embed(title=f"{self.adversaires[0].name} défie {self.adversaires[1].name}", description=f"{self.adversaires[1].name}, acceptes tu le défi??")
        embed.add_field(name=f"Le gagnant remporte l'argent de l'autre", value="")
        await interaction.response.edit_message(embed=embed, view=ParierArgentSelectView(self.adversaires))
        
