import subprocess
from bot import bot, discord
from time import sleep

@bot.tree.command(name='gpt', guild=discord.Object(id=769911179547246592))
async def gpt(interaction: discord.Interaction, msg: str):
    """
    Tout est dans le nom de la commande. C'est un peu long parce que ça attend la réponse entière avant de répondre.
    """
    await interaction.response.defer()
    with open("commands\gpt.bat", mode="w", encoding="utf-8") as f:
        f.write(f"chatgpt {msg} > csv_files/chatgpt.txt")
    subprocess.run("commands\gpt.bat")
    sleep(2)
    with open("csv_files/chatgpt.txt", mode="r", encoding="utf-8", errors='ignore') as f:
        answer = ""
        for lines in f.readlines():
            answer += lines
        try:
            await interaction.followup.send(content=f"```{answer[0:1950]}```")
            x = 1950
            while answer[x:x+1950]:
                await interaction.channel.send(content=f"```{answer[0:1950]}```")
                x += 1950
        except:
            await interaction.channel.send(content=f"```{answer[0:1950]}```")
