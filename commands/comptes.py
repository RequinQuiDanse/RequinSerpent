
from discord.utils import MISSING
from bot import bot, discord

import plotly.graph_objects as go
import sqlite3
from sqlite3 import Error
import pandas as pd
import random
import plotly.graph_objects as go
import os

db_path = 'comptes.db'
def create_connection(db_path = db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def update_montant(cursor, source, destination, ajout, compte_name, compte_owner):

    montant = cursor.execute(f'SELECT SUM(montant) FROM comptes WHERE source = \'{source}\' AND destination = \'{destination}\' AND compte_name = \'{compte_name}\'').fetchall()
    print(montant)
    montant = [el[0] for el in montant][0] 
    if montant != None:
        montant += ajout
        print(montant)
        cursor.execute(f'UPDATE comptes SET montant = {montant} WHERE source = \'{source}\' AND destination = \'{destination}\' AND compte_name = \'{compte_name}\'')
    else:
        cursor.execute(f'INSERT INTO comptes (source, destination, montant, compte_name, compte_owner) VALUES  (\'{source}\', \'{destination}\', {ajout}, \'{compte_name}\', \'{compte_owner}\')')

def calculate_and_insert_reste(compte_name, compte_owner, db_path=db_path):
    # Connect to the SQLite database
    conn = create_connection(db_path)
    cursor = conn.cursor()

    # Query to calculate total amounts arriving into 'Budget'
    cursor.execute(f"""
        SELECT SUM(montant) 
        FROM comptes
        WHERE destination = 'Budget'
        AND compte_name = '{compte_name}'
    """)
    total_arrivals = cursor.fetchone()[0] or 0

    # Query to calculate total amounts leaving 'Budget'
    cursor.execute(f"""
        SELECT SUM(montant) 
        FROM comptes
        WHERE source = 'Budget'
        AND compte_name = '{compte_name}'
    """)
    total_departures = cursor.fetchone()[0] or 0

    # Calculate the remaining amount
    reste = total_arrivals - total_departures

    # Insert the remaining amount as a new row in the table
    update_montant(cursor, source='Budget', destination='Reste', ajout = reste, compte_name=compte_name, compte_owner=compte_owner)


    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def create_sankey(compte_name, db_path=db_path):
    conn = create_connection(db_path)


    # Query to extract data
    query = f'SELECT source, destination, montant FROM comptes WHERE compte_name = \'{compte_name}\''
    df = pd.read_sql_query(query, conn)

    conn.close()

    # Calculate the sum of values for each label
    source_sums = df.groupby('source')['montant'].sum().reset_index()
    destination_sums = df.groupby('destination')['montant'].sum().reset_index()

    # Create a dictionary to store the total amounts for each label
    amounts = {}

    for _, row in source_sums.iterrows():
        if row['source'] != 'Budget':
            amounts[row['source']] = row['montant']

    for _, row in destination_sums.iterrows():
        if row['destination'] in amounts:
            amounts[row['destination']] += row['montant']
        else:
            amounts[row['destination']] = row['montant']

    # Combine the data for the Sankey diagram
    labels = list(pd.concat([df['source'], df['destination']]).unique())
    source_indices = [labels.index(src) for src in df['source']]
    target_indices = [labels.index(dst) for dst in df['destination']]
    values = list(df['montant'])

    # Update labels to include the total amount
    labels_with_amounts = [f"{label} ({amounts[label]})" for label in labels]

    # Generate random colors for each node
    node_colors = [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in labels]

    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=10,
            thickness=15,
            line=dict(color="black", width=0.5),
            label=labels_with_amounts,  # Use the labels with amounts
            color=node_colors
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values
        ),
        )])
    fig.update_layout(
        title_text=f"Diagramme de Sankey pour {compte_name}", 
        font_size=10,
        margin = dict(l=35, r=35, t=35, b=35)

        )


    fig.write_image(fr"csv_files\comptes\{compte_name}.png", format='png')

def add_source(source, destination, amount, compte_name, compte_owner, table_name="comptes", db_path=db_path):
    """
    Ajoute une nouvelle source avec un nom spécifié et dont la destination est 'Budget'.

    :param db_path: Chemin vers la base de données SQLite.
    :param table_name: Nom de la table dans la base de données.
    :param source: Nom de la nouvelle source à ajouter.
    :param amount: Montant associé à la nouvelle source.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert the new source into the table
    update_montant(cursor, source=source, destination=destination, ajout = amount, compte_name=compte_name, compte_owner=compte_owner)


    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    calculate_and_insert_reste(compte_name, compte_owner)
    create_sankey(compte_name)

# def add_budget_to_destination(source, destination, amount, compte_name, table_name="comptes", db_path=db_path):
#     """
#     Ajoute une nouvelle entrée avec la source 'Budget' et une destination spécifiée.

#     :param db_path: Chemin vers la base de données SQLite.
#     :param table_name: Nom de la table dans la base de données.
#     :param source: Nom de la source
#     :param destination: Nom de la destination à ajouter.
#     :param amount: Montant associé à la destination.
#     """
#     # Connect to the SQLite database
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

    
#     # Insert the new entry into the table
#     update_montant(cursor, source=source, destination=destination, ajout = amount, compte_name=compte_name)

#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()
#     calculate_and_insert_reste(compte_name)
#     create_sankey(compte_name)


class AddIncomeModal(discord.ui.Modal, title='Revenu'):
    """
    """
    def __init__(self, compte_name):
        super().__init__()
        self.compte_name = compte_name

    source = discord.ui.TextInput(
        label='Source',
        placeholder='...',
    )
    destination = discord.ui.TextInput(
        label='destination',
        placeholder='...',
    )
    amount = discord.ui.TextInput(
        label='Montant',
        placeholder='...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user.name
        source = self.source.value
        destination = self.destination.value
        amount = int(self.amount.value)
        add_source(source=source, destination=destination, amount=amount, compte_name=self.compte_name, compte_owner=user)
        img = discord.File(fr'csv_files\comptes\{self.compte_name}.png', f'{self.compte_name}.png')
        embed = discord.Embed(color = discord.Colour.random(), title=self.compte_name).set_image(url=f"attachment://{f'{self.compte_name}.png'}")
        await interaction.response.edit_message(embed=embed, attachments=[img], view=AccountButtons(user, self.compte_name))

# class AddExpenditureModal(discord.ui.Modal, title='Dépense'):
#     """
#     """
#     def __init__(self, compte_name):
#         super().__init__()
#         self.compte_name = compte_name

#     source = discord.ui.TextInput(
#         label='Source',
#         placeholder='...',
#     )
#     destination = discord.ui.TextInput(
#         label='Destination',
#         placeholder='...',
#     )
#     amount = discord.ui.TextInput(
#         label='Montant',
#         placeholder='...',
#     )

#     async def on_submit(self, interaction: discord.Interaction):
#         user = interaction.user.name
#         source = self.source.value
#         destination = self.destination.value
#         amount = int(self.amount.value)
#         add_budget_to_destination(source = source, destination=destination, amount=amount, compte_name=self.compte_name)
#         img = discord.File(fr'csv_files\comptes\{self.compte_name}.png', f'{self.compte_name}.png')
#         embed = discord.Embed(color = discord.Colour.random(), title=self.compte_name).set_image(url=f"attachment://{f'{self.compte_name}.png'}")
#         await interaction.response.edit_message(embed=embed, attachments=[img], view=AccountButtons(user, self.compte_name))

class EditCompteModal(discord.ui.Modal, title='Dépense'):
    """
    """
    def __init__(self, compte_name):
        super().__init__()
        self.compte_name = compte_name

    source = discord.ui.TextInput(
        label='Source',
        placeholder='...',
    )
    destination = discord.ui.TextInput(
        label='Destination',
        placeholder='...',
    )
    amount = discord.ui.TextInput(
        label='Montant à enlever (chiffre positif)',
        placeholder='...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user.name
        source = self.source.value
        destination = self.destination.value
        amount = int(self.amount.value)
        conn = create_connection()
        cursor = conn.cursor()
        update_montant(cursor=cursor, source=source, destination=destination, ajout=-amount, compte_name=self.compte_name, compte_owner=user)
        conn.commit()
        conn.close()
        calculate_and_insert_reste(self.compte_name, user)
        create_sankey(self.compte_name)
        img = discord.File(fr'csv_files\comptes\{self.compte_name}.png', f'{self.compte_name}.png')
        embed = discord.Embed(color = discord.Colour.random(), title=self.compte_name).set_image(url=f"attachment://{f'{self.compte_name}.png'}")
        await interaction.response.edit_message(embed=embed, attachments=[img], view=AccountButtons(user, self.compte_name))



class AccountButtons(discord.ui.View):
    """
    """

    def __init__(self, user, compte_name):
        super().__init__()
        self.user = user
        self.compte_name = compte_name

    @discord.ui.button(label="Ajouter un revenu / une dépense", style=discord.ButtonStyle.blurple)
    async def add_income(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if interaction.user.name != self.user:
            return
        await interaction.response.send_modal(AddIncomeModal(self.compte_name))

    # @discord.ui.button(label="Ajouter une dépense", style=discord.ButtonStyle.blurple)
    # async def add_expenditure(self, interaction: discord.Interaction, buttons: discord.ui.Button):
    #     if interaction.user.name != self.user:
    #         return
    #     await interaction.response.send_modal(AddExpenditureModal(self.compte_name))

    @discord.ui.button(label="Diminuer un lien", style=discord.ButtonStyle.blurple)
    async def edit_link(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if interaction.user.name != self.user:
            return
        await interaction.response.send_modal(EditCompteModal(self.compte_name))

class UserSelect(discord.ui.Select):
    """
    """
    def __init__(self, created_account):
        options = [discord.SelectOption(
                label=compte_name) for compte_name in created_account]
       
        super().__init__(placeholder=r'Choisis ton compte',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user.name
        compte = self.values[0]
        path = fr'csv_files\comptes\{user}.png'
        if os.path.exists(path):
            img = discord.File(fr'csv_files\comptes\{user}.png', f'{user}.png')
            embed = discord.Embed(color = discord.Colour.random(), title=user).set_image(url=f"attachment://{f'{user}.png'}")
        else:
            img = discord.File(r'csv_files\comptes\image.png', 'image.png')
            embed = discord.Embed(color = discord.Colour.random(), title=user).set_image(url=f"attachment://{'image.png'}")
        
        conn = create_connection()
        cursor = conn.cursor()
        compte_owner = cursor.execute(f'SELECT compte_owner FROM comptes WHERE compte_name == \'{compte}\' LIMIT 1').fetchone()[0]
        conn.close()
        if compte_owner == user:
            await interaction.response.edit_message(embed=embed, attachments=[img], view=AccountButtons(user, compte))
        else:
            await interaction.response.edit_message(embed=embed, attachments=[img], view=None)

class UserSelectView(discord.ui.View):
    def __init__(self, created_account):
        super().__init__()
        self.add_item(UserSelect(created_account))

class CreateDiagram(discord.ui.Modal, title= 'Créer un diagramme'): #
    # def __init__(self) -> None:
    #     super().__init__()
    #     self.compte_name = compte_name

    compte_name = discord.ui.TextInput(
        label='Nom du diagramme :',
        placeholder='...',
    )
    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user.name
        compte_name = self.compte_name.value
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO comptes (source, destination, montant, compte_name, compte_owner) VALUES (\'init\', \'Budget\', 0, \'{compte_name}\', \'{user}\')')
        conn.commit()
        conn.close()
        create_sankey(compte_name)
        img = discord.File(fr'csv_files\comptes\{compte_name}.png', f'{compte_name}.png')
        embed = discord.Embed(color = discord.Colour.random(), title=compte_name).set_image(url=f"attachment://{f'{compte_name}.png'}")
        await interaction.response.edit_message(embed=embed, attachments=[img], view=AccountButtons(user, compte_name))


class SelectActionButtons(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.user = user

    @discord.ui.button(label="Voir les diagrammes", style=discord.ButtonStyle.blurple)
    async def see_diagram(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if interaction.user.name != self.user:
            return
        conn = create_connection()
        cursor = conn.cursor()
        created_account = cursor.execute('SELECT DISTINCT compte_name FROM comptes').fetchall()
        conn.close()
        created_account = [el[0] for el in created_account]
    
        await interaction.response.send_message(view=UserSelectView(created_account))

    @discord.ui.button(label="Créer un diagramme", style=discord.ButtonStyle.blurple)
    async def add_expenditure(self, interaction: discord.Interaction, buttons: discord.ui.Button):
        if interaction.user.name != self.user:
            return
        await interaction.response.send_modal(CreateDiagram())


@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Permet de visualiser son budget")
async def sankey(interaction: discord.Interaction):
    """
    
    """
    user = interaction.user.name
    await interaction.response.send_message(view=SelectActionButtons(user))
