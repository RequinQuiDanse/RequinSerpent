from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import pickle
import requests
import os
from bot import bot, discord


class addPlaylistModal(discord.ui.Modal, title='Add playlist'):
    """
    modal to enter the url of our playlist we want to add
    """
    url = discord.ui.TextInput(
        label='Url de ta playlist / de ton artiste spotify',
        placeholder='...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        if self.url.value.__contains__("https://open.spotify.com/playlist/"):
            url = self.url.value.replace(
                "https://open.spotify.com/playlist/", "").split("?si=", 1)[0]
            with open("playlist\\token.txt") as f:
                TOKEN = str(f.readlines()).replace("['", "").replace("']", "")
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {token}".format(token=TOKEN)
            }
            r = requests.get(
                f"https://api.spotify.com/v1/playlists/{url}/tracks", headers=headers)
            if r.status_code == 401 or r.status_code == 400:
                return await interaction.response.send_message(content=f'Il faut me redonner un token: `cliques sur LE LIEN` => `descends en bas de la page` => `getToken` => `request token` => `connectes toi` => `copies le token ENTIER en dessous de "OAuth Token"` => `donnes moi le token`', view=tokenButton(), ephemeral=True)
            data = r.json()

            tracksInfo = []
            for song in data["items"]:
                tracksInfo.append(song["track"]["name"])
                tracksInfo.append(song["track"]["artists"][0]["name"])
            r = requests.get(f"https://api.spotify.com/v1/playlists/{url}", headers=headers)
            data = r.json()
            playname = data["name"][:50].replace("'","")
            with open(f"playlist\spotify {playname}.csv", mode='w', newline='',  encoding='utf-8') as csv_file:
                fieldnames = ['id']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                trackNumber = 0
                for song in tracksInfo:
                    try:
                        writer.writerow(
                            {'id': f"{tracksInfo[trackNumber]} {tracksInfo[trackNumber + 1]} audio"})
                        trackNumber += 2
                    except:
                        None

        elif self.url.value.__contains__("https://youtube.com/playlist?list="):
            url = self.url.value.replace(
                "https://youtube.com/playlist?list=", "")
            SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

            def youtube_authenticate():
                # *DO NOT* leave this option enabled https://open.spotify.com/playlist/0p5DBHLpCPQ1YLpVyy2NsA?si=d3c69fab236f49dain production.
                import os
                os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
                api_service_name = "youtube"
                api_version = "v3"
                client_secrets_file = "playlist\code_secret_client.json.json"
                creds = None
                # the file token.pickle stores the user's access and refresh tokens, and is
                # created automatically when the authorization flow completes for the first time
                if os.path.exists("playlist\\token.pickle"):
                    with open("playlist\\token.pickle", "rb") as token:
                        creds = pickle.load(token)
                # if there are no (valid) credentials availablle, let the user log in.
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            client_secrets_file, SCOPES)
                        creds = flow.run_local_server(port=0)
                    # save the credentials for the next run
                    with open("playlist\\token.pickle", "wb") as token:
                        pickle.dump(creds, token)

                return build(api_service_name, api_version, credentials=creds)

            # authenticate to YouTube API
            youtube = youtube_authenticate()
            # -*- coding: utf-8 -*-

            # Sample Python code for youtube.playlistItems.list
            # See instructions for running these code samples locally:
            # https://developers.google.com/explorer-help/code-samples#python



            scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

            def main(youtube):
                # Disable OAuthlib's HTTPS verification when running locally.
                # *DO NOT* leave this option enabled in production.
                os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

                client_secrets_file = "playlist\code_secret_client.json.json"

                # Get credentials and create an API client => déjà fait dans la fonction d'avant l.30
                # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                #   client_secrets_file, scopes)
                request = youtube.playlistItems().list(
                    part="snippet",
                    maxResults=100,
                    playlistId=self.url.value.replace(
                        "https://youtube.com/playlist?list=", "")
                )
                response = request.execute()
                # print(response["items"][0]["snippet"]["resourceId"]["videoId"])

                fieldnames = ['id']
                playname = self.name.value
                with open(f"playlist\youtube {playname}.csv", mode='w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    for song in response["items"]:
                        writer.writerow(
                            {'id': song["snippet"]["resourceId"]["videoId"]})

            main(youtube)

        elif self.url.value.__contains__("https://open.spotify.com/artist/"):
            url = self.url.value.replace(
                "https://open.spotify.com/artist/", "").split("?si=", 1)[0]
            with open("playlist\\token.txt") as f:
                TOKEN = str(f.readlines()).replace("['", "").replace("']", "")
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {token}".format(token=TOKEN)
            }
            r = requests.get(f"https://api.spotify.com/v1/artists/{url}/top-tracks?market=FR", headers=headers)
            if r.status_code == 401 or r.status_code == 400:
                return await interaction.response.send_message(content=f'Il faut me redonner un token: `cliques sur LE LIEN` => `descends en bas de la page` => `getToken` => `request token` => `connectes toi` => `copies le token ENTIER en dessous de "OAuth Token"` => `donnes moi le token`', view=tokenButton(), ephemeral=True)

            data = r.json()
            playname = data["tracks"][0]["artists"][0]["name"]
            
            tracks = []
            for track in data["tracks"]:
                tracks.append(track["name"])
            with open(f"playlist\spotify {playname} top 10 tracks.csv", mode='w', newline='',  encoding='utf-8') as csv_file:
                fieldnames = ['id']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                trackNumber = 0
                for song in tracks:
                    try:
                        writer.writerow(
                            {'id': f"{song} {playname} audio"})
                    except:
                        None
            playname = playname + " top 10 tracks"
        await interaction.response.send_message(content=f'Nouvelle playlist "**{playname}**" ajoutée!')


@bot.tree.command(guild = discord.Object(id=769911179547246592), description="Rajoutes une de tes playlists youtube ou spotify au bot")
async def addplaylist(interaction: discord.Interaction):
    """
    the cmd that send a modal when asked
    """
    await interaction.response.send_modal(addPlaylistModal())


class tokenButton(discord.ui.View):
    """
    the class that contain the button that permit to give the token
    """
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, label="LE LIEN",
                      url="https://developer.spotify.com/console/get-playlist-tracks/"))

    @discord.ui.button(label='Donner le token', style=discord.ButtonStyle.red)
    async def token(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(tokenModal())


class tokenModal(discord.ui.Modal, title="Token"):
    """
    the modal that permit the user to enter his token from spotify api
    """
    token = discord.ui.TextInput(
        label='Token',
        placeholder="Mettre le token entier ici"
    )

    async def on_submit(self, interaction: discord.Interaction):
        with open("playlist\\token.txt", 'w') as f:
            f.write(self.token.value)
        await interaction.response.send_message(content="Merci! Tu peux mtn recommencer pour ajouter ta playlist", ephemeral=True)


# si ça bug faut delete token.pickle