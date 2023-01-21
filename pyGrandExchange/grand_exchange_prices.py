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
            
    return dict(response.json())


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
        if item_name.lower() in items[item]['name'].lower():
            
            json_ = json.dumps(items[str(item)], indent=4)
            
            tabbed_json = tabulate_data(json_)
            
            return tabbed_json
        

def tabulate_data(json_data):
    """Takes json data and turns it into a tabulated dataframe.
    """
    
    df = pd.read_json(json_data, orient='index').T  
    tab = tabulate(df, headers='keys', tablefmt='grid', showindex=False, maxcolwidths=10)
    
    return tab
        
            
print(get_item_by_id(4151))                   # Change this ID to whatever you want.
print(get_item_by_name('Zul-andra teleport')) # Change this name to whatever you want.

''' example output:
+-----------+------+-----------+-----------+---------+---------+------------+----------+---------+---------+----------+---------+
| examine   |   id | members   |   lowalch |   limit |   value |   highalch | icon     | name    |   price |   volume |    last |
+===========+======+===========+===========+=========+=========+============+==========+=========+=========+==========+=========+
| A weapon  | 4151 | True      |     48000 |      70 |  120001 |      72000 | Abyssal  | Abyssal | 1281075 |     4248 | 1297502 |
| from the  |      |           |           |         |         |            | whip.png | whip    |         |          |         |
| Abyss.    |      |           |           |         |         |            |          |         |         |          |         |
+-----------+------+-----------+-----------+---------+---------+------------+----------+---------+---------+----------+---------+
'''           
                








