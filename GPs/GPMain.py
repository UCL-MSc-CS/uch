from GPLogin import login
from Doctormenu import mainmenu

def gpStartHere():
    email = []
    login(email)
    mainmenu(email[0])

gpStartHere()


