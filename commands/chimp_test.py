from matplotlib.pyplot import title
import numpy as np
from bot import bot, discord, commands
import random
import csv
import time
import pandas as pd

# Cerveau du code


class chimpButton(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.userId = ctx.author.id
        # Nombres de cases que l'on voudra bleu
        self.nombreCases = 6
        # Nombres de cases que le joueur a appuyé, utile pour comparer au custom_id
        self.nombreCasesPush = 0
        # Variable pour ranger les cases bleu
        self.buttonBlue = []
        self.ordreCase = []
        self.button = dict()
        self.findButton = []
        self.time = time.time()
        # Créer le plateau
        self.chimpButtonFunc()

    # Les règles du jeu
    async def interaction_check(self, interaction=discord.Interaction):
        if self.userId != interaction.user.id:
            return
        # Si le résultat est bon, passes à la prochaine case
        if str(interaction.data.get('custom_id')) == str(self.nombreCasesPush):
            # if interaction.data.get('custom_id') == "0":
            self.setButtonBlue(interaction.data.get('custom_id'))
            self.nombreCasesPush += 1
            await interaction.response.edit_message(content=f'{int(time.time() - self.time)} secondes', view=self)
        # A chaque tour refait le plateau avec une case en plus.
        else:
            self.endButton()
            temps = str(int(time.time() - self.time))
            score = str(int(self.nombreCases) ** 3 - int(temps) * 5)
            self.csvWritter(interaction.user.name, temps, score)
            if int(score) > 600:
                await interaction.response.edit_message(content=f'Fini! {self.nombreCases} points en {temps} secondes. Score ({score}) enregistré!', view=self)
            else:
                # '
                await interaction.response.edit_message(content=f'Fini! {self.nombreCases} points en {temps} secondes. Score ({score}) trop petit pour être enregistré!', view=self)
        if self.nombreCasesPush == (self.nombreCases):
            self.nombreCases += 1
            self.ordreCase = []
            self.findButton = []
            self.chimpButtonFunc()
            await interaction.edit_original_message(content=int(time.time() - self.time), view=self)

    # Créateur du plateau
    def chimpButtonFunc(self):
        # Néttoie les boutons pour en créer de nouveaux
        self.clear_items()
        # Cette variable défini le nombre de case soit le résultat du boutton attendu
        self.nombreCasesPush = 0
        self.buttonBlue = random.sample(range(1, 25), self.nombreCases)
        self.ordreCase = np.random.choice(
            range(self.nombreCases), size=self.nombreCases, replace=False).tolist()
        self.ordreCase
        y = 0
        for x in range(0, 25):
            if x in self.buttonBlue:
                self.button[x] = discord.ui.Button(style=discord.ButtonStyle.blurple, label=str(
                    self.ordreCase[y]), custom_id=str(self.ordreCase[y]))
                y += 1
            else:
                self.button[x] = discord.ui.Button(
                    style=discord.ButtonStyle.gray, label='⠀', disabled=True)
        for add in range(0, 25):
            self.add_item(self.button[add])

    # Remets toutes les cases en bleu
    def setButtonBlue(self, id):
        self.clear_items()
        y = 0
        idIndex = next(
            i for i, item in enumerate(self.ordreCase)
            if str(item) in str(id))
        for x in range(0, 25):
            if x in self.buttonBlue:
                if y in self.findButton:
                    self.button[x] = discord.ui.Button(style=discord.ButtonStyle.blurple, label=str(
                        self.ordreCase[y]), custom_id=str(self.ordreCase[y]))
                elif y == idIndex:
                    self.button[x] = discord.ui.Button(style=discord.ButtonStyle.blurple, label=str(
                        self.ordreCase[y]), custom_id=str(self.ordreCase[y]))
                    self.findButton.append(idIndex)
                else:
                    self.button[x] = discord.ui.Button(style=discord.ButtonStyle.blurple, label=str(
                        '⠀'), custom_id=str(self.ordreCase[y]))
                y += 1
            else:
                self.button[x] = discord.ui.Button(
                    style=discord.ButtonStyle.gray, label='⠀', disabled=True)
        self.button[25] = discord.ui.Button(
            style=discord.ButtonStyle.red, label='Fin', custom_id=str(25))
        for add in range(0, 25):
            self.add_item(self.button[add])

    def endButton(self):
        self.clear_items()
        y = 0
        for x in range(0, 25):
            if x in self.buttonBlue:
                self.button[x] = discord.ui.Button(style=discord.ButtonStyle.blurple, label=str(
                    self.ordreCase[y]), custom_id=str(self.ordreCase[y]), disabled=True)
                y += 1
            else:
                self.button[x] = discord.ui.Button(
                    style=discord.ButtonStyle.gray, label='⠀', disabled=True)
        for add in range(0, 25):
            self.add_item(self.button[add])

    def csvWritter(self, pseudo, temps, score):
        with open('csv_files\chimpdata.csv', mode='a') as csv_file:
            df = pd.read_csv('csv_files\chimpdata.csv')
            df = df[df.score > 500]
            df.to_csv('csv_files\chimpdata.csv', index=False)
            fieldnames = ['name', 'points', 'time', 'score']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            try:
                writer.writerow(
                    {'name': pseudo, 'points': str(self.nombreCases), 'time': temps, 'score': score})
            except:
                if str(pseudo) == "મ̴̲̾ ̴̢̨એ̴̡̡ક̵̛̤ ̶̡͓અ̷͕͚બ̴̛̼":  # "
                    writer.writerow(
                        {'name': "Adam", 'points': str(self.nombreCases), 'time': temps, 'score': score})
                elif str(pseudo) == "dwɔf we dɛn kɔl dwɔf":
                    writer.writerow(
                        {'name': "Yanis", 'points': str(self.nombreCases), 'time': temps, 'score': score})
                else:
                    print(pseudo)
                    writer.writerow(
                        {'name': "undefinied", 'points': str(self.nombreCases), 'time': temps, 'score': score})


@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Chimp Test")
async def chimptest(interaction: discord.Interaction):
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message("Chimp Test", view=chimpButton(ctx))


@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Chimp Test Scores")
async def chimptestscore(interaction: discord.Interaction):
    file = 'csv_files\chimpdata.csv'
    df = pd.read_csv(file)
    df = df[df.score > 600]
    df.to_csv(file, index=False)
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 1
        embed = discord.Embed(title="Scores du Chimp Test")
        for row in csv_reader:
            embed.add_field(name=f"{row['name']}, score = {row['score']}",
                            value=f"= {row['points']} points en {row['time']} secondes.")
            line_count += 1
    await interaction.response.send_message("Chimp Test", embed=embed)
