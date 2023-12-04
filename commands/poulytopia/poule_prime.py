from bot import discord, bot
from random import randint
from wand.image import Image
import os
from commands.poulytopia import main_commands
class photoButton(discord.ui.View):
    """
    create all the buttons that permit to do edits on a pic
    """
    def __init__(self, path, poule, fermier_id, cur, con, trade_id, poule_place):
        super().__init__()
        # self.path = image

        if not "edit" in path:
            self.path = "commands/poulytopia/pictures/"+path
            rand_path = str(randint(0, 1000))
            self.new_path = "commands/poulytopia/pictures/"+path[:-4:]+"_edit"+rand_path+path[-4::]
            with Image(filename=self.path) as img:
                img.save(filename=self.new_path)
        else:
            self.path = "commands/poulytopia/pictures/"+path.split("_edit")[0]+".png"
            self.new_path = "commands/poulytopia/pictures/"+path
        self.poule = poule
        self.fermier_id = fermier_id
        self.cur = cur
        self.con = con
        self.trade_id = trade_id
        self.poule_place = poule_place
        
    @discord.ui.button(label='Black&White', style=discord.ButtonStyle.gray)
    async def Edge(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.transform_colorspace('gray')
            img.edge(radius=1)
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Reliefs', style=discord.ButtonStyle.grey)
    async def Emboss(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.transform_colorspace('gray')
            img.emboss(radius=3.0, sigma=1.75)
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Shade', style=discord.ButtonStyle.grey)
    async def Shade(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.shade(gray=True,
                      azimuth=286.0,
                      elevation=45.0)
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Sinusoid', style=discord.ButtonStyle.grey)
    async def Sinusoid(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            frequency = 3
            phase_shift = -90
            amplitude = 0.2
            bias = 0.7
            img.function('sinusoid', [frequency, phase_shift, amplitude, bias])
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Charcoal', style=discord.ButtonStyle.grey)
    async def Charcoal(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.charcoal(radius=1.5, sigma=0.5)
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Matrix', style=discord.ButtonStyle.grey)
    async def Matrix(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            matrix = [[0, 0, 1],
                      [0, 1, 0],
                      [1, 0, 0]]
            img.color_matrix(matrix)
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Polaroid', style=discord.ButtonStyle.grey)
    async def Polaroid(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.polaroid()
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Sketch', style=discord.ButtonStyle.grey)
    async def Sketch(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.transform_colorspace("gray")
            img.sketch(0.5, 0.0, 98.0)
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Solarize', style=discord.ButtonStyle.grey)
    async def Solarize(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.solarize(threshold=0.5 * img.quantum_range)
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Swirl', style=discord.ButtonStyle.grey)
    async def Swirl(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.swirl(degree=-90)
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Tint', style=discord.ButtonStyle.grey)
    async def Tint(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.tint(color="green", alpha="rgb(40%, 60%, 80%)")
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='White threshold', style=discord.ButtonStyle.grey)
    async def Adaptive_Threshold(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.transform_colorspace('gray')
            img.adaptive_threshold(width=16, height=16,
                                   offset=-0.08 * img.quantum_range)
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Black threshold', style=discord.ButtonStyle.grey) #Threshold
    async def Random_threeshole(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.transform_colorspace('gray')
            img.random_threshold(low=0.3 * img.quantum_range,
                         high=0.6 * img.quantum_range)
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)


    @discord.ui.button(label='Random colorize', style=discord.ButtonStyle.grey)
    async def Colorize(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.new_path) as img:
            img.colorize(color="blue", alpha=f"rgb({randint(0,25)}%, {randint(0,25)}%, {randint(0,25)}%)")
            img.colorize(color="red", alpha=f"rgb({randint(0,25)}%, {randint(0,25)}%, {randint(0,25)}%)")
            img.colorize(color="green", alpha=f"rgb({randint(0,25)}%, {randint(0,25)}%, {randint(0,25)}%)")
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)

    @discord.ui.button(label='Annulé changements', style=discord.ButtonStyle.green)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        with Image(filename=self.path) as img:
            img.save(filename=self.new_path)
            embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
            await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed)


    @discord.ui.button(label='Enregistrer les changements', style=discord.ButtonStyle.green)
    async def fini(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.fermier_id != interaction.user.id:
            return
        self.clear_items()
        try:
            img = Image(filename=self.new_path)
        except:
            img = Image(filename=self.path)
        img.save(filename=self.new_path)
        embed, file = main_commands.create_embed(title=self.poule['poule_name'], poule=self.poule, fermier_id=self.fermier_id, path=self.new_path.replace("commands/poulytopia/pictures/",""))
        main_commands.insert_poule_prime(self.cur, self.con, self.fermier_id, self.poule["poule_name"], self.new_path.replace("commands/poulytopia/pictures/",""), self.trade_id)
        self.clear_items()
        img.close()
        await interaction.response.edit_message(attachments=[discord.File(self.new_path)], embed=embed, view=main_commands.BackToPoulailler(self.fermier_id, self.poule_place))
        #os.remove(f"photo-{self.idImage}.jpg")