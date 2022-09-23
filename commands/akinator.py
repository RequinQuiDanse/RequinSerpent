from bot import bot, discord, commands
from akinator.async_aki import Akinator
import akinator


class akiButton(discord.ui.View):
    def __init__(self, aki):
        self.aki = aki
        super().__init__(timeout=180)

    @discord.ui.button(label='Non', style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        q = await self.aki.answer("n")
        embed = discord.Embed(title="Akinator").add_field(
            name="Question", value=q)
        if self.aki.progression >= 80:
            await self.aki.win()
            try:
                q = f"C'est {self.aki.first_guess['name']} ({self.aki.first_guess['description']})!"
            except:
                q = "ça bug"
            try:
                embed.set_image(
                    url=f"{self.aki.first_guess['absolute_picture_path']}")
            except:
                print('')
            self.clear_items()
            embed.clear_fields()
            embed.add_field(name="Trouvé!", value=q)
            await self.aki.close()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Je ne pense pas', style=discord.ButtonStyle.red)
    async def pn(self, interaction: discord.Interaction, button: discord.ui.Button):
        q = await self.aki.answer("pn")
        embed = discord.Embed(title="Akinator").add_field(
            name="Question", value=q)
        if self.aki.progression >= 80:
            await self.aki.win()
            try:
                q = f"C'est {self.aki.first_guess['name']} ({self.aki.first_guess['description']})!"
            except:
                q = "ça bug"
            try:
                embed.set_image(
                    url=f"{self.aki.first_guess['absolute_picture_path']}")
            except:
                print('')
            self.clear_items()
            embed.clear_fields()
            embed.add_field(name="Trouvé!", value=q)
            await self.aki.close()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Je ne sais pas', style=discord.ButtonStyle.gray)
    async def idk(self, interaction: discord.Interaction, button: discord.ui.Button):
        q = await self.aki.answer("idk")
        embed = discord.Embed(title="Akinator").add_field(
            name="Question", value=q)
        if self.aki.progression >= 80:
            await self.aki.win()
            try:
                q = f"C'est {self.aki.first_guess['name']} ({self.aki.first_guess['description']})!"
            except:
                q = "ça bug"
            try:
                embed.set_image(
                    url=f"{self.aki.first_guess['absolute_picture_path']}")
            except:
                print('')
            self.clear_items()
            embed.clear_fields()
            embed.add_field(name="Trouvé!", value=q)
            await self.aki.close()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Sûrement', style=discord.ButtonStyle.green)
    async def p(self, interaction: discord.Interaction, button: discord.ui.Button):
        q = await self.aki.answer("p")
        embed = discord.Embed(title="Akinator").add_field(
            name="Question", value=q)
        if self.aki.progression >= 80:
            await self.aki.win()
            try:
                q = f"C'est {self.aki.first_guess['name']} ({self.aki.first_guess['description']})!"
            except:
                q = "ça bug"
            try:
                embed.set_image(
                    url=f"{self.aki.first_guess['absolute_picture_path']}")
            except:
                print('')
            self.clear_items()
            embed.clear_fields()
            embed.add_field(name="Trouvé!", value=q)
            await self.aki.close()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def y(self, interaction: discord.Interaction, button: discord.ui.Button):
        q = await self.aki.answer("y")
        embed = discord.Embed(title="Akinator").add_field(
            name="Question", value=q)
        if self.aki.progression >= 80:
            await self.aki.win()
            try:
                q = f"C'est {self.aki.first_guess['name']} ({self.aki.first_guess['description']})!"
            except:
                q = "ça bug"
            try:
                embed.set_image(
                    url=f"{self.aki.first_guess['absolute_picture_path']}")
            except:
                print('')
            self.clear_items()  
            embed.clear_fields()
            embed.add_field(name="Trouvé!", value=q)
            await self.aki.close()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Retour', style=discord.ButtonStyle.gray, row = 2)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            q = await self.aki.back()
        except:
            q = "Akinator ne peut pas aller plus loin"
        embed = discord.Embed(title="Akinator").add_field(
            name="Question", value=q)
        if self.aki.progression >= 80:
            await self.aki.win()
            try:
                q = f"C'est {self.aki.first_guess['name']} ({self.aki.first_guess['description']})!"
            except:
                q = "ça bug"
            try:
                embed.set_image(
                    url=f"{self.aki.first_guess['absolute_picture_path']}")
            except:
                print('')
            self.clear_items()  
            embed.clear_fields()
            embed.add_field(name="Trouvé!", value=q)
            await self.aki.close()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.edit_message(embed=embed, view=self)

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Akinator")
async def akinator(interaction: discord.Interaction):
    aki = Akinator()
    q = await aki.start_game(language="fr")
    embed = discord.Embed(title="Akinator").add_field(name="Question", value=q)
    await interaction.response.send_message(embed=embed, view=akiButton(aki))
