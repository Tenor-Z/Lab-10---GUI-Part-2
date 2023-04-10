from tkinter import *           #We need everything from tkinter in order to display our input box
from tkinter import ttk             #TTk helps with more advanced capabilities
import api                      #Api is the python file that grabs Pokemon info from the Pokemon API
import image_lib            #Image library is a library that will download, save and set images as the desktop background
import os                   #Os is needed for paths and Windows related stuff
import ctypes                   #Ctypes is needed to replace the Icons


script_path = os.path.abspath(__file__)         #Get the full path of the script
script_dir = os.path.dirname(script_path)           #Get the directory in which it resides in
image_cache_dir = os.path.join(script_dir, 'temp')        #To make the cache directory where downloaded images will be stored, combine the script directory with the folder name

#If the 'temp' folder does not exist in the working directory, simply create it
if not os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)

#Now we must create the main window
root = Tk()                     #Initialize the window function in Tkinter
root.title("Pokémon Viewer")        #Give it our title
root.minsize(600, 600)              #And set the minimum size to 600, 600

#Set the Process ID and use the icon associated for our window
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('PokeViewer')
icon_path = os.path.join(script_dir, 'poke.ico')

#In case the the window gets resized, then everything moves with it as well
#We only need to move column 0 since our content resides in that area
root.iconbitmap(icon_path)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


#Now that we have our window, we can create our frame, which can shape itself to match the size of the window
frame = ttk.Frame(root)                                                                 #Initalize our frame with the window we create
frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)                          #Keep our frame stuck in place (window can move but the frame cannot)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)


#Until we get a pokemon to view as the picture, load the default one for now
img_poke = PhotoImage(file=os.path.join(script_dir,'default.png'))  #Load the file into Python
lbl_poke_image = ttk.Label(frame,image=img_poke)        #Create its label and place it in its coordinates
lbl_poke_image.grid(row=0, column=0)


#Next, we must add our drop down list with pokemon names
pokemon_names_list = api.get_pokemon_names()                    #To get the list of Pokemon, use the function from the api script
cbox_poke_names = ttk.Combobox(frame, values=pokemon_names_list, state='readonly')      #Create a combobox with the value of our searched list (cannot be edited)
cbox_poke_names.set("Select a Pokemon")     #Set our default text
cbox_poke_names.grid(row=1, column=0, padx=10, pady=10)     #And place the coordinates


def handle_pokemon_sel(event):
    """Summary: A handler for Pokemon selection

    Args:
        None
    
    Parameters:
        Event - Replaces the value when a Pokemon is selected
    
    Returns:
        None
    """

    pokemon_name = cbox_poke_names.get()        #Get the name of the selected pokemon

    global image_path           #Global this so we can use the already defined variable
    image_path = api.download_pokemon_artwork(pokemon_name, image_cache_dir)        #Use the api function to download the official artwork along and save it in the cache directory


    if image_path is not None:      #If there actually is an image
        img_poke['file'] = image_path       #Just define the value of 'file' as the image path

    btn_get_info.state(['!disabled'])  #Enable the button

cbox_poke_names.bind('<<ComboboxSelected>>', handle_pokemon_sel)  #And bind the combobox with whatever was selected, displaying the image


def set_pokemon_background():  
    """Summary: Saves a Pokemon image as the background

    Returns:
        pokemon_background: A call to set the image as the background
    """

    pokemon_background = image_lib.set_desktop_background_image(image_path)     #Call the image library function to save the image as the desktop wallpaper
   
    return pokemon_background       #And return it



btn_get_info = ttk.Button(frame, text='Set as Desktop Image', command=set_pokemon_background, state=DISABLED)  #Create the button that responds to the set_pokemon_background
btn_get_info.grid(row=2, column=0, padx=10, pady=10)        #It is disabled by default




root.mainloop()