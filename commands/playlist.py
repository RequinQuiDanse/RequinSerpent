# ENORME PRBLM AVEC LES BOUCLES, NOTAMMENT GETMUSIQUEID!
import asyncio
import glob
import discord
import youtube_dl
from discord.ext import commands
import random
from bot import bot
import lyricsgenius

genius = lyricsgenius.Genius(
    "xjJpaQG9ABRvMJlPmSmUd0tIUC6OHVIKwyunADEvQ7PKbtEMC3ZJYnPj-RSMQKZk")
# Suppress noise about console usage from errors

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,

    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Musique():
    """
    class that will do all the stuff (play, mangage replay, send lyrics)
    """
    def __init__(self):
        pass
    def __del__(self):
        print("Object deleted")
    @classmethod
    async def boucle_musique(self, ctx, musique):  # Func cerveau
        self.ctx = ctx
        self.choix_musique = str(musique).replace("(", "").replace(")",
                                                                   "").replace("'", "").replace(",", "")
        self.replay = False
        self.random = False

        # récupère les données de la musique et si la demande est une playlist ou une musique
        self.url_musique, self.replay = await self.getUrl(self)
        print(self.url_musique)

        await self.ensure_voice(self)  # étape pour bien connecté le bot

        player = await YTDLSource.from_url(self.url_musique, loop=bot.loop, stream=True)

        try:
            self.voice.play(player, after=lambda e: print(
                f'Player error: {e}') if e else None)
        except discord.errors.ClientException as e:
            if str(e) == "Already playing audio.":
                return

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=player.title))
        await self.getSong(self, str(player.title).replace("clip officiel",""))

        while self.voice.is_playing():  # Attend la fin de la musique
            await asyncio.sleep(1)
        self.voice.stop()  # arrête de chanter
        # change le statut du bot
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Quoi?"))

        if (self.replay):  # si on joue une playlist => ça trouve une autre musique et ça rejoue
            # cherchage d'une nouvelle musique
            self.url_musique, self.replay = await self.getUrl(self)

            # le chenapan qui revole
            await self.boucle_musique(self.ctx, self.choix_musique)

    def getMusiqueId(self):  # Permet de récuperer une ligne au hasard d'une playlist
        """
        return a random music name extracted from csv files
        """
        file = f"playlist\{self.asked_playlist}.csv"
        with open(file=file) as f:
            musiqueId = None
            lineCount = 0
            for line in f:  # calcul le nombre de lignes en tout
                lineCount += 1
            # choisit une ligne au hasard
            musiqueRand = random.randint(1, lineCount)
            lineCount = 0
            with open(file=file) as f:
                for line in f:
                    lineCount += 1
                    # Récupère les trucs stockés dans la ligne choisit précédemment
                    if int(lineCount) == int(musiqueRand):
                        musiqueId = line
                        return musiqueId

    async def getUrl(self):  # Permet de jouer une playlist: ça récupère une musique aléatoire à partir de la toute première playlist demandée (self.choix_musique)
        """
        return a youtube url or a music name, depends on what is asked
        also manage if a playlist is asked or no
        """
        self.asked_playlist = self.choix_musique
        if self.asked_playlist == "Aléatoire":  # Si aléatoire était la demande, alors on prend une playlist aléatoire
            self.asked_playlist = str(random.choice(glob.glob("playlist/*.csv"))
                                     ).replace("playlist\\", "").replace(".csv", "")
            self.replay = False

        # Destinée à être supprimé, ça vérifie si la playlist est une playlist youtube ou spotify mais personne n'utilise de playlist youtube
        if self.asked_playlist.__contains__("youtube"):
            url = f"https://www.youtube.com/watch?v={self.getMusiqueId(self)}"
            replay = True

        # si la playlist est spotify ou youtube ça récupère les données sur la musique (titre, auteur etc)
        elif self.asked_playlist.__contains__("spotify"):
            url = f"{self.getMusiqueId(self)}"
            replay = True

        else:  # si c'est ni l'un ni l'autre, ça veut dire que l'utilisateur n'a pas demandé de playlist mais plutôt une simple musique
            url = self.asked_playlist
            replay = False
            if self.asked_playlist == "stop":
                return await self.voice.disconnect()

        return url, replay

    async def getSong(self, _song):
        """
        return lyrics of a song w/ genius api
        """
        song = genius.search_song(_song.lower().replace("audio", ""))
        if song != None:
            # if str(self.ctx.message.channel.id) != '903673532247048192':
            #     channel = bot.get_channel(942818979318210631)
            # else:
            #     channel = bot.get_channel(903673532247048192)
            #     #await channel.send(content= song)
            with open(r'csv_files\lyrics.txt', 'w', encoding='utf-8') as f:
                f.write(str(song.lyrics))
            await self.ctx.reply(file = discord.File(r'csv_files\lyrics.txt'), delete_after=300, view = Lyrics_Button(), ephemeral = True)

    async def ensure_voice(self): # Etape obligatoire permettant de ne pas créer de conflit
        """
        do all the stuff to encuse the bot's voice is well connected
        """
        if self.ctx.voice_client is None:  # vérifie que le demandeur de musique est bien dans un salon vocal 
            if self.ctx.author.voice: # si le bot n'est pas connecté, ça le connecte
                await self.ctx.author.voice.channel.connect()
            else:
                await self.ctx.send("Ta gueule mathis")
        elif self.ctx.voice_client.is_playing(): # Si le bot jouait de la musique au moment de l'appel, ça l'arrête
            self.ctx.voice_client.stop()
        try:  # même moi jsais pas mais j'ai dû le faire sinon "voice is not defined"
            # print("voice réussie ligne 109 donc tu peux supp cette ligne")
            self.voice
        except:
            # print("voice pas réussie ligne 112 donc tu si il n'y a aucun voice réussie faut changer ici")
            self.voice = None
        if (self.voice is None):
            self.voice = self.ctx.voice_client
        self.voice.stop()

class Lyrics_Button(discord.ui.View):
    """
    add a button if user want lyrics to be public
    """
    @discord.ui.button(label='Paroles publiques?', style=discord.ButtonStyle.green)
    async def edit_team(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(file = discord.File(r"csv_files\lyrics.txt"))

music_class = Musique()
@bot.tree.command(description="Joue une playlist")
async def playlist(interaction: discord.Interaction):
    """
    send the playlist's buttons, to permit user to select one
    """
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message("Choisis", view=playlistSelectView(ctx), ephemeral=bool(interaction.channel_id != 942818979318210631))

class playlistSelectView(discord.ui.View):
    """
    add one button per csv file
    """
    def __init__(self, ctx):
        self.ctx = ctx
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, label= "Aléatoire", custom_id= "Aléatoire"))
        for playlist in glob.glob("playlist/*.csv"):
            try:
                self.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, label=str(playlist).replace(
                "playlist\\", "").replace("spotify", "").replace(".csv", ""), custom_id=str(playlist).replace(
                "playlist\\", "").replace(".csv", "")))
            except:
                print("Trop de playlists et pas assez de boutons je crois")
    async def interaction_check(self, interaction=discord.Interaction):

        await music_class.boucle_musique(ctx = self.ctx, musique = interaction.data.get("custom_id"))

"""
class playlistSelect(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        options = [
            discord.SelectOption(
                label='Aléatoire', description='⠀'),
        ]
        super().__init__(placeholder="Quel playlist veux tu?",
                         min_values=1, max_values=1, options=options)

        for playlist in glob.glob("playlist/*.csv"):
                self.add_option(label=str(playlist).replace(
                    "playlist\\", "").replace(".csv", ""), description="⠀")

    async def callback(self, interaction: discord.Interaction):
        await Musique.boucle_musique(ctx = self.ctx, musique = self.values[0])
"""


@bot.tree.command(description="Joue un son")
async def play(interaction: discord.Interaction, musique: str = "Aléatoire"):
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message(f"Joue {musique}", ephemeral=True)
    await music_class.boucle_musique(ctx=ctx, musique=musique)
