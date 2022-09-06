import asyncio
import glob
import re
import discord
import youtube_dl
from discord.ext import commands
import random
import requests
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
    def __init__(self):
        pass

    @classmethod
    async def boucle_musique(self, ctx, musique):
        self.ctx = ctx
        self.choix_musique = str(musique).replace("(", "").replace(")",
                                                                   "").replace("'", "").replace(",", "")
        self.replay = False
        self.random = False


        self.url_musique, self.replay = await self.getUrl(self)

        await self.ensure_voice(self)

        try:
            print(f" choix musique: {self.choix_musique}\n url de la musique: {self.url_musique}\n replay est {self.replay}")
        except:
            print(" erreur dans choix musique: {self.choix_musique}\n url de la musique: {self.url_musique}\n replay est {self.replay}")
        player = await YTDLSource.from_url(self.url_musique, loop=bot.loop, stream=True)
        try:
           self.voice.play(player, after=lambda e: print(
                f'Player error: {e}') if e else None)
        except discord.errors.ClientException as e:
            if str(e) == "Already playing audio.":
                return

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=player.title))

        while self.voice.is_playing():
            await asyncio.sleep(1)
        self.voice.stop()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Quoi?"))

        if self.choix_musique == "Aléatoire":
            self.choix_musique = str(random.choice(glob.glob("playlist/*.csv"))
                      ).replace("playlist\\", "").replace(".csv", "")

            if self.choix_musique.__contains__("youtube"):
                url = f"https://www.youtube.com/watch?v={self.getMusiqueId(self)}"

            elif self.choix_musique.__contains__("spotify"):
                url = f"{self.getMusiqueId(self)}"
                
            else:
                print("Erreur dans if rand")
            await self.boucle_musique()

        elif (self.replay):

            if self.choix_musique.__contains__("youtube"):
                url_musique = f"https://www.youtube.com/watch?v={self.getMusiqueId(self)}"

            elif self.choix_musique.__contains__("spotify"):
                url_musique = f"{self.getMusiqueId(self)}"

            else:
                print("Erreur dans elif replay")

            await self.boucle_musique(self.ctx, self.choix_musique)
 
    def getMusiqueId(self):
        file = f"playlist\{self.choix_musique}.csv"
        with open(file=file) as f:
            musiqueId = None
            lineCount = 0
            for line in f:
                lineCount += 1
            musiqueRand = random.randint(0, lineCount)
            lineCount = 0
            with open(file=file) as f:
                for line in f:
                    lineCount += 1
                    if int(lineCount) == int(musiqueRand):
                        musiqueId = line
                        return musiqueId

    async def getUrl(self):
        if self.choix_musique == "Aléatoire":
            self.choix_musique = str(random.choice(glob.glob("playlist/*.csv"))
                      ).replace("playlist\\", "").replace(".csv", "")
            self.replay = False

        if self.choix_musique.__contains__("youtube"):
            url = f"https://www.youtube.com/watch?v={self.getMusiqueId(self)}"
            replay = True

        elif self.choix_musique.__contains__("spotify"):
            url = f"{self.getMusiqueId(self)}"
            replay = True

        else:
            url = self.choix_musique
            replay = False
            if self.choix_musique == "stop":
                return await self.voice.disconnect()

        return url, replay

    def getSong(song):
        string = str(song)
        titre = string.split().pop(0)
        artiste = string.split().pop(-1)
        song = genius.search_song(titre, artiste)
        return song.lyrics

    async def ensure_voice(self):
        if self.ctx.voice_client is None:
            if self.ctx.author.voice:
                await self.ctx.author.voice.channel.connect()
            else:
                await self.ctx.send("Ta gueule mathis")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif self.ctx.voice_client.is_playing():
            self.ctx.voice_client.stop()
        try:
            # print("voice réussie ligne 109 donc tu peux supp cette ligne")
            self.voice
        except:
            # print("voice pas réussie ligne 112 donc tu si il n'y a aucun voice réussie faut changer ici")
            self.voice = None
        if (self.voice is None):
            self.voice = self.ctx.voice_client
        self.voice.stop()

@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Joue une playlist")
async def playlist(interaction: discord.Interaction):
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message("Choisis", view=playlistSelectView(ctx), ephemeral=True)


class playlistSelectView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.add_item(playlistSelect(ctx))


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


@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Joue un son")
async def play(interaction: discord.Interaction, musique: str = "Aléatoire"):
    ctx = await commands.Context.from_interaction(interaction)
    await interaction.response.send_message(f"Joue {musique}", ephemeral=True)
    await Musique.boucle_musique(ctx = ctx, musique = musique)
