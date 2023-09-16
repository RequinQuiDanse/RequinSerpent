from bot import bot, discord
from pytesseract import pytesseract

#from googletrans import Translator
#translator = Translator()
  
# Defining paths to tesseract.exe
# and the image we would be using
path_to_tesseract = r"D:\Applications légères\Tessera\tesseract.exe"

@bot.tree.command(name='img_to_txt', guild=discord.Object(id=769911179547246592))
async def img_to_txt(interaction: discord.Interaction, img: discord.Attachment):
        """
        simple cmd that from the img send by the user get the text and send it
        """
        await interaction.response.defer()
        # Opening the image & storing it in an image object
        await img.save(r"csv_files/translate.jpg")
        # location to pytesseract library
        pytesseract.tesseract_cmd = path_to_tesseract
            
        # Passing the image object to image_to_string() function
        # This function will extract the text from the image
        text = pytesseract.image_to_string(r"csv_files/translate.jpg").replace("\n", "")
        
            
        # Displaying the extracted text
        #translateResult = translator.translate(text[:-1], dest = 'fr')
        
        x = 0
        await interaction.followup.send(content=img)
        while text[x:x+1950]:
                await interaction.channel.send(text[x:x+1950])
                x += 1950


