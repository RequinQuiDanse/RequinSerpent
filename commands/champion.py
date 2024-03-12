from bot import bot, discord, commands
import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


con = create_connection(path=r"D:\code\data_analyse\2024-total-database.db")
cur = con.cursor()

def do_sql(sql):
    res = None
    print(">>>"+sql)
    try:
        res = cur.execute(sql)
    except Error as e:
        print(f"The error '{e}' occurred")

    return res


db_top_team_2024 = {name:name+"_top_team_2024" for name in ["database", "draft", "bans", "adc_supp", "top_mid_jungle"]}
db_2023 = {name:name+"_2023" for name in ["database", "draft", "bans", "adc_supp", "top_mid_jungle"]}
all_db = [db_2023, db_top_team_2024]



class Champion_Modal(discord.ui.Modal, title='Champion'):
    """
    modal to chose the champ we want
    """
    name = discord.ui.TextInput(
        label='Nom',
        placeholder='Nom du champ ici...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        champ = self.name.value

        await interaction.response.send_message(view=LaneView(champ))


class LaneSelect(discord.ui.Select):
    """
    """
    def __init__(self, champion, db):
        self.champion = champion
        self.db = db
        options = [discord.SelectOption(label=db["database"]) for db in all_db]
        for all_lane in ['top', 'jungle', 'mid', 'adc', 'support']:
            options.append(discord.SelectOption(
                label=all_lane.capitalize(), description=''))

        super().__init__(placeholder='Quelle jeu de données et quelle lane?',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        lane = self.values[0].lower()
        # if self.values[0] == "Données année 2023":
        #     ban_table = "bans_2023"
        #     draft_table = "draft_2023"
        #     bdd = "toutes données 2023"
        #     lane = self.values[1].lower()
        # elif self.values[1] == "Données année 2023":
        #     ban_table = "bans_2023"
        #     draft_table = "draft_2023"
        #     bdd = "toutes données 2023"
        #     lane = self.values[0].lower()
        # elif self.values[0] == "Données top team 2024":
        #     ban_table = "bans_top_team"
        #     draft_table = "draft_top_team"
        #     bdd = "Top team 2024"
        #     lane = self.values[1].lower()
        # else:
        #     ban_table = "bans_top_team"
        #     draft_table = "draft_top_team"
        #     bdd = "Top team 2024"
        #     lane = self.values[0].lower()

        try:
            bans = do_sql(sql='SELECT champion, '+self.champion.replace(' ', '_')+f' FROM {self.db["draft"]} ORDER BY '+self.champion.replace(' ', '_')+' DESC LIMIT 15').fetchall()
        except:
            return await interaction.response.send_message("Champion inconnu", ephemeral=True)

        embed = discord.Embed(title=f"{self.champion} {lane} {self.db["database"]}", color=discord.Color.random())
        for all_lane in ['top', 'jungle', 'mid', 'adc', 'support']:
            if all_lane != lane:
                res = do_sql(f'SELECT {all_lane}, count(*) FROM {self.db["bans"]} WHERE {lane} = "{self.champion}" GROUP BY {all_lane} ORDER BY count(*) DESC LIMIT 10').fetchall()
                string = ''
                for champ in res:
                    string += f'{champ[0]}: {champ[1]} picks\n' 
                embed.add_field(name=all_lane.capitalize()+' les + picks', value=string)

        string = ''
        for champ in bans:
            string += f'{champ[0]}: {champ[1]} bans\n' 
        embed.add_field(name='Champion les + bannis', value=string)
        await interaction.response.edit_message(embed=embed, view=None)


class LaneView(discord.ui.View):
    def __init__(self, champion):
        super().__init__()
        self.add_item(LaneSelect(champion))
        

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Data incroyables sur ton champ")
async def champion(interaction: discord.Interaction):
    """
    """
    await interaction.response.send_modal(Champion_Modal())

class DatabaseChoiceSelect(discord.ui.Select):
    """
    """
    def __init__(self):
        options = [discord.SelectOption(label=db["database"]) for db in all_db]

        super().__init__(placeholder='Quelle jeu de données et quelle lane?',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        db = self.values[0]

        try:
            bans = do_sql(sql='SELECT champion, '+self.champion.replace(' ', '_')+f' FROM {self.db["draft"]} ORDER BY '+self.champion.replace(' ', '_')+' DESC LIMIT 15').fetchall()
        except:
            return await interaction.response.send_message("Champion inconnu", ephemeral=True)

        embed = discord.Embed(title=f"{self.champion} {lane} {self.db["database"]}", color=discord.Color.random())
        for all_lane in ['top', 'jungle', 'mid', 'adc', 'support']:
            if all_lane != lane:
                res = do_sql(f'SELECT {all_lane}, count(*) FROM {self.db["bans"]} WHERE {lane} = "{self.champion}" GROUP BY {all_lane} ORDER BY count(*) DESC LIMIT 10').fetchall()
                string = ''
                for champ in res:
                    string += f'{champ[0]}: {champ[1]} picks\n' 
                embed.add_field(name=all_lane.capitalize()+' les + picks', value=string)

        string = ''
        for champ in bans:
            string += f'{champ[0]}: {champ[1]} bans\n' 
        embed.add_field(name='Champion les + bannis', value=string)
        await interaction.response.edit_message(embed=embed, view=None)


class DatabaseChoiceView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DatabaseChoiceSelect(champion))


class ChooseActionButtons(discord.ui.View):
    @discord.ui.button(label='Meta drafts', style=discord.ButtonStyle.gray)
    async def meta_drafts(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view = ChooseDatabaseButtons(action = "meta"))

    @discord.ui.button(label='Datas sur champion', style=discord.ButtonStyle.gray)
    async def champions_datas(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Champion_Modal())


@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Data incroyables sur des données incroyables")
async def lol_datas(interaction: discord.Interaction):
    """
    """
    await interaction.response.send_message(view=ChooseActionButtons())