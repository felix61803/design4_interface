from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import json
import csv
import datetime
from unicodedata import name
from win32api import GetSystemMetrics
from numpy import genfromtxt
from numpy import array
from numpy import ndarray
import os
import traitement_graphique as interface_3

def interface_part_2(json_name_file,win_1):

    space_next_sous_cycle = 60
    #space_next_sens = 30
    init_nb_sous_cycle = 0
    init_config_y_sous_cycle = 60
    init_config_x_sous_cycle = [40, 120, 400, 530, 1050]
    #init_config_y_sens = 60
    #init_config_x_sens = [120, 200, 330, 430, 510, 645, 745, 810, 800, 910, 1040, 1170]

    dico_all_path = {"part_1_json_name": json_name_file, "name_of_the_interface_2_file": None, "path_to_json_interface_part_1":None, "path_to_json_calculs":None, "path_to_taille_interface_2":None, "path_to_converted_data_interface_Part_1":None, "path_to_converted_sous_cycle_puissance":None, "path_to_folder":None}

    dico_funcs = {}
    dico_sous_cycle_description = {}
    dico_math_entry_label = {}
    dico_math_entry = {}
    dico_button_math_validate = {}
    dico_scrollbar = {}
    dico_warning_line = {}
    dico_validate_calcul_windows = {}
    list_assertion = []
    list_error_calculer = []
    invalide_entry = []
    list_indication = []
    dico_all_error_message = {"assertions_partie_2":list_assertion,"calculer":list_error_calculer, "invalide_entry":invalide_entry,"indication":list_indication}

    def find_the_config_file_path(date):

        path_script = __file__
        to_list = path_script.split('\\')
        list_folder_minus_2_path = to_list[0:len(to_list)-2]
        path_json = "\\".join(list_folder_minus_2_path) + "\\1) setup_donnees\\fichiers_enregistrements\\" + json_name_file

        only_name = json_name_file.split(".json")
        dico_all_path["name_of_the_interface_2_file"] = "default_%s"%(only_name[0]+"_calcul_puissance_" + date)
        path_csv_converted = "\\".join(list_folder_minus_2_path) + "\\1) setup_donnees\\fichiers_enregistrements\\z_%s_can_converti.csv"%(only_name[0])

        path_file = '\\'.join(list_folder_minus_2_path) + "\\2) calcul_puissance" + "\\fichiers_enregistrements\\default_%s"%(only_name[0]+"_calcul_puissance_" + date)

        path_file_taille_interface_2 = '\\'.join(list_folder_minus_2_path) + "\\2) calcul_puissance" + "\\fichiers_enregistrements\\%s"%("z_taille_interface_2.json")

        converted_power_file = '\\'.join(list_folder_minus_2_path) + "\\2) calcul_puissance" + "\\fichiers_enregistrements\\z_%s_calcul_sous_cycle_puissance.csv"%(only_name[0])

        path_to_folder = '\\'.join(list_folder_minus_2_path) + "\\2) calcul_puissance" + "\\fichiers_enregistrements\\"

        return path_json, path_file, path_file_taille_interface_2, path_csv_converted, converted_power_file, path_to_folder

    def get_all_sous_cycle_from_file():

        with open(dico_all_path["path_to_json_calculs"], "r") as f:
            data = json.load(f)

        all_keys = list(data.keys())
        list_all_sous_cycle = []
        for key in all_keys:
            if "sous_cycle" in key:
                list_all_sous_cycle.append(key)
        return list_all_sous_cycle

#    def create_tkinter_widjet():
#        with open(dico_all_path["path_to_json_calculs"], "r") as f:
#            data = json.load(f)
#        print("arriver dans la fonction create_tkinter_widjet")
#        count_all_sens = 1
#        for i in range(len(dico_funcs)):
#            dico_funcs["Fonction %s"%(i+1)].place(x = data["config_x_place_sc"][0], y = data["config_y_place_sc"])
#            dico_sous_cycle_description["sous_cycles_descriptions_%s"%(i+1)].place(x = data["config_x_place_sc"][1], y = data["config_y_place_sc"])
#            dico_button_add_capts["button_fct_%s"%(i+1)].place(x=data["config_x_place_sc"][2],y=data["config_y_place_sc"])
#            dico_button_delete_funcs["button_del_fct_%s"%(i+1)].place(x = data["config_x_place_sc"][3] , y = data["config_y_place_sc"])
#            
#            all_sens_only = []
#            for sensors_by_fonc in list(dico_all_sensors["func_%s"%(i+1)].keys()):
#                if "Capteur" in sensors_by_fonc:
#                    all_sens_only.append(sensors_by_fonc)
#            little_count = 1
#            for sensors_by_fonc in all_sens_only:
#                print(sensors_by_fonc)
#                print(dico_all_sensors["func_%s"%(i+1)][sensors_by_fonc])
#                dico_all_sensors["func_%s"%(i+1)][sensors_by_fonc].place(x=data["config_x_place_sens"][0],y=data["config_y_place_sens"]+space_next_sens+5)
#
#                num_sens = sensors_by_fonc.split(' ')
#
#                dico_capts_add_description["capts_description_%s"%(num_sens[1])].place(x=data["config_x_place_sens"][1],y=data["config_y_place_sens"]+space_next_sens+5)
#                
#                dico_all_sensors["func_%s"%(i+1)]["type_channel_sens_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][2], y =data["config_y_place_sens"]+space_next_sens)
#                dico_can_adresse["adress_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][3], y =data["config_y_place_sens"]+space_next_sens+5)
#                if data["function %s"%(i+1)]["sensor %s"%(num_sens[1])]["type_channel"] == "Analogique":
#                    dico_nb_bit_by_bytes_analogique_menu_1["can_data_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][4], y =data["config_y_place_sens"]+space_next_sens)
#
#                    dico_separator["sep_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][4]+67, y =data["config_y_place_sens"]+space_next_sens+3)
#
#                    dico_nb_bit_by_bytes_analogique_menu_2["can_data_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][4] + 80, y =data["config_y_place_sens"]+space_next_sens)
#
#                    dico_analogique_type_range["type_range_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][5], y =data["config_y_place_sens"]+space_next_sens)
#
#                elif data["function %s"%(i+1)]["sensor %s"%(num_sens[1])]["type_channel"] == "Digital":
#                    dico_bit_from_byte_digital["can_data_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][4] + 90, y =data["config_y_place_sens"]+space_next_sens)
#
#                dico_all_sensors["func_%s"%(i+1)]["number_channel_sens_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][6], y =data["config_y_place_sens"]+space_next_sens)
#
#                dico_value_of_100["max_val_%s"%(num_sens[1])].place(x = data["config_x_place_sens"][7], y =data["config_y_place_sens"]+space_next_sens+5)
#
#                dico_math_checkbutton["math_chekbutton_for_capt_%s"%(num_sens[1])][0].place(x = data["config_x_place_sens"][9], y =data["config_y_place_sens"]+space_next_sens+3)
#                print(count_sensors(data))
#                print(dico_math_label)
#
#                if data["function %s"%(i+1)]["sensor %s"%(num_sens[1])]["math"] != None:
#                    dico_math_label["fonc_%s_capt_%s"%(i+1,num_sens[1])].place(x = data["config_x_place_sens"][10], y =data["config_y_place_sens"]+space_next_sens+3)
#                    dico_math_equation["fonc_%s_capt_%s"%(i+1,num_sens[1])].place(x = data["config_x_place_sens"][11], y =data["config_y_place_sens"]+space_next_sens+3)
#
#                data["config_y_place_sens"] += space_next_sens
#                data["config_y_place_sc"] = data["config_y_place_sens"] + space_next_sous_cycle
#                    
#                count_all_sens += 1
#
#                with open(namefile[1], "r") as f:
#                    data_2 = json.load(f)
#                if data["config_y_place_sc"]>= data_2["windows_scrol_height"]:
#                    data_2["windows_scrol_height"] = data["config_y_place_sc"]
#                    print("la scrollbar va jusqu'à : ", data_2["windows_scrol_height"])
#                
#                with open(namefile[1], "w") as file:
#                    json.dump(data_2, file, indent = 6)
#                
#                with open(dico_all_path["path_to_json_calculs"], "w") as file:
#                    json.dump(data, file, indent = 6)
#                little_count += 1
#            data["config_y_place_sens"] = data["config_y_place_sc"]
#            with open(dico_all_path["path_to_json_calculs"], "w") as file:
#                    json.dump(data, file, indent = 6)
#
#        lol = get_all_function()
#        capt = get_all_capt()
#        print("les fonctions", lol)
#        print("les capteurs", capt)
#
#
#
    def add_function():

        with open(dico_all_path["path_to_json_calculs"], "r") as f:
            data = json.load(f)
            print(data)
            data['config_nb_sc'] = data["config_nb_sc"] + 1

        with open(dico_all_path["path_to_json_calculs"], "w") as file:
            json.dump(data, file, indent = 6)
        
        
        create_functions(data["config_nb_sc"],"new")

    #def get_math_entry(event, num_cycle):
    #    print("event : ",event)
    #    with open(dico_all_path["path_to_json_calculs"], "r") as f:
    #        data = json.load(f)
#
    #    mat_equation = dico_math_entry["math_entry_%s"%(num_cycle)].get()
    #    print(mat_equation)
    #    data['sous_cycle %s'%(num_cycle)]["math_entry_%s"%(num_cycle)] = mat_equation
#
    #    with open(dico_all_path["path_to_json_calculs"], "w") as file:
    #        json.dump(data, file, indent = 6)
#
    #def get_desc_entry(event2, num_cycle):
    #    print("yeeep")
    #    print("event : ",event2)
    #    with open(dico_all_path["path_to_json_calculs"], "r") as f:
    #        data = json.load(f)
#
    #    desc = dico_sous_cycle_description["sous_cycles_descriptions_%s"%(num_cycle)].get()
    #    print(desc)
    #    data['sous_cycle %s'%(num_cycle)]["sous_cycles_descriptions_%s"%(num_cycle)] = desc
#
    #    with open(dico_all_path["path_to_json_calculs"], "w") as file:
    #        json.dump(data, file, indent = 6)
##
    def get_all_entry():
        
        get_all_sous_cycle = get_all_sous_cycle_from_file()
        print("entrer dans la fonction enregistrer")

        with open(dico_all_path["path_to_json_calculs"], "r") as f:
            data = json.load(f)

        for sous_cycle in get_all_sous_cycle:
            only_num = sous_cycle.split(' ')
            lol2 = dico_sous_cycle_description["sous_cycles_descriptions_%s"%(only_num[1])].get()
            print(lol2)
            data['sous_cycle %s'%(only_num[1])]["sous_cycles_descriptions_%s"%(only_num[1])]  = dico_sous_cycle_description["sous_cycles_descriptions_%s"%(only_num[1])].get()
            lol = dico_math_entry["math_entry_%s"%(only_num[1])].get()
            print(lol)
            data['sous_cycle %s'%(only_num[1])]["math_entry_%s"%(only_num[1])] = dico_math_entry["math_entry_%s"%(only_num[1])].get()

            with open(dico_all_path["path_to_json_calculs"], "w") as file:
                json.dump(data, file, indent = 6)
#        list_all_func = get_all_function()
#        list_all_sens = get_all_capt()
#        print("entrer dans la fonction enregistrer")
#
#        with open(dico_all_path["path_to_json_calculs"], "r") as f:
#            data = json.load(f)
#        
#        for fct in list_all_func:
#            number = fct.split(' ')
#            desc = dico_sous_cycle_description["sous_cycles_descriptions_%s"%(number[1])].get()
#            data[fct]["sous_cycles_descriptions_%s"%(number[1])] = desc
#
#            print(data[fct]["sous_cycles_descriptions_%s"%(number[1])])
#
#        for fct_and_capt in list_all_sens:
#            number_fct = fct_and_capt[0].split(' ')
#            number_capt = fct_and_capt[1].split(' ')
#            desc_capt = dico_capts_add_description["capts_description_%s"%(number_capt[1])].get()
#            data[fct_and_capt[0]][fct_and_capt[1]]["capts_description"] = desc_capt
#
#            print(data[fct_and_capt[0]][fct_and_capt[1]]["capts_description"])
#
#            
#            data[fct_and_capt[0]][fct_and_capt[1]]["can_adress"] = dico_can_adresse["adress_%s"%(number_capt[1])].get()
#
#            data[fct_and_capt[0]][fct_and_capt[1]]["value_of_100"] = dico_value_of_100["max_val_%s"%(number_capt[1])].get()
#
#            if dico_math_checkbutton["math_chekbutton_for_capt_%s"%(number_capt[1])][1].get() == 1:
#                data[fct_and_capt[0]][fct_and_capt[1]]["math"] = dico_math_equation["fonc_%s_capt_%s"%(number_fct[1],number_capt[1])].get()
#                if dico_math_equation["fonc_%s_capt_%s"%(number_fct[1],number_capt[1])].get() == '':
#                    data[fct_and_capt[0]][fct_and_capt[1]]["math"] = 'yes'
#            if dico_math_checkbutton["math_chekbutton_for_capt_%s"%(number_capt[1])][1].get() == 0:
#                data[fct_and_capt[0]][fct_and_capt[1]]["math"] = None
#            
#            print(data[fct_and_capt[0]][fct_and_capt[1]]["math"])
#            with open(dico_all_path["path_to_json_calculs"], "w") as file:
#                json.dump(data, file, indent = 6)
    
    def function_from_file():

        get_all_sous_cycle = get_all_sous_cycle_from_file()
        
        dico_funcs.clear()
        dico_sous_cycle_description.clear()
        dico_math_entry_label.clear()
        dico_math_entry.clear
        dico_button_math_validate.clear()
#    
#        
#
        with open(dico_all_path["path_to_json_calculs"], "r") as f:
            data = json.load(f)
        
        data['config_y_place_sc'] = init_config_y_sous_cycle
        data['config_x_place_sc'] = init_config_x_sous_cycle

        with open(dico_all_path["path_to_json_calculs"], 'w') as file:
            json.dump(data, file, indent = 6)


        for sc in get_all_sous_cycle:
            number = sc.split(" ")
            #print('all fonctions : fonction ',number)
            create_functions(number[1],"open")
#
        try:
            assert len(get_all_sous_cycle) == data["config_nb_sc"], \
                "Les nombres de sous-cycles enregistré dans le fichier et détecté ne correspondent pas"
        except AssertionError:
            list_assertion.append("Les nombres de sous-cycles enregistré dans le fichier et détecté ne correspondent pas")
            dico_all_error_message["assertions_partie_2"] = list_assertion
#
        

#        create_tkinter_widjet()


    def print_data_and_calculate(num,obj_line, win):
        try:
            dico_warning_line["selected_line"].destroy()

        except KeyError:
            pass
        
        try:
            dico_validate_calcul_windows["test_box_validate_calcul"].destroy()

        except KeyError:
            pass

        line = obj_line.get()
        #print("Sous Cycle : %s, affiche ligne : %s"%(num, line))
        (header,column) = get_all_column()
        #print(header)
        #
           
        try:
            list_data_line = []
            dico_calcul = {}
            for sensor in header:
                list_data_line.append(column[sensor][int(line)-1])
                dico_calcul[sensor] = column[sensor][int(line)-1]
            #print(header)
            #print(list_data_line)
           # print("dico : ",dico_calcul )
            with open(dico_all_path["path_to_json_calculs"], "r") as f:
                data = json.load(f)

            #new_frame = Frame(win)
            #new_frame.pack(expand=TRUE, fill = BOTH)
           # new_frame.grid(row = 3, column = 0)

            #scrollx = Scrollbar(win, orient = HORIZONTAL)
            #scrollx.grid(row=4, column=0)
            

            txt = Text(win)
            dico_validate_calcul_windows["test_box_validate_calcul"] = txt 
            txt.grid(row = 3, column = 0, padx = 30,pady =10)

            #scrollx.config(command = txt.xview)

            txt.insert(END, header)
            txt.insert(END,"\n")
            txt.insert(END, list_data_line)
            txt.insert(END,"\n")
            txt.insert(END,"\n")
            txt.insert(END,"Equation :    %s"%(data["sous_cycle %s"%(num)]["math_entry_%s"%(num)]))
            txt.insert(END,"\n")
            txt.insert(END,"\n")
            txt.insert(END,"Resultat :    %s"%(eval(data["sous_cycle %s"%(num)]["math_entry_%s"%(num)],dico_calcul)))
            

            


        except IndexError:
            val = Label(win, text="Attention : le fichier ne comporte que %s lignes"%(len(column[header[0]])))
            dico_warning_line["selected_line"] = val
            dico_warning_line["selected_line"].grid(row = 1, column = 2, padx = 30,pady =10)

            try:
                dico_validate_calcul_windows["test_box_validate_calcul"].destroy()

            except KeyError:
                pass

    def validate_calcul(number):
        print("yolo %s"%(number))

        get_all_entry()

        the_frame_level_2 = Toplevel(the_frame, padx=125, pady=130)
        the_frame_level_2.minsize(width=700,height=400)    
        choose_line = Label(the_frame_level_2,text='choisir une ligne',fg="white",bg="blue") #Select title
        ent = Entry(the_frame_level_2, width=20)
        ent.insert(0,"1")
        button = Button(the_frame_level_2, text="calculer", command=lambda : print_data_and_calculate(number, ent, the_frame_level_2))

        choose_line.grid(row = 0, column = 0, padx = 30, pady =10)
        ent.grid(row = 0, column = 1, padx = 30,pady =10)
        button.grid(row = 0, column = 2, padx = 30, pady =10)


    def create_functions(num_sous_cycle, coming_from):
        
        if coming_from == "new":

            print("La fonction %s à bien été appelée"%(num_sous_cycle))
            with open(dico_all_path["path_to_json_calculs"], "r") as f:
                data = json.load(f)
            print(data)

            name_french = "Sous cycle %s"%(num_sous_cycle)
            name = Label(the_frame,text=name_french,fg="white",bg="blue") #Select title
            dico_funcs[name_french] = name
            print(dico_funcs)
            dico_funcs[name_french].place(x = data["config_x_place_sc"][0], y = data["config_y_place_sc"])

            funcs_add_description = Entry(the_frame, width=40)
            funcs_add_description.insert(0,'(description)')
            dico_sous_cycle_description["sous_cycles_descriptions_%s"%(num_sous_cycle)] = funcs_add_description
            #dico_sous_cycle_description["sous_cycles_descriptions_%s"%(num_sous_cycle)].bind("<Leave>", lambda event2: get_desc_entry(event2, num_sous_cycle))
            dico_sous_cycle_description["sous_cycles_descriptions_%s"%(num_sous_cycle)].place(x=data["config_x_place_sc"][1],y=data["config_y_place_sc"])
#
            desc_math_entry_label = Label(the_frame,text="Entrez l'expression: ",fg="white",bg="blue") #Select title
            dico_math_entry_label["desc_sous_cycle_%s"%(num_sous_cycle)] = desc_math_entry_label
            print(dico_math_entry_label)
            dico_math_entry_label["desc_sous_cycle_%s"%(num_sous_cycle)].place(x = data["config_x_place_sc"][2], y = data["config_y_place_sc"])
#
            math_entry = Entry(the_frame, width=75)
            dico_math_entry["math_entry_%s"%(num_sous_cycle)] = math_entry
            #dico_math_entry["math_entry_%s"%(num_sous_cycle)].bind("<Leave>", lambda event: get_math_entry(event, num_sous_cycle))
            dico_math_entry["math_entry_%s"%(num_sous_cycle)].place(x=data["config_x_place_sc"][3],y=data["config_y_place_sc"])

            button_test_calcul = Button(the_frame, text="Valider", command=lambda : validate_calcul(num_sous_cycle))
            dico_button_math_validate["button_math_validate_%s"%(num_sous_cycle)] = button_test_calcul
            dico_button_math_validate["button_math_validate_%s"%(num_sous_cycle)].place(x=data["config_x_place_sc"][4],y=data["config_y_place_sc"])
#
            #button_add_sensors = Button(the_frame, text="Ajouter un capt (1)", command= lambda : add_sensors(num_sous_cycle,"new"))
            #dico_button_add_capts["button_fct_%s"%(num_sous_cycle)] = button_add_sensors
            #print(dico_button_add_capts)
            #dico_button_add_capts["button_fct_%s"%(num_sous_cycle)].place(x=data["config_x_place_sc"][2],y=data["config_y_place_sc"])
            #print("save_button : ", dico_button_add_capts["button_fct_%s"%(num_sous_cycle)])
            #button_delete_function = Button(the_frame, text="Supprimer la fonc (1)", command= lambda : delete_functions(num_sous_cycle))
            #dico_button_delete_funcs["button_del_fct_%s"%(num_sous_cycle)] = button_delete_function
            #print(dico_button_delete_funcs)
            #dico_button_delete_funcs["button_del_fct_%s"%(num_sous_cycle)].place(x = data["config_x_place_sc"][3] , y = data["config_y_place_sc"])
            data['sous_cycle %s'%(num_sous_cycle)] = {"sous_cycles_descriptions_%s"%(num_sous_cycle): "(description)",
                                                    "math_entry_%s"%(num_sous_cycle): ""}
            data["config_y_place_sc"] += 60
            #data["config_y_place_sens"] += 90
                

            with open(dico_all_path["path_to_json_calculs"], 'w') as file:
                json.dump(data, file, indent = 6)


            #add_sensors(num_sous_cycle, coming_from)

        elif coming_from == "open":
            with open(dico_all_path["path_to_json_calculs"], "r") as f:
                data = json.load(f)
            
            name_french = "Sous cycle %s"%(num_sous_cycle)
            name = Label(the_frame,text=name_french ,fg="white",bg="blue") #Select title
            dico_funcs[name_french] = name
            #print(dico_funcs)
            dico_funcs[name_french].place(x = data["config_x_place_sc"][0], y = data["config_y_place_sc"])

            funcs_add_description = Entry(the_frame, width=40)
            funcs_add_description.insert(0,data["sous_cycle %s"%(num_sous_cycle)]["sous_cycles_descriptions_%s"%(num_sous_cycle)])
            dico_sous_cycle_description["sous_cycles_descriptions_%s"%(num_sous_cycle)] = funcs_add_description
            #dico_sous_cycle_description["sous_cycles_descriptions_%s"%(num_sous_cycle)].bind("<Leave>", lambda event2: get_desc_entry(event2, num_sous_cycle))
            dico_sous_cycle_description["sous_cycles_descriptions_%s"%(num_sous_cycle)].place(x=data["config_x_place_sc"][1],y=data["config_y_place_sc"])

            desc_math_entry_label = Label(the_frame,text="Entrez l'expression: ",fg="white",bg="blue") #Select title
            dico_math_entry_label["desc_sous_cycle_%s"%(num_sous_cycle)] = desc_math_entry_label
            print(dico_math_entry_label)
            dico_math_entry_label["desc_sous_cycle_%s"%(num_sous_cycle)].place(x = data["config_x_place_sc"][2], y = data["config_y_place_sc"])

            math_entry = Entry(the_frame, width=75)
            math_entry.insert(0,data["sous_cycle %s"%(num_sous_cycle)]["math_entry_%s"%(num_sous_cycle)])
            dico_math_entry["math_entry_%s"%(num_sous_cycle)] = math_entry
            #dico_math_entry["math_entry_%s"%(num_sous_cycle)].bind("<Leave>", lambda event: get_math_entry(event, num_sous_cycle))
            dico_math_entry["math_entry_%s"%(num_sous_cycle)].place(x=data["config_x_place_sc"][3],y=data["config_y_place_sc"])

            button_test_calcul = Button(the_frame, text="Valider", command=lambda : validate_calcul(num_sous_cycle))
            dico_button_math_validate["button_math_validate_%s"%(num_sous_cycle)] = button_test_calcul
            dico_button_math_validate["button_math_validate_%s"%(num_sous_cycle)].place(x=data["config_x_place_sc"][4],y=data["config_y_place_sc"])

            data["config_y_place_sc"] += 60

            with open(dico_all_path["path_to_json_calculs"], 'w') as file:
                json.dump(data, file, indent = 6)

    def select_file():

        filetypes = (('text files', '*.json'),('All files', '*.*'))
        print(dico_all_path["path_to_json_calculs"])
        filename = fd.askopenfilename(initialfile=dico_all_path["part_1_json_name"],title='Open a file',initialdir=dico_all_path["path_to_folder"],filetypes=filetypes)
        list_str = filename.split("/")
        only_name = list_str[len(list_str)-1]
        #dico_file_name["filename"] = only_name

        if filename != "":
            pass
        else:
            print("action annulée")
            return None

        get_all_entry()

        today = datetime.datetime.now()
        today_format = today.strftime("%b_%d_%Y")
        interface_part_1_file_name = dico_all_path["part_1_json_name"].split('.json')
        name_default = "default_" + interface_part_1_file_name[0] + "_calcul_puissance_" + today_format + ".json"
        print(name_default == dico_all_path["name_of_the_interface_2_file"])
        
        default_file = None
        if name_default == dico_all_path["name_of_the_interface_2_file"]:
            default_file = dico_all_path["path_to_json_calculs"]
        
        get_all_sous_cycle = get_all_sous_cycle_from_file()
        for sous_cycle in get_all_sous_cycle:
            only_num = sous_cycle.split(' ')
            try:
                dico_funcs["Sous cycle %s"%(only_num[1])].destroy()
                dico_sous_cycle_description["sous_cycles_descriptions_%s"%(only_num[1])].destroy()
                dico_math_entry_label["desc_sous_cycle_%s"%(only_num[1])].destroy()
                dico_math_entry["math_entry_%s"%(only_num[1])].destroy()
                dico_button_math_validate["button_math_validate_%s"%(only_num[1])].destroy()
            except KeyError:
                break

        dico_funcs.clear()
        dico_sous_cycle_description.clear()
        dico_math_entry_label.clear()
        dico_math_entry.clear()
        dico_button_math_validate.clear()

        dico_all_path["name_of_the_interface_2_file"] = only_name
        dico_all_path["path_to_json_calculs"] = filename
        name = only_name.split(".json")
        dico_all_path["path_to_converted_sous_cycle_puissance"] = dico_all_path["path_to_folder"] + "z_" + name[0] + "_calcul_sous_cycle_puissance.csv"
        
        if default_file != None:
            os.remove(default_file)
        
        function_from_file()

    def save_in_to_file():

        get_all_entry()

        today = datetime.datetime.now()
        today_format = today.strftime("%b_%d_%Y")
        interface_part_1_file_name = dico_all_path["part_1_json_name"].split('.json')
        name_default = "default_" + interface_part_1_file_name[0] + "_calcul_puissance_" + today_format + ".json"
        print(name_default == dico_all_path["name_of_the_interface_2_file"])
        
        default_file = None
        if name_default == dico_all_path["name_of_the_interface_2_file"]:
            default_file = dico_all_path["path_to_json_calculs"]


        files = [('json', '*.json')]
        file = fd.asksaveasfile(initialfile = dico_all_path["part_1_json_name"],initialdir=dico_all_path["path_to_folder"],filetypes = files, defaultextension = files)
        if file != None:
            list_str = file.name.split("/")
            only_name = list_str[len(list_str)-1]
    
        

            with open(dico_all_path["path_to_json_calculs"], "r") as f:
                data = json.load(f)

            dico_all_path["name_of_the_interface_2_file"] = only_name
            dico_all_path["path_to_json_calculs"] = file.name
            name = only_name.split(".json")
            dico_all_path["path_to_converted_sous_cycle_puissance"] = dico_all_path["path_to_folder"] + "z_" + name[0] + "_sous_cycle_puissance.csv"

            with open(dico_all_path["path_to_json_calculs"], 'w') as file:
                json.dump(data, file, indent = 6)

            if default_file != None:
                os.remove(default_file)

        else:
            print("action annulée")


    def adjust_windows(path_of_taille_file,windows_height_x,windows_height_y):

        with open(path_of_taille_file, 'r') as f:
            data_taille = json.load(f)

        print(windows_height_x)
        print(windows_height_y)
        print(data_taille["windows_width"])
        print(data_taille["windows_length"])
        
        the_frame_part_2 = Toplevel(the_frame)    
        the_frame_part_2.minsize(data_taille["windows_width"], data_taille["windows_length"])
        largeur = Label(the_frame_part_2,text='entrez la largeur',fg="white",bg="blue") #Select title
        ent_largeur = Entry(the_frame_part_2, width=20)
        ent_largeur.insert(0,data_taille['windows_width'])
        hauteur = Label(the_frame_part_2,text='entrez la hauteur',fg="white",bg="blue") #Select title
        ent_hauteur = Entry(the_frame_part_2, width=20)
        ent_hauteur.insert(0,data_taille['windows_length'])
        button = Button(the_frame_part_2, text="terminer", command=lambda : get_ent_button_level_2(path_of_taille_file, ent_largeur, ent_hauteur, the_frame_part_2))
        button2 = Button(the_frame_part_2, text="remettre les paramètres par défault", command=lambda : get_ent_button2_level_2(ent_largeur, ent_hauteur, windows_height_x, windows_height_y))
        largeur.grid(row = 0, column = 0, padx = 30, pady =10)
        ent_largeur.grid(row = 0, column = 1, padx = 30,pady =10)
        hauteur.grid(row = 1, column = 0, padx = 30, pady =10) 
        ent_hauteur.grid(row = 1, column = 1, padx = 30, pady =10)
        button.grid(row = 2, column = 2, padx = 30, pady =10)
        button2.grid(row = 1, column = 2, padx = 30, pady =10)

    def get_ent_button_level_2(name_file,l,h,frame_level_2):
        print(l.get())
        print(h.get())
        with open(name_file, "r") as f:
            data_2 = json.load(f)
        data_2['windows_width'] = int(l.get())
        data_2['windows_length'] = int(h.get())

        with open(name_file, 'w') as file:
            json.dump(data_2, file, indent = 6)  

        frame_level_2.destroy()

    def get_ent_button2_level_2(l,h,x,y):
        l.delete(0,END)
        h.delete(0,END)
        l.insert(0,x)
        h.insert(0,y)
    
    def ajust_height_scorlbar(name_file,y_def):
        with open(name_file, "r") as f:
            data_2 = json.load(f)
        the_frame_level_2 = Toplevel(the_frame, padx=125, pady=130)    
        scrol_height = Label(the_frame_level_2,text='entrez la largeur',fg="white",bg="blue") #Select title
        ent_scrol = Entry(the_frame_level_2, width=20)
        ent_scrol.insert(0,data_2['windows_scrol_height'])
        button = Button(the_frame_level_2, text="terminer", command=lambda : get_scrol_ent_button_level_2(name_file, ent_scrol, the_frame_level_2))
        button2 = Button(the_frame_level_2, text="remettre les paramètres par défault", command=lambda : get_scrol_ent_button2_level_2(ent_scrol, y_def))

        scrol_height.grid(row = 0, column = 0, padx = 30, pady =10)
        ent_scrol.grid(row = 0, column = 1, padx = 30,pady =10)
        button.grid(row = 1, column = 2, padx = 30, pady =10)
        button2.grid(row = 0, column = 2, padx = 30, pady =10)

    def get_scrol_ent_button_level_2(name_file,h,frame_level_2):
        print(h.get())
        with open(name_file, "r") as f:
            data_2 = json.load(f)
        data_2['windows_scrol_height'] = int(h.get())

        with open(name_file, 'w') as file:
            json.dump(data_2, file, indent = 6)  

        frame_level_2.destroy()

    def get_scrol_ent_button2_level_2(h,y):
        h.delete(0,END)
        h.insert(0,y)

    def get_all_column():

        with open(dico_all_path["path_to_converted_data_interface_Part_1"], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
        
        header_without_time = header[1:len(header)]

        my_data = genfromtxt(dico_all_path["path_to_converted_data_interface_Part_1"], delimiter=',', names=True, usecols=tuple(header_without_time), unpack=True)
        #print(my_data)
        dic = {}
        if type(my_data[0]) == ndarray:
            for i in range(len(header_without_time)):
                dic[header_without_time[i]] = my_data[i]
        else:
            dic[header_without_time[0]] = array(my_data)

        return (header_without_time,dic)

    
    def validate_all_entry():
        """
        """
        with open(dico_all_path["path_to_json_calculs"], "r") as f:
            data = json.load(f)
        all_sous_cycle = get_all_sous_cycle_from_file()

        for sous_cycle in all_sous_cycle:
            sous_cycle_desc = sous_cycle.split(" ")
            sous_cycle_num = sous_cycle_desc[1]
        
            all_info = data[sous_cycle]
            if all_info["sous_cycles_descriptions"+"_%s"%(sous_cycle_num)] == "(description)":
                invalide_entry.append("Aucune description entrée pour le sous cycle %s"%(sous_cycle_num))
            if (all_info["math_entry"+"_%s"%(sous_cycle_num)] == "") or (all_info["math_entry"+"_%s"%(sous_cycle_num)] == " "):
                invalide_entry.append("Aucune équation entrée pour le sous cycle %s"%(sous_cycle_num))
            
    # Cette partie sert au numéro 4)     
        if len(all_sous_cycle) != data["config_nb_sc"]:
            invalide_entry.append("Les nombres de fonction enregistré dans le fichier et détecté ne correspondent pas")
           
        dico_all_error_message["invalide_entry"]:invalide_entry

    def calculate_sous_cycle_power():

        get_all_entry()

        validate_all_entry()
        if dico_all_error_message["invalide_entry"] != []:
            fenetre_erreur(dico_all_error_message["invalide_entry"],"invalide_entry")
            return None
        (list_all_sensor, dico_with_all_column) = get_all_column()
        #print(dico_with_all_column)
        list_all_sous_cycle = get_all_sous_cycle_from_file()
        #print(list_all_sous_cycle)
        



        with open(dico_all_path["path_to_json_calculs"], "r") as f:
            data = json.load(f)
        dico_with_converted_value = {}

        list_of_all_array = []
        for sous_cycle in list_all_sous_cycle:
            num_only = sous_cycle.split(' ')
            equation = data[sous_cycle]["math_entry_%s"%(num_only[1])]
            #print(equation)

            array_coverted_value = eval(equation,dico_with_all_column)
            list_of_all_array.append(array_coverted_value)
            dico_with_converted_value[sous_cycle] = array_coverted_value

        #print(dico_with_converted_value)

        nb_line = []
        for key in list(dico_with_converted_value.keys()):
            nb_line.append(len(dico_with_converted_value[key]))
            print(nb_line)

        print("vecteur des nombre de ligne par colonne : ", nb_line)
        nb_line_by_column = nb_line[0]
        same_number_of_value = nb_line.count(nb_line_by_column)

        try:
            assert same_number_of_value == len(nb_line), \
                "Les vecteurs colonnes représentant les donnees dans le temps doivent avoir le même nombre de donnees. Or, un ou plusieurs capteurs ont un nombre de donnees different des autres"
        except AssertionError:
            list_error_calculer.append("Les nombres de sous-cycles enregistré dans le fichier et détecté ne correspondent pas")
            dico_all_error_message["assertions_partie_2"] = list_error_calculer

        nb_column = len(nb_line)



        list_time = []
        with open(dico_all_path["path_to_converted_data_interface_Part_1"], newline='') as csvfile:
            for each_row in csvfile:
                data_from_colum_0 = each_row.split(',')[0]
                list_time.append(data_from_colum_0)
                only_time = list_time[1:len(list_time)]
        #print(only_time)

        #print(only_time)

        dictionnary_of_all_lines_in_csv_file = {}
        for i in range(nb_line[0]):
            all_column_value = []
            all_column_value.append(str(only_time[i]))
            
            for j in range(nb_column):
                all_column_value.append(str(list_of_all_array[j][i]))
            dictionnary_of_all_lines_in_csv_file["ligne %s"%(i+1)] = all_column_value


        #print(dictionnary_of_all_lines_in_csv_file)

        with open(dico_all_path["path_to_converted_sous_cycle_puissance"], 'w', newline='') as csvfile:
            head_list  = ["Time"]
            for sous_cycle_only in list_all_sous_cycle:
                format_sous_cycle = sous_cycle_only.split(" ")
                head_list.append(format_sous_cycle[0] + "_"+format_sous_cycle[1])
            fieldnames = head_list
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            dico_with_all_can_data_converted = {}
            for i in range(nb_line[0]):
                for j in range(nb_column+1):
                    dico_with_all_can_data_converted[head_list[j]] = dictionnary_of_all_lines_in_csv_file["ligne %s"%(i+1)][j]

                writer.writerow(dico_with_all_can_data_converted)

        list_indication = ["Enregistrement effectué sans problème dans : %s"%(dico_all_path["path_to_converted_sous_cycle_puissance"])]
        dico_all_error_message["indication"] =list_indication
            
        fenetre_erreur(dico_all_error_message["indication"],"indication", is_indication=True)
        
        print("Enregistrement effectué sans problème dans : ", dico_all_path["path_to_converted_sous_cycle_puissance"])


    


    def interface_part_3():
        #print(dico_all_path["part_1_json_name"])
        #print(dico_all_path["name_of_the_interface_2_file"])
        get_all_entry()

        no_error = True
        if dico_all_error_message["assertions_partie_2"] != []:
            fenetre_erreur(dico_all_error_message["assertions_partie_2"],"assertions_partie_2")
            no_error =False
        if dico_all_error_message["calculer"] != []:
            fenetre_erreur(dico_all_error_message["calculer"],"calculer")
            no_error = False
        if dico_all_error_message["invalide_entry"] != []:
            fenetre_erreur(dico_all_error_message["invalide_entry"],"invalide_entry")
            no_error = False
    
        validate_all_entry()
        if dico_all_error_message["invalide_entry"] != []:
            fenetre_erreur(dico_all_error_message["invalide_entry"],"invalide_entry")
            no_error = False
        

        if no_error == True:
            interface_3.interface_part_3(dico_all_path["part_1_json_name"],dico_all_path["name_of_the_interface_2_file"],the_frame)
        else:
            print("La troisième interface ne s'ouvrira pas avant que tous les bogs n'ait été résolu")
        
        
    def end_error_message(win,list):
        dico_all_error_message[list].clear()
        win.destroy()

    def fenetre_erreur(message_error_list,list,win1=None,is_indication=False):
        
        with open(dico_all_path["path_to_taille_interface_2"], "r") as f:
            data_2 = json.load(f)
        
        #data_2['windows_scrol_height'] = int(h.get())
        select_frame = the_frame 
        if win1 != None:
            select_frame = win1
        the_frame_level_2 = Toplevel(select_frame, height=data_2["windows_length"], width=data_2["windows_width"])   
        text_box = Text(the_frame_level_2,height=int(data_2["windows_length"]/22), width=int(data_2["windows_width"]/12)) #Select title
        #txt.grid(row = 0, column = 0)
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

    def delete_widgets():


        with open(dico_all_path["path_to_json_calculs"], "r") as f:
            data = json.load(f)

        get_all_sous_cycle = get_all_sous_cycle_from_file()
        for sous_cycle in get_all_sous_cycle:
            only_num = sous_cycle.split(' ')
            try:
                dico_funcs["Sous cycle %s"%(only_num[1])].destroy()
                dico_sous_cycle_description["sous_cycles_descriptions_%s"%(only_num[1])].destroy()
                dico_math_entry_label["desc_sous_cycle_%s"%(only_num[1])].destroy()
                dico_math_entry["math_entry_%s"%(only_num[1])].destroy()
                dico_button_math_validate["button_math_validate_%s"%(only_num[1])].destroy()
            except KeyError:
                break
        
        dico_funcs.clear()
        dico_sous_cycle_description.clear()
        dico_math_entry_label.clear()
        dico_math_entry.clear()
        dico_button_math_validate.clear()

        last_sous_cycle = get_all_sous_cycle.pop()
        get_num = last_sous_cycle.split(" ")

        data["config_nb_sc"] = data["config_nb_sc"]-1
        fonc_deleted = data.pop("sous_cycle %s"%(get_num[1]),None)

        with open(dico_all_path["path_to_json_calculs"], 'w') as file:
            json.dump(data, file, indent = 6)
            
        if fonc_deleted != None:
            print("Le sous cycle %s a bien été supprimé"%(get_num[1]))
    

        function_from_file()


    def end_script():
        get_all_entry()
        exit()
    windows_height_x = int(GetSystemMetrics(0))-20
    windows_height_y = int(GetSystemMetrics(1))-150
    windows_scrol_height = int(GetSystemMetrics(1))

    today = datetime.datetime.now()
    today_format = today.strftime("%b_%d_%Y")
    end_default_file_name = today_format + ".json"

    the_path = find_the_config_file_path(end_default_file_name)
    dico_all_path["path_to_json_interface_part_1"] = the_path[0]
    dico_all_path["path_to_json_calculs"] = the_path[1]
    dico_all_path["path_to_taille_interface_2"] = the_path[2]
    dico_all_path["path_to_converted_data_interface_Part_1"] = the_path[3]
    dico_all_path["path_to_converted_sous_cycle_puissance"] = the_path[4]
    dico_all_path["path_to_folder"] = the_path[5]


    try:
        with open(dico_all_path["path_to_json_interface_part_1"], 'r') as f:
            print("ok")

    except json.JSONDecodeError:
        try:
            assert 1==2, \
                "Il n'y a aucune interface détectée associée à ce fichier"
        except AssertionError:
            list_assertion.append("Il n'y a aucune interface détectée associée à ce fichier")
            dico_all_error_message["assertions_partie_2"] = list_assertion

    except FileNotFoundError:
        try:
            assert 1==2, \
                "Il n'y a aucune interface détectée associée à ce fichier"
        except AssertionError:
            list_assertion.append("Il n'y a aucune interface détectée associée à ce fichier")
            dico_all_error_message["assertions_partie_2"] = list_assertion

    try:
        with open(dico_all_path["path_to_converted_data_interface_Part_1"], 'r') as f:
            print("ok")

    except json.JSONDecodeError:
        try:
            assert 1==2, \
                "Il n'y a aucune donnée convertie en provenance des capteurs"

        except AssertionError:
            list_assertion.append("Il n'y a aucune donnée convertie en provenance des capteurs")
            dico_all_error_message["assertions_partie_2"] = list_assertion

    except FileNotFoundError:
        try:
            assert 1==2, \
                "Il n'y a aucune donnée convertie en provenance des capteurs"

        except AssertionError:
            list_assertion.append("Il n'y a aucune donnée convertie en provenance des capteurs")
            dico_all_error_message["assertions_partie_2"] = list_assertion

    try:

        with open(dico_all_path["path_to_json_calculs"], 'r') as f:
            data = json.load(f)
            dico = {'config_nb_sc' : init_nb_sous_cycle,
                    'config_y_place_sc': init_config_y_sous_cycle,
                    'config_x_place_sc': init_config_x_sous_cycle,   
            }
        with open(dico_all_path["path_to_json_calculs"], 'w') as file:
            json.dump(dico, file, indent = 6)
            print('yes')

    except json.JSONDecodeError:
        print("fichier vide, introuvable ou corrompu!")
        name_only = dico_all_path["path_to_json_calculs"].split("\\")
        print("Création d'un nouveau fichier appelé : %s"%(name_only[len(name_only)-1]))
        dico = {'config_nb_sc' : init_nb_sous_cycle,
                    'config_y_place_sc': init_config_y_sous_cycle,
                    'config_x_place_sc': init_config_x_sous_cycle,   
            }
        with open(dico_all_path["path_to_json_calculs"], 'w') as file:
            json.dump(dico, file, indent = 6)

    except FileNotFoundError:
        print("fichier vide ou introuvable!")
        name_only = dico_all_path["path_to_json_calculs"].split("\\")

        print("Création d'un nouveau fichier appelé : %s"%(name_only[len(name_only)-1]))
        dico = {'config_nb_sc' : init_nb_sous_cycle,
                    'config_y_place_sc': init_config_y_sous_cycle,
                    'config_x_place_sc': init_config_x_sous_cycle,   
            }
        with open(dico_all_path["path_to_json_calculs"], 'w') as file:
            json.dump(dico, file, indent = 6)

    try:
        with open(dico_all_path["path_to_taille_interface_2"], 'r') as f:
            print("ok")

    except json.JSONDecodeError:
        dico_taille = {'windows_width': windows_height_x,
                    'windows_length': windows_height_y,
                    'windows_scrol_height': windows_height_y,}

        with open(dico_all_path["path_to_taille_interface_2"], 'w') as file:
            json.dump(dico_taille, file, indent = 6)

    except FileNotFoundError:
        dico_taille = {'windows_width': windows_height_x,
                    'windows_length': windows_height_y,
                    'windows_scrol_height': windows_scrol_height}

        with open(dico_all_path["path_to_taille_interface_2"], 'w') as file:
            json.dump(dico_taille, file, indent = 6)


#test pour importer le fichier voulu
    
    #with open(dico_all_path["path_to_json_interface_part_1"], 'r') as f:
    #    data = json.load(f)
    #print(data)

#test pour aller chercher le fichier voulu

    #with open(dico_all_path["path_to_converted_data_interface_Part_1"], newline='') as csvfile:
    #    reader = csv.DictReader(csvfile)
    #    header = reader.fieldnames
    #print(header)




    
    tk = Tk()
    tk.title("Python Tkinter")
    with open(dico_all_path["path_to_taille_interface_2"], 'r') as f:
       data_taille = json.load(f)
    tk.minsize(data_taille["windows_width"],data_taille["windows_length"])


    the_frame = tk
        
    largeur = windows_height_x
    hauteur = windows_height_y
    main_frame = Frame(tk)
    main_frame.place(x=0, y=0, width=largeur, height=hauteur)

    main_canvas = Canvas(main_frame, width=largeur, height=hauteur)
    main_canvas.place(x=0, y=0, width=largeur, height=hauteur)

    scroll_v = Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
    dico_scrollbar["vertical"] = scroll_v
    dico_scrollbar["vertical"].pack(side= RIGHT,fill=Y)
    dico_scrollbar["vertical"].pack(side= RIGHT,fill=Y)

    main_canvas.configure(yscrollcommand=scroll_v.set)
    main_canvas.bind("<Configure>",lambda e: main_canvas.configure(scrollregion= main_canvas.bbox("all")))

    second_frame = Frame(main_canvas, width=largeur, height=hauteur)
    main_canvas.create_window((0,0), window=second_frame, anchor="nw")
    with open(dico_all_path["path_to_taille_interface_2"], 'r') as f:
        data = json.load(f)
    second_frame.configure(height=data["windows_scrol_height"])

    the_frame = second_frame

    selection_bar = Menu(tk)
    filemenu = Menu(selection_bar, tearoff=0)
    selection_bar.add_cascade(label="Fichier", menu=filemenu)
    filemenu.add_command(label="Nouveau sous cycle", command=add_function)
    filemenu.add_command(label="Ouvrir...", command=select_file)
    filemenu.add_command(label="Enregistrer", command=get_all_entry)
    filemenu.add_command(label="Enregistrer sous...", command=save_in_to_file)
    filemenu.add_separator()
    #filemenu.add_command(label="Exportation pour RPI", command=export_data_for_rpi)
    #filemenu.add_separator()
    filemenu.add_command(label="Fermer", command=end_script)

    filemenu2 = Menu(selection_bar, tearoff=0)
    selection_bar.add_cascade(label="dimentions", menu=filemenu2)
    filemenu2.add_command(label="taille de la fenêtre", command= lambda : adjust_windows(dico_all_path["path_to_taille_interface_2"],windows_height_x,windows_height_y))
    filemenu2.add_command(label="longueur du scrollbar", command= lambda : ajust_height_scorlbar(dico_all_path["path_to_taille_interface_2"], windows_scrol_height))

    filemenu3 = Menu(selection_bar, tearoff=0)
    selection_bar.add_cascade(label="donnees", menu=filemenu3)
    filemenu3.add_command(label="Suppression d'un sous cycle", command=delete_widgets)
    filemenu3.add_separator()
    filemenu3.add_command(label="Ouvrir interface pour traitement", command=interface_part_3)
    filemenu3.add_separator()
    #filemenu3.add_command(label="Importer le can", command= lambda : convert_all_data(namefile[1]))

    tk.config(menu=selection_bar)
    save_all_manual_entry_button = Button(the_frame, text="Calculer", command=calculate_sous_cycle_power)
    save_all_manual_entry_button.place(x=1200,y=60)
    #validate_button = Button(the_frame, text="Valider", command= lambda : convert_all_data(namefile[1]))
    #validate_button.place(x=1200,y=20)
    print(dico_all_error_message["assertions_partie_2"])
    if dico_all_error_message["assertions_partie_2"] != []:
        fenetre_erreur(dico_all_error_message["assertions_partie_2"],"assertions_partie_2", win_1)
        tk.destroy()

    tk.protocol("WM_DELETE_WINDOW", end_script)
    tk.mainloop()

if __name__ == "__main__":
    #interface_part_2("config_demo.json")
    print("Cette fonction ne devrait être lancé que par le bouton de l'interface graphique")