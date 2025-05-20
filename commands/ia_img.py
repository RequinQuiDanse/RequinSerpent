import os
from bot import discord, bot
import torch
from diffusers.utils import load_image
from PIL import Image


from datetime import datetime
import urllib.request
import base64
import json
import time
import os
out_dir = 'csv_files'
out_dir_t2i = os.path.join(out_dir, 'txt2img')
out_dir_i2i = os.path.join(out_dir, 'img2img')
os.makedirs(out_dir_t2i, exist_ok=True)
os.makedirs(out_dir_i2i, exist_ok=True)
# output_folder = "csv_files/ia_img/"

class choseModelSelect(discord.ui.Select):
    """
    """
    def __init__(self, prompt, img):
        self.prompt = prompt
        self.img = img
        options = [
            discord.SelectOption(
                label='flux1-dev-fp8'),
                            discord.SelectOption(
                label='uberRealisticPornMerge_v23Final', description="/!\\ NSFW = ON /!\\"),
                            discord.SelectOption(
                label='tPonynai3_v65'),
                 discord.SelectOption(
                label='animagineXLV31_v31'),
                
        ]
        super().__init__(placeholder="Quel model veux tu?", min_values=1, max_values=1, options = options)

    async def callback(self, interaction: discord.Interaction):
        if torch.cuda.is_available():

            payload = {
                "prompt": self.prompt,
                "negative_prompt": "",
                "seed": -1,
                "sampler_name": "Euler",
                "scheduler": "Automatic",
                "batch_size": 4,
                "n_iter": 1,
                "steps": 20,
                "cfg_scale": 7,
                "distilled_cfg_scale": 3.5,
                "width": 512,
                "height": 628,
                "denoising_strength": 0,
                "override_settings" : {
                "sd_model_checkpoint": self.values[0],
                "CLIP_stop_at_last_layers": 1,
            }
                }
            await interaction.response.defer()

            if self.img:
                await self.img.save(fp="csv_files/ia_img/original_img.png")


                init_image = load_image(Image.open("csv_files/ia_img/original_img.png").resize((528, 528))).convert("RGB")


            else:
                output_path = call_txt2img_api(payload)

            img = []
            if self.img:
                img = [discord.File(r"csv_files/ia_img/original_img.png"), discord.File(f"{output_path}")]
            else:
                for path in output_path :
                    img.append(discord.File(f"{path}"))
            await interaction.followup.edit_message(message_id= interaction.message.id, content = "", attachments=img, view=None)#f"{self.prompt}\n {self.values[0]}"

        else:
            await interaction.followup.edit_message("CG indispo :§", ephemeral=True)


class choseSelectView(discord.ui.View):
    def __init__(self, prompt, img):
        super().__init__()
        self.add_item(choseModelSelect(prompt, img))



@bot.tree.command(guild = discord.Object(id=769911179547246592), description="J'AI 24G DE VRAM TU PEUX BALANCER")
async def ia_img(interaction: discord.Interaction, prompt:str):
    img = None
    await interaction.response.send_message("cque tu veux on a", view=choseSelectView(prompt, img))




def timestamp():
    return datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")


def encode_file_to_base64(path):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


def decode_and_save_base64(base64_str, save_path):
    with open(save_path, "wb") as file:
        file.write(base64.b64decode(base64_str))


def call_api(api_endpoint, payload):
    data = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(
        f'http://127.0.0.1:7860/{api_endpoint}',
        headers={'Content-Type': 'application/json'},
        data=data,
    )
    response = urllib.request.urlopen(request)
    return json.loads(response.read().decode('utf-8'))


def call_txt2img_api(payload):
    response = call_api('sdapi/v1/txt2img', payload)
    all_path = []
    for index, image in enumerate(response.get('images')):
        save_path = os.path.join(out_dir_t2i, f'txt2img-{timestamp()}-{index}.png')
        all_path.append(save_path)
        decode_and_save_base64(image, save_path)
    return all_path

def call_img2img_api(**payload):
    response = call_api('sdapi/v1/img2img', **payload)
    for index, image in enumerate(response.get('images')):
        save_path = os.path.join(out_dir_i2i, f'img2img-{timestamp()}-{index}.png')
        decode_and_save_base64(image, save_path)


# payload = {
#   "prompt": "Flowers",
#   "negative_prompt": "",
#   "styles": [
#     "string"
#   ],
#   "seed": -1,
#   "sampler_name": "Euler",
#   "scheduler": "Simple",
#   "batch_size": 1,
#   "n_iter": 1,
#   "steps": 20,
#   "cfg_scale": 1,
#   "distilled_cfg_scale": 3.5,
#   "width": 128,
#   "height": 128,
#   "denoising_strength": 0,
# }

