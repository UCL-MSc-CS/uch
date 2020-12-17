from GPs.gpLoginFunction import login
from GPs.Doctormenu import mainmenu

def gpStart():
    email,doctorname = login()
    if email == "exitGPLogin":
        return "exitGPLogin"
    if email:
        mainmenu(email,doctorname)
    return "exitGPLogin"