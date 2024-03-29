from bot import bot, discord, commands
import random
import csv


class flagView(discord.ui.View):
    """
    class that do all the stuff
    """

    def __init__(self, userId, realFlagName, flagsOrder, embed, errorCounter, tourCounter, avatar, question_used):
        self.userId = userId
        self.realFlagName = realFlagName
        self.flagsOrder = flagsOrder
        self.embed = embed
        self.bon = True
        self.errorCounter = errorCounter
        self.tourCounter = tourCounter
        self.avatar = avatar
        self.question_used = question_used  # Pour éviter les répétitions
        super().__init__(timeout=180)
        self.brain()

    def brain(self):
        """
        set up buttons with random flag name in which the answer is
        """
        self.clear_items()
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label=self.flagsOrder[0], custom_id=self.flagsOrder[0]))
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label=self.flagsOrder[1], custom_id=self.flagsOrder[1]))
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label=self.flagsOrder[2], custom_id=self.flagsOrder[2]))
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label=self.flagsOrder[3], custom_id=self.flagsOrder[3]))

    async def interaction_check(self, interaction=discord.Interaction):
        """
        check if the interaction is stop, is next, is good or is false:
        stop: disable buttons and give the score
        next: get a new random flag and 3 others random country names, then send everything. And it count the number of round
        good: disable flag-names-buttons, add a stop and a next button
        false: add an error to the error_counter and make the answer that was clicked in red
        """
        if self.userId != interaction.user.id:
            return
        self.clear_items()
        response = interaction.data.get('custom_id')
        if response == 'stop':
            self.clear_items()
            embed = discord.Embed(
                title=f"Flag Quizz   ```{self.tourCounter - self.errorCounter} sur {self.tourCounter+1} gg```").set_image(url=self.avatar)
            await interaction.response.edit_message(embed=embed, view=None)

        if response == 'next':
            with open(r'csv_files/flag.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                randomResult = random.randint(1, 258)
                # On évite les répétitions
                while str(randomResult) == self.question_used:
                    randomResult = random.randint(1, 31)
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
                        realFlagName = row['realname']
                    elif line == randomFaux1:
                        falseflagName1 = row['realname']
                    elif line == randomFaux2:
                        falseflagName2 = row['realname']
                    elif line == randomFaux3:
                        falseflagName3 = row['realname']
                    line += 1
                allFlagsNames = [realFlagName, falseflagName1,
                                 falseflagName2, falseflagName3]
                flagsOrder = random.sample(allFlagsNames, len(allFlagsNames))
                self.tourCounter += 1
                self.question_used.append(str(randomResult))
                embed = discord.Embed(
                    title=f"Flag Quizz   ```{self.tourCounter - self.errorCounter} sur {self.tourCounter}```").set_image(url=flag)
                await interaction.response.edit_message(view=flagView(self.userId, realFlagName, flagsOrder, embed, self.errorCounter, self.tourCounter, self.avatar, self.question_used), embed=embed)
        count = 0
        if response == self.realFlagName:
            self.bon = True
            for x in self.flagsOrder:
                if str(response) == str(x):
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.green, label=self.flagsOrder[count], custom_id=self.flagsOrder[count], disabled=True))
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.primary, label='Next', custom_id='next', row=2))
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.red, label='Stop', custom_id='stop', row=2))
                else:
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.blurple, label=self.flagsOrder[count], custom_id=self.flagsOrder[count], disabled=True))
                count += 1
        else:
            if self.bon is True:
                self.errorCounter += 1
                self.bon = False
            for x in self.flagsOrder:
                if str(response) == str(x):
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.red, label=self.flagsOrder[count], custom_id=self.flagsOrder[count]))
                else:
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.blurple, label=self.flagsOrder[count], custom_id=self.flagsOrder[count]))
                count += 1
        await interaction.response.edit_message(view=self, embed=self.embed)


@bot.tree.command(guild=discord.Object(id=769911179547246592), description="Flag Quizz (base de donnée avec 258 drapeaux!)")
async def flag(interaction: discord.Interaction):
    """
    cmd that send a flag with 4 country names. user have to find wich is the good
    """
    question_used = []
    with open(r'csv_files/flag.csv', mode='r') as csv_file:
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
                realFlagName = row['realname']
            elif line == randomFaux1:
                falseflagName1 = row['realname']
            elif line == randomFaux2:
                falseflagName2 = row['realname']
            elif line == randomFaux3:
                falseflagName3 = row['realname']
            line += 1
        allFlagsNames = [realFlagName, falseflagName1,
                         falseflagName2, falseflagName3]
        flagsOrder = random.sample(allFlagsNames, len(allFlagsNames))
        embed = discord.Embed(title="Flag Quizz").set_image(url=flag)
        errorCounter = 0
        tourCounter = 0
    avatar = interaction.user.avatar
    question_used.append(str(randomResult))
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message(view=flagView(ctx.author.id, realFlagName, flagsOrder, embed, errorCounter, tourCounter, avatar, question_used), embed=embed)
