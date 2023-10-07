import csv
from bot import bot, discord
from bs4 import BeautifulSoup
import requests
from random import randint, sample
import os.path

def make_request(artist):
    """
    return a list of questions with their answers
    """
    res = requests.get(f'https://raplume.eu/citations/artists/{artist}')
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        text = soup.select(".theiaPostSlider_preloadedSlide")[
            0].getText().strip()
    except:
        return 0

    if "Les meilleures phrases de" not in text:
        return 0
    artist = artist.replace("les-meilleures-phrases-de-","")

    citations_list = []
    temp_word = ""
    song = ""

    for letters in text:
        if letters != '"':
            temp_word += letters
        else:
            if "Source" in temp_word:
                song = temp_word
                temp_word = ""
            else:
                word = temp_word

            if word != "" and song != "":
                citations_list.append([word, song])
                word, song = "", ""
                
    with open(rf'csv_files/rap_citation\{artist}.csv', mode='w', newline="", encoding="UTF-8") as csv_file:
        fieldnames = ['citation', 'artist']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({'citation': fieldnames[0], 'artist': fieldnames[1]})
        i = 0
        for infos in citations_list:
            if i > 0:
                song = infos[1].split(":")[1][1:]
                try:
                    writer.writerow(
                        {'citation': infos[0], 'artist': song})
                except:
                    print("Erreur pdnt csv de make_request()")
            else:
                i += 1
    return 1
    
def get_citation(artist):
    """
    return all the infos needed for a quizz:
    1 question
    1 good answer
    3 bad answers
    """

    if not os.path.exists(rf'csv_files/rap_citation\{artist}.csv'):
        if make_request(artist) != 1:
            if make_request(artist="les-meilleures-phrases-de-"+artist) != 1:
                return 0

    citations_list = []
    with open(rf'csv_files/rap_citation\{artist}.csv', mode='r', encoding="UTF-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            citations_list.append([row['citation'], row['artist']])

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

   # juste un titre
    false_song_1 = citations_list[random_faux_1][1] if len(citations_list[random_faux_1][1]) < 80 and "Source" not in citations_list[random_faux_1][1] else "."
    false_song_2 = citations_list[random_faux_2][1] if len(citations_list[random_faux_2][1]) < 80 and "Source" not in citations_list[random_faux_2][1] else ". "
    false_song_3 = citations_list[random_faux_3][1] if len(citations_list[random_faux_3][1]) < 80 and "Source" not in citations_list[random_faux_3][1] else ".  "
    
    return [song_citation, song_name, false_song_1, false_song_2, false_song_3]

class Quizz_View(discord.ui.View):
    """
    A View that can handle a quizz with 4 buttons and 1 good answer
    """
    def __init__(self, answers, artist, error_counter=0, tour_counter=0):
        """
        Here you save every infos you need (good and bad answers)
        """
        super().__init__(timeout=180)
        self.answers = answers
        self.artist = artist
        self.good_answer = ""
        self.errorCounter = error_counter
        self.tourCounter = tour_counter
        self.bon = True
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
            self.tourCounter += 1
            answers = get_citation(self.artist)
            citation = answers.pop(0)
            embed = discord.Embed(
                title=self.artist + f"\t{self.tourCounter - self.errorCounter}/{self.tourCounter} ✅", description=citation[0:4090])
            await interaction.response.edit_message(embed = embed, view=Quizz_View(answers, self.artist, self.errorCounter, self.tourCounter))
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
            if self.bon is True:
                self.errorCounter += 1
                self.bon = False
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
@bot.tree.command(description="Testes tes connaissances en rap fr")
async def citations(interaction: discord.Interaction, artist: str = "artist"):
    artist = artist.lower()
    ARTISTS = "Alpha Wann, Ash Kidd, Booba, Chilla, Damso, Dinos, Django, Dosseh, Doums, Doxx, Georgio, Hamza, Jazzy Bazz, Josman, Laylow, Lomepal, Lord Esperanza, Lonepsi, Nekfeu, Népal, Ninho, Orelsan, PLK, PNL, Prime, SCH, Sofiane, Vald, Zia"
    if artist == "artist":
        return await interaction.response.send_message(content= ARTISTS)
    elif artist not in ARTISTS.lower():
        return await interaction.response.send_message(content= "L'artist n'est pas répertorié dsl", ephemeral=True)

    await interaction.response.defer()
    answers = get_citation(artist)
    if answers == 0:
        return await interaction.followup.send(content= "Erreur pdnt le scraping tu site dsl", ephemeral=True)

    citation = answers.pop(0)
    embed = discord.Embed(
                    title=artist, description=citation[0:4090])
    await interaction.followup.send(embed = embed, view=Quizz_View(answers, artist))