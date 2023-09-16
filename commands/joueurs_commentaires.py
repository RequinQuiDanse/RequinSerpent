import csv
from bot import bot, discord
import random
import pandas as pd  # comme mathis


def modifier_info_csv(nom_fichier, blaze, nouvelles_infos):
    # Ouvrir le fichier CSV en mode écriture
    with open(nom_fichier, mode='r', encoding="UTF-8") as fichier:
        lecteur_csv = csv.DictReader(fichier)
        donnees = list(lecteur_csv)

    # Trouver la ligne avec le blaze spécifié et mettre à jour les informations
    for ligne in donnees:
        if ligne['blaze'] == blaze:
            ligne.update(nouvelles_infos)
            break

    # Ouvrir le fichier CSV en mode écriture
    with open(nom_fichier, mode='w', newline='', encoding="UTF-8") as fichier:
        champs = ['blaze', 'fort', 'faible']
        ecrivain_csv = csv.DictWriter(fichier, fieldnames=champs)
        ecrivain_csv.writeheader()
        ecrivain_csv.writerows(donnees)

    print(
        f"Les informations pour '{blaze}' ont été mises à jour dans le fichier '{nom_fichier}'")

def chercher_info_csv(nom_fichier, blaze):
    # Ouvrir le fichier CSV en mode lecture
    with open(nom_fichier, mode='r', encoding="UTF-8") as fichier:
        lecteur_csv = csv.DictReader(fichier)
        donnees = list(lecteur_csv)

    print(blaze)
    # Trouver la ligne avec le blaze spécifié
    for ligne in donnees:
        if ligne['blaze'] == blaze:
            return ligne

    # Si le blaze n'a pas été trouvé, renvoyer None
    return None


CLUB = r"csv_files/club_team.csv"
JOUEURS_COMMENTAIRE_CSV = r"csv_files/joueurs_commentaires.csv"


@bot.tree.command(description="Ultimate player infos")
async def player_data(interaction: discord.Interaction):
    """
    cmd to randomly make teams, depends on how much the user wants teams
    """
    embed = get_player_embed()

    await interaction.response.send_message(embed=embed, view=player_data_action())


class player_data_action(discord.ui.View):
    """
    buttons for the user to choose weither he wants to edit teams' players or to make the teams
    """
    @discord.ui.button(label='Modifie les infos', style=discord.ButtonStyle.green)
    async def edit_data(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(player_data_edit())

    @discord.ui.button(label='Choisi un joueur', style=discord.ButtonStyle.green)
    async def choose_player(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(choose_player_modal())

    @discord.ui.button(label='Menu', style=discord.ButtonStyle.green)
    async def menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = get_player_embed()
        await interaction.response.edit_message(embed=embed, view=player_data_action())


class choose_player_modal(discord.ui.Modal, title="Quel joueur veux tu "):
    player = discord.ui.TextInput(
        label="Quelle joueur:",
        placeholder="(attention case sensitive)"
    )

    async def on_submit(self, interaction: discord.Interaction):
        """
        from the group selected (as, club), create random teams
        """
        player_data = chercher_info_csv(
            JOUEURS_COMMENTAIRE_CSV, self.player.value)
        message = [
            f"Point fort : {player_data['fort']}\nPoint faible : {player_data['faible']}"]

        embed = discord.Embed(color=discord.Color.random(),
                              title=player_data["blaze"])
        embed.add_field(name="```Infos :```", value=f'```bash\n"\n' +
                        "\n".join(message)+'\n"```', inline=True)

        await interaction.response.edit_message(embed=embed, view=player_data_action())



class player_data_edit(discord.ui.Modal, title="Modifies les infos d'un joueur"):
    player = discord.ui.TextInput(
        label="Quelle joueur:",
        placeholder="(case sensitive)"
    )
    what_change = discord.ui.TextInput(
        label="Quelle catégorie :",
        placeholder="Point fort = 1 ; Point faible = 2"
    )
    infos = discord.ui.TextInput(
        label="Infos :",
        placeholder=""
    )

    async def on_submit(self, interaction: discord.Interaction):

        colomn = "fort" if self.what_change.value == "1" else "faible"
        modifier_info_csv(JOUEURS_COMMENTAIRE_CSV, self.player.value, {colomn: self.infos.value})
       
        player_data = chercher_info_csv(
            JOUEURS_COMMENTAIRE_CSV, self.player.value)
        message = [
            f"Point fort : {player_data['fort']}\nPoint faible : {player_data['faible']}"]

        embed = discord.Embed(color=discord.Color.random(),
                              title=player_data["blaze"])
        embed.add_field(name="```Infos :```", value=f'```bash\n"\n' +
                        "\n".join(message)+'\n"```', inline=True)
        
        await interaction.response.edit_message(embed=embed)

def get_player_embed():
    club_players = pd.read_csv(CLUB)["club"]
    embed = discord.Embed(color=discord.Color.random(), title="Joueurs")
    embed.add_field(name="```Joueurs:```", value=f'```bash\n"\n' +
                    "\n".join(club_players)+'\n"```', inline=True)
    return embed