from bot import bot, discord
import praw
import random
redd = praw.Reddit(client_id='sWfWyLNn0NDR1Pog4PLaSA',    
                     client_secret='AtWJ8kI2ubmOdZvOS2IX8gHLGiReAg',
                     user_agent='USER_AGENT HERE')

@bot.command(guild = discord.Object(id=769911179547246592), description = "Envoie post reddit sur guerre")
async def reddit(ctx):
    """
    just a cmd that send random reddit post on a specific thread (actually CombatFootage thread)
    """
    await ctx.message.delete()
    #eyeblech, LeagueOfMemes
    #memes_submissions =  reddit.subreddit('CombatFootage').hot()
    memes_submissions = redd.subreddit(
        'CombatFootage').search('flair_name:"Video"')
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    await ctx.send('https://www.reddit.com/'+submission.permalink)