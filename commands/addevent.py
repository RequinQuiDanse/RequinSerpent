import base64
import json
import requests
from ollama import chat
import requests
from datetime import datetime
from bot import bot, discord


def get_coordinates_nominatim(address):
    # URL de l'API Nominatim
    address = address.replace(" ", "+")
    url = f"https://nominatim.openstreetmap.org/search?q=${address}&format=json&limit=1"
    # Paramètres de la requête
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    # Headers including User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0"
    }

    # Faire une requête GET à l'API
    response = requests.get(url, params=params, headers=headers)

    # Vérifier le statut de la réponse
    if response.status_code == 200:
        results = response.json()
        if results:
            # Extraire les coordonnées du premier résultat
            return float(results[0]['lat']), float(results[0]['lon'])
        else:
            return None
    else:
        print(f"Erreur: {response.status_code}")
        return None


# def addEvent(key=-1, content=""):


# content = """
# @everyone  Tomas SALVADO ROBALO vous invite à assister à sa soutenance de Stage International le Mardi 1er Avril à 12h15 ! 🎓

# Ne manquez pas ce récit captivant sur le Brésil, agrémenté de la liste des latinas tombées sous le charme de Tomas. 💃

# Places limitées (11 restantes)
#  https://forms.gle/frNA6heD36z3fJhU8
#  """

# addEvent(12, content)

@bot.tree.command(guild=discord.Object(id=769911179547246592), description="Add Event")
async def addevent(interaction: discord.Interaction, description: str = '', img: discord.Attachment = None, cle_orga: int = 0):
    """

    """
    await interaction.response.defer()
    url = "http://localhost:8000/api.php"
    today = datetime.today()
    formatted_date = today.strftime("%Y:%m:%d")

    params = {
        "action": "checkKey",
    }
    try:
        orga_id = requests.post(url, params=params, data={
                                "key": cle_orga}).text
    except:
        await interaction.followup.send(content="Serveur down")

    if (int(orga_id) < 0):
        return

    prompt = f"""
    You are an agent used for analysing and formatting content.

    Content : "{description}"
    Day of the content : {formatted_date}
    City's of school location : Lens
    School location : 13 rue Jean Souvraz Lens
    
    Analyse the content and determine whether the content is an event, an information or none of them.
    
    If the content is an event, extract the informations and answer following the next template :
        "name": "name of event",
        "date": "date of event format yyyy-mm-dd",
        "heure": "heure of beginning of event format hh:mm",
        "heure2": "hour of ending of the event format hh:mm",
        "description": "description of the event",
        "prix": "price of the event",
        "link": "link of event",
        "address": "address of the event",
    
    Every text field must be in French
    If the date is not given, deduce it from the description
    Remove all discord-like mentions that begins with @
    If you can not find heure but is an event put a logic hour for heure
    If you can not find heure2, set heure2 to null
    If you can not find price, set it to 0.
    If you cannot find link, set it null
    name can not be null
    If the content is an information, set start_time to null.
    
    Do not edit the description given
    Add some '\\n' in the description for a better rendering
    Format your answer in json
    Do not describe your thought pattern
    Do not put any comment
    """
    print(prompt)
    response = chat(
        model='phi4',  # or other supported model
        messages=[{
            'role': 'user',
            'content': prompt
        }]
    )
    print(response['message']['content'])

    data = response['message']['content'].replace(
        "json", "").replace("```", "")
    data = json.loads(data)
    lat, long = get_coordinates_nominatim(
        data["address"])
    data["long"] = long
    data["lat"] = lat
    data["orga_id"] = orga_id
    params = {
        "action": "addEvent",
    }
    if (img):
        await img.save("csv_files/addevent.png")
        with open("csv_files/addevent.png", 'rb') as image_file:
            files = {'image': ("csv_files/addevent.png",
                               image_file, 'image/jpeg')}

            # Envoyer la requête POST avec l'image
            response = requests.post(
                url,  params=params, data=data, files=files)
    else:
        response = requests.post(url, params=params, data=data)

    # Vérifier le statut de la réponse
    if response.status_code == 200:
        # Afficher le contenu de la réponse
        await interaction.followup.send(content="succès")
    else:
        await interaction.followup.send(content="echec")
