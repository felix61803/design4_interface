from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
import json
import csv
import datetime
from unicodedata import name
from win32api import GetSystemMetrics
from numpy import genfromtxt
from numpy import array
from numpy import ndarray
import calcul_cycle_puissace_interface as interface_2
from distutils.dir_util import copy_tree

DEBUG_MODE = True


new_machine_name = {"name_machine":""}

# dimension de la fenêtre par déafault ajusté à la taille de l'écran
windows_height_x = int(GetSystemMetrics(0))-20
windows_height_y = int(GetSystemMetrics(1))-150
windows_scrol_height = int(GetSystemMetrics(1))

# constantes pour les positionnements des widjets des fonctions et des capteurs sur l'interface
space_next_func = 60
space_next_sens = 30
init_nb_func = 0
init_config_y_func = 60
init_config_x_func = [40, 120, 250, 380]
init_config_y_sens = 60
init_config_x_sens = [120, 200, 450, 550, 670, 820, 950]

# dictionnaires et listes contenant les widgets des fonctions et des capteurs sur l'interface
# les numéros représente les numéros de la fonction ou des capteurs
                                                # numéros: numéros des fonctions
dico_funcs = {}                                 # clés: 'Fonction 1', 'Fonction 2', etc...
dico_funcs_add_description = {}                 # clés: 'funcs_description_1', 'funcs_description_2' etc...              
dico_button_add_capts = {}                      # clés: 'button_fct_1', 'button_fct_2', etc...
dico_button_delete_funcs = {}                   # clés: 'button_del_fct_1', 'button_del_fct_2', etc...

                                                # numéros: numéros des capteurs

dico_all_sensors = {}                           # clés: 'func_1':{'Capteur 1':...,           ,   'func_2':{etc...}, etc...
                                                #                 'type_channel_sens_1':...,
                                                #                 'Capteur 2':...,
                                                #                 'type_channel_sens_2':...,
                                                #                 'etc...}
dico_capts_add_description = {}                 # clés: 'capts_description_1', 'capts_description_2', etc...
dico_can_adresse = {}                           # clés: 'adress_1', 'adress_2', etc...
dico_nb_bit_by_bytes_analogique_menu_1 = {}     # clés: 'can_data_1', 'can_data_2', etc...        
dico_separator = {}                             # clés: 'sep_1', 'sep_2', etc...
dico_nb_bit_by_bytes_analogique_menu_2 = {}     # clés: 'can_data_1', 'can_data_2', etc...        
dico_analogique_type_range = {}                 # clés: 'type_range_1', 'type_range_2', etc...
dico_byte_from_digital = {}                     # clés: 'can_data_7', 'can_data_9', etc...
dico_bit_from_digital = {}                      # clés: 'can_data_7', 'can_data_9', etc...
dico_value_of_100 = {}                          # clés: 'max_val_1', 'max_val_2', etc...

# Listes des erreurs pour la vérifications des entrées manuelles et des données. Elles contiennent les messages à afficher pour l'usager
list_assertion = []
error_for_rpi = []
error_import_can = []
invalide_entry = []
list_indication = []
dico_all_error_message = {"assertions_partie_1":list_assertion,"for_rpi":error_for_rpi, "import_can":error_import_can, "invalide_entry":invalide_entry,"indication":list_indication}

#dictionnaire du scrollbar de l'interface
dico_scrollbar = {}

# dictionnaire comprennant les path vers tous les fichiers pertinents
dico_file_name = {"filename":None, "path_to_file":None, "taille_interface_file":None, "path_to_folder":None, "path_to_parent_folder":None, "Path_to_machine_folder":None,"Path_to_interface_folder":None}

# Options des menus déroulants de l'interface
Can_tram_type = ["Digital", "Analogique"]
Can_tram_list = ["1", "2","3","4","5","6","7","8","9","10","11","12","13","14","15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]
Can_range_analogique = ["0 a 100%","-100 a 100%","direct"]
Can_nb_bytes_1 = ["0","1", "2","3","4","5","6"]
Can_nb_bytes_2 = ["1", "2","3","4","5","6","7"]
Can_digital_bit = ["0","1", "2","3","4","5","6","7"]



def find_the_config_file_path(name):
    """ Cette fonction trouve et retourne le path vers tous les fichiers pertinents

        name: Le nom du fichier json créer par défault

        return:
            path_file:                      path absolue vers le fichier json de l'interface
            path_to_taille_interface_file:  path absolue vers le fichier json pour la taille et le scrollbar
            path_to_folder:                 path absolue vers le dossier avec les fichier des interface partie 1: fichiers_enregistrements
            path_to_parent_folder:          path absolue vers le dossier de l'interface partie 1:  1) setup_donnees
            path_to_machine_folder:         path absolue vers le dossier de la machine
            path_to_interface:              path absolue vers le dossier de l'interface graphique (cloner du git)

    """
    if DEBUG_MODE == True:
        print("La fonction find_the_config_file_path a été appelée")
    path_script = __file__
    to_list = path_script.split('\\')
    path_script_minus_2 = to_list[0:len(to_list)-2]
    path_to_machine_folder = '\\'.join(path_script_minus_2)
    path_to_interface = "\\".join(to_list[0:len(to_list)-3])
    path_file = '\\'.join(path_script_minus_2) + "\\1) setup_donnees\\fichiers_enregistrements\\%s"%(name)
    path_to_folder = '\\'.join(path_script_minus_2) + "\\1) setup_donnees\\fichiers_enregistrements\\"
    path_to_taille_interface_file = path_to_folder + "z_taille_interface.json"
    path_to_parent_folder = '\\'.join(path_script_minus_2) + "\\1) setup_donnees\\"
    return path_file, path_to_taille_interface_file, path_to_folder, path_to_parent_folder, path_to_machine_folder, path_to_interface 

def donothing():

    print(dico_funcs)
    print(dico_funcs_add_description)
    print(dico_button_add_capts)
    print(dico_button_delete_funcs)
    print(dico_all_sensors)
    print(dico_capts_add_description)
    print(dico_can_adresse)
    print(dico_nb_bit_by_bytes_analogique_menu_1)
    print(dico_separator)
    print(dico_nb_bit_by_bytes_analogique_menu_2)
    print(dico_analogique_type_range)
    print(dico_byte_from_digital)
    print(dico_bit_from_digital)
    print(dico_value_of_100)

def create_tkinter_widjet():
    """Cette fonction sert à placer sur l'interface tous les widjets (zone de texte, d'entrée manuel, les boutons et les menus déroulants)
        créé préalablement par d'autres fonctions et enregistrés dans les dictionnaires.

        Elle est appelée par les fonctions suivantes: 
                                                     - add_sensors()
                                                     - delete_functions()
                                                     - can_channel_type()
                                                     - function_from_file()

        Les widgets sont positionnés à partir des coordonnées précisées dans les listes suivantes: 
                                                     - space_next_func = 60
                                                     - space_next_sens = 30
                                                     - init_nb_func = 0
                                                     - init_config_y_func = 60
                                                     - init_config_x_func = [40, 120, 250, 380]
                                                     - init_config_y_sens = 60
                                                     - init_config_x_sens = [120, 200, 450, 550, 670, 820, 950]
    """
    if DEBUG_MODE == True:
        print("La fonction create_tkinter_widjet a été appelée")
    with open(dico_file_name["path_to_file"], "r") as f:
        data = json.load(f)

    count_all_sens = 1
    for i in range(len(dico_funcs)):
        dico_funcs["Fonction %s"%(i+1)].place(x = data["config_x_place_func"][0], y = data["config_y_place_func"])
        dico_funcs_add_description["funcs_description_%s"%(i+1)].place(x = data["config_x_place_func"][1], y = data["config_y_place_func"])
        dico_button_add_capts["button_fct_%s"%(i+1)].place(x=data["config_x_place_func"][2],y=data["config_y_place_func"])
        dico_button_delete_funcs["button_del_fct_%s"%(i+1)].place(x = data["config_x_place_func"][3] , y = data["config_y_place_func"])
        
        all_sens_only = []
        for sensors_by_fonc in list(dico_all_sensors["func_%s"%(i+1)].keys()):
            if "Capteur" in sensors_by_fonc:
                all_sens_only.append(sensors_by_fonc)
        little_count = 1
        for sensors_by_fonc in all_sens_only:
            dico_all_sensors["func_%s"%(i+1)][sensors_by_fonc].place(x=data["config_x_place_sens"][0],y=data["config_y_place_sens"]+space_next_sens+5)

            num_sens = sensors_by_fonc.split(' ')

            dico_capts_add_description["capts_description_%s"%(num_sens[1])].place(x=data["config_x_place_sens"][1],y=data["config_y_place_sens"]+space_next_sens+5)
            
            dico_all_sensors["func_%s"%(i+1)]["type_channel_sens_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][2], y =data["config_y_place_sens"]+space_next_sens)
            dico_can_adresse["adress_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][3], y =data["config_y_place_sens"]+space_next_sens+5)
            if data["function %s"%(i+1)]["sensor %s"%(num_sens[1])]["type_channel"] == "Analogique":
                dico_nb_bit_by_bytes_analogique_menu_1["can_data_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][4], y =data["config_y_place_sens"]+space_next_sens)

                dico_separator["sep_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][4]+67, y =data["config_y_place_sens"]+space_next_sens+3)

                dico_nb_bit_by_bytes_analogique_menu_2["can_data_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][4] + 80, y =data["config_y_place_sens"]+space_next_sens)

                dico_analogique_type_range["type_range_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][5], y =data["config_y_place_sens"]+space_next_sens)

            elif data["function %s"%(i+1)]["sensor %s"%(num_sens[1])]["type_channel"] == "Digital":
                dico_byte_from_digital["can_data_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][4], y =data["config_y_place_sens"]+space_next_sens)
                dico_bit_from_digital["can_data_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][4] + 128, y =data["config_y_place_sens"]+space_next_sens)

            dico_value_of_100["max_val_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][6], y =data["config_y_place_sens"]+space_next_sens+5)

            data["config_y_place_sens"] += space_next_sens
            data["config_y_place_func"] = data["config_y_place_sens"] + space_next_func
                
            count_all_sens += 1

            with open(namefile[1], "r") as f:
                data_2 = json.load(f)
            if data["config_y_place_func"]>= data_2["windows_scrol_height"]:
                data_2["windows_scrol_height"] = data["config_y_place_func"]
            
            with open(namefile[1], "w") as file:
                json.dump(data_2, file, indent = 6)
            
            with open(dico_file_name["path_to_file"], "w") as file:
                json.dump(data, file, indent = 6)
            little_count += 1
        data["config_y_place_sens"] = data["config_y_place_func"]
        with open(dico_file_name["path_to_file"], "w") as file:
                json.dump(data, file, indent = 6)
            

def add_machine():
    """ Cette fonction permet d'ouvrir un explorateur de fichier afin que l'usager sélection un dossier de machine. 
            Par la suite, elle créée les différents dossiers nécessaires au fonctionnement de l'interface pour la nouvelle machine

        Elle ne copie pas l'exécutable et le dossier script_pythons

        Elle est appelée par le bouton de l'interface graphique: Nouvelle machine
    """
    if DEBUG_MODE == True:
        print("La fonction add_machine a été appelée")
    get_all_entry()

    file = fd.askdirectory(title= "Sélectionner le dossier de la nouvelle machine ", initialdir=dico_file_name["Path_to_interface_folder"])
    if DEBUG_MODE == True:
        print("Path du dossier pour la nouvelle machine", file)
    

    if file != "":
        os.mkdir(file + "\\1) setup_donnees")
        os.mkdir(file + "\\1) setup_donnees\\fichiers_enregistrements")

        os.mkdir(file + "\\2) calcul_puissance")
        os.mkdir(file + "\\2) calcul_puissance\\fichiers_enregistrements")

        os.mkdir(file + "\\3) traitement_donnes")
        os.mkdir(file + "\\3) traitement_donnes\\fichiers_enregistrements")

        os.mkdir(file + "\\donnees_recoltees_machine")
        os.mkdir(file + "\\fichier_pour_calculateur")
        os.mkdir(file + "\\fichier_pour_la_rpi")
        os.mkdir(file + "\\rapports")
        os.mkdir(file + "\\rapports\\images")

    else:
        print("action annulée")


def add_function():
    """ Ajout 1 au compteur de fonction dans le fichier de configuration et
            appel la fonction create_functions()

        Elle est appelée par le bouton de l'interface graphique: Nouvelle fonction
    """
    if DEBUG_MODE == True:
        print("La fonction add_function a été appelée")

    with open(dico_file_name["path_to_file"], "r") as f:
        data = json.load(f)
        data["config_nb_func"] = data["config_nb_func"] + 1

    with open(dico_file_name["path_to_file"], "w") as file:
        json.dump(data, file, indent = 6)
    
    
    create_functions(data["config_nb_func"],"new")



def count_sensors(data):
    """ Cette fonction compte le nombre de capteurs totals enregistré dans le fichier de configuration .json

        Elle est appelée par la fonction: add_sensors()

        Parmètres: 
                data: dictionnaire contenant le contenu du fichier de configuration JSON

        return: 
                Le nombre de capteurs enregistré dans le fichier de configuration JSON
    """
    if DEBUG_MODE == True:
        print("la fonction count_sensor a été appelée")
    all_keys = list(data.keys())
    all_functions = []
    nb_sensors = 1
    for key in all_keys:
        if "function" in key:
            all_functions.append(key)

    for function in all_functions:
        for the_sensor in data[function]:
            if "sensor" in the_sensor:
                nb_sensors += 1
    if DEBUG_MODE == True:
        print("nombre de sensor : ", nb_sensors)
    return nb_sensors

def add_sensors(val, coming_from, capt = None):
    """ Cette fonction permet de créer tous les widgets désirés lorsque le bouton (Ajouter un capteur) est sélectionné sur l'interface
        
        Elle est séparer en deux partie. La première si un capteur est ajouter par l'interface (coming_from == "new").
            La seconde est lorsqu'un fichier déjà enregistré est ouvert par le bouton: Ouvrir... (comign_from == "open").
        
        Elle est appeler par les fonctions suivante:
                                                    - delete_functions (bouton : supprimer de la fonction)
                                                    - function_from_file()
                                                    - create_functions() (bouton : Ajouter un capteur) (coming_from == "new")
                                                    - create_functions() (coming_from == "new")
                                                    - create_functions() (bouton : Ajouter un capteur) (coming_from == "open")



        Paramètres:
                val: numéro de la fonction
                coming_from: {new,open} si elle est nouvelle à partir de l'interface ou qu'elle est appelé lorsqu'un fichier est ouvert
                capt: numéro du capteur lorsqu'un fichier est ouvert
    """
    if DEBUG_MODE == True:
            print("La fonction add_sensors a été appelée")
    if coming_from == "new":
        if DEBUG_MODE == True:
            print("Capteur ajouté à la fonction : ",val)
        with open(dico_file_name["path_to_file"], "r") as f:
            data = json.load(f)

        
# ajout du nouveau capteur dans le fichier
        nb_sensor = count_sensors(data)
        if DEBUG_MODE == True:
            print("le nombre de capteur est : ",nb_sensor)

        data['function %s'%(val)]['sensor %s'%(nb_sensor)] = {"num_capt" : "func: %s. Capt: %s"%(val,nb_sensor), "capts_description": "(description)", "type_channel" : None,"can_adress":"adresse CAN","can_data":None,"range_type":None,"value_of_100":"valeur de 100%"}
#    
        name_french_sens = "Capteur %s"%(nb_sensor)
        if DEBUG_MODE == True:
            print("Le capteur %s a été créé"%(nb_sensor))
        name_sens = Label(the_frame,text=name_french_sens,fg="white",bg="blue") 
        all_sens_keys = list(dico_all_sensors.keys())
        if "func_%s"%(val) in all_sens_keys:
            dico_all_sensors["func_%s"%(val)][name_french_sens] = name_sens
        else:
            dico_all_sensors["func_%s"%(val)] = {name_french_sens : name_sens}

        capts_add_description = Entry(the_frame, width=40)
        capts_add_description.insert(0,data['function %s'%(val)]['sensor %s'%(nb_sensor)]["capts_description"])
        dico_capts_add_description["capts_description_%s"%(nb_sensor)] = capts_add_description
        

        tram_type = StringVar(the_frame)
        tram_type.set("-") 
        opt_can_type = OptionMenu(the_frame, tram_type, *Can_tram_type, command= lambda value: can_channel_type(value,val,name_french_sens, coming_from="new"))
        opt_can_type.config(font=('calibri',(8)),bg='white',width=8)

        can_adress = Entry(the_frame, width=12)
        can_adress.insert(0,data['function %s'%(val)]['sensor %s'%(nb_sensor)]["can_adress"])
        dico_can_adresse["adress_%s"%(nb_sensor)] = can_adress


        max_value = Entry(the_frame, width=20)
        max_value.insert(0,data['function %s'%(val)]['sensor %s'%(nb_sensor)]["value_of_100"])
        dico_value_of_100["max_val_%s"%(nb_sensor)] = max_value

        dico_all_sensors["func_%s"%(val)]["type_channel_sens_%s"%(nb_sensor)] = opt_can_type
        
        
        
# ajout de 1 au compteur de capteur par fonction        
        data['function %s'%(val)]["config_nb_sens"] += 1
#            

        with open(dico_file_name["path_to_file"], 'w') as file:
            json.dump(data, file, indent = 6)

        
# enlever tout les labels et les boutons de l'interface sans supprimer les objets

        delete_frame = []
        for frame in tk.winfo_children():
            if "!label" in str(frame) or "!button" in str(frame):
                delete_frame.append(frame)

        for frame_to_delete in delete_frame:
            frame_to_delete.forget()  
#

# remettre les paramètres de positionnement par défauts

        with open(dico_file_name["path_to_file"], 'r') as f:
            data = json.load(f)
            data['config_y_place_func'] = init_config_y_func
            data['config_x_place_func'] = init_config_x_func
            data['config_y_place_sens'] = init_config_y_sens
            data['config_x_place_sens'] = init_config_x_sens
            
        with open(dico_file_name["path_to_file"], 'w') as file:
            json.dump(data, file, indent = 6)
#

# replacer tous les objets sur l'interface graphique après l'ajout du capteur     
        create_tkinter_widjet()
#

# créer les objets à partir d'un fichier ouvert par l'usager
    elif coming_from == "open":

        with open(dico_file_name["path_to_file"], "r") as f:
            data = json.load(f)
        name_french_sens = "Capteur %s"%(capt)
        if DEBUG_MODE == True:
            print("Le capteur %s a été lu et créé"%(capt))
        name_sens = Label(the_frame,text=name_french_sens,fg="white",bg="blue") #Select title
        all_sens_keys = list(dico_all_sensors.keys())
        if "func_%s"%(val) in all_sens_keys:
            dico_all_sensors["func_%s"%(val)][name_french_sens] = name_sens
        else:
            dico_all_sensors["func_%s"%(val)] = {name_french_sens : name_sens}

        capts_add_description = Entry(the_frame, width=40)
        capts_add_description.insert(0,data['function %s'%(val)]['sensor %s'%(capt)]["capts_description"])

        dico_capts_add_description["capts_description_%s"%(capt)] = capts_add_description

        tram_type = StringVar(the_frame)

        if data["function %s"%(val)]["sensor %s"%(capt)]["type_channel"] == None:
            tram_type.set("-")
        else:
            tram_type.set(data["function %s"%(val)]["sensor %s"%(capt)]["type_channel"])

        opt_can_type = OptionMenu(the_frame, tram_type, *Can_tram_type, command= lambda value: can_channel_type(value,val,name_french_sens, coming_from="new"))
        opt_can_type.config(font=('calibri',(8)),bg='white',width=8)

        can_adress = Entry(the_frame, width=12)
        can_adress.insert(0,data['function %s'%(val)]['sensor %s'%(capt)]["can_adress"])
        dico_can_adresse["adress_%s"%(capt)] = can_adress

        dico_all_sensors["func_%s"%(val)]["type_channel_sens_%s"%(capt)] = opt_can_type

        max_value = Entry(the_frame, width=20)
        max_value.insert(0,data['function %s'%(val)]['sensor %s'%(capt)]["value_of_100"])
        dico_value_of_100["max_val_%s"%(capt)] = max_value


def get_all_entry():
    """ Cette fonction enregistre toutes les entrées manuelles de l'interface dans le fichier.

        Elle est appelée par les fonctions suivantes:
                                                      - add_machine()
                                                      - select_file()
                                                      - save_in_to_file()
                                                      - export_data_for_rpi()
                                                      - convert_all_data()
                                                      - open_power_cycle_math()
                                                      - exit()
    """
    if DEBUG_MODE == True:
        print("La fonction get_all_entry a été appelée")

    if DEBUG_MODE == True:
        print("entrer dans la fonction enregistrer")

    list_all_func = get_all_function()
    list_all_sens = get_all_capt()

    with open(dico_file_name["path_to_file"], "r") as f:
        data = json.load(f)
    
    for fct in list_all_func:
        number = fct.split(' ')
        desc = dico_funcs_add_description["funcs_description_%s"%(number[1])].get()
        data[fct]["funcs_description_%s"%(number[1])] = desc

    for fct_and_capt in list_all_sens:
        number_fct = fct_and_capt[0].split(' ')
        number_capt = fct_and_capt[1].split(' ')
        desc_capt = dico_capts_add_description["capts_description_%s"%(number_capt[1])].get()
        data[fct_and_capt[0]][fct_and_capt[1]]["capts_description"] = desc_capt

        
        data[fct_and_capt[0]][fct_and_capt[1]]["can_adress"] = dico_can_adresse["adress_%s"%(number_capt[1])].get()

        data[fct_and_capt[0]][fct_and_capt[1]]["value_of_100"] = dico_value_of_100["max_val_%s"%(number_capt[1])].get()

        with open(dico_file_name["path_to_file"], "w") as file:
            json.dump(data, file, indent = 6)

def get_all_function():
    """Cette fonction retourne la liste de toutes les fonctions enregistrées dans le fichier

        Elle est appelée par les fonctions suivantes:
                                                     - get_all_entry()
                                                     - get_all_capt()
                                                     - delete_widgets() (choice == "func")
                                                     - function_from_file()
                                                     - validate_all_entry()

    """
    if DEBUG_MODE == True:
        print("La fonction get_all_function a été appelée")
    with open(dico_file_name["path_to_file"], "r") as f:
        data = json.load(f)

    all_func = list(data.keys())
    get_func = []
    for key in all_func:
        if "function" in key:
            get_func.append(key)
    return get_func

def get_all_capt():
    """ Cette fonction retourne une liste de tuples contenant les capteurs et sa fonction associée [(fonction,capteur), (...,...),...] 

        Elle est appelée par les fonctions suivantes:
                                                     - get_all_entry()
                                                     - delete_widgets()
                                                     - delete_widgets() (choice == "sens")
                                                     - function_from_file()
                                                     - select_file()
                                                     - export_data_for_rpi()
                                                     - find_sensors()
                                                     - validate_all_entry()
    """
    if DEBUG_MODE == True:
        print("La fonction get_all_capt a été appelée")
    with open(dico_file_name["path_to_file"], "r") as f:
        data = json.load(f)

    all_func = get_all_function()
    get_sens = []
    for fonc in all_func:
        for capt in data[fonc]:
            if "sensor" in capt:
                get_sens.append((fonc,capt))
    return get_sens

def delete_widgets(win,fonc, choice):
    """ Cette fonction permet à l'usager de supprimé la dernière fonction du fichier de configuration, 
            OU le dernier capteur de la fonction associée

        Elle retire tous les widgets de l'interface 

        Elle appelle la fonction function_from_file() après la réinitialisation de l'interface afin de replacer les widgets à partir du fichier

        Elle est appelé par les fonctions suivantes: 
                                                    - delete_option_window (buttons : {La dernière fonction, Supprimer le dernier capteur de la fonction})
        Paramètres:
                win:    L'objet de la fenêtre de sélection qui se rouvre
                fonc:   La fonction 
                choice: le choix entre la dernière fonction ou le dernier capteur, {"fonc","capt"}
    """
    if DEBUG_MODE == True:
        print("La fonction delete_widgets a été appelée")
    get_sens = get_all_capt()

    with open(dico_file_name["path_to_file"], "r") as f:
        data = json.load(f)
# Supprimer tous les objets des widgets dans l'interface
    for fonc_and_capt in get_sens:
        only_num_capt = fonc_and_capt[1].split(' ')
        only_num_fonc = fonc_and_capt[0].split(' ')
        try:
            dico_funcs["Fonction %s"%(only_num_fonc[1])].destroy()
            dico_funcs_add_description["funcs_description_%s"%(only_num_fonc[1])].destroy()
            dico_button_add_capts["button_fct_%s"%(only_num_fonc[1])].destroy()
            dico_button_delete_funcs["button_del_fct_%s"%(only_num_fonc[1])].destroy()
            dico_all_sensors["func_%s"%(only_num_fonc[1])]["type_channel_sens_%s"%(only_num_capt[1])].destroy()
            dico_all_sensors["func_%s"%(only_num_fonc[1])]["Capteur %s"%(only_num_capt[1])].destroy()
            dico_capts_add_description["capts_description_%s"%(only_num_capt[1])].destroy()
            dico_can_adresse["adress_%s"%(only_num_capt[1])].destroy()
            if data[fonc_and_capt[0]][fonc_and_capt[1]]["type_channel"] == "Analogique":
                dico_nb_bit_by_bytes_analogique_menu_1["can_data_%s"%(only_num_capt[1])].destroy()
                dico_separator["sep_%s"%(only_num_capt[1])].destroy()
                dico_nb_bit_by_bytes_analogique_menu_2["can_data_%s"%(only_num_capt[1])].destroy()
                dico_analogique_type_range["type_range_%s"%(only_num_capt[1])].destroy()
            elif data[fonc_and_capt[0]][fonc_and_capt[1]]["type_channel"] == "Digital":
                dico_byte_from_digital["can_data_%s"%(only_num_capt[1])].destroy()
                dico_bit_from_digital["can_data_%s"%(only_num_capt[1])].destroy()
            dico_value_of_100["max_val_%s"%(only_num_capt[1])].destroy()

        except KeyError:
            break
#
# "fonc représente la suppression de la dernière fonction"
# "capt représente la suppression du dernier capteur associées à la fonction du bouton appuyé"

    if choice == "fonc":
        list_all_func = get_all_function()
        fonc_2 = list_all_func.pop()
        get_num = fonc_2.split(" ")

        data["config_nb_func"] = data["config_nb_func"]-1
        fonc_deleted = data.pop("function %s"%(get_num[1]),None)

        with open(dico_file_name["path_to_file"], 'w') as file:
            json.dump(data, file, indent = 6)
            
        if fonc_deleted != None:
            print("La fonction %s a bien été supprimé"%(get_num[1]))
        else:
            print("Aucune fonction supprimée")
        
        win.destroy()


    elif choice == "sens":
        get_all_capt_by_fonc = []
        for one_fonction in get_sens:
            get_num_fonc = one_fonction[0].split(" ")
            get_num_capt = one_fonction[1].split(" ")
            if get_num_fonc[1] == fonc:
                get_all_capt_by_fonc.append(one_fonction[1])
        if DEBUG_MODE == True:
            print(" Capteur de la fonction : ",get_all_capt_by_fonc)
        capt_to_remove = get_all_capt_by_fonc.pop()
        only_num =capt_to_remove.split(" ") 
        data["function %s"%(fonc)]["config_nb_sens"] = data["function %s"%(fonc)]["config_nb_sens"]-1
        capt_deleted = data["function %s"%(fonc)].pop("sensor %s"%(only_num[1]),None)

        with open(dico_file_name["path_to_file"], 'w') as file:
            json.dump(data, file, indent = 6)

        if capt_deleted != None:
            print("Le capteur %s de la fonction %s à bien été supprimé"%(only_num[1],fonc))
        else:
            print("Aucun capteur supprimé")
    
    function_from_file()

def destroy_win(win):
    """ Cette fonction ferme et détruit la fenêtre qui s'ouvre pour la supression de la fonction

        Elle est appelée par le bouton Terminer de l'interface graphique (par la fonction : delete_option_window) 
    """
    if DEBUG_MODE == True:
        print("La fonction destroy_win a été appelée")
    win.destroy()

def delete_option_window(num_fonc):
    """ Cette fonction créée la fenêtre lorsque le bouton (Supprimer de la fonction) est sélectionné

        Elle est appelé par le bouton : Supprimer de la fonction. C'est les fonctions suivantes qui le crée
                                            -create_functions (coming_from == "new"):
                                            -create_functions (coming_fraom == "open"):
    """
    if DEBUG_MODE == True:
        print("La fonction delete_option_window a été appelée")
    the_frame_level_2 = Toplevel(the_frame, padx=125, pady=130)    
    
    button = Button(the_frame_level_2, text="La dernière fonction", command=lambda : delete_widgets(the_frame_level_2,num_fonc,"fonc"))
    button2 = Button(the_frame_level_2, text="Supprimer le dernier capteur de la fonction %s"%(num_fonc), command=lambda : delete_widgets(the_frame_level_2,num_fonc,"sens"))
    button3 = Button(the_frame_level_2,text="Terminer", command=lambda : destroy_win(the_frame_level_2))
    button.grid(row = 1, column = 2, padx = 30, pady =10)
    button2.grid(row = 2, column = 2, padx = 30, pady =10)
    button3.grid(row=1, column=3, padx = 30, pady =10)


def can_channel_type(val, num_fonc, num_capteur, coming_from=None):
    """ Cette fonction permet de créer les widgets byte 1 - byte 2 et le menu déroulant du Range pour les capteurs analogique
            et les entrées des octets et du bit pour les capteurs digitaux. Elle supprime aussi les objets lorsque la sélection pour un capteur
            passe de analogique à digital et vis versa. 

        Elle est appelée par les fonctions suivantes:
                                                     - function_from_file
                                                     - (add_sensors) Lorsque le type de channel (analogique ou digital) est sélectionné par l'usager
                                                        pour chacun des capteurs 
        Paramètre:
            val: valeur sélectionnée par l'usager, {Analogique,Digital}
            num_fonc: numéro de la fonction
            num_capteur: 
            coming_from: {None, new, open} lorsque la fonction est appelé par add_sensors, et que le widget est créer: new
                                            lorsque la donction est appelée par function_from_file et qu'un fichier est ouvert: open
                                            Le reste du temps None
    """
    if DEBUG_MODE == True:
        print("La fonction can_channel_type a été appelée")
    channel_type = val
    nb_capteur = num_capteur.split(' ')

    with open(dico_file_name["path_to_file"], 'r') as f:
        data = json.load(f)

    do_nothing = False

    if (data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["type_channel"] == channel_type) and (coming_from == "new"):
        do_nothing = True

    if do_nothing == False:
        
        if coming_from != "open":
            data['config_y_place_func'] = init_config_y_func
            data['config_x_place_func'] = init_config_x_func
            data['config_y_place_sens'] = init_config_y_sens
            data['config_x_place_sens'] = init_config_x_sens

        data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["type_channel"] = channel_type

        with open(dico_file_name["path_to_file"], 'w') as file:
            json.dump(data, file, indent = 6)
        
        if channel_type == "Analogique":
            if DEBUG_MODE == True:
                print("Le 'range' du capteur %s de la fonction %s : %s"%(nb_capteur[1],num_fonc,data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"]))
    # Cette condition sert à supprimé les entreée pour les capteur analogique si la fonction digital est sélectionné à la place 
    # lorsque qu'une interface est loadée
            if (data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"] == "digital") and (coming_from == "new"):
                dico_byte_from_digital["can_data_%s"%(nb_capteur[1])].destroy()
                dico_bit_from_digital["can_data_%s"%(nb_capteur[1])].destroy()

                data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"] = [None,None]
                data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"] = "analog"
                with open(dico_file_name["path_to_file"], 'w') as file:
                    json.dump(data, file, indent = 6)

    # Cette condition sert à supprimé les entreée pour les capteur analogique si la fonction digital est sélectionné à la place 
    # lorsque qu'une nouvelle interface est crée
            elif coming_from == "new":
                data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"] = [None,None]
                data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"] = "analog"
                with open(dico_file_name["path_to_file"], 'w') as file:
                    json.dump(data, file, indent = 6)

            elif coming_from == "open":
                if data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"][0] == None:
                    data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"][0] ="byte 1"

                if data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"][1] == None:
                    data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"][1] ="byte 2"

            can_data_type_1 = StringVar(the_frame)
            can_data_type_1.set("byte 1")
            
            if (coming_from == "open") and (type(data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"]) == list):
                can_data_type_1.set(data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"][0])
        
            can_data_1 = OptionMenu(the_frame, can_data_type_1, *Can_nb_bytes_1, command= lambda value: nb_bytes_for_message_1(value,num_fonc,nb_capteur[1]))
            can_data_1.config(font=('calibri',(8)),bg='white',width=3)

            separator = Label(the_frame,text="-",fg="white",bg="blue")

            can_data_type_2 = StringVar(the_frame)
            can_data_type_2.set("byte 2")
            if (coming_from == "open") and (type(data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"]) == list):
                can_data_type_2.set(data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"][1]) 
            can_data_2 = OptionMenu(the_frame, can_data_type_2, *Can_nb_bytes_2, command= lambda value: nb_bytes_for_message_2(value,num_fonc,nb_capteur[1]))
            can_data_2.config(font=('calibri',(8)),bg='white',width=3)

            type_range_analogique = StringVar(the_frame)
            type_range_analogique.set("Range")
            if (coming_from == "open") and (data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"] != None) and (data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"] != "digital") and (data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"] != "analog"):
                type_range_analogique.set(data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"])
            range = OptionMenu(the_frame, type_range_analogique, *Can_range_analogique, command= lambda value: type_of_range_analogique(value,num_fonc,nb_capteur[1]))
            range.config(font=('calibri',(8)),bg='white',width=9)

            dico_nb_bit_by_bytes_analogique_menu_1["can_data_%s"%(nb_capteur[1])] = can_data_1
            dico_separator["sep_%s"%(nb_capteur[1])] = separator
            dico_nb_bit_by_bytes_analogique_menu_2["can_data_%s"%(nb_capteur[1])] = can_data_2
            dico_analogique_type_range["type_range_%s"%(nb_capteur[1])] = range

        if channel_type == "Digital":
    # Cette condition sert à supprimé les entreée pour les capteur digitaux si la fonction analogique est sélectionnée à la place 
    # lorsque qu'une interface est loadée

            if ((data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"] == [None,None]) or (data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"] != None) or (data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"] == "analog") or (data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"] != None)) and (coming_from == "new"):
                dico_nb_bit_by_bytes_analogique_menu_1["can_data_%s"%(nb_capteur[1])].destroy()
                dico_separator["sep_%s"%(nb_capteur[1])].destroy()
                dico_nb_bit_by_bytes_analogique_menu_2["can_data_%s"%(nb_capteur[1])].destroy()
                dico_analogique_type_range["type_range_%s"%(nb_capteur[1])].destroy()

            elif coming_from == "open":
                if data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"] == None:
                    data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"] = "b"

            data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["range_type"] = "digital"
            with open(dico_file_name["path_to_file"], 'w') as file:
                json.dump(data, file, indent = 6) 
            digital_byte_of_message = StringVar(the_frame)
            digital_byte_of_message.set("octet")

            digital_bit_from_byte = StringVar(the_frame)
            digital_bit_from_byte.set("bit")

            if (coming_from == "open") and ((type(data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"]) != list) or (data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"] != None)):
                try:
                    assert data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"].find("b") != -1, \
                        "un capteur digital %s n'a pas le bon format dans le fichier. Il devrait être du format xbx mais il est de %s"%(nb_capteur[1], data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"])
                except AssertionError:
                    list_assertion.append("un capteur digital %s n'a pas le bon format dans le fichier. Il devrait être du format xbx mais il est de %s"%(nb_capteur[1], data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"]))
                    dico_all_error_message["assertions_partie_1"] = list_assertion

                digital_values = data["function %s"%(num_fonc)]["sensor %s"%(nb_capteur[1])]["can_data"].split("b")
                digital_byte_of_message.set(digital_values[0])
                digital_bit_from_byte.set(digital_values[1])

            digital_byte = OptionMenu(the_frame, digital_byte_of_message, *Can_digital_bit, command= lambda value: byte_message_digital(value,num_fonc,nb_capteur[1]))
            digital_byte.config(font=('calibri',(8)),bg='white',width=13)
            dico_byte_from_digital["can_data_%s"%(nb_capteur[1])] = digital_byte

            digital_bit_of_message = OptionMenu(the_frame, digital_bit_from_byte, *Can_digital_bit, command= lambda value: bit_from_message_digital(value,num_fonc,nb_capteur[1]))
            digital_bit_of_message.config(font=('calibri',(8)),bg='white',width=13)
            dico_bit_from_digital["can_data_%s"%(nb_capteur[1])] = digital_bit_of_message
            
        if coming_from != "open":
            create_tkinter_widjet()


    
def nb_bytes_for_message_1(val, fonc, nb_sens):
    """ Cette fonction sert à écrire dans le fichier l'octet 1 sélectionné par l'usager (pour les capteurs analogiques)

        Elle est appelée par la fonction suivante: can_channel_type (menu déroulant lorsqu'un octet est sélectionné par l'usager)

        paramètres: 
            val     : octet sélectionné par l'usager
            fonc    : fonction associée
            nb_sens : capteur associé
    """

    if DEBUG_MODE == True:
        print("La fonction nb_bytes_for_message_1 a été appelée")
    first_byte_of_message = val
    if DEBUG_MODE == True:
        print("selected type : ",first_byte_of_message)
        print("fonction ", fonc)
        print("sensor", nb_sens)

    with open(dico_file_name["path_to_file"], 'r') as f:
        data = json.load(f)
    try:
        assert data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["type_channel"] == "Analogique", \
            "le capteur %s est digital, mais devrait être analogique"%(nb_sens)
    except AssertionError:
        list_assertion.append("le capteur %s est digital, mais devrait être analogique"%(nb_sens))
        dico_all_error_message["assertions_partie_1"] = list_assertion
    if data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"] == None:
        data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"] = (first_byte_of_message,None)
    
    elif data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"] != None:
        data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"] = (first_byte_of_message,data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"][1])

    with open(dico_file_name["path_to_file"], 'w') as file:
        json.dump(data, file, indent = 6)

def nb_bytes_for_message_2(val, fonc, nb_sens):
    """ Cette fonction sert à écrire dans le fichier l'octet 2 sélectionné par l'usager (pour les capteurs analogiques)
    
        Elle est appelée par la fonction suivante: can_channel_type (menu déroulant lorsqu'un octet est sélectionné par l'usager)

        paramètres: 
            val     : octet sélectionné par l'usager
            fonc    : fonction associée
            nb_sens : capteur associé
    """
    if DEBUG_MODE == True:
        print("La fonction nb_bytes_for_message_2 a été appelée")
    last_byte_of_message = val
    if DEBUG_MODE == True:
        print("selected type : ",last_byte_of_message)
        print("fonction ", fonc)
        print("sensor", nb_sens)

    with open(dico_file_name["path_to_file"], 'r') as f:
        data = json.load(f)

    try:
        assert data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["type_channel"] == "Analogique", \
            "le capteur %s est digital, mais devrait être analogique"%(nb_sens)
    except AssertionError:
        list_assertion.append("le capteur %s est digital, mais devrait être analogique"%(nb_sens))
        dico_all_error_message["assertions_partie_1"] = list_assertion

    if data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"] == None:
        data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"] = (None,last_byte_of_message)
    
    elif data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"] != None:
        data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"] = (data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"][0],last_byte_of_message)

    with open(dico_file_name["path_to_file"], 'w') as file:
        json.dump(data, file, indent = 6)

def type_of_range_analogique(val, fonc, nb_sens):
    """ Cette fonction sert à écrire dans le fichier le range sélectionné par l'usager (pour les capteurs analogiques)
    
        Elle est appelée par la fonction suivante: can_channel_type (menu déroulant lorsque le range est sélectionné par l'usager)

        paramètres: 
            val     : range sélectionné par l'usager
            fonc    : fonction associée
            nb_sens : capteur associé
    """
    if DEBUG_MODE == True:
        print("La fonction type_of_range_analogique a été appelée")
    type_of_range = val
    if DEBUG_MODE == True:
        print("selected type : ",type_of_range)
        print("fonction ", fonc)
        print("sensor", nb_sens)

    with open(dico_file_name["path_to_file"], 'r') as f:
        data = json.load(f)

    try:
        assert data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["type_channel"] == "Analogique", \
            "le capteur %s est digital, mais devrait être analogique"%(nb_sens)
    except AssertionError:
        list_assertion.append("le capteur %s est digital, mais devrait être analogique"%(nb_sens))
        dico_all_error_message["assertions_partie_1"] = list_assertion

    data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["range_type"] = type_of_range

    with open(dico_file_name["path_to_file"], 'w') as file:
        json.dump(data, file, indent = 6)

def bit_from_message_digital(val, fonc, nb_sens):
    """ Cette fonction sert à écrire dans le fichier le bit de l'octet sélectionné par l'usager (pour les capteurs digitaux)
    
        Elle est appelée par la fonction suivante: can_channel_type (menu déroulantde droite (le bit de l'octet) est sélectionné par l'usager)

        Le message est écrire avec le numéro de l'octet {0,1,2,3,4,5,6,7} suivi de la lettre b suivi de du bit de l'octet {0,1,2,3,4,5,6,7}.
            par exemple: l'octet 2 et le bit 1 --> 2b1

        paramètres: 
            val     : bit de l'octet sélectionné par l'usager
            fonc    : fonction associée
            nb_sens : capteur associé
    """
    if DEBUG_MODE == True:
        print("La fonction bit_from_message_digital a été appelée")
    bit_with_message = val
    if DEBUG_MODE == True:
        print("selected type bit : ",bit_with_message)
        print("fonction ", fonc)
        print("sensor", nb_sens)

    with open(dico_file_name["path_to_file"], 'r') as f:
        data = json.load(f)

    try:
        assert data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["type_channel"] == "Digital", \
            "le capteur %s est analogique, mais devrait être digital"%(nb_sens)
    except AssertionError:
        list_assertion.append("le capteur %s est analogique, mais devrait être digital"%(nb_sens))
        dico_all_error_message["assertions_partie_1"] = list_assertion

    val_digital_bit = data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"]
    if (type(val_digital_bit) == list) or (val_digital_bit == None):
        val_digital_bit = "b" + bit_with_message
        
    else:
        if val_digital_bit.find("b") == -1:
                val_digital_bit = "b" + bit_with_message
        else:
            only_bit = val_digital_bit.split("b")
            val_digital_bit = only_bit[0] + "b" + bit_with_message




    data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"] = val_digital_bit

    with open(dico_file_name["path_to_file"], 'w') as file:
        json.dump(data, file, indent = 6)


def byte_message_digital(val, fonc, nb_sens):
    """ Cette fonction sert à écrire dans le fichier l'octet sélectionné par l'usager (pour les capteurs digitaux)
    
        Elle est appelée par la fonction suivante: can_channel_type (menu déroulantde gauche (l'octet) est sélectionné par l'usager)

        Le message est écrire avec le numéro de l'octet {0,1,2,3,4,5,6,7} suivi de la lettre b suivi de du bit de l'octet {0,1,2,3,4,5,6,7}.
            par exemple: l'octet 2 et le bit 1 --> 2b1
            
        paramètres: 
            val     : l'octet sélectionné par l'usager
            fonc    : fonction associée
            nb_sens : capteur associé
    """
    if DEBUG_MODE == True:
        print("La fonction byte_message_digital a été appelée")

    byte_with_message = val
    if DEBUG_MODE == True:
        print("selected type byte: ",byte_with_message)
        print("fonction ", fonc)
        print("sensor", nb_sens)

    with open(dico_file_name["path_to_file"], 'r') as f:
        data = json.load(f)

    try:
        assert data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["type_channel"] == "Digital", \
            "le capteur %s est analogique, mais devrait être digital"%(nb_sens)
    except AssertionError:
        list_assertion.append("le capteur %s est analogique, mais devrait être digital"%(nb_sens))
        dico_all_error_message["assertions_partie_1"] = list_assertion

    
    val_digital_byte = data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"]
    if (type(val_digital_byte) == list) or (val_digital_byte == None):
        val_digital_byte = byte_with_message + "b"
    else:
        if val_digital_byte.find("b") == -1:
            val_digital_byte = byte_with_message + "b"
        else:
            only_byte = val_digital_byte.split("b")
            val_digital_byte = byte_with_message + "b" + only_byte[1]

    data["function %s"%(fonc)]["sensor %s"%(nb_sens)]["can_data"] = val_digital_byte

    with open(dico_file_name["path_to_file"], 'w') as file:
        json.dump(data, file, indent = 6)

def function_from_file():
    """ Cette fonction permet de lire un fichier json et de créer tous les widgets s'y trouvant.

        La fonction create_tkinter_widjet est ensuite appelée pour placer ces widgets sur l'interface

        Elle est appelée par les fonctions suivantes:
                                                        - delete_widgets
                                                        - select_file (bouton de l'interface (Ouvrir...))
    """
    if DEBUG_MODE == True:
        print("La fonction function_from_file a été appelée")
    get_fonc = get_all_function()
    get_sens = get_all_capt()
# Supprimer tous les widgets enregistrer dans les dictionnaires
    dico_funcs.clear()
    dico_funcs_add_description.clear()
    dico_button_add_capts.clear()
    dico_button_delete_funcs.clear()
    dico_all_sensors.clear()
    dico_capts_add_description.clear()
    dico_can_adresse.clear()
    dico_nb_bit_by_bytes_analogique_menu_1.clear()
    dico_separator.clear()
    dico_nb_bit_by_bytes_analogique_menu_2.clear()
    dico_analogique_type_range.clear()
    dico_byte_from_digital.clear()
    dico_bit_from_digital.clear()
    dico_value_of_100.clear()

    dico_scrollbar.clear()
#
    with open(dico_file_name["path_to_file"], "r") as f:
        data = json.load(f)

# Créer tous les fonctions dans le fichier
    for fonc in get_fonc:
        number = fonc.split(" ")
        create_functions(number[1],"open")
#
    try:
        assert len(get_fonc) == data["config_nb_func"], \
            "Les nombres de fonction enregistré dans le fichier et détecté ne correspondent pas" # il y a un compteur de fonction dans le fichier
    except AssertionError:
        list_assertion.append("Les nombres de fonction enregistré dans le fichier et détecté ne correspondent pas")
        dico_all_error_message["assertions_partie_1"] = list_assertion

# Créer tous les capteurs dans le fichier               
    for fct_and_capt in get_sens:
        number_fct = fct_and_capt[0].split(' ')
        number_capt = fct_and_capt[1].split(' ')
        add_sensors(number_fct[1], "open",number_capt[1])
#
# Créer tous les menus déroulants des sélections des octets et des bits pour les capteurs analogiques ou digitaux
    for fct_and_capt in get_sens:
        number_fct = fct_and_capt[0].split(' ')
        if data[fct_and_capt[0]][fct_and_capt[1]]["type_channel"] != None:
            val_type =  data[fct_and_capt[0]][fct_and_capt[1]]["type_channel"] 
            can_channel_type(val_type, number_fct[1], fct_and_capt[1], coming_from="open")
#


    data['config_y_place_func'] = init_config_y_func
    data['config_x_place_func'] = init_config_x_func
    data['config_y_place_sens'] = init_config_y_sens
    data['config_x_place_sens'] = init_config_x_sens

    with open(dico_file_name["path_to_file"], 'w') as file:
        json.dump(data, file, indent = 6)

# Placer les widgets créés sur l'interface graphique
    create_tkinter_widjet()
#

def create_functions(num_fct, coming_from):
    """ Cette fonction sert à créer et à placer la ligne des fonctions sur l'interface graphique (fonction, entrée, bouton 1, bouton 2)

        Elle est appelée par les fonctions suivantes: 
                                                     - add_function()
                                                     - function_from_file()
        paramètre:
                num_fct: fonction à créer
                coming_from {new,open}: -new si appelée par la fonction add_function (bouton de l'interface (Nouvelle fonction))
                                        -open si appelée par la fonction function_from_file (bouton de l'interface (Ouvrir...))
    """
    if DEBUG_MODE == True:
        print("La fonction create_functions a été appelée")
    
    if coming_from == "new":
        if DEBUG_MODE == True:
            print("La fonction %s a bien été appelée"%(num_fct))
        with open(dico_file_name["path_to_file"], "r") as f:
            data = json.load(f)

        name_french = "Fonction %s"%(num_fct)
        name = Label(the_frame,text=name_french,fg="white",bg="blue") #Select title
        dico_funcs[name_french] = name
        dico_funcs[name_french].place(x = data["config_x_place_func"][0], y = data["config_y_place_func"])

        funcs_add_description = Entry(the_frame, width=20)
        funcs_add_description.insert(0,'(description)')
        dico_funcs_add_description["funcs_description_%s"%(num_fct)] = funcs_add_description
        dico_funcs_add_description["funcs_description_%s"%(num_fct)].place(x=data["config_x_place_func"][1],y=data["config_y_place_func"])


        button_add_sensors = Button(the_frame, text="Ajouter un capteur", command= lambda : add_sensors(num_fct,"new"))
        dico_button_add_capts["button_fct_%s"%(num_fct)] = button_add_sensors
        dico_button_add_capts["button_fct_%s"%(num_fct)].place(x=data["config_x_place_func"][2],y=data["config_y_place_func"])
        button_delete_function = Button(the_frame, text="Supprimer de la fonction", command= lambda : delete_option_window(num_fct))
        dico_button_delete_funcs["button_del_fct_%s"%(num_fct)] = button_delete_function
        dico_button_delete_funcs["button_del_fct_%s"%(num_fct)].place(x = data["config_x_place_func"][3] , y = data["config_y_place_func"])
        data['function %s'%(num_fct)] = {"funcs_description_%s"%(num_fct): "(description)",
        "config_nb_sens" : 0}
        data["config_y_place_func"] += 60
            

        with open(dico_file_name["path_to_file"], 'w') as file:
            json.dump(data, file, indent = 6)


        add_sensors(num_fct, coming_from)

    elif coming_from == "open":
        with open(dico_file_name["path_to_file"], "r") as f:
            data = json.load(f)
        
        name_french = "Fonction %s"%(num_fct)
        name = Label(the_frame,text=name_french ,fg="white",bg="blue") #Select title
        dico_funcs[name_french] = name
        dico_funcs[name_french].place(x = data["config_x_place_func"][0], y = data["config_y_place_func"])

        funcs_add_description = Entry(the_frame, width=20)
        funcs_add_description.insert(0,data["function %s"%(num_fct)]["funcs_description_%s"%(num_fct)])
        dico_funcs_add_description["funcs_description_%s"%(num_fct)] = funcs_add_description
        dico_funcs_add_description["funcs_description_%s"%(num_fct)].place(x=data["config_x_place_func"][1],y=data["config_y_place_func"])

        button_add_sensors = Button(the_frame, text="Ajouter un capteur", command= lambda : add_sensors(num_fct,'new'))
        dico_button_add_capts["button_fct_%s"%(num_fct)] = button_add_sensors
        dico_button_add_capts["button_fct_%s"%(num_fct)].place(x=data["config_x_place_func"][2],y=data["config_y_place_func"])
        button_delete_function = Button(the_frame, text="Supprimer de la fonction", command= lambda : delete_option_window(num_fct))
        dico_button_delete_funcs["button_del_fct_%s"%(num_fct)] = button_delete_function
        dico_button_delete_funcs["button_del_fct_%s"%(num_fct)].place(x = data["config_x_place_func"][3] , y = data["config_y_place_func"])


def select_file():
    """ Cette fonction sert à modifier le fichier utilisé par l'interface graphique.
        Elle permet d'importer les informations contenues dans le fichier dans l'interface graphique en appelant la fonction function_from_file
        Elle permet aussi de supprmier le fichier json par défaut automatiquement créer lorsqu'une nouvelle interface est ouverte.
    
        Elle est appelée par le bouton Ouvrir... de l'interface graphique

    """

    if DEBUG_MODE == True:
        print("La fonction select_file a été appelée")

    filetypes = (('text files', '*.json'),('All files', '*.*'))
    filename = fd.askopenfilename(title="Sélectionner l'interface à ouvrir",initialdir=dico_file_name["path_to_folder"],filetypes=filetypes)
    list_str = filename.split("/")
    only_name = list_str[len(list_str)-1]
    
    if filename != "":
        pass
    else:
        print("action annulée")
        return None

    today = datetime.datetime.now()
    today_format = today.strftime("%b_%d_%Y")
    name_default = "default_config_interface_" + today_format + ".json"
    default_file = None
    if name_default == dico_file_name["filename"]:
        default_file = dico_file_name["path_to_file"]

    get_all_entry()
    get_sens = get_all_capt()

    with open(dico_file_name["path_to_file"], "r") as f:
            data = json.load(f)

    for fonc_and_capt in get_sens:
            only_num_capt = fonc_and_capt[1].split(' ')
            only_num_fonc = fonc_and_capt[0].split(' ')
            try:
                dico_funcs["Fonction %s"%(only_num_fonc[1])].destroy()
                dico_funcs_add_description["funcs_description_%s"%(only_num_fonc[1])].destroy()
                dico_button_add_capts["button_fct_%s"%(only_num_fonc[1])].destroy()
                dico_button_delete_funcs["button_del_fct_%s"%(only_num_fonc[1])].destroy()
                dico_all_sensors["func_%s"%(only_num_fonc[1])]["type_channel_sens_%s"%(only_num_capt[1])].destroy()
                dico_all_sensors["func_%s"%(only_num_fonc[1])]["Capteur %s"%(only_num_capt[1])].destroy()
                dico_capts_add_description["capts_description_%s"%(only_num_capt[1])].destroy()
                dico_can_adresse["adress_%s"%(only_num_capt[1])].destroy()
                if data[fonc_and_capt[0]][fonc_and_capt[1]]["type_channel"] == "Analogique":
                    dico_nb_bit_by_bytes_analogique_menu_1["can_data_%s"%(only_num_capt[1])].destroy()
                    dico_separator["sep_%s"%(only_num_capt[1])].destroy()
                    dico_nb_bit_by_bytes_analogique_menu_2["can_data_%s"%(only_num_capt[1])].destroy()
                    dico_analogique_type_range["type_range_%s"%(only_num_capt[1])].destroy()
                elif data[fonc_and_capt[0]][fonc_and_capt[1]]["type_channel"] == "Digital":
                    dico_byte_from_digital["can_data_%s"%(only_num_capt[1])].destroy()
                    dico_bit_from_digital["can_data_%s"%(only_num_capt[1])].destroy()
                dico_value_of_100["max_val_%s"%(only_num_capt[1])].destroy()
            except KeyError:
                break
    dico_funcs.clear()
    dico_funcs_add_description.clear()
    dico_button_add_capts.clear()
    dico_button_delete_funcs.clear()
    dico_all_sensors.clear()
    dico_capts_add_description.clear()
    dico_can_adresse.clear()
    dico_nb_bit_by_bytes_analogique_menu_1.clear()
    dico_separator.clear()
    dico_nb_bit_by_bytes_analogique_menu_2.clear()
    dico_analogique_type_range.clear()
    dico_byte_from_digital.clear()
    dico_bit_from_digital.clear()
    dico_value_of_100.clear()

    dico_scrollbar.clear()

    dico_file_name["filename"] = only_name
    dico_file_name["path_to_file"] = filename

    if default_file != None:
        os.remove(default_file)
    

    function_from_file()

def save_in_to_file():
    """ Cette fonction sert à enregistrer les informations contenus dans un interface grapique dans un fichier JSON de nom différent

        Elle est appelée par le bouton Enregistrer sous... de l'interface graphique

    """
    if DEBUG_MODE == True:
        print("La fonction save_in_to_file a été appelée")

    today = datetime.datetime.now()
    today_format = today.strftime("%b_%d_%Y")
    name_default = "default_config_interface_" + today_format + ".json"
    default_file = None
    if name_default == dico_file_name["filename"]:
        default_file = dico_file_name["path_to_file"]

    get_all_entry()
    
    files = [('json', '*.json')]
    file = fd.asksaveasfile(title = "Sauvegarder l'interface graphique", initialfile = dico_file_name["filename"],initialdir=dico_file_name["path_to_folder"],filetypes = files, defaultextension = files)

    if file != None:
        list_str = file.name.split("/")
        only_name = list_str[len(list_str)-1]
        with open(dico_file_name["path_to_file"], "r") as f:
            data = json.load(f)
        dico_file_name["filename"] = only_name
        dico_file_name["path_to_file"] = file.name

        with open(dico_file_name["path_to_file"], 'w') as file:
            json.dump(data, file, indent = 6)

        if default_file != None:
            os.remove(default_file)
    else:
        print("action annulée")

def export_data_for_rpi():
    """ Cette fonction sert à produire le fichier configCan.csv et à l'enregistrer dans le dossier fichier_pour_la_rpi (à partir des informations du fichier json)

        Dans ce fichier, chaque colonne est une adresse et les lignes représentent les octets à lire pour chaque capteur
    
        Elle est appelée par le bouton (Exportation pour RPI) de l'interface graphique

    """

    if DEBUG_MODE == True:
        print("La fonction export_data_for_rpi a été appelée")

    get_all_entry()

    get_capts = get_all_capt()


    with open(dico_file_name["path_to_file"], "r") as f:
            data = json.load(f)


    # Cette partie sert à aller chercher toutes les can_data pour chacune des adresse et à les classer dans un dictionnaire (dico) avec les adresses comme 
    # clés et un dictionnaire comprenant le numero du capteur et la valeur du can_data associée comme valeur
    dico = {}
    for all_capt in get_capts:
        can_ad = data[all_capt[0]][all_capt[1]]["can_adress"]

        try:
            assert (can_ad[len(can_ad)-2:len(can_ad)] =="FD") or (can_ad[len(can_ad)-2:len(can_ad)] =="fd") or (can_ad[len(can_ad)-2:len(can_ad)] =="Fd") or (can_ad[len(can_ad)-2:len(can_ad)] =="fD"),\
                "les adresses doivent se terminer par (FD,fd,Fd ou fD) et non pas : %s, (Capteur %s)"%(can_ad[len(can_ad)-2:len(can_ad)],all_capt[1])
        except AssertionError:
            error_for_rpi.append("les adresses doivent se terminer par (FD,fd,Fd ou fD) et non pas : %s, (Capteur %s)"%(can_ad[len(can_ad)-2:len(can_ad)],all_capt[1]))
            dico_all_error_message["for_rpi"] = error_for_rpi
        try:
            assert len(can_ad) == 10,\
                "Les adresses doivent être composé de 10 caractères et non pas %s, (%s)"%(len(can_ad),"Capteur %s"%(all_capt[1]))

        except AssertionError:
            error_for_rpi.append("Les adresses doivent être composé de 10 caractères et non pas %s, (%s)"%(len(can_ad),"Capteur %s"%(all_capt[1])))
            dico_all_error_message["for_rpi"] = error_for_rpi
        
        can_ad = can_ad[0:len(can_ad)-2] + "fd"

        if can_ad in list(dico.keys()):
            dico[can_ad][all_capt[1]] = data[all_capt[0]][all_capt[1]]["can_data"]

    # Cette partie sert à formater les can_data analogique de ["1","2"] à "1_2"
            if type(data[all_capt[0]][all_capt[1]]["can_data"]) == list:
                val_1 = data[all_capt[0]][all_capt[1]]["can_data"][0]
                val_2 = data[all_capt[0]][all_capt[1]]["can_data"][1]
                val_final = val_1+"_"+val_2
                dico[can_ad][all_capt[1]] = val_final
        else:
            dico[can_ad] = {all_capt[1]:data[all_capt[0]][all_capt[1]]["can_data"]}
    # Cette partie sert à formater les can_data analogique de ["1","2"] à "1_2"
            if type(data[all_capt[0]][all_capt[1]]["can_data"]) == list:
                val_1 = data[all_capt[0]][all_capt[1]]["can_data"][0]
                val_2 = data[all_capt[0]][all_capt[1]]["can_data"][1]
                val_final = val_1+"_"+val_2
                dico[can_ad] = {all_capt[1]:val_final}

    # Cette boucle sert a aller chercher les 6 digits de chacune des adresses et de les enregistrer dans une list (only_digit_of_adress_list) 
    all_keys = dico.keys()

    only_digit_of_adress_list = []
    for adress in all_keys:
        ad_complete = adress
        adress = adress[2:len(adress)]
        only_digit_list = ""
        for digit in adress:
            if digit.isdigit():
                only_digit_list += digit
        try:
            assert ad_complete[0:2] == "0x", \
                "Les adresses doivent commencées par les symboles 0x et non pas %s, (Capteur %s)"%(ad_complete[0:3],list(dico[ad_complete].keys())[0])
        except AssertionError:
            error_for_rpi.append("Les adresses doivent commencées par les symboles 0x et non pas %s, (Capteur %s)"%(ad_complete[0:3],list(dico[ad_complete].keys())[0]))
            dico_all_error_message["for_rpi"] = error_for_rpi
        try:
            assert len(only_digit_list) == 6,\
                "Les adresses doivent être composé de 6 digits et non pas %s, (Capteur %s)"%(len(only_digit_list),list(dico[ad_complete].keys())[0])
        except AssertionError:
            error_for_rpi.append("Les adresses doivent être composé de 6 digits et non pas %s, (Capteur %s)"%(len(only_digit_list),list(dico[ad_complete].keys())[0]))
            dico_all_error_message["for_rpi"] = error_for_rpi
        only_digit_of_adress_list.append(int(only_digit_list))

    if dico_all_error_message["for_rpi"] != []:
        fenetre_erreur(dico_all_error_message["for_rpi"],"for_rpi")
        return None
    
    only_digit_of_adress_list.sort()
    adresse_sorted_complete = []
    for half_adress in only_digit_of_adress_list:
        adresse_sorted_complete.append("0x" + str(half_adress) + "fd")

    # Cette boucle créer un nouveau dictionnaire avec les clés en ordre croissant avec leurs valeurs respectives
    dico_for_csv = {}
    list_with_all_adress = []
    for adress in adresse_sorted_complete:
        list_csv = []
        list_with_all_adress.append(adress)
        for tupl in list(dico[adress].keys()):
            list_csv.append((tupl,dico[adress][tupl]))
        dico_for_csv[adress] = list_csv

    # Cette boucle trouve quelle clée possède le plus grand nombre de valeur et enregistre cette valeur (number_of_line_in_csv)
    number_of_line_in_csv = 0
    for ad in list(dico_for_csv.keys()):
        if len(list(dico_for_csv[ad])) > number_of_line_in_csv:
            number_of_line_in_csv = len(list(dico_for_csv[ad]))

    # Cette boucle complète les colonnes d'adresse avec des '' (case vide)
    for ad in list(dico_for_csv.keys()):
        if len(dico_for_csv[ad]) < number_of_line_in_csv:
            for i in range(number_of_line_in_csv - len(list(dico_for_csv[ad]))):
                dico_for_csv[ad].append(("vide",''))

    dictionnary_of_all_lines_in_csv_file = {}
    
    if DEBUG_MODE == True:
        print(" ")
        print("Formatage du fichier csv : ")
        print(" ")

    for i in range(number_of_line_in_csv):
        Line_of_csv_file_in_list = []
        for ad in list(dico_for_csv.keys()):
            Line_of_csv_file_in_list.append(dico_for_csv[ad][i][1])
        dictionnary_of_all_lines_in_csv_file["ligne %s"%(i+1)] = Line_of_csv_file_in_list


    file_name_csv = dico_file_name["Path_to_machine_folder"] + "\\fichier_pour_la_rpi\\configCan.csv"


    with open(file_name_csv, 'w', newline='') as csvfile:
        fieldnames = adresse_sorted_complete
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        dico_with_all_can_data = {}
        for i in range(number_of_line_in_csv):
            for j in range(len(list_with_all_adress)):
                dico_with_all_can_data[list_with_all_adress[j]] = dictionnary_of_all_lines_in_csv_file["ligne %s"%(i+1)][j]

            writer.writerow(dico_with_all_can_data)

    list_indication = ["Données pour la RPI importées","Enregistrement effectué sans problème. Exporté dans : %s"%("configCan.csv")]
    dico_all_error_message["indication"] =list_indication
        
    fenetre_erreur(dico_all_error_message["indication"],"indication", is_indication=True)
    print("Enregistrement effectué sans problème. Exporté dans : %s"%("configCan.csv"))

def adjust_windows(name_file, x_def, y_def):
    """ Cette fonction créer une fenêtre pour permettant à l'usager de modifier la taille de l'interface

        Elle est appelée par le bouton de l'interface graphique suivant: taille de la fenêtre 

        paramètre:
            name_file : path du fichier json de la taille de l'interface
            x_def     : longueur par défaut
            y_def     : hauteur par défaut
    """
    if DEBUG_MODE == True:
        print("La fonction adjust_windows a été appelée")

    with open(name_file, "r") as f:
        data_2 = json.load(f)
    the_frame_level_2 = Toplevel(the_frame, padx=125, pady=130)    
    largeur = Label(the_frame_level_2,text='entrez la largeur',fg="white",bg="blue") #Select title
    ent_largeur = Entry(the_frame_level_2, width=20)
    ent_largeur.insert(0,data_2['windows_width'])
    hauteur = Label(the_frame_level_2,text='entrez la hauteur',fg="white",bg="blue") #Select title
    ent_hauteur = Entry(the_frame_level_2, width=20)
    ent_hauteur.insert(0,data_2['windows_length'])
    button = Button(the_frame_level_2, text="terminer", command=lambda : get_ent_button_level_2(name_file, ent_largeur, ent_hauteur, the_frame_level_2))
    button2 = Button(the_frame_level_2, text="remettre les paramètres par défaut", command=lambda : get_ent_button2_level_2(ent_largeur, ent_hauteur, x_def, y_def))

    largeur.grid(row = 0, column = 0, padx = 30, pady =10)
    ent_largeur.grid(row = 0, column = 1, padx = 30,pady =10)
    hauteur.grid(row = 1, column = 0, padx = 30, pady =10) 
    ent_hauteur.grid(row = 1, column = 1, padx = 30, pady =10)
    button.grid(row = 2, column = 2, padx = 30, pady =10)
    button2.grid(row = 1, column = 2, padx = 30, pady =10)

def get_ent_button_level_2(name_file,l,h,frame_level_2):
    """ Cette fonction permet d'enrengistrer les valeurs entrée par l'usager de la taille de l'interface graphique.

        Elle est appelée par la fonction suivante: adjust_windows (bouton (terminer) de la fenêtre)

        paramètre:
            name_file : path du fichier json de la taille de l'interface
            l     : longueur entrée par l'usager
            h     : hauteur entrée par l'usager
            frame_level_2: l'objet la fenêtre (pour la détruire automatiquement)
    """
    if DEBUG_MODE == True:
        print("La fonction get_ent_button_level_2 a été appelée")

    with open(name_file, "r") as f:
        data_2 = json.load(f)
    data_2['windows_width'] = int(l.get())
    data_2['windows_length'] = int(h.get())

    with open(name_file, 'w') as file:
        json.dump(data_2, file, indent = 6)  

    frame_level_2.destroy()

def get_ent_button2_level_2(l,h,x,y):
    """ Cette fonction permet de remettre les valeurs par défaut de la taille de l'interface graphique.

        Elle est appelée par la fonction suivante: adjust_windows (bouton (remettre les paramètres par défaut) de la fenêtre))

        paramètre:
            l : longueur entrée par l'usager
            h : hauteur entrée par l'usager
            x : longueur par défaut
            y : hauteur par défaut
    """
    if DEBUG_MODE == True:
        print("La fonction get_ent_button2_level_2 a été appelée")
    l.delete(0,END)
    h.delete(0,END)
    l.insert(0,x)
    h.insert(0,y)
    
def ajust_height_scorlbar(name_file,y_def):
    """ Cette fonction créer une fenêtre permettant à l'usager de modifier la longueur du scrollbar

        Elle est appelé par le bouton de l'interface suivant: longueur du scrollbar

        paramètre: 
            name_file : path vers le fichier de la taille de l'interface
            y_def     : longueur du scrollbar par défaut
    """
    if DEBUG_MODE == True:
        print("La fonction get_ent_button_level_2 a été appelée")
    with open(name_file, "r") as f:
        data_2 = json.load(f)
    the_frame_level_2 = Toplevel(the_frame, padx=125, pady=130)    
    scrol_height = Label(the_frame_level_2,text='entrez la largeur',fg="white",bg="blue") #Select title
    ent_scrol = Entry(the_frame_level_2, width=20)
    ent_scrol.insert(0,data_2['windows_scrol_height'])
    button = Button(the_frame_level_2, text="terminer", command=lambda : get_scrol_ent_button_level_2(name_file, ent_scrol, the_frame_level_2))
    button2 = Button(the_frame_level_2, text="remettre les paramètres par défaut", command=lambda : get_scrol_ent_button2_level_2(ent_scrol, y_def))

    scrol_height.grid(row = 0, column = 0, padx = 30, pady =10)
    ent_scrol.grid(row = 0, column = 1, padx = 30,pady =10)
    button.grid(row = 1, column = 2, padx = 30, pady =10)
    button2.grid(row = 0, column = 2, padx = 30, pady =10)

def get_scrol_ent_button_level_2(name_file,h,frame_level_2):
    """ Cette fonction permet d'enrengistrer les valeurs entrée par l'usager de la longueur du scrollbar.

        Elle est appelée par la fonction suivante: ajust_height_scorlbar (bouton (terminer) de la fenêtre)

        paramètre:
            name_file : path du fichier json de la taille de l'interface
            h     : hauteur du scrollbar entrée par l'usager
            frame_level_2: l'objet la fenêtre (pour la détruire automatiquement)
    """
    if DEBUG_MODE == True:
        print("La fonction get_scrol_ent_button_level_2 a été appelée")
    with open(name_file, "r") as f:
        data_2 = json.load(f)
    data_2['windows_scrol_height'] = int(h.get())

    with open(name_file, 'w') as file:
        json.dump(data_2, file, indent = 6)  

    frame_level_2.destroy()

def get_scrol_ent_button2_level_2(h,y):
    """ Cette fonction permet de remettre la valeur par défaut de la longueur du scrollbar.

        Elle est appelée par la fonction suivante: ajust_height_scorlbar (bouton (remettre les paramètres par défaut) de la fenêtre))

        paramètre:
            h : longueur du scrollbar entrée par l'usager
            y : longueur du scrollbar par défaut
    """
    if DEBUG_MODE == True:
        print("La fonction get_scrol_ent_button2_level_2 a été appelée")
    h.delete(0,END)
    h.insert(0,y)

def find_sensors(adress_can_data):
    """ Cette fonction permet de retrouver les capteurs associés adresses du fichier csv CAN.csv reçu par le système d'acquisition

        Elle est appelée par la fonction : convert_all_data

        paramètre:
            adress_can_data: liste de toutes les adresses suivit d'un _ et des octets et bits des messages

        return: list d'un tuple comprenant quatre éléments
                 (l'adresse, les octets et bits du message, la fonction associée, le capteur associé, le numéro du capteur uniquement avec C devant)
    """
    if DEBUG_MODE == True:
        print("La fonction find_sensors a été appelée")

    list_of_sensor_by_column = []

    all_fonc_and_sens = get_all_capt()

    with open(dico_file_name["path_to_file"], "r") as f:
        data = json.load(f)

    for adress in adress_can_data:
        separate = adress.split("_")
        can_adress = separate[0]
        can_data = (separate[1],"D")


        if len(separate) == 3:
            can_data = separate[len(separate)-2:len(separate)]
            can_data = ("%s-%s"%(can_data[0],can_data[1]),"A")

        for sensor in all_fonc_and_sens:
            parse_string_for_eval = sensor[1].split(' ')
            the_adress = data[sensor[0]][sensor[1]]["can_adress"]
            the_adress = the_adress[0:len(the_adress)-2] + "fd"

            the_can_data_bit = data[sensor[0]][sensor[1]]["can_data"]
            if type(the_can_data_bit) == list:
                the_can_data_bit = "%s-%s"%(the_can_data_bit[0],the_can_data_bit[1])

            if (can_adress == the_adress) and (can_data[0] == the_can_data_bit):
                list_of_sensor_by_column.append((can_adress,can_data,sensor[0],sensor[1],"C"+parse_string_for_eval[1]))
    
    if DEBUG_MODE == True:
        print("listes des capteurs trouvées à partir des données CAN reçu : ",list_of_sensor_by_column)
    return list_of_sensor_by_column

def convert_all_data():
    """ Cette fonction permet d'importer les données du fichier CAN.csv dans l'interface
        Elle permet de faire des traitements pour reconvertir les données reçus selon les valeurs entrées dans l'interface graphique par l'usager
        
        Elle est appelée par le bouton de l'interface suivant: Importer le can

        Elle crée un fichier csv appelé z_(nom du fichier json)_can_converti.csv comprennant les données CAN reçus reconverties
    """
    if DEBUG_MODE == True:
        print("La fonction convert_all_data a été appelée")

    get_all_entry()

    name_file_without_extention = dico_file_name["filename"].split(".json")

    export_data_converted = dico_file_name["path_to_folder"] + '\\' + "z_" + name_file_without_extention[0] +'_can_converti.csv'

    filetypes = (('text files', '*.csv'),('All files', '*.*'))
    data_csv = fd.askopenfilename(title='Sélectionner les données CAN',initialdir=dico_file_name["Path_to_machine_folder"] + "\\donnees_recoltees_machine",filetypes=filetypes)
    list_str = data_csv.split("/")
    only_name = list_str[len(list_str)-1]

    if data_csv != "":
    
        with open(data_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
        
        try:
            assert header[0] == "Time", \
                "La première colonne attendu devrait être la colonne du temps"
        
        except AssertionError:
            error_import_can.append("La première colonne attendu devrait être la colonne du temps")
            dico_all_error_message["import_can"] = error_import_can
            if DEBUG_MODE == True:
                print(dico_all_error_message["import_can"])
            fenetre_erreur(dico_all_error_message["import_can"],"import_can")
            return None

        header_without_time = header[1:len(header)]

        try:
            my_data = genfromtxt(data_csv, delimiter=',', names=True, usecols=tuple(header_without_time), unpack=True)
            if type(my_data[0]) != ndarray:
                my_data = [array(my_data)]
        except ValueError as e:
            error_import_can.append("erreur dans le fichier CAN: %s"%(e))
            dico_all_error_message["import_can"] = error_import_can
            if DEBUG_MODE == True:
                print(dico_all_error_message["import_can"])
            fenetre_erreur(dico_all_error_message["import_can"],"import_can")
            return None
        associate_with_sensor_list = find_sensors(header_without_time)
    

        with open(dico_file_name["path_to_file"], "r") as f:
            data = json.load(f)
            
        dic = {}
        all_formul_list = []
        for i in range(len(header_without_time)):
            try:
                dic[associate_with_sensor_list[i][4]] = my_data[i]
            except IndexError:
                error_import_can.append("Le nombre de capteurs provenant du fichier CAN.csv et celui sur l'interface ne correspondent pas")
                dico_all_error_message["import_can"] = error_import_can
                break


            convert_bit_to_value = None
            if associate_with_sensor_list[i][1][1] == "A":
                find_bytes = associate_with_sensor_list[i][1][0]
                nb_bytes = find_bytes.split('-')
                nb_bytes = (int(nb_bytes[1]) - int(nb_bytes[0]))+1
                nb_bit = 255**nb_bytes
                analog_range = data[associate_with_sensor_list[i][2]][associate_with_sensor_list[i][3]]["range_type"]

                if analog_range == "0 a 100%":
                    max_value = data[associate_with_sensor_list[i][2]][associate_with_sensor_list[i][3]]["value_of_100"]
                    if max_value.find(',') !=-1:
                        convert_comma_to_dot = max_value.split(',')
                        max_value = convert_comma_to_dot[0]+'.'+convert_comma_to_dot[1]
                    all_formul_list.append("(%s/%s)*%s"%(max_value,nb_bit,list(dic.keys())[i]))

                elif analog_range == "-100 a 100%":
                    max_value = data[associate_with_sensor_list[i][2]][associate_with_sensor_list[i][3]]["value_of_100"]
                    if max_value.find(',') !=-1:
                        convert_comma_to_dot = max_value.split(',')
                        max_value = convert_comma_to_dot[0]+'.'+convert_comma_to_dot[1]
                    convert_bit_to_value = "((%s - %s)/%s)*%s"%(list(dic.keys())[i],nb_bit/2,nb_bit/2,max_value)
                    all_formul_list.append(convert_bit_to_value)
                elif analog_range == "direct":
                    max_value = data[associate_with_sensor_list[i][2]][associate_with_sensor_list[i][3]]["value_of_100"]
                    convert_bit_to_value = list(dic.keys())[i]
                    all_formul_list.append(convert_bit_to_value)

            elif associate_with_sensor_list[i][1][1] == "D":
                max_value = data[associate_with_sensor_list[i][2]][associate_with_sensor_list[i][3]]["value_of_100"]
                if max_value.find(',') !=-1:
                        convert_comma_to_dot = max_value.split(',')
                        max_value = convert_comma_to_dot[0]+'.'+convert_comma_to_dot[1]
                all_formul_list.append("%s*%s"%(max_value,list(dic.keys())[i]))

        list_of_all_array = []
        nb_line = []
        if DEBUG_MODE == True:
            print("les formules : ",all_formul_list)
        for formul in all_formul_list:
            list_of_all_array.append(eval(formul,dic))
            nb_line.append(len(list_of_all_array[0]))
        if DEBUG_MODE == True:
            print("vecteur des nombre de ligne par colonne : ", nb_line)
            
        try:
            nb_line_by_column = nb_line[0]
            same_number_of_value = nb_line.count(nb_line_by_column)
            try:
                assert same_number_of_value == len(nb_line), \
                    "Les vecteurs colonnes représentant les donnees dans le temps doivent avoir le même nombre de donnees. Or, un ou plusieurs capteurs ont un nombre de donnees different des autres"
            except AssertionError:
                error_import_can.append("Les vecteurs colonnes représentant les donnees dans le temps doivent avoir le même nombre de donnees. Or, un ou plusieurs capteurs ont un nombre de donnees different des autres")
                dico_all_error_message["import_can"] = error_import_can
                fenetre_erreur(dico_all_error_message["import_can"],"import_can")
        
        except IndexError:
            error_import_can.append("Il y a un problème avec le fichier de donnée CAN. Il possède peut-être 1 seule colonne alors qu'au moins 2 sont attendue(temps et données)")
            dico_all_error_message["import_can"] = error_import_can
        
        
            
        if dico_all_error_message["import_can"] != []:
            fenetre_erreur(dico_all_error_message["import_can"],"import_can")
            return None

        validate_all_entry()
        if dico_all_error_message["invalide_entry"] != []:
            fenetre_erreur(dico_all_error_message["invalide_entry"],"invalide_entry")
            return None
        
        nb_column = len(nb_line)

        adresse_sorted_complete = []
        for ad_and_sens in associate_with_sensor_list :
            adresse_sorted_complete.append((ad_and_sens[0],ad_and_sens[4]))

        number_of_line_in_csv = len(list_of_all_array[0])

        list_time = []
        with open(data_csv, newline='') as csvfile:
            for each_row in csvfile:
                data_from_colum_0 = each_row.split(',')[0]
                list_time.append(data_from_colum_0)
                only_time = list_time[1:len(list_time)]

        dictionnary_of_all_lines_in_csv_file = {}
        for i in range(number_of_line_in_csv):
            all_column_value = []
            all_column_value.append(str(only_time[i]))
            
            for j in range(nb_column):
                all_column_value.append(str(list_of_all_array[j][i]))
            dictionnary_of_all_lines_in_csv_file["ligne %s"%(i+1)] = all_column_value
        

        

        with open(export_data_converted, 'w', newline='') as csvfile:
            sensor_list  = ["Time"]
            for sensor_only in adresse_sorted_complete:
                sensor_list.append(sensor_only[1])
            fieldnames = sensor_list
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            dico_with_all_can_data_converted = {}
            for i in range(nb_line[0]):
                for j in range(len(adresse_sorted_complete)+1):
                    dico_with_all_can_data_converted[sensor_list[j]] = dictionnary_of_all_lines_in_csv_file["ligne %s"%(i+1)][j]

                writer.writerow(dico_with_all_can_data_converted)

        list_indication = ["CAN importé","Enregistrement effectué sans problème dans : %s"%("z_" + name_file_without_extention[0] +'_can_converti.csv')]
        dico_all_error_message["indication"] =list_indication
            
        fenetre_erreur(dico_all_error_message["indication"],"indication", is_indication=True)

        print("Enregistrement effectué sans problème dans : %s"%("z_" + name_file_without_extention[0] +'_can_converti.csv'))
    else:
        print("action annulée")

def validate_all_entry():
    """
    Cette fonction vérifie que:
        1) Il y a quelque chose d'écris dans chaque entrées entrées manuel de l'interface

        2) Aucun menu déroulant n'a été oublié

        3) Les adresses entrées sont du bon format

        4) le nombre de fonction dans l'interface et celui calculer dans le fichier correspond

        5) les nombres de capteurs par fonction dans l'interface et ceux calculer dans le fichier correspondent

    Lorsqu'il y a des erreur, les messages d'erreur sont enregistrés sous forme de list (invalide_entry) dans le dictionaire (dico_all_error_message) sous la clés ("invalide_entry")
    
    Elle est appelée par les fonctions suivantes:
                                                 - convert_all_data
                                                 - open_power_cycle_math
    """
    if DEBUG_MODE == True:
        print("La fonction validate_all_entry a été appelée")

    with open(dico_file_name["path_to_file"], "r") as f:
        data = json.load(f)
    all_fonc_and_capt = get_all_capt()
#   Cette partie sert au numéro 5) 
    get_fonc = get_all_function()
    nb_capt_by_fonc = {}
    count_capt_by_fonc = 0
#
    for capt in all_fonc_and_capt:
        fonc_desc = capt[0].split(" ")
        fonc_num = fonc_desc[1]
        capt_num = capt[1].split(" ")
        list_all_func_until_now = list(nb_capt_by_fonc.keys())
        if str(fonc_num) not in list_all_func_until_now:
            count_capt_by_fonc = 0
            nb_capt_by_fonc[str(fonc_num)] = count_capt_by_fonc
        count_capt_by_fonc += 1
        nb_capt_by_fonc[str(fonc_num)] = count_capt_by_fonc
        all_info = data[capt[0]][capt[1]]
        if data[capt[0]]["funcs_description"+"_%s"%(fonc_num)] == "(description)":
            invalide_entry.append("Aucune description entrée pour la fonction %s"%(fonc_num))
        if all_info["capts_description"] == "(description)":
            invalide_entry.append("Aucune description entrée pour le capteur %s"%(capt_num[1]))
        if all_info["can_adress"] == "adresse CAN":
            invalide_entry.append("Aucune adresse CAN n'a été entrée pour le capteur %s"%(capt_num[1]))
# Cette partie sert au numéro 3)
        else:
            adress = all_info["can_adress"]
            if len(adress) != 10:
                invalide_entry.append("Les adresses doivent être de 10 caratères et pas de %s, (capteur %s)"%(len(adress),capt_num[1]))
            if adress[0:2] != "0x":
                invalide_entry.append("Les adresses doivent commencées par 0x et pas par %s, (capteur %s)"%(adress[0:2],capt_num[1]))
            if (adress[8:10] != "fd") and (adress[8:10] != "Fd") and (adress[8:10] != "fD") and (adress[8:10] != "FD"):
                invalide_entry.append("Les adresses doivent terminées par [fd, Fd, fD, FD] et pas par %s, (capteur %s)"%(adress[8:10],capt_num[1]))
            if adress[2:8].isnumeric() == False:
                invalide_entry.append("Les adresses doivent êtres composées de 6 digits. L'adresse %s est invalide, (capteur %s)"%(adress[2:8],capt_num[1]))
#
        if all_info["type_channel"] == None:
            invalide_entry.append("Aucun type de channel sélectionné pour le capteur %s"%(capt_num[1]))
        elif all_info["type_channel"] == "Digital":
            if (all_info["can_data"] == None) or (len(all_info["can_data"]) != 3):
                invalide_entry.append("l'octets ou le bit associés aux messages du capteur %s n'a pas été entrée"%(capt_num[1]))
        elif all_info["type_channel"] == "Analogique":
            for i in range(2):
                if (all_info["can_data"][i] == None):
                    invalide_entry.append("le premier octet ou le dernier octet des messages du capteur %s n'a pas été entrée"%(capt_num[1]))
            if all_info["range_type"] == "analog":
                invalide_entry.append("le range du capteur %s n'a pas été entrée"%(capt_num[1]))

        if all_info["value_of_100"] == "valeur de 100%":
            invalide_entry.append("Aucune valeur de 100% n'a été entrée pour le capteur {}".format(capt_num[1]))
        
# Cette partie sert au numéro 4)     
    if len(get_fonc) != data["config_nb_func"]:
        invalide_entry.append("Les nombres de fonction enregistré dans le fichier et détecté ne correspondent pas")
# Cette partie sert au numéro 5)
    nb_capt_by_all_fonc = list(nb_capt_by_fonc.keys())
    for num_fonc in nb_capt_by_all_fonc:
        if data["function "+num_fonc]["config_nb_sens"] != nb_capt_by_fonc[num_fonc]: 
            invalide_entry.append("Les nombres de capteur enregistré dans le fichier et détecté ne correspondent pas pour la fonction %s"%(num_fonc))
    
    dico_all_error_message["invalide_entry"]:invalide_entry


def open_power_cycle_math():
    """ Cette fonction affiche les erreurs et s'il n'y a aucune erreur, ouvre la deuxième partie de l'interface graphique

        Elle est appelée par le bouton de l'interface graphique suivant: Ouvrir la fenêtre des cycles de puissance 
    """

    if DEBUG_MODE == True:
        print("La fonction open_power_cycle_math a été appelée")

    get_all_entry()

    no_error = True

    if dico_all_error_message["for_rpi"] != []:
        fenetre_erreur(dico_all_error_message["for_rpi"],"for_rpi")
        no_error =False
    if dico_all_error_message["import_can"] != []:
        fenetre_erreur(dico_all_error_message["import_can"],"import_can")
        no_error = False
    if dico_all_error_message["assertions_partie_1"] != []:
        fenetre_erreur(dico_all_error_message["assertions_partie_1"],"assertions_partie_1")
        no_error = False
  
    validate_all_entry()
    if dico_all_error_message["invalide_entry"] != []:
        fenetre_erreur(dico_all_error_message["invalide_entry"],"invalide_entry")
        no_error = False
    

    if no_error == True:
        interface_2.interface_part_2(dico_file_name["filename"],the_frame)
    else:
        print("La deuxième interface ne s'ouvrira pas avant que tous les bogs n'ait été résolu")

def end_error_message(win,list):
    """ Cette fonction supprime les erreurs et ferme la fenêtre d'erreurs

        Elle est appelée par le bouton terminer de la fenetre d'erreur, fonction fenetre_erreur

        paramètre:
            win: objet de la fenêtre d'erreur
            list: liste de toutes les erreurs
    """

    if DEBUG_MODE == True:
        print("La fonction end_error_message a été appelée")

    dico_all_error_message[list].clear()
    win.destroy()

def fenetre_erreur(message_error_list,list,is_indication=False):
    """ Cette fonction permet de créer la fenetre d'erreur et la zone de texte et affiche chacune des erreurs sur une ligne

        Elle est appelée par les fonction suivante:
                                                   - export_data_for_rpi (x2) 
                                                   - convert_all_data (x6)
                                                   - open_power_cycle_math (x4)
    """

    if DEBUG_MODE == True:
        print("La fonction fenetre_erreur a été appelée")
    
    with open(dico_file_name["taille_interface_file"], "r") as f:
        data_2 = json.load(f)
    
    the_frame_level_2 = Toplevel(the_frame, height=data_2["windows_length"], width=data_2["windows_width"])   
    text_box = Text(the_frame_level_2,height=int(data_2["windows_length"]/22), width=int(data_2["windows_width"]/12))
    text_box.place(x=0, y=0)
    
    if is_indication == False:
        text_box.insert(END, "Attention les erreurs suivantes sont survenues:")
        text_box.insert(END,"\n")
        text_box.insert(END,"\n")
    for message in message_error_list:
        text_box.insert(END, message)
        text_box.insert(END,"\n")
        text_box.insert(END,"\n")  
    button = Button(the_frame_level_2, text="terminer", command=lambda : end_error_message(the_frame_level_2,list))

    button.place(x=int((data_2["windows_width"]+data_2["windows_width"]/2)/2),y=0)

def end_script():
    """ Cette fonction permet de fermer l'interface graphique

        Elle est appelée par les boutons de l'interface graphique suivant: - Fermer
                                                                           - Le x rouge de l'interface
    """
    if DEBUG_MODE == True:
        print("La fonction end_script a été appelée")
    get_all_entry()
    exit()
    
today = datetime.datetime.now()
today_format = today.strftime("%b_%d_%Y")
if DEBUG_MODE == True:
    print(today_format)
file_name = "default_config_interface_" + today_format + ".json"
namefile = find_the_config_file_path(file_name)
dico_file_name["filename"] = file_name
dico_file_name["path_to_file"] = namefile[0]
dico_file_name["taille_interface_file"] = namefile[1]
dico_file_name["path_to_folder"] = namefile[2]
dico_file_name["path_to_parent_folder"] = namefile[3]
dico_file_name["Path_to_machine_folder"] = namefile[4]
dico_file_name["Path_to_interface_folder"] = namefile[5]
if DEBUG_MODE == True:
    print(" ")
    print(dico_file_name["filename"])
    print(" ")
    print(dico_file_name["path_to_file"])
    print(" ")
    print(dico_file_name["taille_interface_file"])
    print(" ")
    print(dico_file_name["path_to_folder"])
    print(" ")
    print(dico_file_name["path_to_parent_folder"])
    print(" ")
    print(dico_file_name["Path_to_machine_folder"])
    print(" ")
    print(dico_file_name["Path_to_interface_folder"])
    print(" ")

if DEBUG_MODE == True:
    print("Mode DEGBUG activé")

try:
    with open(dico_file_name["path_to_file"], 'r') as f:
        data = json.load(f)
        dico = {'config_nb_func' : init_nb_func,
                'config_y_place_func': init_config_y_func,
                'config_x_place_func': init_config_x_func,
                'config_y_place_sens': init_config_y_sens,
                'config_x_place_sens': init_config_x_sens
                

        }
    with open(dico_file_name["path_to_file"], 'w') as file:
        json.dump(dico, file, indent = 6)

except json.JSONDecodeError:
    print("fichier vide, introuvable ou corrompu!")
    print("Création d'un nouveau fichier appelé : %s"%(dico_file_name["filename"]))
    dico = {'config_nb_func' : init_nb_func,
                'config_y_place_func': init_config_y_func,
                'config_x_place_func': init_config_x_func,
                'config_y_place_sens': init_config_y_sens,
                'config_x_place_sens': init_config_x_sens

        }
    with open(dico_file_name["path_to_file"], 'w') as file:
        json.dump(dico, file, indent = 6)

except FileNotFoundError:
    print("fichier vide ou introuvable!")
    print("Création d'un nouveau fichier appelé : %s"%(dico_file_name["filename"]))
    dico = {'config_nb_func' : init_nb_func,
                'config_y_place_func': init_config_y_func,
                'config_x_place_func': init_config_x_func,
                'config_y_place_sens': init_config_y_sens,
                'config_x_place_sens': init_config_x_sens

        }
    with open(dico_file_name["path_to_file"], 'w') as file:
        json.dump(dico, file, indent = 6)


try:
    with open(namefile[1], 'r') as f:
        pass

except json.JSONDecodeError:
    dico_2 = {'windows_width': windows_height_x,
                  'windows_length': windows_height_y,
                  'windows_scrol_height': windows_height_y,}

    with open(namefile[1], 'w') as file:
        json.dump(dico_2, file, indent = 6)

except FileNotFoundError:
    dico_2 = {'windows_width': windows_height_x,
                  'windows_length': windows_height_y,
                  'windows_scrol_height': windows_scrol_height}

    with open(namefile[1], 'w') as file:
        json.dump(dico_2, file, indent = 6)


tk = Tk()
tk.title("Python Tkinter")
with open(namefile[1], 'r') as f:
    data_2 = json.load(f)
tk.minsize(data_2['windows_width'],data_2['windows_length'])
scrollbar_set = True

the_frame = tk

if scrollbar_set == True:
    largeur = windows_height_x
    hauteur = windows_height_y
    main_frame = Frame(tk)
    main_frame.place(x=0, y=0, width=largeur, height=hauteur)

    main_canvas = Canvas(main_frame, width=largeur, height=hauteur)
    main_canvas.place(x=0, y=0, width=largeur, height=hauteur)

    scroll_v = Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
    dico_scrollbar["vertical"] = scroll_v
    dico_scrollbar["vertical"].pack(side= RIGHT,fill=Y)

    main_canvas.configure(yscrollcommand=dico_scrollbar["vertical"].set)
    main_canvas.bind("<Configure>",lambda e: main_canvas.configure(scrollregion= main_canvas.bbox("all")))

    second_frame = Frame(main_canvas, width=largeur, height=hauteur)
    main_canvas.create_window((0,0), window=second_frame, anchor="nw")
    with open(namefile[1], 'r') as f:
        data_2 = json.load(f)
        second_frame.configure(height=data_2['windows_scrol_height'])

    the_frame = second_frame

selection_bar = Menu(tk)
filemenu = Menu(selection_bar, tearoff=0)
selection_bar.add_cascade(label="Fichier", menu=filemenu)
filemenu.add_command(label="Nouvelle fonction", command=add_function)
filemenu.add_command(label="Ouvrir...", command=select_file)
#filemenu.add_command(label="Enregistrer", command=get_all_entry)
filemenu.add_command(label="Enregistrer sous...", command=save_in_to_file)
filemenu.add_separator()
filemenu.add_command(label="Nouvelle machine", command=add_machine)
filemenu.add_separator()
#filemenu.add_command(label="print dico", command=donothing)
filemenu.add_command(label="Fermer", command=end_script)

filemenu2 = Menu(selection_bar, tearoff=0)
selection_bar.add_cascade(label="dimentions", menu=filemenu2)
filemenu2.add_command(label="taille de la fenêtre", command= lambda : adjust_windows(namefile[1], windows_height_x,windows_height_y))
filemenu2.add_command(label="longueur du scrollbar", command= lambda : ajust_height_scorlbar(namefile[1], windows_scrol_height))

filemenu3 = Menu(selection_bar, tearoff=0)
selection_bar.add_cascade(label="donnees", menu=filemenu3)
filemenu3.add_command(label="Exportation pour RPI", command=export_data_for_rpi)
filemenu3.add_separator()
filemenu3.add_command(label="Importer le can", command=convert_all_data)
filemenu3.add_separator()
filemenu3.add_command(label="Ouvrir la fenêtre des cycles de puissance", command=open_power_cycle_math)


tk.config(menu=selection_bar)
tk.protocol("WM_DELETE_WINDOW", end_script)
tk.mainloop()