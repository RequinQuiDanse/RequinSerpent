from bot import bot, discord
from wand.image import Image

class rotateModal(discord.ui.Modal, title="Créer ton sondage"):
    """
    text-input for user to say from which degrees he wants to rotate his pic
    """
    def __init__(self, img):
        super().__init__()
        self.img = img
    degree = discord.ui.TextInput(
        label="Combien de degrés? ",
        placeholder="(-90 = de gauche à droite; 90 =  de droite à gauche)"
    )

    async def on_submit(self, interaction: discord.Interaction):
        await self.img.save(fp=r"csv_files/photo-rotate.jpg")
        # Import the image
        with Image(filename = r"csv_files/photo-rotate.jpg") as img:
            # Clone the image in order to process
            img.rotate(int(self.degree.value), 'red', True)
                # Save the image
            img.save(filename=r"csv_files/photo-rotate.jpg")
            await interaction.response.send_message(file = discord.File(r"csv_files/photo-rotate.jpg"))

@bot.tree.command(description="Fait tourner une image parce que des fois c relou", guild= discord.Object(id=769911179547246592))
async def rotate_picture(interaction: discord.Interaction, img: discord.Attachment):
    """
    integrated-cmd that permit to rotate a picture and send a msg with it
    """
    await interaction.response.send_modal(rotateModal(img))