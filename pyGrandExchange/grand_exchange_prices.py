import requests
import time
import json


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
    
    
    return json.dumps(items[str(item_id)], indent=4)


def get_item_by_name(item_name):
    
    """Returns the item info for the specified item name."""
    
    items = get_return_item_info() 
     
    for item in items:
        if item_name.lower() in items[item]['name'].lower():
            return json.dumps(items[item], indent=4)
        
            
print(get_item_by_id(4151))

print(get_item_by_name('Zul-andra teleport'))

''' example output:
{
    "examine": "A weapon from the Abyss.",
    "id": 4151,
    "members": true,
    "lowalch": 48000,
    "limit": 70,
    "value": 120001,
    "highalch": 72000,
    "icon": "Abyssal whip.png",
    "name": "Abyssal whip",
    "price": 1281075,
    "volume": 4248,
    "last": 1297502
}
'''           
                








