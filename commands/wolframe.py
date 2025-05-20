from bot import bot, discord
from PIL import Image
# import sys
# sys.path.append(r'D:/code/pix_2_text/.env/Lib/site-packages')

from pix2text import Pix2Text



import requests

from PIL import Image
import io


@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Maths :)")
async def wolframe(interaction: discord.Interaction, img: discord.Attachment):
    """
    calculatrice
    """
    await interaction.response.defer()
    await img.save(fp=r"csv_files/maths_img/image.png")
    img_fp = r"csv_files/maths_img/image.png"
    p2t = Pix2Text.from_config()
    outs = p2t.recognize_text_formula(img_fp, resized_shape=768, return_text=True)
    input = outs.replace("$","").replace("\n","").replace("\operatorname{c o s}","cos").replace("\operatorname{s i n}","sin").replace("+","%2B").replace(" ","")

    try :
        app_id = "Y5QP3A-E5K6E2VGL2"
        url = f"https://api.wolframalpha.com/v2/simple?appid={app_id}&input={input}"
        print(url)
        r = requests.get(url)


        image = Image.open(io.BytesIO(r.content))


        width, height = image.size

        print(height)
        section_height = (height-150) // 4

        for i in range(4):
            box = (0, i * section_height+75, width, (i + 1) * section_height+100)
            
            section = image.crop(box)
            
            section.save(fr'csv_files/maths_img/section_{i + 1}.png')  

        imgs = [discord.File(fr"csv_files/maths_img/section_{i + 1}.png") for i in range(0, 4)]
        await interaction.followup.send(content=input, files = imgs)
    except :
        await interaction.followup.send(content=input+"\nBug Wolframet")
