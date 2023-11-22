import time
import webbrowser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from image_recognition import press_to
import time
import os
import shutil
from config import quality,web_or_idm_defult_download_directrory,idm,need_anime_websites_SourceCodes_junk_file


def utf8_to_ascii(lines_array):
    try:
        decoded_lines = [line.encode('utf-8').decode('ascii', 'ignore') for line in lines_array]
        return decoded_lines
    except Exception as e:
        return f"An error occurred: {e}"
    
def extract_string(arr):
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
    selected_lines2 = [line2 for line2 in selected_lines if '[AnimeOut]' in line2 ]
    return selected_lines2

def steps(img):
    global skiped 
    step = 0
    stept = time.time()# Get the current time in seconds
    stept = stept / 60

    while step == 0:
        press_to('i am human.png')
        if press_to(img) == True:
            step = 1
        time.sleep(0.01)
        c = time.time()
        c = (c / 60) - stept
        if(c >= 0.8):
            step = 1
            skiped = 1
        
def procedure():
    global now,skiped
    webbrowser.open(converted_web_links[now])
    step1 = 0
    import time

    steps('1.png')
    steps('2.png')
   
    if idm: 
        steps('3.png')
        steps('4.png')
    
   # print ("done !")
    if skiped == 1 :
        print(f"error : {converted_web_links[now]} skiped ")
        skiped = 0
        return False
    return True
    
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
        print(f"{now-1} done,{len(converted_web_links) - now-1} in queue. next - " + converted_web_links[now])
        extract_text(converted_web_links[now])
       # print(all)
        r = procedure()
        now += 1
        if r == 1:
            break


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
times = 1
executed_once = False  # Flag to check if on_created logic executed

converted_web_links = select_qulity(web_site,quality)
converted_web_links = extract_string(converted_web_links)


skiped = 0
now = -1

all = []

def Quality(q):
    global quality
    quality = q
     
def Run_User_Downloading_Simulation():

    print(f"Links {len(converted_web_links)} were found that have quality {quality}")

    if(0 != len(converted_web_links)):
        act()
    else:
        print("Something went wrong in the need_anime_websites_SourceCodes_junk_file.No link found, chek the qulity in the config.py and website source code contaning file")
        all = list(set(all))
        for x in all:
            clean_up(web_or_idm_defult_download_directrory,x)
            
    class MyHandler(FileSystemEventHandler):
        def on_created(self, event):
            global now, times, executed_once,all
            if not event.is_directory and not executed_once:
                executed_once = True  # Set the flag to True after executing once
                
                if len(converted_web_links) > now and ".tmp" not in event.src_path:
                   # print(f'File {event.src_path} has been created')
                    times = 1
                    now += 1
                    if(now < len(converted_web_links) and now > 0):
                        act()
                    else :
                        all = list(set(all))
                        for x in all:
                            clean_up(web_or_idm_defult_download_directrory,x)
                            print("ALL DONE :)")
                    

    def start_observer():
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path=web_or_idm_defult_download_directrory
, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(5)  # Adjust the polling interval as needed
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    # Run the observer
    start_observer()

Run_User_Downloading_Simulation()