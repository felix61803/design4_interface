import os
import shutil
import numpy as np
import pandas as pd
import calendar
from datetime import datetime
from fpdf import FPDF

import matplotlib.pyplot as plt
from matplotlib import rcParams


def construct(path,nb_graph_by_page):
        
    # Construct data shown in document

    nb_graph_by_page_counter = 0
    pages_data = []
    temp = []
    
    all_graph_png = os.listdir(path)

    for fname in all_graph_png:
        # nombre de graphique par page
        if "cycle_puissance.png" not in fname:
            if nb_graph_by_page_counter == nb_graph_by_page:
                pages_data.append(temp)
                temp = []
                nb_graph_by_page_counter = 0

            temp.append(path + "\\" + fname)
            nb_graph_by_page_counter += 1

    return [*pages_data, temp]

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        
    def header(self):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`
        #self.image(r'C:\Users\felix\Desktop\Design4\Design_4\interface_graphique\Machine_manitou\script_pythons\asserts\logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, 'Rapport de consommation', 0, 1, 'R')
        self.ln(20)
        
    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, pictures):
        # Determine how many plots there are per page and set positions
        # and margins accordingly
        if len(pictures) == 3:
            self.image(pictures[0], 15, 25, self.WIDTH - 30)
            self.image(pictures[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
            self.image(pictures[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
        elif len(pictures) == 2:
            self.image(pictures[0], 15, 25, self.WIDTH - 30)
            self.image(pictures[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
        else:
            self.image(pictures[0], 15, 25, self.WIDTH - 30)

    def print_page(self, pictures):
        # Generates the report
        self.add_page()
        self.page_body(pictures)