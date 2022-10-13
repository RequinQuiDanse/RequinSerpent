from bot import bot, discord
from bs4 import BeautifulSoup
import requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; x64)\ AppleWebKit/537.36 (KHMTL, like GECKO) \ Chrome/58.0.3029.110 Safari/534.3"}


@bot.tree.command(description="Donne la méteo sur 1 semaine")
async def meteo(interaction: discord.Interaction, city: str = "Betz"):
    """
    simple cmd that was long to do that fetch weather and send it in a week
    """
    res = requests.get(f'https://www.google.com/search?q={city+ " weather".replace(" ", "+")}\
      &oq={city}&aqs=chrome.0.35i3912j014j46jj69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    week_weather = soup.select("#wob_dp")[0].getText().strip()
    top = soup.select(".gNCp2e")
    temp = []
    for element in top:
        if element.getText().__len__() == 6:
            temp.append(element.getText()[0:2])
        elif element.getText().__len__() == 5:
            temp.append(element.getText()[0:1])

    week = ["Lundi", "Mardi", "Mercredi",
            "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    if week_weather[0:3] == "lun":
        day = 0
    if week_weather[0:3] == "mar":
        day = 1
    if week_weather[0:3] == "mer":
        day = 2
    if week_weather[0:3] == "jeu":
        day = 3
    if week_weather[0:3] == "ven":
        day = 4
    if week_weather[0:3] == "sam":
        day = 5
    if week_weather[0:3] == "dim":
        day = 6

    meteo = []
    temps = soup.select(".uW5pk")
    for element in temps:
        meteo.append(element["alt"])

    embed = discord.Embed(title=f"Météo {city}", color=discord.Color.random())
    for x in range(8):
        embed.add_field(
            name= f"{str(week[day])} {str(temp[x])} °", value = f"```{meteo[x]}```", inline = True)
        day += 1
        if day == 7:
            day = 0

    await interaction.response.send_message(embed=embed)
