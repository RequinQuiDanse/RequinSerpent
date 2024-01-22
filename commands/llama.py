from bot import bot, discord, commands

import time

import asyncio
import ollama
import subprocess



@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Demandes ce que tu veux")
async def llama(interaction: discord.Interaction, prompt:str):
    """
    cmd to talk to an uncensored llm
    """
    await interaction.response.defer(ephemeral=True)
    
    stream = ollama.chat(
        model='llama2-uncensored',
        messages=[{'role':'user','content': prompt}],
        stream=True,
    )

    first = True
    total_resp = ""
    atime = time.time()


    try:
        for chunk in stream:
            total_resp += chunk['message']['content']
            if time.time() - atime >1:
                atime = time.time()
                if first:
                    await interaction.followup.send("Prompt en chargement...", ephemeral=True)
                    msg = await interaction.channel.send(content=total_resp)
                    first = False
                else:
                    await msg.edit(content = total_resp)


    except:
        await interaction.followup.send(content=f"Lancement du chatbot... Refais le prompt dans qlq secondes", ephemeral=True)

        subprocess.run('ubuntu run systemctl stop ollama')
        server_command = "ubuntu run ollama serve"
        await asyncio.create_subprocess_shell(
            server_command
        )