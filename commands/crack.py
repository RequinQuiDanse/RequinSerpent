from bot import bot, discord, commands


rb = ('https://www.game3rb.com/?s=')
skidrow = ('https://www.skidrowcodex.net/?s=')
dodi = ('https://dodi-repacks.site/?s=')
igg = ('https://igg-games.com/?s=')
firgil = ('https://fitgirl-repacks.site/?s=')
rmecha = ('https://repack-mechanics.com/?do=search&subaction=search&story=')
amigos = ('https://www.elamigos-games.com/?q=')
amiogos = ('https://elamigos.site/#TopOfPage')
steam = ('https://steamunlocked.net/?s=')


class crackModal(discord.ui.Modal, title='Crack'):
    """
    modal to enter the name of the game we want
    """
    name = discord.ui.TextInput(
        label='Nom',
        placeholder='Nom du jeu ici...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        query = self.name.value.replace(r' ', '+')

        await interaction.response.send_message(content = f'Crack de {self.name.value}:', view=CrackResult(query))


class CrackResult(discord.ui.View):
    """
    set up buttons of all verified sites with cracked games
    """
    def __init__(self, query=str):
        super().__init__()
        self.add_item(discord.ui.Button(label='Game3rb', url=rb +
                      query))
        self.add_item(discord.ui.Button(label='Skidrow',
                      url=skidrow+query))
        self.add_item(discord.ui.Button(label='Dodi', url=dodi +
                      query))
        self.add_item(discord.ui.Button(label='Igg', url=igg +
                      query))
        self.add_item(discord.ui.Button(label='FitGirl',
                      url=firgil+query))
        self.add_item(discord.ui.Button(label='Rmecha',
                      url=rmecha+query))
        self.add_item(discord.ui.Button(label='Amigos',
                      url=amigos+query))
        self.add_item(discord.ui.Button(label='Amigos v2',
                      url=amiogos+query))
        self.add_item(discord.ui.Button(label='SteamUnlocked',
                      url=steam+query))

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Crack un jeu")
async def crack(interaction: discord.Interaction):
    """
    cmd to search easily for a game's crack
    """
    await interaction.response.send_modal(crackModal())


