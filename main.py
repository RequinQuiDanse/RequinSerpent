from bot import bot, discord
import asyncio
import glob
import random

import commands.playlist
import commands.crack
import commands.reddit
import commands.avatar
import commands.translate
import commands.chimp_test
import commands.flag
import commands.sendcode
import commands.akinator
import commands.addplaylist
import commands.legende
import commands.sondage
import commands.img_to_txt
import commands.meteo
import commands.rotate_picture
import commands.ultimate_team
# import commands.ia_img
import commands.gpt
import commands.puissance4
import commands.rap_citation
import commands.joueurs_commentaires
import commands.general_quizz
import commands.not_commands.fool
import commands.not_commands.embed
import commands.not_commands.ultimate_quizz
import commands.not_commands.ultimate
import commands.not_commands.parle
import commands.not_commands.vids
import commands.not_commands.supp
import commands.not_commands.git

@bot.event
async def on_ready():
    #print("Sync")
    await bot.tree.sync(guild = discord.Object(id=769911179547246592)) # guild = discord.Object(id=769911179547246592) else None

    await asyncio.sleep(5)
    commands = []
    for x in glob.glob("commands/*.py"):
        commands.append(x.replace("\\","/"))
    while True:
        ma_guild = bot.get_guild(769911179547246592)
        try:
            if str(ma_guild.me.activity.type) != "ActivityType.listening" :
                activ = '/' + str(random.choice(commands)).replace("commands/","").replace(".py","")
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=activ))
        except:
            activ = '/' + str(random.choice(commands)).replace("commands/","").replace(".py","")
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=activ))
        await asyncio.sleep(150)


with open("token.txt") as f:
    TOKEN = str(f.readlines()).replace("['", "").replace("']", "")

bot.run(TOKEN)