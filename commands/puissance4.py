from bot import bot, discord, commands

LETTERS = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣"
# LETTERS_LIST = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬"]
LETTERS_LIST = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
BLACK_CASE = "▫️ "
RED_MARK = "🔴 "
YELLOW_MARK = "🟡 "
GREEN_MARK = "✅ "


@bot.tree.command(guild=discord.Object(id=769911179547246592), description="Puissance 4")
async def puissance_4(interaction: discord.Interaction, adversaire: str):
    plateau = f"{LETTERS}\n{BLACK_CASE*7}\n{BLACK_CASE*7}\n{BLACK_CASE*7}\n{BLACK_CASE*7}\n{BLACK_CASE*7}\n{BLACK_CASE*7}"
    ctx = await commands.Context.from_interaction(interaction)
    adversaire = int(adversaire.replace("<@", "").replace(">", ""))
    await interaction.response.send_message(content=plateau, view=Power4_Buttons(ctx, adversaire))


class Power4_Buttons(discord.ui.View):
    def __init__(self, ctx, adversaire):
        super().__init__(timeout=None)
        self.button = dict()
        self.user_id = ctx.message.author.id
        self.adversaire = adversaire
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
        self.tour += 1
        if self.tour % 2 == 0:
            if interaction.user.id != self.adversaire:
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
                line = i-1
                break
            elif i == 5:
                self.board[colomn][i] = color
                line = i
                break
            i += 1

        self.plateau = LETTERS

        result = self.verif()

        if result != 0:

            # for element in result:
            #     self.board[element[0]][element[1]] = GREEN_MARK
            self.clear_items()

        for hauteur in range(6):
            self.plateau += "\n"
            for largeur in range(7):
                self.plateau += str(self.board[largeur][hauteur])

        await interaction.response.edit_message(content=self.plateau, view=self)

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