import glob
from bot import bot, discord, commands


class sendCodeSelect(discord.ui.Select):
    """
    select with almost all my codes, for the user to select one. Once the user respond, the bot send the code on discord
    """
    def __init__(self, ctx):
        self.ctx = ctx
        options = [
            # discord.SelectOption(
            #     label='play', description='La commande pour les musiques'),
            # discord.SelectOption(
            #     label='crack', description='La commande pour crack des jeux'),
            # discord.SelectOption(
            #     label='vids', description='La commande qui envoie de vids x'),
            # discord.SelectOption(
            #     label='supp', description='La commande pour supp des mess'),
            # discord.SelectOption(
            #     label='photo', description='La commande pour modifier les avatars des gens'),
            # discord.SelectOption(
            #     label='translate', description='La commande pour traduire des messages'),
            # discord.SelectOption(
            #     label='chimp', description='La commande pour le chimp test ma commande la plus dur'),
            # discord.SelectOption(
            #     label='flag', description='La commande pour le flag quizz'),
            # discord.SelectOption(
            #     label='sendcode', description='La commande pour cette commande'),
            # discord.SelectOption(
            #     label='reddit', description='La commande pour reddit'),
        ]
        super().__init__(placeholder="Quel code veux tu?", min_values=1, max_values=1, options = options)
        for cmd in glob.glob("commands/*.py"):
            self.add_option(label = cmd.replace("commands\\",""), description= "⠀")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content = "```fix\n" + f"{self.values[0]}```"+ "\n(Cliques sur la double flèche pour voir tout le code)",file=discord.File(f"commands/{self.values[0]}"))

class sendCodeView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.add_item(sendCodeSelect(ctx))


@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Envoie le code d'une commande")
async def sendcode(interaction: discord.Interaction):
    """
    cmd that send the code the user want to see
    """
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message("Choisis le code que tu veux", view=sendCodeView(ctx))


'''
       with open(f"commands/{self.values[0]}", "r", errors='ignore') as f:
            data = f.read().replace('\n', '\n')
            print( str(data)[5930:5945])
        if self.values[0] == "play":
            for x in range(28000, 50000, 1950):
                if(str(data)[x:x+1950]):
                    await self.ctx.channel.send(content=f"```py\n{str(data)[x:x+1950]}```")
        else:
            for x in range(0, 10000, 1950):
                if(str(data)[x:x+1950]):
                    await self.ctx.channel.send(content=f"```py\n{str(data)[x:x+1950]}```")'''