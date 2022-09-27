from bot import bot, discord



class poolModal(discord.ui.Modal, title="Créer ton sondage"):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg
    pool = discord.ui.TextInput(
        label="1, 2, 3... Max = 10 ou a, b, c...",
        placeholder=""
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        react = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                 "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        reacta = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']

        if any(chr.isdigit() for chr in self.pool.value):
            if self.pool.value.__contains__(";"):
                await self.msg.add_reaction(react[int(self.pool.value.replace(";", ""))-1])
                await interaction.followup.send(content="C'est bon chef", ephemeral=True)
            else:
                for x in range(int(self.pool.value)):
                    await self.msg.add_reaction(react[x])
                await interaction.followup.send(content="C'est bon chef", ephemeral=True)
        else:
            if self.pool.value.__contains__(";"):
                letter = self.pool.value.replace(";","")
                for x in range(26):
                    if chr(x+97) == str(letter):
                        await self.msg.add_reaction(reacta[x])
                await interaction.followup.send(content="C'est bon chef", ephemeral=True)
            else:
                for x in range(26):
                    if chr(x+97) == str(self.pool.value):
                        for y in range(x+1):
                            await self.msg.add_reaction(reacta[y])
                await interaction.followup.send(content="C'est bon chef", ephemeral=True)



@bot.tree.context_menu(name='Sondage')
async def pool(interaction: discord.Interaction, msg: discord.Message):
    await interaction.response.send_modal(poolModal(msg=msg))
