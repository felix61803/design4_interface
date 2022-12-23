import datetime
import json
import time
import csv

#from pynput import keyboard
import msvcrt

puissance_file = "cycle_puissance.json"
puissance_file_csv = "cycle_puissance_essai.csv"

with open(puissance_file_csv, 'w', newline='') as csvfile:
    fieldnames = ['Puissance', 'recuperation','duree']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'Puissance': '1800', 'recuperation': ' ', 'duree': '345'})
    writer.writerow({'Puissance': '4560', 'recuperation': 'x', 'duree': '23'})
    writer.writerow({'Puissance': '1456', 'recuperation': ' ', 'duree': '45'})
    writer.writerow({'Puissance': '234',  'recuperation': 'x', 'duree': '456'})
    writer.writerow({'Puissance': '453',  'recuperation': 'x', 'duree': '435'})
    writer.writerow({'Puissance': '456',  'recuperation': ' ', 'duree': '34'})
    writer.writerow({'Puissance': '1254', 'recuperation': ' ', 'duree': '37'})
    writer.writerow({'Puissance': '456',  'recuperation': ' ', 'duree': '98'})
    writer.writerow({'Puissance': '345',  'recuperation': ' ', 'duree': '231'})
    writer.writerow({'Puissance': '4563', 'recuperation': ' ', 'duree': '134'})