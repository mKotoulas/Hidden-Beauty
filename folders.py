from pathlib import Path  
from os import makedirs,walk,rename
from os.path import isfile  
from rich import print
from rich.prompt import Confirm,Prompt 
from constants import ENCRYPTION_KEYS_PATH,MODIFIED_IMAGES_PATH

def prepare_folders(*folders)->None:   
    folders=folders
    for folder in folders:makedirs(folder,exist_ok=True)   
       

def make_png(path:str)->str:  
    for root,dirs,files in walk(path): 
        for filename in files:
            if filename.lower()[-3:] not in ["png","jpg","jpeg"]:non_image=True
            stem=Path(f"{root}/{filename}").stem
            if filename.lower().endswith(("jpeg","jpg")):
                rename(f"{root}/{filename}",f"{root}/{stem}.png")  
    

def get_file(path:str)->str:   
    while True: 
        filename=Prompt.ask("[green]Name of file to hide") 
        if Path(filename).suffix:
            for root,dirs,files in walk(path):
                file_path=f"{root}/{filename}"
                if isfile(file_path): return file_path   
        else:
            for root,dirs,files in walk(path):
                for file in files:
                    if filename==Path(file).stem:
                        if Confirm.ask(f"[blue]Is [green]{file}[/] what you wanted to type?:"): return f"{root}/{file}"  
        print("[red on white]Invalid filename!")   



def get_image(path:str)->str: 
    while True:
        filename=Prompt.ask("[green]Name of image") 
        if Path(filename).suffix:
            for root,dirs,files in walk(path):
                file_path=f"{root}/{filename}"
                if isfile(file_path): return file_path
        else:
            for root,dirs,files in walk(path):
                for file in files:
                    if filename==Path(file).stem: return f"{root}/{file}"
        print("[red on white]Invalid filename!") 

def get_key()->bytes:
    while True:
        key_name=Prompt.ask("[green]Key filename")  
        suffix=Path(key_name).suffix 
        if not suffix:key_name+=".key"
        path=f"{ENCRYPTION_KEYS_PATH}/{key_name}" 
        if isfile(path):
            with open(path,"rb") as f: return f.read() 
        print("Invalid filename")
             

    


      




     