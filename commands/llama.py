from bot import bot, discord, commands

import time

import asyncio
import ollama
import subprocess



@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Demandes ce que tu veux")
async def llama(interaction: discord.Interaction):
    """
    cmd to talk to an uncensored llm
    """
    await interaction.response.send_modal(PromptModal())

class PromptModal(discord.ui.Modal, title='Prompt'):
    """
    modal to enter the prompt
    """
    name = discord.ui.TextInput(
        label='Prompt',
        placeholder='...',
    )
    # hidden = discord.ui.TextInput(
    #     label='Écris quelque chose pour que le message soit caché',
    #     placeholder='Par défaut publique',
    # )

    async def on_submit(self, interaction: discord.Interaction):
        prompt = self.name.value
        # await interaction.response.send_message(content = f'Crack de {self.name.value}:', view=CrackResult(query))


        await interaction.response.defer(ephemeral=True)
        channel = interaction.channel
        async with channel.typing():
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
                            await interaction.followup.send(f"Prompt en chargement... \n>{prompt}", ephemeral=True)
                            msg = await interaction.channel.send(content=total_resp)
                            first = False
                        else:
                            await msg.edit(content = total_resp)
                await msg.edit(content = total_resp)


            except:
                await interaction.followup.send(content=f"Lancement du chatbot... Refais le prompt dans qlq secondes. \n{prompt}", ephemeral=True)

                subprocess.run('ubuntu run systemctl stop ollama')
                server_command = "ubuntu run ollama serve"
                await asyncio.create_subprocess_shell(
                    server_command
                )