#This is much different than the original API script used in Lab 5 and 9

import requests         #We need requests to send GET messages to PokeAPI
import image_lib            #We need the image library for saving and downloading images
import os
 
POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'             #The URL for PokeAPI

#The Main function runs all of the other functions. The content provided in the parameters are default values if nothing is provided
def main():
    poke_info = get_pokemon_info("Snorlax")             #Get Pokemon info about Snorlax
    poke_info = get_pokemon_info(123)
    names = get_pokemon_names()
    download_pokemon_artwork('Hydreigon', r'C:\Windows')        #Download the artwork for Hydreigon for example
    return
 
def get_pokemon_info(pokemon_name):
    """Gets information about a specified Pokemon from the PokeAPI.
 
    Args:
        pokemon_name (str): Pokemon name (or Pokedex number)
 
    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    pokemon_name = str(pokemon_name).strip().lower()  #A pokemon's name will be stripped of whitespace and lowercased for further use (string form)
 

    url = POKE_API_URL + pokemon_name       #The total URL is the PokeAPI url plus the Pokemon's name
 
    print(f'Getting information for {pokemon_name}...', end='')
    resp_msg = requests.get(url)       #Send our request to PokeAPI
 

    if resp_msg.status_code == requests.codes.ok:       #If the connection was okay
        print('success')
        return resp_msg.json()                          #Return a dictionary of the information
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')         
        return
    

def get_pokemon_names(offset=0, limit=100000):

    """Summary: Gets the total amount of Pokemon's names
    It will gather all of the Pokemon in existance and put it in a list
    for further use

    Args:
        None


    Returns:
        list: Pokemon names
    """

    query_params = {
        'offset' : offset,          #Offset will limit down to 0
        'limit' : limit             #Limit of Pokemon selected will be 10'000 (so basically get all Pokemon)
        }
    
    print(f'Getting list of Pokemon names ...', end='')

    resp_msg = requests.get(POKE_API_URL, params=query_params)      #Send our request to get em' all with the url and the query parameters

    if resp_msg.status_code == requests.codes.ok:           #If the communication was okay
        pokemon_dict = resp_msg.json()                                  #Put the information in the dictionary
        pokemon_names_list = [p['name']for p in pokemon_dict['results']]        #We get each pokemon name through list iteration which goes through the data in each name value in the results and increments it
        return pokemon_names_list           #Return the total names
    else:
        print('Failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return



def download_pokemon_artwork(pokemon_name, save_dir):

    """Summary: For every Pokemon name we have discovered
    we must be able to get their images if the user desires so
    This function accomplishes this by examining the dictionary found
    by sending requests to PokeAPI

    Parameters:
        pokemon_name: A pokemon's name
        save_dir: The directory in which the image will be saved into

    Returns:
        image_path: Full path to the image
    """

    pokemon_info = get_pokemon_info(pokemon_name)   #Get info about the pokemon
    if pokemon_info is None:            #If the pokemon does not exist
        return
    
    artwork_url = pokemon_info['sprites']['other']['official-artwork']['front_default'] #Get the official artwork through the sprites key and move towards the front-default key

    image_bytes = image_lib.download_image(artwork_url)     #Download the image using the URL of the artwork
    if image_bytes is None:
        return
    

    file_ext = artwork_url.split('.')[-1]       #To get the file extension, we split the name by the . which indicates the start and end of a file name
    image_path = os.path.join(save_dir, f'{pokemon_name}.{file_ext}')       #For the image path, we just join the save directory with the pokemon's name and file extension

    if image_lib.save_image_file(image_bytes, image_path):          #If we successfully saved the file
        return image_path                               #Return the image path

if __name__ == '__main__':
    main()