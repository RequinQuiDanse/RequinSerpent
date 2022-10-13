from bot import bot, discord
from googletrans import Translator
translator = Translator()
@bot.tree.context_menu(name='Translate', guild=discord.Object(id=769911179547246592))
async def translate(interaction: discord.Interaction, message: discord.Message):
    """
    little integrated-cmd that translate a msg in french and then send a msg with the translation
    """
    translateResult = translator.translate(message.content, dest = 'fr')
    await interaction.response.send_message(f'>Origine: {message.content}\n>Traduction: {translateResult.text}')
