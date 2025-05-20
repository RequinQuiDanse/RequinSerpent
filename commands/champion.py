from bot import bot, discord, commands
import sqlite3
from sqlite3 import Error

# Fonction pour exécuter une requête SQL avec ouverture/fermeture de connexion


def execute_query(path, query):
    try:
        # Ouverture de la connexion
        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()
            print(">>>", query)
            result = cursor.execute(query)
            # Commit uniquement pour les requêtes modifiant les données
            if query.strip().lower().startswith(("insert", "update", "delete")):
                connection.commit()
            return result.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")
        return None


# Définir les bases de données et leur configuration
db_top_team_2024 = {name: name + "_top_team_2024" for name in [
    "database", "draft", "bans", "adc_supp", "top_mid_jungle"]}
db_2023 = {name: name +
           "_2023" for name in ["database", "draft", "bans", "adc_supp", "top_mid_jungle"]}
all_db = {db_2023["database"]: db_2023,
          db_top_team_2024['database']: db_top_team_2024}
all_db_names = [db["database"] for db in all_db.values()]

# Classe Modal pour choisir un champion


class Champion_Modal(discord.ui.Modal, title='Champion'):
    name = discord.ui.TextInput(
        label='Nom',
        placeholder='Nom du champ ici...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        champ = self.name.value
        await interaction.response.send_message(view=LaneView(champ))

# Classe Select pour choisir la lane et la base de données


class LaneSelect(discord.ui.Select):
    def __init__(self, champion):
        self.champion = champion.title()
        options = [discord.SelectOption(label=name) for name in all_db_names]
        for all_lane in ['top', 'jungle', 'mid', 'adc', 'support']:
            options.append(discord.SelectOption(
                label=all_lane.capitalize(), description=''))

        super().__init__(placeholder='Quelle jeu de données et quelle lane?',
                         min_values=2, max_values=2, options=options)

    async def callback(self, interaction: discord.Interaction):
        lane = self.values[0].lower()
        db_name = self.values[1] if self.values[0] in all_db_names else self.values[0]
        db = all_db.get(db_name)

        if not db:
            return await interaction.response.send_message("Base de données inconnue", ephemeral=True)

        lane = self.values[1].lower(
        ) if self.values[0] in all_db_names else self.values[0].lower()
        path = r"2024-total-database.db"

        try:
            bans = execute_query(
                path,
                f"SELECT champion, {self.champion.replace(' ', '_')} FROM {db['bans']} ORDER BY {
                    self.champion.replace(' ', '_')} DESC LIMIT 15"
            )
            if not bans:
                raise ValueError("Champion inconnu")
        except Exception:
            return await interaction.response.send_message("Champion inconnu", ephemeral=True)

        embed = discord.Embed(title=f"{self.champion} {lane} {
                              db['database']}", color=discord.Color.random())
        for all_lane in ['top', 'jungle', 'mid', 'adc', 'support']:
            if all_lane != lane:
                res = execute_query(
                    path,
                    f"SELECT {all_lane}, count(*) FROM {db['draft']} WHERE {lane} = '{
                        self.champion}' GROUP BY {all_lane} ORDER BY count(*) DESC LIMIT 10"
                )
                if res:
                    embed.add_field(name=f"{all_lane.capitalize()} les + picks",
                                    value="\n".join(f"{champ[0]}: {champ[1]} picks" for champ in res))

        # Ajouter les statistiques spécifiques aux duos ou trios
        if lane in ['adc', 'support']:
            res = execute_query(
                path,
                f"SELECT adc, support, count FROM {db['adc_supp']} WHERE {
                    lane} = '{self.champion}' ORDER BY count DESC LIMIT 10"
            )
            if res:
                embed.add_field(name="Duos adc supp", value="\n".join(
                    f"{duo[0]} - {duo[1]}: {duo[2]} picks" for duo in res))
        elif lane in ['top', 'jungle', 'mid']:
            res = execute_query(
                path,
                f"SELECT top, jungle, mid, count FROM {db['top_mid_jungle']} WHERE {
                    lane} = '{self.champion}' ORDER BY count DESC LIMIT 10"
            )
            if res:
                embed.add_field(name="Trio top mid jungle", value="\n".join(
                    f"{trio[0]} - {trio[1]} - {trio[2]}: {trio[3]} picks" for trio in res))

        if bans:
            embed.add_field(name="Champion les + bannis",
                            value="\n".join(f"{champ[0]}: {champ[1]} bans" for champ in bans))

        await interaction.response.edit_message(embed=embed, view=None)

# Classe View pour sélectionner la lane


class LaneView(discord.ui.View):
    def __init__(self, champion):
        super().__init__()
        self.add_item(LaneSelect(champion))


@bot.tree.command(guild=discord.Object(id=769911179547246592), description="Data incroyables sur ton champ")
async def champion(interaction: discord.Interaction):
    await interaction.response.send_modal(Champion_Modal())
