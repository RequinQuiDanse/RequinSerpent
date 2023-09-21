from bot import bot, discord
from wand.image import Image
import random
# https://docs.wand-py.org/en/0.6.7/index.html
import os

class guildSelect(discord.ui.Select):
    """
    create a select with a list of ppl preregistred. permit the user to select avatar from someone
    """
    def __init__(self):

        options = [
            discord.SelectOption(
                label='533764434305351690', description='Adam'),
            discord.SelectOption(
                label='247027162853539841', description='Fanny'),
            discord.SelectOption(
                label='780181339529674783', description='Isack'),
            discord.SelectOption(
                label='658694225008918529', description='Lyrian'),
            discord.SelectOption(label='379227572682227712',
                                 description='Mathias'),
            discord.SelectOption(
                label='666683391311085589', description='Mathis'),
            discord.SelectOption(
                label='888076017103671330', description='Nolan'),
            discord.SelectOption(
                label='712368494846672957', description='Samuel'),
            discord.SelectOption(
                label='656561010358091777', description='Sarah'),
            discord.SelectOption(
                label='666880865984315415', description='Thayan'),
            discord.SelectOption(
                label='453869081662193686', description='Tym'),
            discord.SelectOption(
                label='537369335585439754', description='Yanis'),
            discord.SelectOption(
                label='549248069447843850', description='Slev'),
        ]

        super().__init__(placeholder='Choisis ta cible',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = bot.get_guild(769911179547246592)
        x = await guild.fetch_member(self.values[0])
        avatar = str(x.avatar)
        embed = discord.Embed(color = discord.Colour.dark_magenta(), title= x.name).    mage(url=avatar)
        await interaction.response.send_message(embed=embed, view=photoButton(x))


class guildSelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(guildSelect())

class photoButton(discord.ui.View):
    """
    create all the buttons that permit to do edits on a pic
    """
    def __init__(self, x):
        super().__init__()
        self.avatar = str(x.avatar)
        self.avatarMobile = str(x.avatar)
        self.idImage = random.randrange(0,30)
        self.name = x.name
        #f"photo-{self.idImage}.jpg" = f"photo-{self.idImage}.jpg"
        #f"attachment://photo-{self.idImage}.jpg" = f"attachment://photo-{self.idImage}.jpg"
        
    @discord.ui.button(label='Black&White', style=discord.ButtonStyle.gray)
    async def Edge(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.transform_colorspace('gray')
            img.edge(radius=1)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Reliefs', style=discord.ButtonStyle.grey)
    async def Emboss(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.transform_colorspace('gray')
            img.emboss(radius=3.0, sigma=1.75)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Shade', style=discord.ButtonStyle.grey)
    async def Shade(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.shade(gray=True,
                      azimuth=286.0,
                      elevation=45.0)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Spread', style=discord.ButtonStyle.grey)
    async def Spread(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.spread(radius=8.0)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Charcoal', style=discord.ButtonStyle.grey)
    async def Charcoal(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.charcoal(radius=1.5, sigma=0.5)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Matrix', style=discord.ButtonStyle.grey)
    async def Matrix(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            matrix = [[0, 0, 1],
                      [0, 1, 0],
                      [1, 0, 0]]
            img.color_matrix(matrix)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Polaroid', style=discord.ButtonStyle.grey)
    async def Polaroid(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.polaroid()
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Sketch', style=discord.ButtonStyle.grey)
    async def Sketch(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.transform_colorspace("gray")
            img.sketch(0.5, 0.0, 98.0)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Solarize', style=discord.ButtonStyle.grey)
    async def Solarize(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.solarize(threshold=0.5 * img.quantum_range)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Swirl', style=discord.ButtonStyle.grey)
    async def Swirl(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.swirl(degree=-90)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Tint', style=discord.ButtonStyle.grey)
    async def Tint(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.tint(color="green", alpha="rgb(40%, 60%, 80%)")
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Adaptive Threshold', style=discord.ButtonStyle.grey)
    async def Adaptive_Threshold(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.transform_colorspace('gray')
            img.adaptive_threshold(width=16, height=16,
                                   offset=-0.08 * img.quantum_range)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)

    @discord.ui.button(label='Random threeshole', style=discord.ButtonStyle.grey) #Threshold
    async def Random_threeshole(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.transform_colorspace('gray')
            img.random_threshold(low=0.3 * img.quantum_range,
                         high=0.6 * img.quantum_range)
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)


    @discord.ui.button(label='Colorize', style=discord.ButtonStyle.grey)
    async def Colorize(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatarMobile) as img:
            img.colorize(color="blue", alpha="rgb(10%, 0%, 20%)")
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments =[discord.File(f"photo-{self.idImage}.jpg")], embed= embed)

    @discord.ui.button(label='Reset', style=discord.ButtonStyle.green)
    async def Reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.avatar) as img:
            img.save(filename=f"photo-{self.idImage}.jpg")
            self.avatarMobile = f"photo-{self.idImage}.jpg"
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed)


    @discord.ui.button(label='Fini', style=discord.ButtonStyle.green)
    async def Fini(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        with Image(filename=self.avatarMobile) as img:
            img.save(filename=f"photo-{self.idImage}.jpg")
            embed = discord.Embed(title= self.name).set_image(url= f"attachment://photo-{self.idImage}.jpg")
            await interaction.response.edit_message(attachments=[discord.File(f"photo-{self.idImage}.jpg")], embed = embed, view= self)
            os.remove(f"photo-{self.idImage}.jpg")

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Jeu avec avatar")
async def avatar(interaction: discord.Interaction):
    """
    cmd that permit user to edit a picture with filters from wand module
    """
    await interaction.response.send_message("Choisis", view=guildSelectView(), ephemeral=True)
