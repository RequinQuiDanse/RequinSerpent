import os
from bot import bot, discord, commands


from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display


class legendeModal(discord.ui.Modal, title="Légende une photo"):
    """
    modal for the user to enter the caption and then send a pic with it
    """
    def __init__(self, msg):
        super().__init__()
        self.msg = msg
    legende = discord.ui.TextInput(
        label="Ta légende: ",
        placeholder="..."
    )
    async def on_submit(self, interaction: discord.Interaction):
        with Image(filename=str(self.msg.attachments[0])) as canvas:
            with Drawing() as context:
                canvas.polaroid()
                context.fill_color = Color('rgb(0, 0, 0)')
                context.stroke_color = Color('rgb(0, 0, 0)')
                context.font_style = 'italic'
                context.font_size = 5 * canvas.size[1] / 100
                context.text(x= int(5 * canvas.size[1] / 100),
                             y=canvas.size[1] - int(1 * canvas.size[1] / 100),
                             body=self.legende.value)
                context(canvas)
                canvas.format = "png"
                canvas.save(filename=f"photo.jpg")
                await interaction.response.send_message(file = discord.File("photo.jpg"))
                os.remove(f"photo.jpg")


@bot.tree.context_menu(name='Légende une photo', guild=discord.Object(id=769911179547246592))
async def legende(interaction: discord.Interaction, msg: discord.Message):
    """
    little integrated-cmd to add a legend in a picture
    """
    await interaction.response.send_modal(legendeModal(msg=msg))
