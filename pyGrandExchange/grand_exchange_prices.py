import requests
import time
import json
import pandas as pd
from tabulate import tabulate


def get_return_item_info():
    
    """Grabs all item info from the OSRS Grand Exchange API and returns it as a dictionary."""
    
    while True:
        try:
            response = requests.get('https://chisel.weirdgloop.org/gazproj/gazbot/os_dump.json')
            
            RETRIES = 5   # Number of retries before exiting the program.
            error = None  # Error message to print if we reach the maximum number of retries.
            
        except requests.exceptions.HTTPError as err:
            print(f"{5 - RETRIES}:Error getting JSON dump. Waiting 5 seconds before trying again...")
            RETRIES -= 1    # Decrement retries by 1
            time.sleep(5)  # Sleep for 5 seconds
            error = err
            continue
        
        finally:
            # If we've reached the maximum number of retries, exit the program.
            if RETRIES == 0:
                print(f"Maximum retries reached. Exiting...\n {error}")
                return exit()
            
            else:
                # For now, just pull the data once and finish.
                break
    full_dict = dict(response.json())
    
    return full_dict


def get_item_by_id(item_id):
    
    """Returns the item info for the specified item ID."""
    
    items = get_return_item_info()
    
    json_ = json.dumps(items[str(item_id)], indent=4)
    
    tabbed_json = tabulate_data(json_)
    
    return tabbed_json


def get_item_by_name(item_name):
    
    """Returns the item info for the specified item name."""
    
    items = get_return_item_info() 
     
    for item in items:
        
        try:
            if item_name.lower() == items[str(item)]['name'].lower():
                
                json_ = json.dumps(items[str(item)], indent=4)
                
                tabbed_json = tabulate_data(json_)
                
                return tabbed_json
            
            else:
                pass
        except KeyError:
            pass
        except TypeError:
            return "Item not found."
        

def tabulate_data(json_data):
    """Takes json data and turns it into a tabulated dataframe.
    """
    
    df = pd.read_json(json_data, orient='index').T  
    tab = tabulate(df, headers='keys', tablefmt='grid', showindex=False, maxcolwidths=10)
    
    return tab

def menu():
    
    from rich import print
    
    print('[red]Grand Exchange Price Lookup Tool[/red]')
    print('-' * 50)
    print('[green]Enter the [yellow underline]Item ID[/yellow underline] or '
          '[yellow underline]Item Name[/yellow underline] to lookup the price of an item.[/green]')
    print('[blue]Enter "exit" to exit the program.[/blue]')
    
    while True:
        user_input = input('Enter item ID or name: ')
        
        if user_input.lower() == 'exit':
            print('Exiting...')
            return exit()
        
        elif user_input.isdigit():
            print(get_item_by_id(user_input))
            
        else:
            print(get_item_by_name(user_input))
            
        continue
       
menu()        
                








