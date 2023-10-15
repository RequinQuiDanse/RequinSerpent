from bot import bot, discord, commands
from commands.poulytopia import main_commands
LETTERS = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣"
# LETTERS_LIST = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬"]
LETTERS_LIST = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
BLACK_CASE = "▫️ "
RED_MARK = "🔴 "
YELLOW_MARK = "🟡 "
GREEN_MARK = "✅ "

@bot.tree.command(description="Puissance 4")
async def puissance_4(interaction: discord.Interaction, adversaire_id: str):


    ctx = await commands.Context.from_interaction(interaction)

    guild = bot.get_guild(634062663391117333)
    user_id = ctx.message.author.id
    user_name = ctx.message.author.name
    adversaire = guild.get_member_named(adversaire_id)
    adversaire_name = adversaire.name
    adversaire_id = adversaire.id

    plateau = f"**🔴 {user_name} VERSUS {adversaire_name} 🟡**\n\n"
    plateau += f"\t{LETTERS}\n\t{BLACK_CASE*7}\n\t{BLACK_CASE*7}\n\t{BLACK_CASE*7}\n\t{BLACK_CASE*7}\n\t{BLACK_CASE*7}\n\t{BLACK_CASE*7}"
    
    await interaction.response.send_message(content=plateau, view=Power4_Buttons(user_id, adversaire_id, user_name, adversaire_name))


class Power4_Buttons(discord.ui.View):
    def __init__(self, user_id, adversaire_id, user_name, adversaire_name, poule_bet=None):
        super().__init__(timeout=None)
        self.button = dict()
        self.user_id = user_id
        self.adversaire_id = adversaire_id
        self.user_name = user_name
        self.adversaire_name = adversaire_name
        self.poule_bet = poule_bet
        self.tour = 0
        self.plateau = ""
        self.a = [BLACK_CASE, BLACK_CASE, BLACK_CASE,
                  BLACK_CASE, BLACK_CASE, BLACK_CASE]
        self.b = [BLACK_CASE, BLACK_CASE, BLACK_CASE,
                  BLACK_CASE, BLACK_CASE, BLACK_CASE]
        self.c = [BLACK_CASE, BLACK_CASE, BLACK_CASE,
                  BLACK_CASE, BLACK_CASE, BLACK_CASE]
        self.d = [BLACK_CASE, BLACK_CASE, BLACK_CASE,
                  BLACK_CASE, BLACK_CASE, BLACK_CASE]
        self.e = [BLACK_CASE, BLACK_CASE, BLACK_CASE,
                  BLACK_CASE, BLACK_CASE, BLACK_CASE]
        self.f = [BLACK_CASE, BLACK_CASE, BLACK_CASE,
                  BLACK_CASE, BLACK_CASE, BLACK_CASE]
        self.g = [BLACK_CASE, BLACK_CASE, BLACK_CASE,
                  BLACK_CASE, BLACK_CASE, BLACK_CASE]
        self.board = [self.a, self.b, self.c, self.d, self.e, self.f, self.g]
        self.width = 7
        self.height = 6
        self.set_buttons()

    def set_buttons(self):
        for i in range(7):
            self.button[i] = discord.ui.Button(
                style=discord.ButtonStyle.blurple, label=LETTERS_LIST[i], custom_id=str(i))

        for add in range(7):
            self.add_item(self.button[add])

    async def interaction_check(self, interaction: discord.Interaction, /):
        await interaction.response.defer()
        self.tour += 1
        if self.tour % 2 == 0:
            if interaction.user.id != self.adversaire_id:
                self.tour -= 1
                await interaction.response.send_message(content="Pas ton tour", ephemeral=True)
                return
            color = YELLOW_MARK
        else:
            if interaction.user.id != self.user_id:
                self.tour -= 1
                await interaction.response.send_message(content="Pas ton tour", ephemeral=True)
                return
            color = RED_MARK
        # if interaction.user.id == self.user_id:
        #     color = YELLOW_MARK
        # else:
        #     color = RED_MARK

        colomn = int(interaction.data.get('custom_id'))

        i = 0
        for element in self.board[colomn]:
            if element != BLACK_CASE:
                self.board[colomn][i-1] = color
                # line = i-1
                break
            elif i == 5:
                self.board[colomn][i] = color
                # line = i
                break
            i += 1

        self.plateau = f"**🔴 {self.user_name} VERSUS {self.adversaire_name} 🟡**\n\n"

        result = self.verif()

        if result != 0:
            for element in result:
                if color == RED_MARK:
                    self.board[element[0]][element[1]] = "❤ "
                else:
                    self.board[element[0]][element[1]] = "🔆 "

            self.clear_items()

            if self.tour % 2 == 0:
                self.plateau += f"**{self.adversaire_name} REMPORTE**, {self.user_name} perd\n"
            else:
                self.plateau += f"**{self.user_name} REMPORTE**, {self.adversaire_name} perd\n"

            if self.tour % 2 == 0:
                winner_id = self.adversaire_id
                loser_id = self.user_id
            else:
                winner_id = self.user_id
                loser_id = self.adversaire_id

            if type(self.poule_bet) == list:
                if self.tour % 2 == 0:
                    main_commands.sell_poule(main_commands.cur, main_commands.con, loser_id, self.poule_bet[0])
                    main_commands.add_poule_no_verif(main_commands.cur, main_commands.con, winner_id, self.poule_bet[0], main_commands.datetime.now())
                else:
                    main_commands.sell_poule(main_commands.cur, main_commands.con, loser_id, self.poule_bet[1])
                    main_commands.add_poule_no_verif(main_commands.cur, main_commands.con, winner_id, self.poule_bet[1], main_commands.datetime.now())

            elif self.poule_bet == "tirage":
                poule = main_commands.get_random_poule(main_commands.cur)

                embed, file = main_commands.create_embed(
                    title=f"**{poule['poule_name']}**", poule=poule, avatar=None, fermier_id=winner_id)
                
                await interaction.followup.send(
                    file=file, embed=embed, view=main_commands.Daily_Button(poule, winner_id)
                )

            elif type(self.poule_bet) == int:
                main_commands.gain_money(main_commands.cur, main_commands.con, fermier_id = winner_id, value=self.poule_bet)
                main_commands.lose_money(main_commands.cur, main_commands.con, fermier_id = loser_id, value=self.poule_bet)

        self.plateau += '\t'+LETTERS

        for hauteur in range(6):
            self.plateau += "\n\t"
            for largeur in range(7):
                self.plateau += str(self.board[largeur][hauteur])

        await interaction.followup.edit_message(message_id=interaction.message.id, content=self.plateau, view=self)

    async def on_timeout(self):
        if type(self.poule_bet) == list:
            if self.tour % 2 == 0:
                main_commands.sell_poule(main_commands.cur, main_commands.con, self.user_id, self.poule_bet[0])
                main_commands.add_poule_no_verif(main_commands.cur, main_commands.con, self.adversaire_id, self.poule_bet[0], main_commands.datetime.now())
            else:
                main_commands.sell_poule(main_commands.cur, main_commands.con, self.adversaire_id, self.poule_bet[1])
                main_commands.add_poule_no_verif(main_commands.cur, main_commands.con, self.user_id, self.poule_bet[1], main_commands.datetime.now())

    def verif(self):
        # Vérifie toutes les combinaisons de 4 pions sur le tableau
        for x in range(self.width):
            for y in range(self.height):
                # Vérifie la ligne
                if y + 3 < self.height:
                    pions = [self.board[x][y+i] for i in range(4)]
                    if all(pion == YELLOW_MARK for pion in pions):
                        return [[x, y+i] for i in range(4)]
                    elif all(pion == RED_MARK for pion in pions):
                        return [[x, y+i] for i in range(4)]
                # Vérifie la colonne
                if x + 3 < self.width:
                    pions = [self.board[x+i][y] for i in range(4)]
                    if all(pion == YELLOW_MARK for pion in pions):
                        return [[x+i, y] for i in range(4)]
                    elif all(pion == RED_MARK for pion in pions):
                        return [[x+i, y] for i in range(4)]
                # Vérifie la diagonale de gauche à droite
                if x + 3 < self.width and y + 3 < self.height:
                    pions = [self.board[x+i][y+i] for i in range(4)]
                    if all(pion == YELLOW_MARK for pion in pions):
                        return [[x+i, y+i] for i in range(4)]
                    elif all(pion == RED_MARK for pion in pions):
                        return [[x+i, y+i] for i in range(4)]
                # Vérifie la diagonale de droite à gauche
                if x - 3 >= 0 and y + 3 < self.height:
                    pions = [self.board[x-i][y+i] for i in range(4)]
                    if all(pion == YELLOW_MARK for pion in pions):
                        return [[x-i, y+i] for i in range(4)]
                    elif all(pion == RED_MARK for pion in pions):
                        return [[x-i, y+i] for i in range(4)]
        return 0



# def verif(self, colomn, line):

#     # Calcul le nombre de cases dans la même ligne
#     # ex: X = largeur; Y = hauteur et on fait varier x
#     yellow_close = []
#     red_close = []
#     for i in range(7):
#         try:
#             if self.board[i][line] == YELLOW_MARK:
#                 red_close = []
#                 yellow_close.append([i, line])
#                 if len(yellow_close) == 4:
#                     return yellow_close
#             elif self.board[i][line] == RED_MARK:
#                 yellow_close = []
#                 red_close.append([i, line])
#                 if len(red_close) == 4:
#                     return red_close
#             else:
#                 yellow_close = []
#                 red_close = []
#         except:
#             pass

#     # Calcul le nombre de case dans la même colonne
#     # ex:y = largeur, x =hauteur et on fait varier x
#     yellow_close = []
#     red_close = []
#     for i in range(6):
#         try:
#             if self.board[colomn][i] == YELLOW_MARK:
#                 yellow_close.append([colomn, i])
#                 red_close = []
#                 if len(yellow_close) == 4:
#                     return yellow_close
#             elif self.board[colomn][line-i] == RED_MARK:
#                 red_close.append([colomn, i])
#                 yellow_close = []
#                 if len(red_close) == 4:
#                     return red_close
#             else:
#                 yellow_close = []
#                 red_close = []
#         except:
#             pass

#     # En diagonale de droite à gauche
#     # x = largeur, y = largeur et on augmente la hauteur d1 et on diminue la largeur d'1
#     yellow_close = []
#     red_close = []
#     for i in range(6):
#         try:
#             if self.board[colomn-i][line+i] == YELLOW_MARK:
#                 yellow_close.append([colomn-i, line+i])
#                 red_close = []
#                 if len(yellow_close) == 4:
#                     return yellow_close
#             elif self.board[colomn-i][line+i] == RED_MARK:
#                 red_close.append([colomn-i, line+i])
#                 yellow_close = []
#                 if len(red_close) == 4:
#                     return red_close
#             else:
#                 yellow_close = []
#                 red_close = []
#         except:
#             pass

#     # Diagonale de droite à gauche
#     # x = largeur, y = hauteur et on varie diminue d'1 la hauteur chaque tour et on augmente de 1 la largeur
#     yellow_close = []
#     red_close = []
#     for i in range(6):
#         try:
#             if self.board[colomn+i][line+i] == YELLOW_MARK:
#                 yellow_close.append([colomn+i, line+i])
#                 red_close = []
#                 if len(yellow_close) == 4:
#                     return yellow_close
#             elif self.board[colomn+i][line+i] == RED_MARK:
#                 red_close.append([colomn+i, line+i])
#                 yellow_close = []
#                 if len(red_close) == 4:
#                     return red_close
#             else:
#                 yellow_close = []
#                 red_close = []
#         except:
#             pass

#     return 0