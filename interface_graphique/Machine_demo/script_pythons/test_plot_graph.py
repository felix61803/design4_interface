#import tkinter
#from tkinter import *
#from PIL import Image, ImageTk
#
##root = Tk()
##root.minsize(1500, 734)
##
### Create a photoimage object of the image in the path
##image1 = Image.open("C:\\Users\\felix\\Desktop\\Design4\\Design_4\\interface_graphique\\Machine_demo\\3) traitement_donnes\\fichiers_enregistrements\\Itachi.webp")
##image1.resize((50,20), Image.ANTIALIAS)
##test = ImageTk.PhotoImage(image1)
##
##label1 = tkinter.Label(image=test)
##label1.image = test
##
### Position image
##label1.place(x=0, y=0)
##root.mainloop()
##
#from tkinter import *
#from PIL import Image,ImageTk
##
###Create an instance of tkinter frame
#win = Tk()
#
##Set the geometry of tkinter frame
#win.minsize(1500,755)
#
##Create a canvas
#canvas= Canvas(win, width= 600, height= 400)
#canvas.place(x=50,y=0, width=600, height=400)
#
##Load an image in the script
#img= (Image.open("C:\\Users\\felix\\Desktop\\Design4\\Design_4\\interface_graphique\\Machine_demo\\3) traitement_donnes\\fichiers_enregistrements\\Itachi.webp"))
#
##Resize the Image using resize method
#resized_image= img.resize((300,205), Image.Resampling.LANCZOS)
#new_image= ImageTk.PhotoImage(resized_image)
#
##Add image to the Canvas Items
#canvas.create_image(10,10, anchor=NW, image=new_image)
#
#win.mainloop()
#
#
##https://matplotlib.org/stable/users/explain/event_handling.html
##https://matplotlib.org/stable/gallery/event_handling/coords_demo.html
#

print(round(2.5))
print(round(2.6))
print(round(2.51))