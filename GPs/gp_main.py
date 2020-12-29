from GPs.gp_login_function import login
from GPs.doctor_main_menu import mainmenu

def gpStart():
    email,doctorname = login()
    if email == "exitGPLogin":
        return "exitGPLogin"
    if email:
        mainmenu(email,doctorname)
    return "exitGPLogin"