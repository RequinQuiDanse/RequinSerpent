from bot import bot, discord, commands
import random
import csv

emoji = ["🇦", "🇧", "🇨"]

# Class qui va définir le fonctionnement de l'object qu'est le message avec les questions réponses


class Ultimate_View(discord.ui.View):
    def __init__(self, userId, real_answer, answer_order, embed, errorCounter, tourCounter, avatar, question_used):
        self.userId = userId  # user Id pour empêcher que qlq d'autre rep
        self.real_answer = real_answer  # stock la bonne rep
        # stock la bonne et les mauvaises rép aléatoirement
        self.answer_order = answer_order
        self.embed = embed  # le contenue textuel du message
        self.bon = True  # permet de compter les points
        self.errorCounter = errorCounter  # permet de compter les points
        self.tourCounter = tourCounter  # permet de compter les points
        # pour le style, à la fin du questionnaire ça affiche l'avatar de l'utilisateur
        self.avatar = avatar
        # Pour ne pas répéter les questions déjà utilisées
        self.question_used = question_used
        super().__init__(timeout=180)
        self.brain()

    def brain(self):  # nettoie et redéfini les boutons
        self.clear_items()
        # ajoute les boutons avec leurs valeurs etc
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label=emoji[0], custom_id=self.answer_order[0]))
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.blurple, label=emoji[1], custom_id=self.answer_order[1]))
        if self.answer_order.__len__() == 3:
            self.add_item(discord.ui.Button(
                style=discord.ButtonStyle.blurple, label=emoji[2], custom_id=self.answer_order[2]))

    async def interaction_check(self, interaction=discord.Interaction):
        if self.userId != interaction.user.id:  # empêche les gens d'utiliser le quizz d'un autre
            return
        self.clear_items()
        response = interaction.data.get('custom_id')

        if response == 'stop':  # Mets fin au quizz
            self.clear_items()
            self.tourCounter += 1
            embed = discord.Embed(
                title=f"Ultimate Quizz   ```{self.tourCounter - self.errorCounter} sur {self.tourCounter} gg```").set_image(url=self.avatar)
            await interaction.response.edit_message(embed=embed, view=None)

        if response == 'Suivant':  # lance une autre question
            self.tourCounter += 1
            random_file = random.choice(
                [r"csv_files\ultimate.csv", r"csv_files\ultimate_gestes.csv"])
            with open(random_file, mode='r', encoding="UTF-8") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line = 0
                real_answer_link = None

                # Déclaration des questions / réponses si on utilise les questions manuscrites
                if random_file == r"csv_files\ultimate.csv":
                    randomResult = random.randint(1, 31)
                    # On évite les répétitions
                    while str(random_file) + str(randomResult) in self.question_used:
                        randomResult = random.randint(1, 31)
                    for row in csv_reader:  # On récupère la ligne choisit au hasard auparavant
                        if line == randomResult:
                            question = row['question']
                            real_answer = row['answer']
                            false_answer_1 = row['false_answer_1']
                            false_answer_2 = row['false_answer_2']
                        line += 1

                     # On stock les réponses
                    all_answers = [real_answer, false_answer_1]
                    if str(false_answer_2) != "None":
                        all_answers = [real_answer,
                                       false_answer_1, false_answer_2]

                    # Change l'ordre des questions pour les afficher aléatoirements (sinon la bonne réponse serait tjr la première)
                    answer_order = random.sample(all_answers, len(all_answers))

                    # Création du message discord
                    embed = discord.Embed(title=f"Ultimate Quizz ```{self.tourCounter - self.errorCounter} sur {self.tourCounter}```",
                                          description=f"**```{question}```**")
                    embed.add_field(
                        name=emoji[0], value=f"```{answer_order[0]}```", inline=True)
                    embed.add_field(
                        name=emoji[1], value=f"```{answer_order[1]}```", inline=True)
                    # Mets une 3ème question si il yen a une (pour les questions manuscrites)
                    if str(false_answer_2) != "None":
                        embed.add_field(
                            name=emoji[2], value=f"```{answer_order[2]}```", inline=True)

                    self.question_used.append(
                        str(random_file) + str(randomResult))  # on stock la question pour ne pas qu'elle revienne plus tard

                    # et c'est la chenille qui redémarre
                    await interaction.response.edit_message(view=Ultimate_View(self.userId, real_answer, answer_order, embed, self.errorCounter, self.tourCounter, self.avatar, self.question_used), embed=embed)

                else:  # Si on utilise les images en questions
                    # La questions/réponse que l'on veut
                    randomResult = random.randint(1, 14)
                    # On évite les répétitions
                    while str(random_file) + str(randomResult) in self.question_used:
                        randomResult = random.randint(1, 31)
                    # On prend une autre réponse au hasard
                    randomFaux1 = random.randint(1, 14)
                    while randomFaux1 == randomResult:  # check pour ne pas avoir 2 fois la même réponse
                        randomFaux1 = random.randint(1, 14)
                    randomFaux2 = random.randint(1, 14)
                    # check pour ne pas avoir 2 fois la même réponse
                    while randomFaux2 == randomResult or randomFaux2 == randomFaux1:
                        randomFaux2 = random.randint(1, 14)
                    for row in csv_reader:  # On récupère 3 lignes aléatoires choisit avant, 1 sera la bonne et 2 seront les fausses réponses
                        if line == randomResult:
                            question = "Qu'elle est ce signe?"
                            real_answer = row['answer']
                            real_answer_link = row['link']
                        elif line == randomFaux1:
                            false_answer_1 = row['answer']
                        elif line == randomFaux2:
                            false_answer_2 = row['answer']
                        line += 1

                    # Stockage des réponses
                    all_answers = [real_answer, false_answer_1]
                    if str(false_answer_2) != "None":
                        all_answers = [real_answer,
                                       false_answer_1, false_answer_2]
                    # Changement de l'ordre des questions
                    answer_order = random.sample(all_answers, len(all_answers))

                    # msg discord
                    embed = discord.Embed(title=f"Ultimate Quizz ```{self.tourCounter - self.errorCounter} sur {self.tourCounter}```",
                                          description=f"**```{question}```**").set_image(url=real_answer_link)
                    embed.add_field(
                        name=emoji[0], value=f"```{answer_order[0]}```", inline=True)
                    embed.add_field(
                        name=emoji[1], value=f"```{answer_order[1]}```", inline=True)
                    # Mets une 3ème question si il yen a une (pour les questions manuscrites)
                    # if str(false_answer_2) != "None":
                    embed.add_field(
                        name=emoji[2], value=f"```{answer_order[2]}```", inline=True)

                    self.question_used.append(
                        str(random_file) + str(randomResult)) # Stockage de la question pour ne pas qu'elle revienne après
                    print(f"Real answer ligne: {randomResult} / lenght: {real_answer.__len__()}\nfalse answer1 ligne: {randomFaux1} / lenght: {false_answer_1.__len__()}\nfalse answer2 ligne: {randomFaux2} / lenght: {false_answer_2.__len__()}\nfalse answer3 ligne: {randomResult} / lenght: {real_answer.__len__()}")

                    # et c'est la chenille qui redémarre
                    await interaction.response.edit_message(view=Ultimate_View(self.userId, real_answer, answer_order, embed, self.errorCounter, self.tourCounter, self.avatar, self.question_used), embed=embed)

        count = 0
        if response == self.real_answer: # Quand la réponse est bonne:
            self.bon = True # permet de compter les points
            for x in self.answer_order: # galère pour mettre la case en vert et rajouter les boutons "suivant" et "next"
                if str(response) == str(x):
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.green, label=emoji[count], custom_id=self.answer_order[count], disabled=True))
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.primary, label='Suivant', custom_id='Suivant', row=2))
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.red, label='Stop', custom_id='stop', row=2))
                else: # rajoute les boutons A B ou C qui ne sont pas la réponse (pas facile à expliquer jsp même pas comment je suis arriver à coder comme ça c moche)
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.blurple, label=emoji[count], custom_id=self.answer_order[count], disabled=True))
                count += 1
        else: # Si le réponse est fausse:
            if self.bon is True: # compte les points
                self.errorCounter += 1
                self.bon = False
            for x in self.answer_order: # galère pour mettre le bouton en rouge / gris
                if str(response) == str(x):
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.red, label=emoji[count], custom_id=self.answer_order[count]))
                else:
                    self.add_item(discord.ui.Button(
                        style=discord.ButtonStyle.blurple, label=emoji[count], custom_id=self.answer_order[count]))
                count += 1

        # et c la chenille qui fait jsp quoi
        await interaction.response.edit_message(view=self, embed=self.embed)

    # Ca c'est parce que JE COMPRENDS RIEN YA UN MSG D'ERREUR QUI DIT QUE J'AI Déjà REP AU MESSAGE ET JSP COMMENT L'ENLEVER bordel dcp j'ai dit que quand il ya une erreur ba ça affiche rien ntr discord.py
    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item) -> None:
        if str(error).__contains__("This interaction has already been responded to before"):
            print("", end="")
        # return await super().on_error(interaction, error, item)
#________________________________________________________________________________________________________________________________#


@bot.tree.command(description="Ultimate Quizz (base de donnée avec nos questions!)")
async def quizz(interaction: discord.Interaction): # Ici on creer la commande sur discord, et on dit ce qu'il se passe quand on l'appel
    question_used = [] # je vais stocker toutes les questions déjà utilisées pour ne pas les répéter (jsp si ça marche encore)
    random_file = random.choice(
        [r"csv_files\ultimate.csv", r"csv_files\ultimate_gestes.csv"]) # choisis un des 2 fichier de questions au hasard
    with open(random_file, mode='r', encoding="UTF-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line = 0
        real_answer_link = None

        # Déclaration des questions et réponses si on utilise les questions manuscrites
        if random_file == r"csv_files\ultimate.csv":
            randomResult = random.randint(1, 31)
            for row in csv_reader: # Récupère questions et réponses d'une ligne au hasard choisit auparavant
                if line == randomResult: 
                    question = row['question']
                    real_answer = row['answer']
                    false_answer_1 = row['false_answer_1']
                    false_answer_2 = row['false_answer_2']
                line += 1

            # stockage des réponses pour les réutiliser tout le temps après (vérification des réponses si elles sont bonnes ou mauvaises)
            all_answers = [real_answer, false_answer_1] 
            if str(false_answer_2) != "None":
                all_answers = [real_answer, false_answer_1, false_answer_2]

            # Change l'ordre des questions pour les afficher aléatoirement sinon ça serait tjr la questions 1 qui serait affiché en première
            answer_order = random.sample(all_answers, len(all_answers))
            
            # Création du msg discord
            embed = discord.Embed(title="Ultimate Quizz",
                                  description=f"**```{question}```**")
            embed.add_field(
                name=emoji[0], value=f"```{answer_order[0]}```", inline=True)
            embed.add_field(
                name=emoji[1], value=f"```{answer_order[1]}```", inline=True)
            # Mets une 3ème question si il yen a une (pour les questions manuscrites)
            if str(false_answer_2) != "None":
                embed.add_field(
                    name=emoji[2], value=f"```{answer_order[2]}```", inline=True)
                print(
                    f"Real answer ligne: {randomResult} / lenght: {real_answer.__len__()}\nfalse answer1 lenght: {false_answer_1.__len__()}\nfalse answer2 lenght: {false_answer_2.__len__()}")
            print(
                f"Real answer ligne: {randomResult} / lenght: {real_answer.__len__()}\nfalse answer1 lenght: {false_answer_1.__len__()}")

            errorCounter = 0 # Pour compter les points
            tourCounter = 0 # Pour compter les points
            avatar = interaction.user.avatar # Pour le style j'afficher l'avatar de l'utilisateur à la fin trop stylé nan?
            question_used.append(str(random_file) + str(randomResult)) # stockage des questions pour ne pas les répétés
            ctx = await commands.Context.from_interaction(interaction)
            # la chenille qui passe la première
            await interaction.response.send_message(view=Ultimate_View(ctx.author.id, real_answer, answer_order, embed, errorCounter, tourCounter, avatar, question_used), embed=embed)

        else:  # Si on utilise les images en questions
            # La questions/réponse que l'on veut
            randomResult = random.randint(1, 14)
            # On prend une autre réponse au hasard
            randomFaux1 = random.randint(1, 14)
            while randomFaux1 == randomResult:  # check pour ne pas avoir 2 fois la même réponse
                randomFaux1 = random.randint(1, 14)
            randomFaux2 = random.randint(1, 14)
            while randomFaux2 == randomResult or randomFaux2 == randomFaux1: # check pour ne pas avoir 2 fois la même réponse
                randomFaux2 = random.randint(1, 14)
            for row in csv_reader: # On récupère 3 lignes aléatoires choisit avant, 1 sera la bonne et 2 seront les fausses réponses
                if line == randomResult:
                    question = "Qu'elle est ce signe?"
                    real_answer_link = row['link']
                    real_answer = row['answer']
                elif line == randomFaux1:
                    false_answer_1 = row['answer']
                elif line == randomFaux2:
                    false_answer_2 = row['answer']
                line += 1

            # Stockage des réponses
            all_answers = [real_answer, false_answer_1]
            if str(false_answer_2) != "None":
                all_answers = [real_answer, false_answer_1, false_answer_2]

            # Change l'ordre des questions
            answer_order = random.sample(all_answers, len(all_answers))

            # msg discord
            embed = discord.Embed(title="Ultimate Quizz",
                                  description=f"**```{question}```**").set_image(url=real_answer_link)
            embed.add_field(
                name=emoji[0], value=f"```{answer_order[0]}```", inline=True)
            embed.add_field(
                name=emoji[1], value=f"```{answer_order[1]}```", inline=True)
            # Mets une 3ème question si il yen a une (pour les questions manuscrites)
            if str(false_answer_2) != "None":
                embed.add_field(
                    name=emoji[2], value=f"```{answer_order[2]}```", inline=True)

            errorCounter = 0 # Pour compter les points
            tourCounter = 0 # Pour compter les points
            avatar = interaction.user.avatar # stock l'avatar du quizzeur
            question_used.append(str(random_file) + str(randomResult)) # stock questions sur un emplacement de mémoire ou jspquoi j'ai pas réussi le test de nsi de toute façon
            ctx = await commands.Context.from_interaction(interaction)
            print(f"Real answer ligne: {randomResult} / lenght: {real_answer.__len__()}\nfalse answer1 ligne: {randomFaux1} / lenght: {false_answer_1.__len__()}\nfalse answer2 ligne: {randomFaux2} / lenght: {false_answer_2.__len__()}\nfalse answer3 ligne: {randomResult} / lenght: {real_answer.__len__()}")
            await interaction.response.send_message(view=Ultimate_View(ctx.author.id, real_answer, answer_order, embed, errorCounter, tourCounter, avatar, question_used), embed=embed)
