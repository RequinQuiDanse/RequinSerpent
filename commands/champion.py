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
    # print(">>>"+sql)
    try:
        res = cur.execute(sql)
    except Error as e:
        print(f"The error '{e}' occurred")

    return res



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
    def __init__(self, champion):
        self.champion = champion
        options = []
        for all_lane in ['top', 'jungle', 'mid', 'adc', 'support']:
            options.append(discord.SelectOption(
                label=all_lane.capitalize(), description=''))

        super().__init__(placeholder='Quelle lane?',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        lane = self.values[0]
        try:
            bans = do_sql(('SELECT champion, '+self.champion.replace(' ', '_')+' FROM bans_count ORDER BY Varus DESC LIMIT 15')).fetchall()
        except:
            return await interaction.response.send_message("Champion inconnu")

        embed = discord.Embed(title=self.champion, color=discord.Color.random())
        for all_lane in ['top', 'jungle', 'mid', 'adc', 'support']:
            if all_lane != lane:
                res = do_sql(f"SELECT {all_lane}, count(*) FROM draft WHERE {lane} = '{self.champion}' GROUP BY {all_lane} ORDER BY count(*) DESC LIMIT 10").fetchall()
                string = ''
                for champ in res:
                    string += f'{champ[0]}: {champ[1]} picks\n' 
                embed.add_field(name=all_lane.capitalize()+' les + picks', value=string)

        string = ''
        for champ in bans:
            string += f'{champ[0]}: {champ[1]} picks\n' 
        embed.add_field(name='Champion les + bannis', value=string)
        await interaction.response.send_message(embed=embed)


class LaneView(discord.ui.View):
    def __init__(self, champion):
        super().__init__()
        self.add_item(LaneSelect(champion))

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Data incroyables sur ton champ")
async def champion(interaction: discord.Interaction):
    """
    """
    await interaction.response.send_modal(Champion_Modal())
