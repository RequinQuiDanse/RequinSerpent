from bot import bot, discord


def embedCreator(color, title, discUrl=None, imageUrl=None):
    if imageUrl is not None:
        embed = discord.Embed(
            title=f"**{title}**", color=color, url=discUrl)
        embed.set_image(
            url=imageUrl)
    else:
        embed = discord.Embed(
            title=f"**{title}**", color=color, description=discUrl)
    return embed


@bot.command()
async def embed(ctx):
    # Échauffements
    color = discord.Color.random()

    embed = discord.Embed(
        title="**Échauffements:**", color=color)
    await ctx.channel.send(embed=embed)

    # échauffement physique
    embed = embedCreator(color, "Échauffement physique", "Durée ~~ 15min")
    await ctx.channel.send(embed=embed)

    # entraînement de domont
    embed = embedCreator(color, "La Domont", "https://discinapp.page.link/mTnobd7xWN93xhzcA",
                         "https://media.discordapp.net/attachments/959575339481313310/1004456053154533376/Screenshot_20220803_202758.jpg?width=328&height=676")
    embed2 = embedCreator(color, "La Domont", "https://discinapp.page.link/mTnobd7xWN93xhzcA",
                          "https://media.discordapp.net/attachments/959575339481313310/1004456052768653423/Screenshot_20220803_202823.jpg?width=365&height=675")
    embed3 = embedCreator(color, "La Domont", "https://discinapp.page.link/mTnobd7xWN93xhzcA",
                          "https://media.discordapp.net/attachments/959575339481313310/1004456052516978699/Screenshot_20220803_202900.jpg?width=342&height=676")
    embed4 = embedCreator(color, "La Domont", "https://discinapp.page.link/mTnobd7xWN93xhzcA",
                          "https://media.discordapp.net/attachments/959575339481313310/1004456052248547498/Screenshot_20220803_202920.jpg?width=322&height=676")
    await ctx.channel.send(embeds=[embed, embed2, embed3, embed4])

    # Z/Flèche
    embed = embedCreator(color, "Le Z / La flèche", "Durée ~~ 10/15min")
    await ctx.channel.send(embed=embed)

    # Le carré à dishy
    embed = embedCreator(color, "Le carré à dishy", "https://discinapp.page.link/SGUF3sp35GMbxNee7",
                         "https://media.discordapp.net/attachments/959575339481313310/1004462822761177088/Screenshot_20220803_205542_com.discin.discin.jpg?width=822&height=676")
    embed2 = embedCreator(color, "Le carré à dishy", "https://discinapp.page.link/SGUF3sp35GMbxNee7",
                          "https://media.discordapp.net/attachments/959575339481313310/1004462822438228028/Screenshot_20220803_205551_com.discin.discin.jpg?width=784&height=676")
    embed3 = embedCreator(color, "Le carré à dishy", "https://discinapp.page.link/SGUF3sp35GMbxNee7",
                          "https://media.discordapp.net/attachments/959575339481313310/1004462822056530040/Screenshot_20220803_205608_com.discin.discin.jpg?width=781&height=676")
    embed4 = embedCreator(color, "Le carré à dishy", "https://discinapp.page.link/SGUF3sp35GMbxNee7",
                          "https://media.discordapp.net/attachments/959575339481313310/1004462821729378444/Screenshot_20220803_205621_com.discin.discin.jpg?width=751&height=676")
    await ctx.channel.send(embeds=[embed, embed2, embed3, embed4])
    
    # Exercices
    color = discord.Color.random()

    embed = discord.Embed(title="**Exercices:**", color=color)
    await ctx.channel.send(embed=embed)

    # analyse et longues
    embed = embedCreator(color, "Analyse et longue", "https://discinapp.page.link/rEXwUUm8NTpfrHSs5",
                         "https://media.discordapp.net/attachments/959575339481313310/1004461133974999071/Screenshot_20220803_204639_com.discin.discin.jpg?width=645&height=676")
    embed2 = embedCreator(color, "Analyse et longue", "https://discinapp.page.link/rEXwUUm8NTpfrHSs5",
                         "https://media.discordapp.net/attachments/959575339481313310/1004461133673021461/Screenshot_20220803_204706_com.discin.discin.jpg?width=632&height=676")
    embed3 = embedCreator(color, "Analyse et longue", "https://discinapp.page.link/rEXwUUm8NTpfrHSs5",
                         "https://media.discordapp.net/attachments/959575339481313310/1004461133467496558/Screenshot_20220803_204722_com.discin.discin.jpg?width=633&height=676")
    embed4 = embedCreator(color, "Analyse et longue", "https://discinapp.page.link/rEXwUUm8NTpfrHSs5",
                         "https://media.discordapp.net/attachments/959575339481313310/1004461133261967370/Screenshot_20220803_204753_com.discin.discin.jpg?width=657&height=676")
    await ctx.channel.send(embeds=[embed, embed2, embed3, embed4])

    # Hard
    color = discord.Color.random()

    embed = discord.Embed(title="**Pour se dépenser:**", color=color)
    await ctx.channel.send(embed=embed)
    # Passe à 10
    embed = embedCreator(color, "Passe à 10", "Durée 3 * 5 min")
    await ctx.channel.send(embed=embed)
    # matchs
    embed = embedCreator(color, "Matchs", "Durée ~~ 10/15min * 2")
    await ctx.channel.send(embed=embed)

    # le drapeau suisse
    embed = embedCreator(color, "Le drapeau Suisse d'Isack", "Durée ~~ 20min")
    
    # Pour se reposer
    color = discord.Color.random()
    
    embed = discord.Embed(title="**Pour se reposer:**", color=color)
    await ctx.channel.send(embed=embed)
    # Taureau
    embed = embedCreator(color, "Taureau avec plusieurs taureaux", "10 min")
    await ctx.channel.send(embed=embed) 

"""

    embed = discord.Embed(
        title="**Échauffement**", color=discord.Color.random())
    embed.add_field(name="",
                    value="")
    await ctx.channel.send(embed=embed)

    embed = discord.Embed(
        title="**Échauffement**", color=discord.Color.random())
    embed.set_image(
        url="https://media.discordapp.net/attachments/959575339481313310/959867024027299940/unknown.png?width=1006&height=676")
    await ctx.channel.send(embed=embed)

"""
