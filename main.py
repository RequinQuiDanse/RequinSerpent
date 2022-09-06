from bot import bot, discord

import commands.musique
import commands.crack
import commands.vids
import commands.supp
import commands.reddit
import commands.photo
import commands.translate
import commands.chimp_test
import commands.flag
import commands.sendcode
import commands.ultimate
import commands.akinatorcode
import commands.addplaylist
import commands.parle
import commands.legende
import commands.pool
import commands.fool
import commands.embed

creation = True
if creation is True:
    @bot.event
    async def on_ready():
        await bot.tree.sync()

with open("token.txt") as f:
    TOKEN = str(f.readlines()).replace("['", "").replace("']", "")
    
bot.run(TOKEN)
