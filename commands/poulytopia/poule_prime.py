from bot import discord, bot
import random
from wand.image import Image
import os
from commands.poulytopia import main_commands
class photoButton(discord.ui.View):
    """
    create all the buttons that permit to do edits on a pic
    """
    def __init__(self, path, poule, fermier_id):
        super().__init__()
        # self.image_mobile = image
        self.path = "commands/poulytopia/pictures/"+path
        self.poule = poule
        self.fermier_id = fermier_id
        
    @discord.ui.button(label='Black&White', style=discord.ButtonStyle.gray)
    async def Edge(self, interaction: discord.Interaction, button: discord.ui.Button):
        print(self.path)
        with Image(filename=self.path) as img:
            img.transform_colorspace('gray')
            img.edge(radius=1)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Reliefs', style=discord.ButtonStyle.grey)
    async def Emboss(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.transform_colorspace('gray')
            img.emboss(radius=3.0, sigma=1.75)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Shade', style=discord.ButtonStyle.grey)
    async def Shade(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.shade(gray=True,
                      azimuth=286.0,
                      elevation=45.0)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Spread', style=discord.ButtonStyle.grey)
    async def Spread(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.spread(radius=8.0)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Charcoal', style=discord.ButtonStyle.grey)
    async def Charcoal(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.charcoal(radius=1.5, sigma=0.5)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Matrix', style=discord.ButtonStyle.grey)
    async def Matrix(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            matrix = [[0, 0, 1],
                      [0, 1, 0],
                      [1, 0, 0]]
            img.color_matrix(matrix)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Polaroid', style=discord.ButtonStyle.grey)
    async def Polaroid(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.polaroid()
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Sketch', style=discord.ButtonStyle.grey)
    async def Sketch(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.transform_colorspace("gray")
            img.sketch(0.5, 0.0, 98.0)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Solarize', style=discord.ButtonStyle.grey)
    async def Solarize(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.solarize(threshold=0.5 * img.quantum_range)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Swirl', style=discord.ButtonStyle.grey)
    async def Swirl(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.swirl(degree=-90)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Tint', style=discord.ButtonStyle.grey)
    async def Tint(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.tint(color="green", alpha="rgb(40%, 60%, 80%)")
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Adaptive Threshold', style=discord.ButtonStyle.grey)
    async def Adaptive_Threshold(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.transform_colorspace('gray')
            img.adaptive_threshold(width=16, height=16,
                                   offset=-0.08 * img.quantum_range)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Random threeshole', style=discord.ButtonStyle.grey) #Threshold
    async def Random_threeshole(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.transform_colorspace('gray')
            img.random_threshold(low=0.3 * img.quantum_range,
                         high=0.6 * img.quantum_range)
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)


    @discord.ui.button(label='Colorize', style=discord.ButtonStyle.grey)
    async def Colorize(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image_mobile) as img:
            img.colorize(color="blue", alpha="rgb(10%, 0%, 20%)")
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)

    @discord.ui.button(label='Reset', style=discord.ButtonStyle.green)
    async def Reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        with Image(filename=self.image) as img:
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)


    @discord.ui.button(label='Fini', style=discord.ButtonStyle.green)
    async def Fini(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        with Image(filename=self.image_mobile) as img:
            new_path = self.path[:-4:]+"_edit"+self.path[-4::]
            img.save(filename=new_path)
            self.image_mobile = new_path
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(new_path)], embed=embed)
            #os.remove(f"photo-{self.idImage}.jpg")
