
import webbrowser

from image_recognition import press_to

import os
import shutil
from config import quality,web_or_idm_defult_download_directrory,idm,need_anime_websites_SourceCodes_junk_file


def utf8_to_ascii(lines_array):
    try:
        decoded_lines = [line.encode('utf-8').decode('ascii', 'ignore') for line in lines_array]
        return decoded_lines
    except Exception as e:
        return f"An error occurred: {e}"
    
def replace_character_in_string(input_string, old_char, new_char):
    modified_string = input_string.replace(old_char, new_char)
    return modified_string

def replace_character_in_list_of_strings(list_of_strings, old_char_code, new_char):
    old_char = chr(old_char_code)
    modified_list = []

    for string in list_of_strings:
        modified_string = string.replace(old_char, new_char)
        modified_list.append(modified_string)

    return modified_list
    
def extract_string(arr):
 #   replace_character_in_list_of_strings(arr,39,'"')
    extracted_strings = []
    for string in arr:
        start_index = string.find('"')
        if start_index != -1:
            end_index = string.find('"', start_index + 1)
            if end_index != -1:
                extracted_string = string[start_index + 1:end_index]
                extracted_strings.append(extracted_string)
    return extracted_strings

def select_qulity(lines_array,q):
    selected_lines = [line for line in lines_array if q in line  ]
    selected_lines = lines_array
    selected_lines2 = [line2 for line2 in selected_lines if '[AnimeOut]' in line2 ]
    return selected_lines2

def steps(img):
    global skiped 
    step = 0
    stept = time.time()# Get the current time in seconds
    stept = stept / 60

    print(f"waiting till {img}")
    while step == 0:
        press_to('i am human.png')
        if press_to(img) == True:
            step = 1
            print(f"{img} is done")
        time.sleep(0.01)
        c = time.time()
        c = (c / 60) - stept
        if(c >= 0.8):
            step = 1
            skiped = 1
            print (f"{img} skiped and {converted_web_links[now]} is skiped")
        



def procedure():
    global now,skiped
    webbrowser.open(converted_web_links[now])
    step1 = 0
    import time

    skiped = 0

    steps('1.png')
    if(not skiped):
        steps('2.png')
   
    if idm: 
        if(not skiped):
            steps('3.png')
        if(not skiped):
            steps('4.png')
    
    if skiped :
        return False
    else : 
        return True
   # steps('5.png') 
   # print ("done !")
   
def clean_up(directory,name):
    try:
        # Check if the directory exists
        if not os.path.exists(directory):
            print("Directory does not exist.")
            return
        
        # List all files in the directory
        files = os.listdir(directory)
        
        # Create a new folder named name
        animeout_folder = os.path.join(directory,'[AnimeOut] ' + name + ' ['+ quality +']')
        os.makedirs(animeout_folder, exist_ok=True)
        
        # Move files containing name to the new folder
        for file in files:
            if name in file:
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    shutil.move(file_path, os.path.join(animeout_folder, file))
        
        print("File Process completed successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def act():
    global converted_web_links,now,all
    
    while(1):
        print(f"{now-1} done,{len(converted_web_links) - now - 1} in queue")
        print("next -> " + converted_web_links[now])
            
        extract_text(converted_web_links[now])
        #print(all)
        r = procedure()
        
        if r : 
            now += 1
            break
        now += 1
    
    print("waiting till download finishes")


def extract_text(text):
    global all
    start_index = text.find("[AnimeOut]")  # Find the starting index of '[AnimeOut]'
    end_index = text.find('-', start_index)  # Find the index of '-' after '[AnimeOut]'

    if start_index != -1 and end_index != -1:
        all.append(text[start_index + len("[AnimeOut]") + 1:end_index].strip())  # Extract the text
        return True
    else:
        return False

 # Replace 'strings.txt' with your file name
with open(need_anime_websites_SourceCodes_junk_file, 'r' ,encoding='utf-8') as file:
    web_site = file.readlines()

#   web_site = [line.strip() for line in web_site]

web_site = utf8_to_ascii(web_site)

now = 0
executed_once = False  # Flag to check if on_created logic executed


skiped = 0
now = 0

all = []

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        global all
        if not event.is_directory and not event.src_path.endswith('.tmp'):
            print(f'File {event.src_path} has been created')
            if now < len(converted_web_links) and now > 0:
                act()
            else:
                all = list(set(all))
                for x in all:
                    clean_up(web_or_idm_defult_download_directrory, x)
                print("ALL DONE :)")


def watch_directory(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

converted_web_links = select_qulity(web_site,quality)
converted_web_links = replace_character_in_list_of_strings(web_site,39,'"')
converted_web_links = extract_string(converted_web_links)
converted_web_links = select_qulity(converted_web_links,quality)

print(f"Links {len(converted_web_links)} were found that have quality {quality}")

for x in converted_web_links:
    print(x)

if 0 != len(converted_web_links):
        act()
else:
    print("Something went wrong in the need_anime_websites_SourceCodes_junk_file. No link found, check the quality in the config.py and website source code containing file")
    all = list(set(all))
    for x in all:
        clean_up(web_or_idm_defult_download_directrory, x)

if __name__ == "__main__":
    directory_to_watch = web_or_idm_defult_download_directrory  # Replace with your directory path
    watch_directory(directory_to_watch)
