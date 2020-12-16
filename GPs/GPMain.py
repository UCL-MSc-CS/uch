from GPs.gpLoginFunction import login
from GPs.Doctormenu import mainmenu

def gpStart():
    email = []
    choice = login(email)
    if choice == "exitGPLogin":
        return choice
    if email:
        mainmenu(email[0])
    return "exitGPLogin"