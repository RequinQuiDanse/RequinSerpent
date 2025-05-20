from bot import bot, discord
from ollama import chat
import subprocess
from pix2text import Pix2Text
import os

def get_steps_from_llm(equation):
    prompt = f"""

    You are a mathematic expert. Your task is to solve mathematics exercises. You need to precisly follow the given syntax.

    Exercise = {equation}

    Answer following the next template :
    Step X : title
    explanations

    Step X : title
    explanations

    ..."""
    print(prompt)
    
    response = chat(
        model='phi4',  # or other supported model
        messages=[{
            'role': 'user',
            'content': prompt
        }]
    )

    steps_data = response['message']['content'].replace(
        "\u21d2", "").replace("\u222B", "")

    # print("______________________equations_________________________")
    # print(steps_data)
    # print("_______________________________________________")

    return get_steps_from_llm2(steps_data)



def get_steps_from_llm2(last):
    prompt = f"""
    You are a LaTeX expert. You task is to convert plain text into a LaTeX format.
    Your answer must be well structured with titles and sections.
    The plain text is provided here: {last}
    """
    # print("__________________prompt_____________________________")
    # print(prompt)
    # print("_______________________________________________")
    
    response = chat(
        model='phi4',  # or other supported model
        messages=[{
            'role': 'user',
            'content': prompt
        }]
    )

    steps_data = response['message']['content']
    return steps_data


def create_combined_frame(latex_code=None):
    with open("csv_files/maths_img/latex_document.tex", "w") as f:
        f.write(latex_code)

    # Step 2: Compile the LaTeX document to PDF
    subprocess.run(
        ["pdflatex", "-interaction=batchmode","-output-directory=csv_files/maths_img/",  "csv_files/maths_img/latex_document.tex"])

    dossier = "csv_files/maths_img/math_ai"

    # Boucle sur tous les fichiers du dossier
    for nom_fichier in os.listdir(dossier):
        chemin_fichier = os.path.join(dossier, nom_fichier)
        os.remove(chemin_fichier)  # Supprime le fichier

    subprocess.run(["pdftoppm", "csv_files/maths_img/latex_document.pdf", "csv_files/maths_img/math_ai/latex_document", "-png"])
    for nom_fichier in os.listdir(dossier):
        chemin_fichier = os.path.join(dossier, nom_fichier)
        subprocess.run(["convert",chemin_fichier,"-trim",chemin_fichier])

@bot.tree.command(guild=discord.Object(id=769911179547246592), description="Maths ai")
async def math_ai(interaction: discord.Interaction, question: str='', img: discord.Attachment=None):
    """
    """
    input=''
    await interaction.response.defer()
    if (question =='') and (img is None):
        await interaction.followup.send(content="Faut donner un truc à faire")
    else:
        if img :
            img_fp = r"csv_files/maths_img/image.png"
            await img.save(img_fp)
            p2t = Pix2Text.from_config()
            outs = p2t.recognize_text_formula(img_fp, resized_shape=768, return_text=True)
            input = outs.replace("$","").replace("\n","").replace("\operatorname{c o s}","cos").replace("\operatorname{s i n}","sin").replace("+","%2B").replace(" ","")

    prompt = f"{question}  {input}"
    latex_code = get_steps_from_llm(prompt).replace("\u222b", "").replace(
        "\u21d2", "").replace("\\[", "").replace("\\]", "")
    print(latex_code)
    try:
        latex_code = latex_code.split("```")[1][5::]
    except:
        pass
    # if not latex_code.__contains__("begin"):
    #     latex_code = "\\begin{document}" + latex_code+"\\end{document}"
    # if not latex_code.__contains__("usepackage{amsmath}"):
    #     latex_code = "\\usepackage{amsmath}" + latex_code
    # if not latex_code.__contains__("usepackage{nopageno}"):
    #     latex_code = "\\usepackage{nopageno}" + latex_code
    # if not latex_code.__contains__("documentclass{article}"):
    #     latex_code = "\\documentclass{article}" + latex_code
    print(latex_code)
    try:
        latex_code=latex_code.split("\\begin{document}")[1]
        latex_code = "\\documentclass{article}\n\\usepackage{amsmath}\n\\usepackage{nopageno}\n\\begin{document}" + latex_code
    except:
        latex_code = "\\documentclass{article}\n\\usepackage{amsmath}\n\\usepackage{nopageno}\n\\begin{document}" + latex_code +"\\end{document}"
        pass
    print(latex_code+")(@!#)(#($()_*@#$_)@(#_)@#)")

    # latex_code = "\\documentclass{article}\n\\usepackage{amsmath}\n\\usepackage{nopageno}\n\\begin{document}" + latex_code
    # print(latex_code +"LASTOONE___________________")
        
    create_combined_frame(latex_code)
    
    imgs=[]
    dossier = "csv_files/maths_img/math_ai"
    for nom_fichier in os.listdir(dossier):
        chemin_fichier = os.path.join(dossier, nom_fichier)
        imgs.append(discord.File(chemin_fichier))
    await interaction.followup.send(files=imgs)
