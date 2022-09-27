from bot import bot, discord
import random
import pandas as pd  # comme mathis

as_team = r"csv_files/as_team.csv"
club_team = r"csv_files/club_team.csv"



@bot.tree.command(guild=discord.Object(id=769911179547246592), description="Ultimate team maker")
async def ultimate_team(interaction: discord.Interaction):
    CLUB = pd.read_csv(club_team)["club"]
    AS = pd.read_csv(as_team)["as"]
    embed = discord.Embed(color=discord.Color.random(), title="Joeurs")
    embed.add_field(name="```Club:```", value=f'```bash\n"\n'+"\n".join(CLUB)+'\n"```', inline=True)
    embed.add_field(name="```As:```", value=f'```ini\n[\n'+"\n".join(AS)+'\n]```', inline=True)

    await interaction.response.send_message(embed=embed, view=Compo_Options())

# class Compo_Choice(discord.ui.View):

#     @discord.ui.button(label='Équipe Club', style=discord.ButtonStyle.green)
#     async def club(self, interaction: discord.Interaction, button: discord.ui.Button):
#         embed =  discord.Embed(color= discord.Color.random(), title= "Équipe club")
#         embed.add_field(name= "Joueurs:", value= "\n".join(CLUB))
#         self.clear_items()
#         await interaction.response.edit_message(embed = embed, view = Compo_Options())

#     @discord.ui.button(label='Équipe AS', style=discord.ButtonStyle.blurple)
#     async def a_s(self, interaction: discord.Interaction, button: discord.ui.Button):
#         embed =  discord.Embed(color= discord.Color.random(), title= "Équipe AS")
#         embed.add_field(name= "Joueurs:", value= "\n".join(AS))
#         self.clear_items()
#         await interaction.response.edit_message(embed = embed, view = Compo_Options())


class Compo_Options(discord.ui.View):

    @discord.ui.button(label='Modifier les joueurs', style=discord.ButtonStyle.green)
    async def edit_team(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Edit_Team_Modal())

    @discord.ui.button(label='Faire équipe', style=discord.ButtonStyle.green)
    async def make_team(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Make_Team_Modal())


class Edit_Team_Modal(discord.ui.Modal, title="Edit la team"):

    team = discord.ui.TextInput(
        label="Quelle équipe: Club = 1 ; As = 2",
        placeholder="0 si rien"
    )
    ajouter = discord.ui.TextInput(
        label="Ajouter un joueur?",
        placeholder="0 si rien"
    )

    retirer = discord.ui.TextInput(
        label="Retirer des joueurs",
        placeholder="0 si rien"
    )

    async def on_submit(self, interaction: discord.Interaction):
        if self.team.value == "1":
            team = fr"csv_files/club_team.csv"
            _team = "club"
            read = pd.read_csv(club_team)["club"]
        elif self.team.value == "2":
            team = fr"csv_files/as_team.csv"
            _team = "as"
            read = pd.read_csv(as_team)["as"]
        else:
            return
        if self.ajouter.value != "0":
            df = pd.DataFrame({_team: [self.ajouter.value]})
            df.to_csv(team, mode="a", index=False, header=False)

        if self.retirer.value != "0":
            line = 0
            for row in read:
                if row == self.retirer.value:
                    read = read.drop(line, axis=0, inplace=False)
                    read.to_csv(team, index=False)
                line += 1

        CLUB = pd.read_csv(club_team)["club"]
        AS = pd.read_csv(as_team)["as"]
        embed = discord.Embed(color=discord.Color.random(), title="Joeurs")
        embed.add_field(name="```Club:```", value=f'```bash\n"\n'+"\n".join(CLUB)+'\n"```', inline=True)
        embed.add_field(name="```As:```", value=f'```ini\n[\n'+"\n".join(AS)+'\n]```', inline=True)

        await interaction.response.edit_message(embed=embed)


class Make_Team_Modal(discord.ui.Modal, title="Fait les équipes"):

    team = discord.ui.TextInput(
        label="Quelle équipe: Club = 1 ; As = 2",
        placeholder="0 si rien"
    )
    number_of_team = discord.ui.TextInput(
        label="Cbm d'équipes? 1, 2, 3..?",
        placeholder="0 si rien"
    )

    async def on_submit(self, interaction: discord.Interaction):
        CLUB = pd.read_csv(club_team)["club"]
        AS = pd.read_csv(as_team)["as"]
        embed = discord.Embed(color=discord.Color.random(), title=f"Équipes:")

        number_of_team = chr(int(self.number_of_team.value)+97)  # 1 = b; 2 = c

        TEAMS = list(letter_range("A", number_of_team))
        players = []

        line = 0
        if self.team.value == "1":
            for i in CLUB:
                players.append(i)
            my_teams = assign_players_to_teams(TEAMS, players)
            for team, name in my_teams.items():
                name = str(name).replace(
                    "[", "-").replace("'", "").replace(",", "").replace("]", "")
                if line % 2 == 0:
                    embed.add_field(
                        name=f"Équipe {team}:", value=f"```diff\n{name}```", inline=True)
                else: 
                    embed.add_field(
                        name=f"Équipe {team}:", value=f"```fix\n{name}```", inline=True)
                line += 1

        elif self.team.value == "2":
            for i in AS:
                players.append(i)
            my_teams = assign_players_to_teams(TEAMS, players)
            for team, name in my_teams.items():
                name = str(name).replace(
                    "[", "-").replace("'", "").replace(",", "").replace("]", "")
                if line % 2 == 0:
                    embed.add_field(
                        name=f"Équipe {team}:", value=f"```diff\n{name}```", inline=True)
                else: 
                    embed.add_field(
                        name=f"Équipe {team}:", value=f"```fix\n{name}```", inline=True)
                line += 1
        else:
            print("Problème")

        await interaction.response.edit_message(embed=embed)


def letter_range(start, stop="{", step=1):
    """Yield a range of lowercase letters."""
    for ord_ in range(ord(start.upper()), ord(stop.upper()), step):
        yield chr(ord_)


def assign_players_to_teams(teams, players):
    players_on_teams = dict()
    # changed to .sample because .shuffle doesn't work on tuples / immutable sequences
    randomized_players = random.sample(players, len(players))
    for i, team in enumerate(teams):
        players_on_teams[team] = randomized_players[i::len(teams)]
    return players_on_teams
