from GPs.gp_login_function import gp_login
from GPs.gp_main_menu import gp_main_menu

def gp_start():
    """
    Main function for all code associated with GP Activities (including login)

    This function will be called from root.py.
    """
    email,doctorname = gp_login()
    if email == "exitGPLogin":
        return "exitGPLogin"
    if email:
        gp_main_menu(email, doctorname)
    return "exitGPLogin"