from GPs.gpLoginFunction import login
from GPs.Doctormenu import mainmenu

def gpStart():
    email = login()
    if email == "exitGPLogin":
        return email
    if email:
        mainmenu(email)
    return "exitGPLogin"