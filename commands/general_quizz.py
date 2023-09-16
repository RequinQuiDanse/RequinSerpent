from bot import bot, discord
import csv
from random import randint, sample
def get_citation(reverse):
    """
    return all the infos needed for a quizz:
    1 question
    1 good answer
    3 bad answers
    """

    citations_list = []
    with open(rf'csv_files/all.csv', mode='r', encoding="UTF-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            if reverse: 
                citations_list.append([row['fr'], row['all']])
            else:
                citations_list.append([row['all'], row['fr']])

    random_number = randint(1, len(citations_list)-1)
    song_citation = citations_list[random_number][0]
    song_name = citations_list[random_number][1]
    

    # choisi bien 3 faux titres différents
    random_faux_1 = randint(1, len(citations_list)-1)
    random_faux_2 = randint(1, len(citations_list)-1)
    random_faux_3 = randint(1, len(citations_list)-1)

    while citations_list[random_faux_1][1] == citations_list[random_number][1]:
        random_faux_1 = randint(1, len(citations_list)-1)

    while citations_list[random_faux_2][1] == citations_list[random_number][1] or citations_list[random_faux_2][1] == citations_list[random_faux_1][1]:
        random_faux_2 = randint(1, len(citations_list)-1)

    while citations_list[random_faux_3][1] == citations_list[random_number][1] or citations_list[random_faux_3][1] == citations_list[random_faux_1][1] or citations_list[random_faux_3][1] == citations_list[random_faux_2][1]:
        random_faux_3 = randint(1, len(citations_list)-1)

    false_song_1 = citations_list[random_faux_1][1] if len(citations_list[random_faux_1][1]) < 80 else "."
    false_song_2 = citations_list[random_faux_2][1] if len(citations_list[random_faux_2][1]) < 80 else ". "
    false_song_3 = citations_list[random_faux_3][1] if len(citations_list[random_faux_3][1]) < 80 else ".  "
    
    return [song_citation, song_name, false_song_1, false_song_2, false_song_3]

class Quizz_View(discord.ui.View):
    """
    A View that can handle a quizz with 4 buttons and 1 good answer
    """
    def __init__(self, answers, reverse):
        """
        Here you save every infos you need (good and bad answers)
        """
        super().__init__(timeout=180)
        self.answers = answers
        self.good_answer = ""
        self.reverse = reverse
        self.buttons()

    def buttons(self):
        """
        Here you set up the 4 buttons. 
        optionnaly if it isn't already done you can randomize the buttons order
        """
        self.good_answer = self.answers[0]
        self.random_song_order = sample(self.answers, len(self.answers))
        self.clear_items()
        for i in range(4):
            if self.random_song_order[i] != "." and self.random_song_order[i] != ". " and self.random_song_order[i] != ".  ":
                self.add_item(discord.ui.Button(
                    style=discord.ButtonStyle.blurple, label=self.random_song_order[i], custom_id=self.random_song_order[i]))

    async def interaction_check(self, interaction=discord.Interaction):
        """
        Here is were we handle the user's response:
        good answer = put button green and display the "next" button
        bad answer = put the button in red
        "next" button = retrieve a new question with new answers
        """
        self.clear_items()
        count = 0
        response = interaction.data.get('custom_id')
        if response == 'next':
            answers = get_citation(self.reverse)
            citation = answers.pop(0)
            await interaction.response.edit_message(content = citation, view=Quizz_View(answers, self.reverse))
        elif response == self.good_answer:
            for i in self.random_song_order:
                if str(response) == str(i):
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.green, label=self.random_song_order[count], custom_id=self.random_song_order[count], disabled=True))
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.primary, label='Next', custom_id='next', row=2))
                else:
                    if self.random_song_order[count] != "." and self.random_song_order[count] != ". " and self.random_song_order[count] != ".  ":
                        self.add_item(discord.ui.Button(
                            style=discord.ButtonStyle.blurple, label=self.random_song_order[count], custom_id=self.random_song_order[count], disabled=True))
                count += 1
        else:
            for x in self.random_song_order:
                if str(response) == str(x):
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.red, label=self.random_song_order[count], custom_id=self.random_song_order[count]))
                else:
                    if self.random_song_order[count] != "." and self.random_song_order[count] != ". " and self.random_song_order[count] != ".  ":
                        self.add_item(discord.ui.Button(
                            style=discord.ButtonStyle.blurple, label=self.random_song_order[count], custom_id=self.random_song_order[count]))
                count += 1
        try:
            await interaction.response.edit_message(view=self)


        except:
            pass



@bot.tree.command(description="Permet ptet d'apprendre", guild = discord.Object(id=769911179547246592))
async def all_quizz(interaction: discord.Interaction, reverse:bool = False):

    await interaction.response.defer()
    answers = get_citation(reverse)

    citation = answers.pop(0)
    await interaction.followup.send(content = citation, view=Quizz_View(answers, reverse))