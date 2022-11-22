from cryptography.fernet import Fernet,InvalidToken
from menu_items import encryption_menu,draw_line,clear
from folders import get_key
from constants import ENCRYPTION_KEYS_PATH
from os import walk
from rich import print 
from rich.prompt import IntPrompt  
from os import listdir
from sys import exit

def generate_key()->bytes:
    counter=0
    for root,dirs,files in walk(ENCRYPTION_KEYS_PATH):
        for _ in files:counter+=1 
    key=Fernet.generate_key()
    path=f"{ENCRYPTION_KEYS_PATH}/key{counter+1}.key"
    with open(path,"wb") as k:k.write(key)
    #print(f"[green]New key generated at {Path(path)}")
    print(f"File enrypted with key at:{path}") 
    return key 

def encrypt_file(file:bytes)->bytes:
    encryption_menu()
    choice=IntPrompt.ask("[blue]Select",choices=["1","2"],show_choices=False)    
    if choice==1:key=get_key()    
    else:key=generate_key()   
    fernet=Fernet(key) 
    file_encrypted=fernet.encrypt(file)
    clear()   
    return file_encrypted 
    
def decrypt_file(file:bytes)->bytes: 
    for key_name in listdir(ENCRYPTION_KEYS_PATH):
        key_path=f"{ENCRYPTION_KEYS_PATH}/{key_name}" 
        with open(key_path,"rb") as f: key=f.read() 
        fernet = Fernet(key) 
        try:
            file = fernet.decrypt(file)
            print(f"File succesfully decrypted with key:{key_path}") 
            return file
        except InvalidToken: continue 
    print(f"[red on white] Tried every key at {ENCRYPTION_KEYS_PATH} but all keys failed.\n Either you dont have the key to decrypt the file or the key has expired")
    exit()   
 

      


 
