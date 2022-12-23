from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import json
import csv
import datetime
from unicodedata import name
from win32api import GetSystemMetrics
from numpy import genfromtxt
from numpy import searchsorted
from numpy import arange
from numpy import savetxt
from numpy import c_
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.widgets import SpanSelector
import os
from PIL import Image,ImageTk
import glob


def interface_part_3(json_name_file, json_name_file_part_2):
    init_nb_sous_cycle = 0
    init_config_y_sous_cycle = 60
    init_config_x_sous_cycle = [40, 120, 250, 380, 900]

    dico_all_path = {"part_1_json_name":json_name_file,"part_2_json_name": json_name_file_part_2, "name_of_the_interface_3_file": None, "path_to_json_interface_part_1":None, "path_to_json_interface_part_2":None, "path_to_json_traitement":None, "path_to_taille_interface_3":None, "path_to_converted_data_interface_Part_1":None,"path_to_sous_cycle_data_interface_Part_2":None, "path_to_converted_cycle_puissance":None, "path_to_folder":None, "path_to_suppressed_cycle_file":None,"path_to_suppressed_sous_cycle_file":None, "path_fluxVideo":None, "path_camera_1":None,"path_camera_2":None, "path_to_gps_file":None, "Path_to_machine_folder":None, "Path_to_interface_folder":None}

    dico_fig_cycle_puissance = {}
    dico_all_figs_sous_cycle_puissance = {}
    dico_plot_cycle_puisance ={}
    dico_all_plots_sous_cycle_puissance = {}
    dico_x_axis_plots = {}
    dico_y_axis_plot_cycle_puissance = {}
    dico_all_y_axis_plot_sous_cycle_puissance = {}
    dico_x_axis_plots_deleted = {}
    dico_y_axis_plots_deleted = {}
    dico_all_y_axis_plot_sous_cycle_puissance_deleted = {}
    dico_headers = {"cycle":None, "sous_cycles":None}
    dico_canvas_cycle_puissance = {}
    dico_all_canvas_sous_cycle_puissance = {}
    dico_selection = {"int":None}
    dico_selection_mouse_coord = {"id":None}
    dico_format_cam = {"cam1":None, "cam2":None}
    dico_canvas_cam = {"cam1":None, "cam2":None}
    dico_line_and_time = {}
    dico_gps = {}
    dico_label_gps = {}
    dico_entry_gps = {}




    dico_scrollbar = {}

    def find_the_config_file_path(date):

        path_script = __file__
        to_list = path_script.split('\\')
        list_folder_minus_2_path = to_list[0:len(to_list)-2]
        path_to_machine_folder = '\\'.join(list_folder_minus_2_path)
        path_to_interface = "\\".join(to_list[0:len(to_list)-3])
        path_json_part_1 = "\\".join(list_folder_minus_2_path) + "\\1) setup_donnees\\fichiers_enregistrements\\" + json_name_file
        path_json = "\\".join(list_folder_minus_2_path) + "\\2) calcul_puissance\\fichiers_enregistrements\\" + json_name_file_part_2

        only_name = json_name_file.split(".json")
        only_name_part_2 = json_name_file_part_2.split(".json")

        dico_all_path["name_of_the_interface_3_file"] = "default_%s"%(only_name[0]+"_traitement_puissance_" + date)
        only_name_part_3 = dico_all_path["name_of_the_interface_3_file"].split(".json")
        path_csv_converted = "\\".join(list_folder_minus_2_path) + "\\1) setup_donnees\\fichiers_enregistrements\\z_%s_can_converti.csv"%(only_name[0])
        path_csv_sous_cycle = "\\".join(list_folder_minus_2_path) + "\\2) calcul_puissance\\fichiers_enregistrements\\z_%s_calcul_sous_cycle_puissance.csv"%(only_name_part_2[0])

        path_file = '\\'.join(list_folder_minus_2_path) + "\\3) traitement_donnes" + "\\fichiers_enregistrements\\default_%s"%(only_name[0]+"_traitement_puissance_" + date)

        path_file_taille_interface_3 = '\\'.join(list_folder_minus_2_path) + "\\3) traitement_donnes" + "\\fichiers_enregistrements\\%s"%("z_taille_interface_3.json")

        converted_power_file = '\\'.join(list_folder_minus_2_path) + "\\3) traitement_donnes" + "\\fichiers_enregistrements\\z_%s_cycle_puissance_totale.csv"%(only_name_part_3[0])

        path_to_folder = '\\'.join(list_folder_minus_2_path) + "\\3) traitement_donnes" + "\\fichiers_enregistrements\\"

        return path_json_part_1, path_json, path_file, path_file_taille_interface_3, path_csv_converted, path_csv_sous_cycle, converted_power_file, path_to_folder,path_to_machine_folder,path_to_interface

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

    def select_file():

        today = datetime.datetime.now()
        today_format = today.strftime("%b_%d_%Y")
        interface_part_1_file_name = dico_all_path["part_1_json_name"].split('.json')
        name_default = "default_" + interface_part_1_file_name[0] +"_traitement_puissance_" + today_format + ".json"
        print(name_default == dico_all_path["name_of_the_interface_3_file"])
        
        default_file = None
        if name_default == dico_all_path["name_of_the_interface_3_file"]:
            default_file = dico_all_path["path_to_json_traitement"]
        
#        get_all_sous_cycle = get_all_sous_cycle_from_file()
#        for sous_cycle in get_all_sous_cycle:
#            only_num = sous_cycle.split(' ')
#            try:
#                dico_funcs["Sous cycle %s"%(only_num[1])].destroy()
#                dico_sous_cycle_description["sous_cycles_descriptions_%s"%(only_num[1])].destroy()
#                dico_math_entry_label["desc_sous_cycle_%s"%(only_num[1])].destroy()
#                dico_math_entry["math_entry_%s"%(only_num[1])].destroy()
#                dico_button_math_validate["button_math_validate_%s"%(only_num[1])].destroy()
#            except KeyError:
#                break
#
#        dico_funcs.clear()
#        dico_sous_cycle_description.clear()
#        dico_math_entry_label.clear()
#        dico_math_entry.clear()
#        dico_button_math_validate.clear()
#        
        filetypes = (('text files', '*.json'),('All files', '*.*'))
        print(dico_all_path["path_to_json_traitement"])
        filename = fd.askopenfilename(title="Sélectionner l'interface à ouvrir",initialdir=dico_all_path["path_to_folder"],filetypes=filetypes)
        list_str = filename.split("/")
        only_name = list_str[len(list_str)-1]
        #dico_file_name["filename"] = only_name

        dico_all_path["name_of_the_interface_3_file"] = only_name
        dico_all_path["path_to_json_traitement"] = filename
        name = only_name.split(".json")
        dico_all_path["path_to_converted_cycle_puissance"] = dico_all_path["path_to_folder"] + "z_" + name[0] + "_cycle_puissance_totale.csv"
        if default_file != None:
            os.remove(default_file)


        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

            #data["all_paths"]["path_to_suppressed_cycle_file"] = "init"
            #data["all_paths"]["path_to_suppressed_sous_cycle_file"] = "init"
            data["all_paths"]["path_to_converted_cycle_puissance"] = dico_all_path["path_to_converted_cycle_puissance"]
            data["all_paths"]["name_of_the_interface_3_file"] =  dico_all_path["name_of_the_interface_3_file"]
            #data["all_paths"]["path_to_json_traitement"] = dico_all_path["path_to_json_traitement"]

        with open(dico_all_path["path_to_json_traitement"], 'w') as file:
            json.dump(data, file, indent = 6)
        
        
        get_path_pictures()
        get_gps_file()
        
        if data["calculs"] == "oui":
            calculate_cycle_power()


        if data["affichage"] == "oui":
            try_not_for_loops()
        

#        function_from_file()



    def save_in_to_file():

        today = datetime.datetime.now()
        today_format = today.strftime("%b_%d_%Y")
        interface_part_1_file_name = dico_all_path["part_1_json_name"].split('.json')
        name_default = "default_" + interface_part_1_file_name[0] +"_traitement_puissance_" + today_format + ".json"
        print(name_default == dico_all_path["name_of_the_interface_3_file"])
        
        default_file = None
        if name_default == dico_all_path["name_of_the_interface_3_file"]:
            default_file = dico_all_path["path_to_json_traitement"]

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

        files = [('json', '*.json')]
        file = fd.asksaveasfile(title= "Sauvegarder l'interface graphique",initialfile = data["all_paths"]["part_1_json_name"],initialdir=dico_all_path["path_to_folder"],filetypes = files, defaultextension = files)
        list_str = file.name.split("/")
        only_name = list_str[len(list_str)-1]

        

#        with open(dico_all_path["path_to_json_traitement"], "r") as f:
#            data = json.load(f)

        dico_all_path["name_of_the_interface_3_file"] = only_name
        dico_all_path["path_to_json_traitement"] = file.name
        name = only_name.split(".json")
        dico_all_path["path_to_converted_cycle_puissance"] = dico_all_path["path_to_folder"] + "z_" + name[0] + "_cycle_puissance_totale.csv"

#        with open(dico_all_path["path_to_json_traitement"], 'w') as file:
#            json.dump(data, file, indent = 6)

        with open(default_file, "r") as f:
            data_old = json.load(f)

            #data_old["all_paths"]["path_to_suppressed_cycle_file"] = "init"
            #data_old["all_paths"]["path_to_suppressed_sous_cycle_file"] = "init"

        if default_file != None:
            os.remove(default_file)

        with open(dico_all_path["path_to_json_traitement"], 'w') as file:
            json.dump(data_old, file, indent = 6)

        calculate_cycle_power()

    def plot_graph_converted():

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

        with open(data["all_paths"]["path_to_converted_data_interface_Part_1"], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames

        header_without_time = header[1:len(header)]

        dataArray = genfromtxt(data["all_paths"]["path_to_converted_data_interface_Part_1"], delimiter=',',usecols=tuple(header_without_time),names=True)
        #print(dataArray)
        #print(dataArray.dtype.names)
        num_column = len(dataArray.dtype.names)
        #print(num_column)
        for col_name in dataArray.dtype.names:
            pyplot.figure()
            pyplot.plot(dataArray[col_name], label=col_name)
            pyplot.legend()
        pyplot.show()




    def plot_graph_sous_cycle():


        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

        with open(data["all_paths"]["path_to_converted_cycle_puissance"], newline='') as csvfile:
            reader0 = csv.DictReader(csvfile)
            header0 = reader0.fieldnames

        header_without_time0 = header0[1:len(header0)]

        dataArray0 = genfromtxt(data["all_paths"]["path_to_converted_cycle_puissance"], delimiter=',',usecols=tuple(header_without_time0),names=True)
        print(len(dataArray0))
        x_val = arange(1, len(dataArray0)+1, 1)
        y_val_10 = dataArray0[dataArray0.dtype.names[0]]

        with open(data["all_paths"]["path_to_sous_cycle_data_interface_Part_2"], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            #for line in reader:
                #print(line)
            #print(reader)
            header = reader.fieldnames

        header_without_time = header[1:len(header)]

        dataArray = genfromtxt(data["all_paths"]["path_to_sous_cycle_data_interface_Part_2"], delimiter=',',usecols=tuple(header_without_time),names=True)
        print(len(dataArray))
        x_val = arange(1, len(dataArray)+1, 1)
        y_val = dataArray[dataArray.dtype.names[0]]

        pyplot.figure()
        pyplot.plot(dataArray0[dataArray0.dtype.names[0]], label=dataArray0.dtype.names[0])
        pyplot.legend()

        for col_name in dataArray.dtype.names:
            pyplot.figure()
            pyplot.plot(dataArray[col_name], label=col_name)
            pyplot.legend()#
        pyplot.show()       

    def try_not_for_loops():

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

        dico_line_and_time.clear()
        count = 1
        if data["all_paths"]["path_to_suppressed_cycle_file"] == "init":
            with open(data["all_paths"]["path_to_converted_cycle_puissance"], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for line in reader:
                    dico_line_and_time["%s"%(count)] = line["Time"]
                    count+=1
        elif data["all_paths"]["path_to_suppressed_cycle_file"] == "delete":
            name_file = data["all_paths"]["name_of_the_interface_3_file"]
            name_file = name_file.split(".json")
            path_to_suppress_total_cycle = data["all_paths"]["path_to_folder"] + "z_" + name_file[0] + "_total_cycle_apres_suppression.csv"
            path_to_suppress_sous_cycle = data["all_paths"]["path_to_folder"] + "z_" + name_file[0] + "_sous_cycle_apres_suppression.csv"

            with open(path_to_suppress_total_cycle, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for line in reader:
                    dico_line_and_time["%s"%(count)] = line["Time"]
                    count+=1

        photo_canvas_1 = Canvas(the_frame)
        dico_canvas_cam["cam1"] = photo_canvas_1 
        dico_canvas_cam["cam1"].place(x=40, y=30)

        photo_canvas_2 = Canvas(the_frame)
        dico_canvas_cam["cam2"] = photo_canvas_2
        dico_canvas_cam["cam2"].place(x=600, y=30)

        gps_label = Label(the_frame, text="Position GPS : ")
        dico_label_gps["gps"] = gps_label
        dico_label_gps["gps"].place(x=1130, y=120)

        gps_label_1 = Entry(the_frame,width=30)
        dico_entry_gps["gps"] = gps_label_1
        dico_entry_gps["gps"].insert(0,"aucune donnée")
        dico_entry_gps["gps"].place(x=1130, y=140)
        

        
        if data["all_paths"]["path_to_suppressed_cycle_file"] == "init":
            with open(data["all_paths"]["path_to_converted_cycle_puissance"], newline='') as csvfile:
                reader0 = csv.DictReader(csvfile)
                header0 = reader0.fieldnames
                dico_headers["cycle"] = reader0.fieldnames

        elif data["all_paths"]["path_to_suppressed_cycle_file"] == "delete":
            with open(path_to_suppress_total_cycle, newline='') as csvfile:
                reader0 = csv.DictReader(csvfile)
                header0 = reader0.fieldnames
                dico_headers["cycle"] = reader0.fieldnames

        header_without_time0 = header0[1:len(header0)]

        if data["all_paths"]["path_to_suppressed_cycle_file"] == "init":
            dataArray0 = genfromtxt(data["all_paths"]["path_to_converted_cycle_puissance"], delimiter=',',usecols=tuple(header_without_time0),names=True)
        elif data["all_paths"]["path_to_suppressed_cycle_file"] == "delete":
            dataArray0 = genfromtxt(path_to_suppress_total_cycle, delimiter=',',usecols=tuple(header_without_time0),names=True)

        print(len(dataArray0))
        x_val = arange(1, len(dataArray0)+1, 1)
        dico_x_axis_plots["x_val"] = x_val
        y_val_10 = dataArray0[dataArray0.dtype.names[0]]
        dico_y_axis_plot_cycle_puissance["y_val_10"] = y_val_10

        if data["all_paths"]["path_to_suppressed_sous_cycle_file"] == "init":
            with open(data["all_paths"]["path_to_sous_cycle_data_interface_Part_2"], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                header = reader.fieldnames
                dico_headers["sous_cycles"] = reader.fieldnames

        elif data["all_paths"]["path_to_suppressed_sous_cycle_file"] == "delete":
            with open(path_to_suppress_sous_cycle, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                header = reader.fieldnames
                dico_headers["sous_cycles"] = reader.fieldnames

        header_without_time = header[1:len(header)]

        if data["all_paths"]["path_to_suppressed_sous_cycle_file"] == "init":
            dataArray = genfromtxt(data["all_paths"]["path_to_sous_cycle_data_interface_Part_2"], delimiter=',',usecols=tuple(header_without_time),names=True)
        elif data["all_paths"]["path_to_suppressed_sous_cycle_file"] == "delete":
            dataArray = genfromtxt(path_to_suppress_sous_cycle, delimiter=',',usecols=tuple(header_without_time),names=True)
        
        num_column = len(dataArray.dtype.names)
    
        for i in range(num_column):
            dico_all_y_axis_plot_sous_cycle_puissance["y_val_%s"%(i+1)] = dataArray[dataArray.dtype.names[i]]
        
        fig0 = Figure(figsize = (10,3), dpi = 100)
        dico_fig_cycle_puissance["fig0"] = fig0
        plot0 = dico_fig_cycle_puissance["fig0"].add_subplot(1,1,1)
        dico_plot_cycle_puisance["plot0"] = plot0
        dico_plot_cycle_puisance["plot0"].plot(dico_x_axis_plots["x_val"], dico_y_axis_plot_cycle_puissance["y_val_10"], label=dataArray.dtype.names[0])
        dico_plot_cycle_puisance["plot0"].set_title(dataArray0.dtype.names[0])
        if data["all_paths"]["path_to_suppressed_sous_cycle_file"] == "init":
            data["Valeur_initiale_x_zoom"] = str(dico_x_axis_plots["x_val"][0])
            data["valeur_finale_x_zoom"] = str(dico_x_axis_plots["x_val"][len(dico_x_axis_plots["x_val"])-1])
            with open(dico_all_path["path_to_json_traitement"], 'w') as file:
                json.dump(data, file, indent = 6)

        canvas = FigureCanvasTkAgg(dico_fig_cycle_puissance["fig0"], master=the_frame)
        dico_canvas_cycle_puissance["canvas"] = canvas

        dico_canvas_cycle_puissance["canvas"].get_tk_widget().place(x=40, y=350,width=1300, height=370)

        #canvas.get_tk_widget().place(x=0, y=0, width=windows_height_x, height=windows_height_y)
        #toolbar = NavigationToolbar2Tk(canvas,the_frame)
        #toolbar.update()
        #canvas.get_tk_widget().place(x=40, y=350,width=1300, height=370)

        dico_canvas_cycle_puissance["canvas"].draw()

        larg = 1300
        heig = 370
        third_frame = Frame(the_frame)
        third_frame.place(x=40, y=730, width=larg+20, height=heig)

        third_canvas = Canvas(third_frame, width=largeur, height=hauteur)
        third_canvas.place(x=0, y=0, width=larg, height=heig)

        scroll_v_2 = Scrollbar(third_frame, orient=VERTICAL, command=third_canvas.yview)
        #dico_scrollbar["vertical"] = scroll_v
        #dico_scrollbar["vertical"].pack(side= RIGHT,fill=Y)
        #dico_scrollbar["vertical"].pack(side= RIGHT,fill=Y)
        scroll_v_2.pack(side= RIGHT,fill=Y)

        third_canvas.configure(yscrollcommand=scroll_v_2.set)
        third_canvas.bind("<Configure>",lambda e: third_canvas.configure(scrollregion= third_canvas.bbox("all")))

        forth_frame = Frame(third_canvas, width=larg, height=heig)
        third_canvas.create_window((0,0), window=forth_frame, anchor="nw")
        #with open(dico_all_path["path_to_taille_interface_3"], 'r') as f:
        #    data = json.load(f)
        forth_frame.configure(height=num_column*heig)

        #one_but = Button(forth_frame, text="bruhluhluh")
        #one_but.place(x=0, y=0)
        count = 0
        for i in range(num_column):
            dico_all_figs_sous_cycle_puissance["fig%s"%(i+1)] = Figure(figsize = (5,5), dpi = 100)
            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)] = dico_all_figs_sous_cycle_puissance["fig%s"%(i+1)].add_subplot(1,1,1)

            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)].sharex(dico_plot_cycle_puisance["plot0"])
            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)].plot(dico_x_axis_plots["x_val"], dico_all_y_axis_plot_sous_cycle_puissance["y_val_%s"%(i+1)], label=dataArray.dtype.names[i])
            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)].set_title(dataArray.dtype.names[i])
            dico_all_canvas_sous_cycle_puissance["canvas%s"%(i+1)] = FigureCanvasTkAgg(dico_all_figs_sous_cycle_puissance["fig%s"%(i+1)], master=forth_frame)
        

            dico_all_canvas_sous_cycle_puissance["canvas%s"%(i+1)].get_tk_widget().place(x=0, y=count*heig, width=larg, height=heig)
            #toolbar = NavigationToolbar2Tk(canvas2,the_frame)
            #toolbar.update()
            #canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            dico_all_canvas_sous_cycle_puissance["canvas%s"%(i+1)].draw()
            count += 1

        #fig2 = Figure(figsize = (5,5), dpi = 100)
        #plot2 = fig2.add_subplot(1,1,1)
        #plot2.sharex(plot0)
        #plot2.plot(x_val, y_val_2, label=dataArray.dtype.names[1])
        #plot2.set_title(dataArray.dtype.names[1])
#
        #canvas2 = FigureCanvasTkAgg(fig2, master=forth_frame)
       #
#
        #canvas2.get_tk_widget().place(x=0, y=heig, width=larg, height=heig)
        ##toolbar = NavigationToolbar2Tk(canvas2,the_frame)
        ##toolbar.update()
        ##canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        #canvas2.draw()

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)
        
        data["affichage"] = "oui"
        with open(dico_all_path["path_to_json_traitement"], 'w') as file:
                json.dump(data, file, indent = 6)

#
    def get_all_column():

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

        with open(data["all_paths"]["path_to_sous_cycle_data_interface_Part_2"], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            header = reader.fieldnames
        
        header_without_time = header[1:len(header)]

        my_data = genfromtxt(data["all_paths"]["path_to_sous_cycle_data_interface_Part_2"], delimiter=',', names=True, usecols=tuple(header_without_time), unpack=True)
        #print(my_data)
        dic = {}
        for i in range(len(header_without_time)):
            dic[header_without_time[i]] = my_data[i]
        return (header_without_time,dic)

    def calculate_cycle_power():

        (header_list, dico_data) = get_all_column()

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

        #print(header_list)
        #print(dico_data)
        calcul_string = ""
        for column_name in header_list:
            calcul_string += column_name + "+"
        #print(calcul_string[0:len(calcul_string)-1])

        array_power_data = eval(calcul_string[0:len(calcul_string)-1],dico_data)
        nb_line = len(array_power_data)
        #print("nb_line : ", nb_line)
        list_time = []
        with open(data["all_paths"]["path_to_converted_data_interface_Part_1"], newline='') as csvfile:
            for each_row in csvfile:
                data_from_colum_0 = each_row.split(',')[0]
                list_time.append(data_from_colum_0)
                only_time = list_time[1:len(list_time)]
        #print(only_time)

        #print(only_time)
        dico_power_data_and_time = {"Time": only_time,"cycle_puissance":array_power_data}

        #print(dico_power_data_and_time)
        #print(dico_power_data_and_time["Time"][0])
        #print(dico_power_data_and_time["cycle_puissance"][0])

        

        #dictionnary_of_all_lines_in_csv_file = {}
        #for i in range(nb_line[0]):
        #    all_column_value = []
        #    all_column_value.append(str(only_time[i]))
        #    
        #    for j in range(nb_column):
        #        all_column_value.append(str(list_of_all_array[j][i]))
        #    dictionnary_of_all_lines_in_csv_file["ligne %s"%(i+1)] = all_column_value
#
#
        #print(dictionnary_of_all_lines_in_csv_file)



        with open(data["all_paths"]["path_to_converted_cycle_puissance"], 'w', newline='') as csvfile:
            head_list  = ["Time", "cycle_puissance"]
            fieldnames = head_list
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for i in range(nb_line):
                dico_with_all_can_data_converted = {"Time":dico_power_data_and_time["Time"][i], "cycle_puissance":dico_power_data_and_time["cycle_puissance"][i]}
                writer.writerow(dico_with_all_can_data_converted)

        print("Enregistrement effectué sans problème dans : ", data["all_paths"]["path_to_converted_cycle_puissance"])

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)
        
        data["calculs"] = "oui"
        with open(dico_all_path["path_to_json_traitement"], 'w') as file:
                json.dump(data, file, indent = 6)

    def span_select_function(x_min,x_max):

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)
        
        name_file = data["all_paths"]["name_of_the_interface_3_file"]
        name_file = name_file.split(".json")

        path_to_suppress_total_cycle = data["all_paths"]["path_to_folder"] + "z_" + name_file[0] + "_total_cycle_apres_suppression.csv"
        path_to_suppress_sous_cycle = data["all_paths"]["path_to_folder"] + "z_" + name_file[0] + "_sous_cycle_apres_suppression.csv"

        #print("x_min,x_max : ",x_min,x_max)
        indmin, indmax = searchsorted(dico_x_axis_plots["x_val"], (x_min, x_max))
        #print("indmin : ",indmin )
        #print("indmax : ",indmax )
        indmax = min(len(dico_x_axis_plots["x_val"]) - 1, indmax)
        #print("indmax : ",indmax )

        thisx = dico_x_axis_plots["x_val"][indmin:indmax]
        print("thisx : ",thisx)
        thisy = dico_y_axis_plot_cycle_puissance["y_val_10"][indmin:indmax]
        #print("thisy : ",thisy)
#            line2.set_data(thisx, thisy)
#            fig2.set_xlim(thisx[0], thisx[-1])
#            fig2.set_ylim(thisy.min(), thisy.max())
        dico_fig_cycle_puissance["fig0"].canvas.draw_idle()
        #print("c_[thisx, thisy] : ",c_[thisx, thisy])

        # save
        #savetxt("text.out", c_[thisx, thisy])
        if data["all_paths"]["path_to_suppressed_cycle_file"] == "init":

            dico_line_and_time.clear()
            count = 1
            with open(data["all_paths"]["path_to_converted_cycle_puissance"], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for line in reader:
                    dico_line_and_time["%s"%(count)] = line["Time"]
                    count+=1

            

            with open(data["all_paths"]["path_to_converted_cycle_puissance"], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                count_line = 1
                with open(path_to_suppress_total_cycle, 'w', newline='') as csvfile_power:
                    head_list  = ["Time", "cycle_puissance"]
                    fieldnames = head_list
                    writer_power = csv.DictWriter(csvfile_power, fieldnames=fieldnames)

                    writer_power.writeheader()

                    for line in reader:
                        #print(line)
                        if count_line+1 not in thisx:
                            writer_power.writerow(line)                   
                        count_line += 1
            data["all_paths"]["path_to_suppressed_cycle_file"] = "delete"

            with open(dico_all_path["path_to_json_traitement"], 'w') as file:
                json.dump(data, file, indent = 6)
        
        elif data["all_paths"]["path_to_suppressed_cycle_file"] == "delete":

            dico_line_and_time.clear()
            count = 1
            with open(path_to_suppress_total_cycle, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for line in reader:
                    dico_line_and_time["%s"%(count)] = line["Time"]
                    count+=1

            with open(path_to_suppress_total_cycle, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                count_line = 1
                all_line_list = []
                for line in reader:
                    #print(line)
                    if count_line+1 not in thisx:
                        all_line_list.append(line)                  
                    count_line += 1
            print("nb_ligne_cycle",len(all_line_list))


            with open(path_to_suppress_total_cycle, 'w', newline='') as csvfile_power:
                head_list  = ["Time", "cycle_puissance"]
                fieldnames = head_list
                writer_power = csv.DictWriter(csvfile_power, fieldnames=fieldnames)

                writer_power.writeheader()
                count_line = 1
                for line in all_line_list:
                    #print(line)
                    if count_line+1 not in thisx:
                        writer_power.writerow(line)                   
                    count_line += 1
                print("count",count_line)

            data["all_paths"]["path_to_suppressed_cycle_file"] = "delete"

            with open(dico_all_path["path_to_json_traitement"], 'w') as file:
                json.dump(data, file, indent = 6)

        print("Enregistrement effectué sans problème dans : ", "z_" + name_file[0] + "_total_cycle_apres_suppression.csv")
        

        if data["all_paths"]["path_to_suppressed_sous_cycle_file"] == "init":    
            with open(data["all_paths"]["path_to_sous_cycle_data_interface_Part_2"], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                count_line = 1
                with open(path_to_suppress_sous_cycle, 'w', newline='') as csv_new_file:

                    writer = csv.DictWriter(csv_new_file, fieldnames=dico_headers["sous_cycles"])
                    writer.writeheader()

                    for line in reader:
                        #print(line)
                        if count_line+1 not in thisx:
                            writer.writerow(line)                   
                        count_line += 1
            data["all_paths"]["path_to_suppressed_sous_cycle_file"] = "delete"

            with open(dico_all_path["path_to_json_traitement"], 'w') as file:
                json.dump(data, file, indent = 6)

        elif data["all_paths"]["path_to_suppressed_sous_cycle_file"] == "delete":
            with open(path_to_suppress_sous_cycle, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                count_line = 1
                all_line_list = []
                for line in reader:
                    #print(line)
                    if count_line+1 not in thisx:
                        all_line_list.append(line)                  
                    count_line += 1
            print("nb_ligne_sous_cycle",len(all_line_list))

            with open(path_to_suppress_sous_cycle, 'w', newline='') as csv_new_file:

                    writer = csv.DictWriter(csv_new_file, fieldnames=dico_headers["sous_cycles"])
                    writer.writeheader()
                    count_line = 1
                    for line in all_line_list:
                        #print(line)
                        if count_line+1 not in thisx:
                            writer.writerow(line)                   
                        count_line += 1
                    print("count",count_line)

#       dico_x_axis_plots_deleted 
            data["all_paths"]["path_to_suppressed_sous_cycle_file"] = "delete"

            with open(dico_all_path["path_to_json_traitement"], 'w') as file:
                json.dump(data, file, indent = 6)

        print("Enregistrement effectué sans problème dans : ", "z_sous_cycle_apres_suppression.csv")
        

        with open(path_to_suppress_total_cycle, newline='') as csvfile_new_power:
            reader_new = csv.DictReader(csvfile_new_power)
            header_new = reader_new.fieldnames

        header_without_time_new = header_new[1:len(header_new)]
        #print(header_without_time_new)

        dataArray_new = genfromtxt(path_to_suppress_total_cycle, delimiter=',',usecols=tuple(header_without_time_new),names=True)
        #print(len(dataArray_new))
        x_val_new = arange(1, len(dataArray_new)+1, 1)
        dico_x_axis_plots_deleted["x_val_new"] = x_val_new
        y_val_10_new = dataArray_new[dataArray_new.dtype.names[0]]
        dico_y_axis_plots_deleted["y_val_new"] = y_val_10_new
        print(len(dico_x_axis_plots_deleted["x_val_new"]))
        print(len(dico_y_axis_plots_deleted["y_val_new"]))
        #dico_plot_cycle_puisance["plot0"].set_data(dico_x_axis_plots_deleted["x_val_new"],dico_y_axis_plots_deleted["y_val_new"])
        dico_fig_cycle_puissance["fig0"].clf()
        plot0 = dico_fig_cycle_puissance["fig0"].add_subplot(1,1,1)
        dico_plot_cycle_puisance["plot0"] = plot0
        dico_plot_cycle_puisance["plot0"].plot(dico_x_axis_plots_deleted["x_val_new"], dico_y_axis_plots_deleted["y_val_new"], label=dataArray_new.dtype.names[0])
        dico_plot_cycle_puisance["plot0"].set_title(dataArray_new.dtype.names[0])
        dico_fig_cycle_puissance["fig0"].canvas.draw_idle()


        with open(path_to_suppress_sous_cycle, newline='') as csvfile_sous_cycle_supprimer:
            reader = csv.DictReader(csvfile_sous_cycle_supprimer)
            header = reader.fieldnames
            dico_headers["sous_cycles"] = reader.fieldnames

        header_without_time = header[1:len(header)]

        dataArray_sous_cycle_new = genfromtxt(path_to_suppress_sous_cycle, delimiter=',',usecols=tuple(header_without_time),names=True)

        num_column = len(dataArray_sous_cycle_new.dtype.names)
        for i in range(num_column):
            dico_all_y_axis_plot_sous_cycle_puissance_deleted["y_val_new%s"%(i+1)] = dataArray_sous_cycle_new[dataArray_sous_cycle_new.dtype.names[i]]
        print(len(dico_x_axis_plots_deleted["x_val_new"]))
        print(len(dico_all_y_axis_plot_sous_cycle_puissance_deleted["y_val_new1"]))
        print(len(dico_all_y_axis_plot_sous_cycle_puissance_deleted["y_val_new2"]))
        count = 0
        for i in range(num_column):
            dico_all_figs_sous_cycle_puissance["fig%s"%(i+1)].clf()
            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)] = dico_all_figs_sous_cycle_puissance["fig%s"%(i+1)].add_subplot(1,1,1)

            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)].sharex(dico_plot_cycle_puisance["plot0"])
            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)].plot(dico_x_axis_plots_deleted["x_val_new"], dico_all_y_axis_plot_sous_cycle_puissance_deleted["y_val_new%s"%(i+1)], label=dataArray_sous_cycle_new.dtype.names[i])
            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)].set_title(dataArray_sous_cycle_new.dtype.names[i])
            dico_all_figs_sous_cycle_puissance["fig%s"%(i+1)].canvas.draw_idle()
            count+=1
        
        
    def default():


        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)
        

        data["all_paths"]["path_to_suppressed_cycle_file"] = "init"
        data["all_paths"]["path_to_suppressed_sous_cycle_file"] = "init"

        with open(dico_all_path["path_to_json_traitement"], 'w') as file:
                json.dump(data, file, indent = 6)

        try_not_for_loops()
        name_file = data["all_paths"]["name_of_the_interface_3_file"]
        name_file = name_file.split(".json")
        path_to_suppress_total_cycle = data["all_paths"]["path_to_folder"] + "z_" + name_file[0] + "_total_cycle_apres_suppression.csv"
        path_to_suppress_sous_cycle = data["all_paths"]["path_to_folder"] + "z_" + name_file[0] + "_sous_cycle_apres_suppression.csv"

        try:
            os.remove(path_to_suppress_total_cycle)
            os.remove(path_to_suppress_sous_cycle)
        except FileNotFoundError:
            print("Les paramètres actuelles sont déjà les paramètres par défault")

        print("Les fichiers de données avec sélections ont été supprimés")

#        dico_line_and_time.clear()
#        count = 1
#        with open(data["all_paths"]["path_to_converted_cycle_puissance"], newline='') as csvfile:
#            reader = csv.DictReader(csvfile)
#            for line in reader:
#                dico_line_and_time["%s"%(count)] = line["Time"]
#                count+=1
#
#        with open(data["all_paths"]["path_to_converted_cycle_puissance"], newline='') as csvfile_init_power:
#            reader_init = csv.DictReader(csvfile_init_power)
#            header_init = reader_init.fieldnames
#
#        header_without_time_new = header_init[1:len(header_init)]
#        print(header_without_time_new)
#
#        dataArray_init = genfromtxt(data["all_paths"]["path_to_converted_cycle_puissance"], delimiter=',',usecols=tuple(header_without_time_new),names=True)
#        print(len(dataArray_init))
#        x_val = arange(1, len(dataArray_init)+1, 1)
#        dico_x_axis_plots["x_val"] = x_val
#        y_val_10 = dataArray_init[dataArray_init.dtype.names[0]]
#        dico_y_axis_plot_cycle_puissance["y_val"] = y_val_10
#
#        #dico_plot_cycle_puisance["plot0"].set_data(dico_x_axis_plots_deleted["x_val_new"],dico_y_axis_plots_deleted["y_val_new"])
#        dico_fig_cycle_puissance["fig0"].clf()
#        plot0 = dico_fig_cycle_puissance["fig0"].add_subplot(1,1,1)
#        dico_plot_cycle_puisance["plot0"] = plot0
#        dico_plot_cycle_puisance["plot0"].plot(dico_x_axis_plots["x_val"], dico_y_axis_plot_cycle_puissance["y_val"], label=dataArray_init.dtype.names[0])
#        dico_plot_cycle_puisance["plot0"].set_title(dataArray_init.dtype.names[0])
#        dico_fig_cycle_puissance["fig0"].canvas.draw_idle()
#
#
#        with open(data["all_paths"]["path_to_sous_cycle_data_interface_Part_2"], newline='') as csvfile_sous_cycle_init:
#            reader = csv.DictReader(csvfile_sous_cycle_init)
#            header = reader.fieldnames
#            dico_headers["sous_cycles"] = reader.fieldnames
#
#        header_without_time = header[1:len(header)]
#
#        dataArray_sous_cycle = genfromtxt(data["all_paths"]["path_to_sous_cycle_data_interface_Part_2"], delimiter=',',usecols=tuple(header_without_time),names=True)
#
#        num_column = len(dataArray_sous_cycle.dtype.names)
#        for i in range(num_column):
#            dico_all_y_axis_plot_sous_cycle_puissance_deleted["y_val_new%s"%(i+1)] = dataArray_sous_cycle[dataArray_sous_cycle.dtype.names[i]]
#        
#        count = 0
#        for i in range(num_column):
#            dico_all_figs_sous_cycle_puissance["fig%s"%(i+1)].clf()
#            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)] = dico_all_figs_sous_cycle_puissance["fig%s"%(i+1)].add_subplot(1,1,1)
#
#            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)].sharex(dico_plot_cycle_puisance["plot0"])
#            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)].plot(dico_x_axis_plots["x_val"], dico_all_y_axis_plot_sous_cycle_puissance["y_val_%s"%(i+1)], label=dataArray_sous_cycle.dtype.names[i])
#            dico_all_plots_sous_cycle_puissance["plot%s"%(i+1)].set_title(dataArray_sous_cycle.dtype.names[i])
#            dico_all_figs_sous_cycle_puissance["fig%s"%(i+1)].canvas.draw_idle()
#            count+=1
#
#        
#        name_file = data["all_paths"]["name_of_the_interface_3_file"]
#        name_file = name_file.split(".json")
#        path_to_suppress_total_cycle = data["all_paths"]["path_to_folder"] + "z_" + name_file[0] + "_total_cycle_apres_suppression.csv"
#        path_to_suppress_sous_cycle = data["all_paths"]["path_to_folder"] + "z_" + name_file[0] + "_sous_cycle_apres_suppression.csv"
#
#       
#
#        try_not_for_loops()

        

    def span_select_function_zoom(x_min,x_max):
        print(dico_x_axis_plots["x_val"])
        #print("x_min,x_max : ",x_min,x_max)
        indmin, indmax = searchsorted(dico_x_axis_plots["x_val"], (x_min, x_max))
        #print("indmin : ",indmin )
        #print("indmax : ",indmax )
        indmax = min(len(dico_x_axis_plots["x_val"]) - 1, indmax)
        print("indmax et idmin: ",indmax, indmin)
        dico_plot_cycle_puisance["plot0"].set_xlim([indmin, indmax])

        thisx = dico_x_axis_plots["x_val"][indmin:indmax]
        print("thisx : ",thisx)
        thisy = dico_y_axis_plot_cycle_puissance["y_val_10"][indmin:indmax]
        #print("thisy : ",thisy)
#            line2.set_data(thisx, thisy)
#            fig2.set_xlim(thisx[0], thisx[-1])
#            fig2.set_ylim(thisy.min(), thisy.max())
        dico_fig_cycle_puissance["fig0"].canvas.draw_idle()
        #print("c_[thisx, thisy] : ",c_[thisx, thisy])

        # save
        #savetxt("text.out", c_[thisx, thisy])

        #with open(dico_all_path["path_to_sous_cycle_data_interface_Part_2"], newline='') as csvfile:
        #    reader = csv.DictReader(csvfile)
        #    count_line = 1
        #    with open(dico_all_path["path_to_folder"] + "z_total_cycle_apres_suppression.csv", 'w', newline='') as csv_new_file:
#
        #        writer = csv.DictWriter(csv_new_file, fieldnames=dico_headers["sous_cycles"])
        #        writer.writeheader()
#
        #        for line in reader:
        #            #print(line)
        #            if count_line not in thisx:
        #                writer.writerow(line)                    
        #            count_line += 1
#
##
        print("Le graphique est supposé être zoomer")

    def dezoomer():
        
        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)
        #print(dico_x_axis_plots["x_val"][0],dico_x_axis_plots["x_val"][len(dico_x_axis_plots["x_val"])-1])
        dico_plot_cycle_puisance["plot0"].set_xlim([float(data["Valeur_initiale_x_zoom"]),float(data["valeur_finale_x_zoom"])])
        dico_fig_cycle_puissance["fig0"].canvas.draw_idle()

    def delete_selected_part_of_plot():
        print("delete yeah")
#
        span = SpanSelector(dico_plot_cycle_puisance["plot0"], span_select_function, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'))

        dico_selection["int1"] = dico_canvas_cycle_puissance["canvas"].mpl_connect('key_press_event', span)
        #dico_canvas_cycle_puissance["canvas"].mpl_disconnect(cid)
        print("int1",dico_selection)


    def zoom_to_selected_part_of_plot():
        span = SpanSelector(dico_plot_cycle_puisance["plot0"], span_select_function_zoom, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='green'))

        dico_selection["int2"] = dico_canvas_cycle_puissance["canvas"].mpl_connect('key_press_event', span)
        #dico_canvas_cycle_puissance["canvas"].mpl_disconnect(cid)
        print("int2",dico_selection)

    def let_go_selection():
        print(dico_selection)
        #dico_canvas_cycle_puissance["canvas"].mpl_disconnect(dico_selection["int1"])
        #dico_canvas_cycle_puissance["canvas"].mpl_disconnect(dico_selection["int2"])
        dico_canvas_cycle_puissance["canvas"].mpl_disconnect(dico_selection_mouse_coord["id"])

    def on_move(event):

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

        if event.inaxes:
            print("position en x : ",int(event.xdata))
            try:
                print("Temps : ",dico_line_and_time[str(int(event.xdata))])
            except KeyError:
                print("aucune donnée de puissance dans cette partie du graphique")
        
        #Load an image in the script
        #cam_1= Image.open("C:\\Users\\felix\\Desktop\\Design4\\Design_4\\interface_graphique\\Machine_demo\\3) traitement_donnes\\fichiers_enregistrements\\Itachi.webp")
        try:
            print("Image 1 : ",dico_format_cam["cam1"][dico_line_and_time[str(int(event.xdata))]])
            cam_1= Image.open(data["all_paths"]["path_camera_1"] + "\\"+dico_format_cam["cam1"][dico_line_and_time[str(int(event.xdata))]])
            #Resize the Image using resize method
            resized_image= cam_1.resize((500,300), Image.Resampling.LANCZOS)
            the_frame.new_image= new_image = ImageTk.PhotoImage(resized_image,master=the_frame)

            #Add image to the Canvas Items
            dico_canvas_cam["cam1"].create_image(0,0, anchor=NW, image=new_image)
        except KeyError:
            print("Aucune image 1 associée")

        except TypeError:
            print("à l'extérieur du graphique")

        #Load an image in the script
        #cam_2= Image.open("C:\\Users\\felix\\Desktop\\Design4\\Design_4\\interface_graphique\\Machine_demo\\3) traitement_donnes\\fichiers_enregistrements\\Itachi.webp")
        try:
            print("Image 2 : ",dico_format_cam["cam1"][dico_line_and_time[str(int(event.xdata))]])
            cam_2= Image.open(data["all_paths"]["path_camera_2"] + "\\"+dico_format_cam["cam2"][dico_line_and_time[str(int(event.xdata))]])

            #Resize the Image using resize method
            resized_image= cam_2.resize((500,300), Image.Resampling.LANCZOS)
            the_frame.new_image_2= new_image_2 = ImageTk.PhotoImage(resized_image,master=the_frame)

            #Add image to the Canvas Items
            dico_canvas_cam["cam2"].create_image(0,0, anchor=NW, image=new_image_2)
        except KeyError:
            print("Aucune image 2 associée")
        
        except TypeError:
            print("à l'extérieur du graphique")

        try:
            gps_value = dico_gps[dico_line_and_time[str(int(event.xdata))]]
            print("GPS : ", gps_value)
            dico_entry_gps["gps"].delete(0,END)
            dico_entry_gps["gps"].insert(0,gps_value)
        except KeyError:
            print("Aucune position GPS associée")
        
        except TypeError:
            print("à l'extérieur du graphique")



    def get_coord():
        dico_selection_mouse_coord["id"] = dico_canvas_cycle_puissance["canvas"].mpl_connect('motion_notify_event', on_move)



    def get_path_pictures():

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

        if data["photo_loader"] == "non":

            folder = fd.askdirectory(title= "Sélectionner le dossier des photos (FluxVideo)", initialdir=dico_all_path["Path_to_machine_folder"] + "\\donnees_recoltees_machine")
            print(folder)

            data["all_paths"]["path_fluxVideo"] = folder
            data["all_paths"]["path_camera_1"] = folder + "\\Camera1"
            data["all_paths"]["path_camera_2"] = folder + "\\Camera2"

            with open(dico_all_path["path_to_json_traitement"], 'w') as file:
                json.dump(data, file, indent = 6)

            dico_picture_cam_1 = {}
            for picture in glob.glob(data["all_paths"]["path_camera_1"]+ "\\*.jpg"):
                only_name = picture.split("\\")
                without_extention = only_name[len(only_name)-1].split(".")
                #print(without_extention[0:len(without_extention)-1])
                #print(".".join(without_extention[0:len(without_extention)-1]))
                without_name = ".".join(without_extention[0:len(without_extention)-1]).split("Camera1_")
                dico_picture_cam_1[without_name[1]] = only_name[len(only_name)-1]

            dico_picture_cam_2 = {}
            for picture in glob.glob(data["all_paths"]["path_camera_2"]+ "\\*.jpg"):
                only_name = picture.split("\\")
                without_extention = only_name[len(only_name)-1].split(".")
                #print(without_extention[0:len(without_extention)-1])
                #print(".".join(without_extention[0:len(without_extention)-1]))
                without_name = ".".join(without_extention[0:len(without_extention)-1]).split("Camera2_")
                dico_picture_cam_2[without_name[1]] = only_name[len(only_name)-1]

        elif data["photo_loader"] == "oui":

            dico_picture_cam_1 = {}
            for picture in glob.glob(data["all_paths"]["path_camera_1"]+ "\\*.jpg"):
                only_name = picture.split("\\")
                without_extention = only_name[len(only_name)-1].split(".")
                #print(without_extention[0:len(without_extention)-1])
                #print(".".join(without_extention[0:len(without_extention)-1]))
                without_name = ".".join(without_extention[0:len(without_extention)-1]).split("Camera1_")
                dico_picture_cam_1[without_name[1]] = only_name[len(only_name)-1]

            dico_picture_cam_2 = {}
            for picture in glob.glob(data["all_paths"]["path_camera_2"]+ "\\*.jpg"):
                only_name = picture.split("\\")
                without_extention = only_name[len(only_name)-1].split(".")
                #print(without_extention[0:len(without_extention)-1])
                #print(".".join(without_extention[0:len(without_extention)-1]))
                without_name = ".".join(without_extention[0:len(without_extention)-1]).split("Camera2_")
                dico_picture_cam_2[without_name[1]] = only_name[len(only_name)-1]


        dico_format_cam["cam1"] = dico_picture_cam_1
        dico_format_cam["cam2"] = dico_picture_cam_2
        #print(dico_format_cam)


        data["photo_loader"] = "oui"
        with open(dico_all_path["path_to_json_traitement"], 'w') as file:
            json.dump(data, file, indent = 6)

        print("caméra importées")

    def get_gps_file():

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

        if data["gps_loader"] == "non":
            filetypes = (('text files', '*.csv'),('All files', '*.*'))
            data_csv = fd.askopenfilename(title='Sélectioner le fichier des données GPS',initialdir=dico_all_path["Path_to_machine_folder"] + "\\donnees_recoltees_machine",filetypes=filetypes)
            list_str = data_csv.split("/")
            only_name = list_str[len(list_str)-1]

            #print(data_csv)
            #print(only_name)
            data["all_paths"]["path_to_gps_file"] = data_csv

            data["gps_loader"] = "oui"
            with open(dico_all_path["path_to_json_traitement"], 'w') as file:
                json.dump(data, file, indent = 6)

            with open(data["all_paths"]["path_to_gps_file"], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                header = reader.fieldnames
                for line in reader:
                    dico_gps[line[header[0]]] = line[header[1]]

        elif data["photo_loader"] == "oui":
            with open(data["all_paths"]["path_to_gps_file"], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                header = reader.fieldnames
                for line in reader:
                    dico_gps[line[header[0]]] = line[header[1]]

        print("gps importé")

    def close_win_export_calculator(win,obj_entry):
        time_stamp_calculator = float(obj_entry.get())
        win.destroy()
        print(time_stamp_calculator)

        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

        name_file = data["all_paths"]["name_of_the_interface_3_file"]
        name_file = name_file.split(".json")

        path_to_suppress_total_cycle = data["all_paths"]["path_to_folder"] + "z_" + name_file[0] + "_total_cycle_apres_suppression.csv"
        

        files = [('csv', '*.csv')]
        power_file = fd.asksaveasfile(title="Enrgistrer le fichier de cycle de puissance formaté pour le calculateur",initialfile = "cycle_puissance",initialdir=dico_all_path["Path_to_machine_folder"] + "\\fichier_pour_calculateur",filetypes = files, defaultextension = files)
        list_str = power_file.name.split("/")
        only_name = list_str[len(list_str)-1]

        print(power_file.name)
        print(type(power_file.name))
        print(str(power_file.name))


        if data["all_paths"]["path_to_suppressed_cycle_file"] == "init":
            list_line_csv = []
            dico_for_calculator = {}
            with open(data["all_paths"]["path_to_converted_cycle_puissance"], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                header = reader.fieldnames
                for line in reader:
                    if float(line[header[1]]) < 0:
                        list_line_csv.append({"Puissance":line[header[1]],"recuperation":"x","duree":"%s"%(time_stamp_calculator)})
                    else:
                        list_line_csv.append({"Puissance":line[header[1]],"recuperation":" ","duree":"%s"%(time_stamp_calculator)})

            


            with open(power_file.name, 'w', newline='') as csv_new_file:

                writer = csv.DictWriter(csv_new_file, fieldnames=["Puissance", "recuperation", "duree"])
                writer.writeheader()

                for line in list_line_csv:
                    writer.writerow(line)                   
                
            print("Enregistrement effectué sans problème dans : ", only_name)
            print("non supress")
#
#        

        elif data["all_paths"]["path_to_suppressed_cycle_file"] == "delete":

            list_line_csv = []
            dico_for_calculator = {}
            with open(path_to_suppress_total_cycle, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                header = reader.fieldnames
                
                for line in reader:
                    if float(line[header[1]]) < 0:
                        list_line_csv.append({"Puissance":line[header[1]],"recuperation":"x","duree":"%s"%(time_stamp_calculator)})
                    else:
                        list_line_csv.append({"Puissance":line[header[1]],"recuperation":" ","duree":"%s"%(time_stamp_calculator)})

            


            with open(power_file.name, 'w', newline='') as csv_new_file:

                writer = csv.DictWriter(csv_new_file, fieldnames=["Puissance", "recuperation", "duree"])
                writer.writeheader()
                
                for line in list_line_csv:
                    writer.writerow(line)                   
                
            print("Enregistrement effectué sans problème dans : ", only_name)
            print("supress")

    def export_data_for_calculator():


        with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)


        list_nb_data_second = [0]
        list_tuple_time_without_sec_and_sec = [(None,None)]
        with open(data["all_paths"]["path_to_converted_cycle_puissance"], newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                header = reader.fieldnames
                count = 1
                index = 0
                for line in reader:
                    sep = line["Time"].split(".")
                    all_but_second = ".".join(sep[0:len(sep)-1])
                    only_second = sep[2]
                    #print(all_but_second,only_second)
                    #print(list_tuple_time_without_sec_and_sec[len(list_tuple_time_without_sec_and_sec)-1][0])
                    #print(list_tuple_time_without_sec_and_sec[len(list_tuple_time_without_sec_and_sec)-1][1])
                    if (list_tuple_time_without_sec_and_sec[len(list_tuple_time_without_sec_and_sec)-1][0] == all_but_second) and (list_tuple_time_without_sec_and_sec[len(list_tuple_time_without_sec_and_sec)-1][1] == only_second):
                        list_tuple_time_without_sec_and_sec.append((all_but_second,only_second))
                        count += 1
                        list_nb_data_second[index] = count
                        #print("yeep")
                    
                    else:
                        list_tuple_time_without_sec_and_sec.append((all_but_second,only_second))
                        count = 1
                        index += 1
                        list_nb_data_second.append(count)

                        #print("change")

        print(list_nb_data_second)
        total_for_mean = len(list_nb_data_second)-3
        val_sum = list_nb_data_second[2]
        for number in list_nb_data_second[2:len(list_nb_data_second)-1]:
            val_sum += number
        mean = val_sum/total_for_mean

        

#        the_frame_level_2 = Toplevel(the_frame, padx=125, pady=130)
#        the_frame_level_2.minsize(width=700,height=400)
#
#        the_text_frame = Frame(the_frame_level_2)
#        the_text_frame.grid(row = 0, column = 0, padx = 30,pady =10)
#
#        txt = Text(the_text_frame)
#        txt.pack(expand = True, fill = "both")
#
#        scrolly = Scrollbar(the_text_frame)
#        scrolly.config(command = txt.yview)
#        scrolly.pack(side=RIGHT, fill=Y)
#        txt["yscrollcommand"] = scrolly.set

        the_frame_level_2 = Toplevel(the_frame, padx=125, pady=130)
        the_frame_level_2.minsize(width=700,height=400)

        txt = Text(the_frame_level_2)
        txt.grid(row = 0, column = 0)

        scrolly = Scrollbar(the_frame_level_2, orient=VERTICAL)
        scrolly.grid(row = 0, column = 1, sticky="w")        
        

        txt.insert(END, "liste de la quantité de données reçu par seconde (sans la première et la dernière)")
        txt.insert(END,"\n")
        txt.insert(END,"\n")
        txt.insert(END, "valeur moyenne :     %s"%(mean))
        txt.insert(END,"\n")
        txt.insert(END,"\n")
        txt.insert(END, "La valeur d'échantillonnage (de durée par échantillon) pour le calculateur est  donc de 1/%s :     %s seconde(s) par ligne de cycle de puissance"%(round(mean),1/round(mean)))
        txt.insert(END,"\n")
        txt.insert(END,"\n")
        txt.insert(END, list_nb_data_second[2:len(list_nb_data_second)-1])
        txt.insert(END,"\n")

        scrolly.config(command = txt.yview)
        
        txt["yscrollcommand"] = scrolly.set

        label_entry = Label(the_frame_level_2, text="valeur de durée:")
        manual_entry = Entry(the_frame_level_2,width=30)
        manual_entry.insert(0,str(1/round(mean)))
        close_button = Button(the_frame_level_2, text="Terminer", command= lambda : close_win_export_calculator(the_frame_level_2,manual_entry))

        label_entry.grid(row = 1, column = 2, padx = 30,pady =10)
        manual_entry.grid(row = 2, column = 2, padx = 30,pady =10)
        close_button.grid(row = 0, column = 2)





    def end_script():
        exit()

    windows_height_x = int(GetSystemMetrics(0))-20
    windows_height_y = int(GetSystemMetrics(1))-150
    windows_scrol_height = int(GetSystemMetrics(1))

    today = datetime.datetime.now()
    today_format = today.strftime("%b_%d_%Y")
    end_default_file_name = today_format + ".json"

    the_path = find_the_config_file_path(end_default_file_name)

    dico_all_path["path_to_json_interface_part_1"] = the_path[0]
    dico_all_path["path_to_json_interface_part_2"] = the_path[1]
    dico_all_path["path_to_json_traitement"] = the_path[2]
    dico_all_path["path_to_taille_interface_3"] = the_path[3]
    dico_all_path["path_to_converted_data_interface_Part_1"] = the_path[4]
    dico_all_path["path_to_sous_cycle_data_interface_Part_2"] = the_path[5]
    dico_all_path["path_to_converted_cycle_puissance"] = the_path[6]
    dico_all_path["path_to_folder"] = the_path[7]
    dico_all_path["Path_to_machine_folder"] = the_path[8]
    dico_all_path["Path_to_interface_folder"] = the_path[9]

# Ces deux dictionnaires enregistrent un inidice indiquant si un fichier de supression est utilisé ou pas.
# Si le fichier initial doit être utilisé, l'indice est "init" si le fichier de données supprimés, "delete"
    dico_all_path["path_to_suppressed_cycle_file"] = "init"
    dico_all_path["path_to_suppressed_sous_cycle_file"] = "init"

    print(dico_all_path["path_to_json_interface_part_1"])
    print(dico_all_path["path_to_json_interface_part_2"])
    print(dico_all_path["path_to_json_traitement"])
    print(dico_all_path["path_to_taille_interface_3"])
    print(dico_all_path["path_to_converted_data_interface_Part_1"])
    print(dico_all_path["path_to_sous_cycle_data_interface_Part_2"])
    print(dico_all_path["path_to_converted_cycle_puissance"])
    print(dico_all_path["path_to_folder"])
    print(dico_all_path["Path_to_machine_folder"])
    print(dico_all_path["Path_to_interface_folder"])



    try:
        with open(dico_all_path["path_to_json_interface_part_1"], 'r') as f:
            print("ok")

    except json.JSONDecodeError:
        assert 1==2, \
            "Il n'y a aucune interface détectée associée à ce fichier (.json dans 1) setup donnees)"

    except FileNotFoundError:
        assert 1==2, \
            "Il n'y a aucune interface détectée associée à ce fichier (.json dans 1) setup donnees)"

    try:
        with open(dico_all_path["path_to_json_interface_part_2"], 'r') as f:
            print("ok")

    except json.JSONDecodeError:
        assert 1==2, \
            "Il n'y a aucune interface détectée associée à ce fichier (.json dans 2) calcul_puissance)"

    except FileNotFoundError:
        assert 1==2, \
            "Il n'y a aucune interface détectée associée à ce fichier (.json dans 2) calcul_puissance)"

    try:
        with open(dico_all_path["path_to_converted_data_interface_Part_1"], 'r') as f:
            print("ok")

    except json.JSONDecodeError:
        assert 1==2, \
            "Il n'y a aucune donnée convertie en provenance des capteurs"

    except FileNotFoundError:
        assert 1==2, \
            "Il n'y a aucune donnée convertie en provenance des capteurs"


    try:
        with open(dico_all_path["path_to_sous_cycle_data_interface_Part_2"], 'r') as f:
            print("ok")

    except json.JSONDecodeError:
        assert 1==2, \
            "Il n'y a aucune donnée de calcul de puissance enregistrée"

    except FileNotFoundError:
        assert 1==2, \
            "Il n'y a aucune donnée de calcul de puissance enregistrée"


    try:

        with open(dico_all_path["path_to_json_traitement"], 'r') as f:
            data = json.load(f)
            dico = {'all_paths': dico_all_path,"calculs":"non", "affichage":"non", "photo_loader":"non","gps_loader":"non"}

        with open(dico_all_path["path_to_json_traitement"], 'w') as file:
            json.dump(dico, file, indent = 6)
            print('yes')

    except json.JSONDecodeError:
        print("fichier vide, introuvable ou corrompu!")
        name_only = dico_all_path["path_to_json_traitement"].split("\\")
        print("Création d'un nouveau fichier appelé : %s"%(name_only[len(name_only)-1]))
        dico = {'all_paths': dico_all_path,"calculs":"non", "affichage":"non","photo_loader":"non","gps_loader":"non"}

        with open(dico_all_path["path_to_json_traitement"], 'w') as file:
            json.dump(dico, file, indent = 6)

    except FileNotFoundError:
        print("fichier vide ou introuvable!")
        name_only = dico_all_path["path_to_json_traitement"].split("\\")

        print("Création d'un nouveau fichier appelé : %s"%(name_only[len(name_only)-1]))
        dico = {'all_paths': dico_all_path,"calculs":"non", "affichage":"non","photo_loader":"non","gps_loader":"non"}

        with open(dico_all_path["path_to_json_traitement"], 'w') as file:
            json.dump(dico, file, indent = 6)

    try:
        with open(dico_all_path["path_to_taille_interface_3"], 'r') as f:
            print("ok")

    except json.JSONDecodeError:
        dico_taille = {'windows_width': windows_height_x,
                    'windows_length': windows_height_y,
                    'windows_scrol_height': windows_height_y,}

        with open(dico_all_path["path_to_taille_interface_3"], 'w') as file:
            json.dump(dico_taille, file, indent = 6)

    except FileNotFoundError:
        dico_taille = {'windows_width': windows_height_x,
                    'windows_length': windows_height_y,
                    'windows_scrol_height': windows_scrol_height}

        with open(dico_all_path["path_to_taille_interface_3"], 'w') as file:
            json.dump(dico_taille, file, indent = 6)

    with open(dico_all_path["path_to_json_traitement"], "r") as f:
        data = json.load(f)

    with open(dico_all_path["path_to_json_traitement"], "r") as f:
            data = json.load(f)

    data["all_paths"]["path_to_json_interface_part_1"] = dico_all_path["path_to_json_interface_part_1"]
    data["all_paths"]["path_to_json_interface_part_2"] = dico_all_path["path_to_json_interface_part_2"]
    data["all_paths"]["path_to_json_traitement"] = dico_all_path["path_to_json_traitement"]
    data["all_paths"]["path_to_taille_interface_3"] = dico_all_path["path_to_taille_interface_3"]
    data["all_paths"]["path_to_converted_data_interface_Part_1"] = dico_all_path["path_to_converted_data_interface_Part_1"]
    data["all_paths"]["path_to_sous_cycle_data_interface_Part_2"] = dico_all_path["path_to_sous_cycle_data_interface_Part_2"]
    data["all_paths"]["path_to_converted_cycle_puissance"] = dico_all_path["path_to_converted_cycle_puissance"]
    data["all_paths"]["path_to_folder"] = dico_all_path["path_to_folder"]
    data["all_paths"]["Path_to_machine_folder"] = dico_all_path["Path_to_machine_folder"]
    data["all_paths"]["Path_to_interface_folder"] = dico_all_path["Path_to_interface_folder"]

# Ces deux dictionnaires enregistrent un inidice indiquant si un fichier de supression est utilisé ou pas.
# Si le fichier initial doit être utilisé, l'indice est "init" si le fichier de données supprimés, "delete"
    data["all_paths"]["path_to_suppressed_cycle_file"] = "init"
    data["all_paths"]["path_to_suppressed_sous_cycle_file"] = "init"

    with open(dico_all_path["path_to_json_traitement"], 'w') as file:
            json.dump(data, file, indent = 6)

    tk = Tk()
    tk.title("Python Tkinter")
    with open(data["all_paths"]["path_to_taille_interface_3"], 'r') as f:
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

    main_canvas.configure(yscrollcommand=scroll_v.set)
    main_canvas.bind("<Configure>",lambda e: main_canvas.configure(scrollregion= main_canvas.bbox("all")))

    second_frame = Frame(main_canvas, width=largeur, height=hauteur)
    main_canvas.create_window((0,0), window=second_frame, anchor="nw")
    with open(data["all_paths"]["path_to_taille_interface_3"], 'r') as f:
        data_2 = json.load(f)
    second_frame.configure(height=data_2["windows_scrol_height"])

    the_frame = second_frame

    selection_bar = Menu(tk)
    filemenu = Menu(selection_bar, tearoff=0)
    selection_bar.add_cascade(label="Fichier", menu=filemenu)
    #filemenu.add_command(label="plot_graphique", command=plot_graph)
    filemenu.add_command(label="Ouvrir...", command=select_file)
    #filemenu.add_command(label="Enregistrer", command=get_all_entry)
    filemenu.add_command(label="Enregistrer sous...", command=save_in_to_file)
    filemenu.add_separator()
    filemenu.add_command(label="dossier des photos", command=get_path_pictures)
    filemenu.add_separator()
    filemenu.add_command(label="importer gps", command=get_gps_file)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=end_script)

    filemenu2 = Menu(selection_bar, tearoff=0)
    selection_bar.add_cascade(label="dimentions", menu=filemenu2)
    filemenu2.add_command(label="taille de la fenêtre", command= lambda : adjust_windows(data["all_paths"]["path_to_taille_interface_3"],windows_height_x,windows_height_y))
    filemenu2.add_command(label="longueur du scrollbar", command= lambda : ajust_height_scorlbar(data["all_paths"]["path_to_taille_interface_3"], windows_scrol_height))

    filemenu3 = Menu(selection_bar, tearoff=0)
    selection_bar.add_cascade(label="donnees", menu=filemenu3)
    filemenu3.add_command(label="Traiter les données", command=try_not_for_loops)
    filemenu3.add_separator()
    filemenu3.add_command(label="Les graphiques des données reconvertie en unité réel (brut)", command=plot_graph_converted)
    filemenu3.add_command(label="Les graphiques des données de puissance (brut)", command=plot_graph_sous_cycle)
    filemenu3.add_separator()
    filemenu3.add_command(label="Exporter vers calculateur", command=export_data_for_calculator)

    
    #filemenu3.add_separator()
    #filemenu3.add_command(label="Importer le can", command= lambda : convert_all_data(namefile[1]))

    tk.config(menu=selection_bar)
    save_all_manual_entry_button = Button(the_frame, text="Calculer", command=calculate_cycle_power)
    save_all_manual_entry_button.place(x=1200,y=60)
    delete_section_plot = Button(the_frame, text="Supprimer", command=delete_selected_part_of_plot)
    delete_section_plot.place(x=1350,y=380)
    zoom_section_plot = Button(the_frame, text="Zoomer", command=zoom_to_selected_part_of_plot)
    zoom_section_plot.place(x=1350,y=410)
    let_go_section_plot = Button(the_frame, text="Relacher", command=let_go_selection)
    let_go_section_plot.place(x=1350,y=350)
    dezoom = Button(the_frame, text="Dezoomer", command=dezoomer)
    dezoom.place(x=1350,y=440)
    par_def = Button(the_frame, text="paramètres par défaut", command=default)
    par_def.place(x=1350,y=470)
    par_def = Button(the_frame, text="position souris", command=get_coord)
    par_def.place(x=1350,y=500)

    #validate_button = Button(the_frame, text="Valider", command= lambda : convert_all_data(namefile[1]))
    #validate_button.place(x=1200,y=20)
    tk.mainloop()

if __name__ == "__main__":
    #print("Cette fonction ne devrait être lancé que par le bouton de l'interface graphique")
    interface_part_3("essai_2_29_nov.json","essai_2_29_nov_test.json")
    