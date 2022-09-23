from dataclasses import replace
from bot import bot, discord
import glob

@bot.command()
async def embed1(ctx):
    await ctx.channel.send(content = f"```**Nouvelle année sco**```")

    for image_file in glob.glob(f"C:/Users/adamh/Pictures/emploi_du _temps_1ere/*"):
        img = str(image_file).replace("C:/Users/adamh/Pictures/emploi_du _temps_1ere\\","")
        img = img[: int(img.__len__()-4)]
        #embed = discord.Embed(title = img)
        #embed.set_image(url = f'attachment://{image_file}')
        await ctx.channel.send(file = discord.File(image_file), content = f"```{img}```")