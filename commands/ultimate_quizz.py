import time
from bot import bot, discord, commands
import random
import csv

emoji = ["1️⃣", "2️⃣", "3️⃣"]

class Ultimate_View(discord.ui.View):
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
            style=discord.ButtonStyle.blurple, label= emoji[0], custom_id=self.answer_order[0]))
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label= emoji[1], custom_id=self.answer_order[1]))
        if self.answer_order.__len__() == 3:
            self.add_item(discord.ui.Button(
                style=discord.ButtonStyle.blurple, label= emoji[2], custom_id=self.answer_order[2]))

    async def interaction_check(self, interaction=discord.Interaction):
        if self.userId != interaction.user.id:
            return
        self.clear_items()
        response = interaction.data.get('custom_id')
        #response = self.answer_order[response]
        if response == 'stop':
            self.clear_items()
            embed = discord.Embed(
                title=f"Ultimate Quizz   ```{self.tourCounter - self.errorCounter} sur {self.tourCounter} gg```").set_image(url=self.avatar)
            await interaction.response.edit_message(embed=embed, view=None)

        if response == 'Suivant':
            with open(r'csv_files\ultimate.csv', mode='r', encoding= "UTF-8") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                randomResult = random.randint(1, 22)
                randomFaux1 = random.randint(1, 22)
                if randomFaux1 == randomResult:
                    randomFaux1 = random.randint(1, 22)
                randomFaux2 = random.randint(1, 22)
                if randomFaux2 == randomResult or randomFaux2 == randomFaux1:
                    randomFaux2 = random.randint(1, 22)
                randomFaux3 = random.randint(1, 22)
                if randomFaux3 == randomResult or randomFaux3 == randomFaux1 or randomFaux3 == randomFaux2:
                    randomFaux3 = random.randint(1, 22)
                line = 0
                for row in csv_reader:
                    if line == randomResult:
                        question = row['question']
                        real_answer = row['answer']
                        false_answer_1 = row['false_answer_1']
                        false_answer_2 = row['false_answer_2']
                    line += 1
                all_answers = [real_answer, false_answer_1]
                if false_answer_2 is not None:
                    all_answers = [real_answer, false_answer_1, false_answer_2]
                answer_order = random.sample(all_answers, len(all_answers))
                self.tourCounter += 1
                embed = discord.Embed(
                    title=f"Ultimate Quizz   ```{self.tourCounter - self.errorCounter} sur {self.tourCounter}```", description=f"```{question}```")
                embed.add_field(
                    name= emoji[0], value=answer_order[0], inline=False)
                embed.add_field(
                    name= emoji[1], value=answer_order[1], inline=False)
                if false_answer_2:
                    embed.add_field(name= emoji[2], value=answer_order[2], inline=False)
                await interaction.response.edit_message(view=Ultimate_View(self.userId, real_answer, answer_order, embed, self.errorCounter, self.tourCounter, self.avatar), embed=embed)
        count = 0
        if response == self.real_answer:
            self.bon = True
            for x in self.answer_order:
                if str(response) == str(x):
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.green, label = emoji[count], custom_id=self.answer_order[count], disabled=True))
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.primary, label='Suivant', custom_id='Suivant', row=2))
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
                        style=discord.ButtonStyle.red, label= emoji[count], custom_id = self.answer_order[count]))
                else:
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.blurple, label= emoji[count], custom_id = self.answer_order[count]))
                count += 1
        await interaction.response.edit_message(view=self, embed=self.embed)


@bot.tree.command(guild=discord.Object(id=769911179547246592), description="Ultimate Quizz (base de donnée avec nos questions!)")
async def ultimate(interaction: discord.Interaction):
    with open(r'csv_files\ultimate.csv', mode='r', encoding= "UTF-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        randomResult = random.randint(1, 22)
        randomFaux1 = random.randint(1, 22)
        if randomFaux1 == randomResult:
            randomFaux1 = random.randint(1, 22)
        randomFaux2 = random.randint(1, 22)
        if randomFaux2 == randomResult or randomFaux2 == randomFaux1:
            randomFaux2 = random.randint(1, 22)
        randomFaux3 = random.randint(1, 22)
        if randomFaux3 == randomResult or randomFaux3 == randomFaux1 or randomFaux3 == randomFaux2:
            randomFaux3 = random.randint(1, 22)
        line = 0
        for row in csv_reader:
            if line == randomResult:
                question = row['question']
                real_answer = row['answer']
                false_answer_1 = row['false_answer_1']
                false_answer_2 = row['false_answer_2']
            line += 1

        all_answers = [real_answer, false_answer_1]
        if false_answer_2 is None:
            all_answers = [real_answer, false_answer_1, false_answer_2]
        answer_order = random.sample(all_answers, len(all_answers))
        embed = discord.Embed(title="Ultimate Quizz",
                              description=f"```{question}```")
        embed.add_field(name = emoji[0], value=answer_order[0], inline=False)
        embed.add_field(name = emoji[1], value=answer_order[1], inline=False)
        if false_answer_2:
            embed.add_field(name = emoji[2], value=answer_order[2], inline=False)
        errorCounter = 0
        tourCounter = 0
    avatar = interaction.user.avatar
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message(view=Ultimate_View(ctx.author.id, real_answer, answer_order, embed, errorCounter, tourCounter, avatar), embed=embed)
