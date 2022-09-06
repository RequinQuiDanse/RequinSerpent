from bot import bot, discord, commands
import random
import csv


class flagView(discord.ui.View):
    def __init__(self, userId, real_answer, answer_order, embed, errorCounter, tourCounter, avatar):
        self.userId = userId
        self.real_answer = real_answer
        self.answer_order = answer_order
        self.embed = embed
        self.bon = True
        self.errorCounter = errorCounter
        self.tourCounter = tourCounter
        self.avatar = avatar
        super().__init__(timeout=180)
        self.brain()

    def brain(self):
        self.clear_items()
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label=self.answer_order[0], custom_id=self.answer_order[0]))
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label=self.answer_order[1], custom_id=self.answer_order[1]))
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label=self.answer_order[2], custom_id=self.answer_order[2]))
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label=self.answer_order[3], custom_id=self.answer_order[3]))

    async def interaction_check(self, interaction=discord.Interaction):
        if self.userId != interaction.user.id:
            return
        self.clear_items()
        response = interaction.data.get('custom_id')
        if response == 'stop':
            self.clear_items()
            embed = discord.Embed(title=f"Flag Quizz   ```{self.tourCounter - self.errorCounter} sur {self.tourCounter} gg```").set_image(url=self.avatar)
            await interaction.response.edit_message(embed = embed, view= None)

        if response == 'next':
            with open(r'csv_files\flag.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                randomResult = random.randint(1, 258)
                randomFaux1 = random.randint(1, 258)
                if randomFaux1 == randomResult:
                    randomFaux1 = random.randint(1, 258)
                randomFaux2 = random.randint(1, 258)
                if randomFaux2 == randomResult or randomFaux2 == randomFaux1:
                    randomFaux2 = random.randint(1, 258)
                randomFaux3 = random.randint(1, 258)
                if randomFaux3 == randomResult or randomFaux3 == randomFaux1 or randomFaux3 == randomFaux2:
                    randomFaux3 = random.randint(1, 258)
                line = 0
                for row in csv_reader:
                    if line == randomResult:
                        flag = f"https://flagcdn.com/256x192/{row['shortname']}.png"
                        real_answer = row['realname']
                    elif line == randomFaux1:
                        falseflagName1 = row['realname']
                    elif line == randomFaux2:
                        falseflagName2 = row['realname']
                    elif line == randomFaux3:
                        falseflagName3 = row['realname']
                    line += 1
                allFlagsNames = [real_answer, falseflagName1,
                                falseflagName2, falseflagName3]
                answer_order = random.sample(allFlagsNames, len(allFlagsNames))
                self.tourCounter += 1
                embed = discord.Embed(title=f"Flag Quizz   ```{self.tourCounter - self.errorCounter} sur {self.tourCounter}```").set_image(url=flag)
                await interaction.response.edit_message(view=flagView(self.userId, real_answer, answer_order, embed, self.errorCounter, self.tourCounter, self.avatar), embed=embed)
        count = 0
        if response == self.real_answer:
            self.bon = True
            for x in self.answer_order:
                if str(response) == str(x):
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.green, label=self.answer_order[count], custom_id=self.answer_order[count], disabled=True))
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.primary, label='Next', custom_id='next', row=2))
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.red, label='Stop', custom_id='stop', row=2))
                else:
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.blurple, label=self.answer_order[count], custom_id=self.answer_order[count], disabled=True))
                count += 1
        else:
            if self.bon is True:
                self.errorCounter += 1
                self.bon = False
            for x in self.answer_order:
                if str(response) == str(x):
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.red, label=self.answer_order[count], custom_id=self.answer_order[count]))
                else:
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.blurple, label=self.answer_order[count], custom_id=self.answer_order[count]))
                count += 1
        await interaction.response.edit_message(view=self, embed=self.embed)



@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Flag Quizz (base de donnée avec 258 drapeaux!)")
async def flag(interaction: discord.Interaction):
    with open(r'csv_files\flag.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        randomResult = random.randint(1, 258)
        randomFaux1 = random.randint(1, 258)
        if randomFaux1 == randomResult:
            randomFaux1 = random.randint(1, 258)
        randomFaux2 = random.randint(1, 258)
        if randomFaux2 == randomResult or randomFaux2 == randomFaux1:
            randomFaux2 = random.randint(1, 258)
        randomFaux3 = random.randint(1, 258)
        if randomFaux3 == randomResult or randomFaux3 == randomFaux1 or randomFaux3 == randomFaux2:
            randomFaux3 = random.randint(1, 258)
        line = 0
        for row in csv_reader:
            if line == randomResult:
                flag = f"https://flagcdn.com/256x192/{row['shortname']}.png"
                real_answer = row['realname']
            elif line == randomFaux1:
                falseflagName1 = row['realname']
            elif line == randomFaux2:
                falseflagName2 = row['realname']
            elif line == randomFaux3:
                falseflagName3 = row['realname']
            line += 1
        allFlagsNames = [real_answer, falseflagName1,
                         falseflagName2, falseflagName3]
        answer_order = random.sample(allFlagsNames, len(allFlagsNames))
        embed = discord.Embed(title="Flag Quizz").set_image(url=flag)
        errorCounter = 0
        tourCounter = 0
    avatar = interaction.user.avatar
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message(view=flagView(ctx.author.id, real_answer, answer_order, embed, errorCounter, tourCounter, avatar), embed=embed)