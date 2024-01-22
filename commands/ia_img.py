from bot import discord, bot
from PIL import Image
import random
import subprocess
import glob
import torch
import time
import datetime
@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Je n'ai que 4giga de vram, donc ~~3min/photo")
async def ia_img(interaction: discord.Interaction, sentence:str, img:discord.Attachment = None):
    if torch.cuda.is_available():
        sentence = sentence.replace('"',"").replace("{","").replace("}","").replace(":","").replace(",","")
        _time = time.time()
        minute = datetime.datetime.now().minute+3 if len(str(datetime.datetime.now().minute+3))==2 else "0" + str(datetime.datetime.now().minute+3)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"Hot {datetime.datetime.now().hour}h {minute}"))
        await interaction.response.defer()
        seed = random.randint(0,42999999)
        if img:
            await img.save(fp="csv_files/ia_img\original_img.png")
            subprocess.run(fr'C:\Users\adamh\anaconda3\envs\ldm\python.exe D:\code\stable-diffusion\stable-diffusion\optimizedSD\optimized_img2img.py --prompt "{sentence}" --seed {seed} --init-img csv_files/ia_img\original_img.png --strength 0.6 --n_samples 2 --H 512 --W 512 --precision full --outdir csv_files/ia_img')
            _seed = "0.0000"
            for x in glob.glob(fr'csv_files/ia_img\{sentence[:133].replace(" ","_")}\*.png'):
                _seed = float(_seed) + 0.0001
            _seed = round(float(_seed) - 0.0001,5)
            print(_seed)
            __seed = "00000" if str(round(float(_seed) - 0.0001,5)).replace(".","") == "00" else str(round(float(_seed) - 0.0001,5)).replace(".","")
            print(__seed)
            img = [discord.File(r"csv_files/ia_img\original_img.png"), discord.File(fr'csv_files/ia_img\{sentence[:133].replace(" ","_")}\seed_{seed}_{__seed}.png'), discord.File(fr'csv_files/ia_img\{sentence[:133].replace(" ","_")}\seed_{seed+1}_{str(_seed).replace(".","")}.png')]
            await interaction.followup.send(content = f"{sentence}, {round((int(time.time() - _time)/60),2)}min", files=img)
        else:
            subprocess.run(fr'C:\Users\adamh\anaconda3\envs\ldm\python.exe D:\code\stable-diffusion\stable-diffusion\optimizedSD\optimized_txt2img.py --prompt "{sentence}" --seed {seed} --H 512 --W 512 --n_samples 2 --ddim_steps 50 --precision full --outdir "csv_files/ia_img"')
            _seed = "0.0000"
            for x in glob.glob(fr'csv_files/ia_img\{sentence[:133].replace(" ","_")}\*.png'):
                _seed = float(_seed) + 0.0001
            _seed = "00000" if str(_seed).replace(".","") == "00001" else str(round(float(_seed) - 0.0001,5)).replace(".","")
            img = [discord.File(fr'csv_files/ia_img\{sentence[:133].replace(" ","_")}\seed_{seed}_{_seed}.png')]
            await interaction.followup.send(content = f"{sentence}, {round((int(time.time() - _time)/60),2)}min", files=img)
    else:
        await interaction.response.send_message("CG indispo :§", ephemeral=True)
'''
import io
import os
import warnings
from IPython.display import display
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

import getpass, os
# NB: host url is not prepended with \"https\" nor does it have a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# To get your API key, visit https://beta.dreamstudio.ai/membership https://beta.dreamstudio.ai/membership?tab=apiKeys
os.environ['STABILITY_KEY'] = "sk-o67kIP2S3flFALsyZVFtYgfEMo0elK8oaN6B79uubejj1qp4"


@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Génère une photo à partir de paramètres")
async def ia_pic(interaction: discord.Interaction, sentence:str, img:discord.Attachment = None):
    await interaction.response.defer()
    if img is not None:
        await img.save(fp=r"csv_files/photo_ia.png")
        try:
            img = Image.open(fp=r"csv_files/photo_ia.png").resize((512,512))
        except:
            img = None
            interaction.followup.send("L'image passe pas")
    stability_api = client.StabilityInference(
        key=os.environ['STABILITY_KEY'], 
        verbose=True,
    )
    # the object returned is a python generator
    answers = stability_api.generate(
        prompt=sentence,
        init_image= Image.open(fp=r"csv_files/photo_ia.png").resize((512,512)) if img is not None else None,  #if pic is not None else None
        start_schedule=0.6, # this controls the "strength" of the prompt relative to the init image
        #seed=None, # if provided, specifying a random seed makes results deterministic 34567 429999999
        #steps=500, # defaults to 50 if not specified 5 => plus c grand plus ça demande
        #start_schedule=0.6, # this controls the "strength" of the prompt relative to the init image
    )
    # iterating over the generator produces the api response
    for resp in answers:
        #print(resp.artifacts)
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                sentence += "\n Arrêtes de générer du porno."
            if artifact.type == generation.ARTIFACT_IMAGE:
                _img = Image.open(io.BytesIO(artifact.binary))
                _img.save(fp=r"csv_files/photo_ia2.png")
                await interaction.followup.send(content = sentence, files=[discord.File(r"csv_files/photo_ia.png"), discord.File(r"csv_files/photo_ia2.png")])
'''