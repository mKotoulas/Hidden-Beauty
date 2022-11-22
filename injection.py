from folders import prepare_folders,make_png,get_file,get_image 
from constants import * 
from rich import print 
from pathlib import Path 
from cryptograph import encrypt_file  
import numpy as np
from PIL import Image  
from math import ceil   
from sys import exit     
from os import walk  
from menu_items import clear
from rich.prompt import Confirm 

def lsb_count(channels:int,file_size:int)->int:
    if file_size==channels:return 1
    else: return file_size//channels +1   

def store_bits(channel:int,values:str,nbits:int)->int: 
    mask=255-(2**nbits-1)   
    return (channel&mask)| (int(values,2))         
  
def retrieve_bits(channel:int,n_bits:int): 
    return (str(bin(channel)[2:]).zfill(8))[-n_bits:]



def inject_file(file:bytes,filename:bytes,target_image:np.ndarray,random:bool)->np.ndarray:  
    img_arr_flat=target_image.flatten()                  #1-D array of integers representing channels values (0-255)  
    total_channels=len(img_arr_flat)                      #number of rgb channels in the picture 
    channels_after_fn=total_channels-(MAX_FILENAME_SIZE+1)      #rgb channels left for storing the filesize and the file
    max_file_size=4*channels_after_fn                     #max file size the pic can store in bits 
    channels_for_size=len(bin(max_file_size)[2:])         #maximum rgb channels dedicated to store the maximum filesize.Size of the file is stored as a binary number representing the number of bits in the file.  
    available_channels=channels_after_fn-channels_for_size #number of channels available for storing the file 
    file_size_inbits=len(file)*8  #size of the file in bits
    bits_to_alter=lsb_count(available_channels,file_size_inbits)
    if bits_to_alter>4:
        exit(f"File size is too big...\nYou can store a maximum of {round((available_channels*4)/(8*10**6),4)} MB in that png!")
    channels_used_float=file_size_inbits/bits_to_alter #channels used 
    channels_used=int(channels_used_float) if file_size_inbits%bits_to_alter==0 else int(channels_used_float)+1
    free_channels=available_channels-channels_used # channels left for random values
    last_channel=ceil(bits_to_alter*(channels_used_float%1))  
    lsb_last_channel=last_channel if last_channel!=0 else bits_to_alter         

   

    bin_file="".join(f"{x:0>8b}" for x in file) #convert file in binary format 
    bin_fn="".join(f"{x:0>8b}" for x in filename).zfill(MAX_FILENAME_SIZE) #convert filename in binary format 
    bin_size=str(bin(file_size_inbits)[2:]).zfill(channels_for_size)      
    index=str(bin(bits_to_alter)[2:]).zfill(3) 
    #store index
    print("[green]Storing index...")
    img_arr_flat[0]=store_bits(img_arr_flat[0],index,3)  
    idx=1

    #store filename
    print("[green]Storing filename...") 
    for i,h in enumerate(bin_fn):img_arr_flat[idx+i]=store_bits(img_arr_flat[idx+i],h,1) 
    idx+=MAX_FILENAME_SIZE      
    
    #store file_size(binary)
    print("[green]Storing file...")
    for i,h in enumerate(bin_size):img_arr_flat[idx+i]=store_bits(img_arr_flat[idx+i],h,1) 
    idx+=channels_for_size    
    
    #store file 
    file_idx=0 
    end_loop=idx+(channels_used-1)  
    for i in range(idx,end_loop):
        img_arr_flat[i]=store_bits(img_arr_flat[i],bin_file[file_idx:(file_idx+bits_to_alter)],bits_to_alter)        
        file_idx+=bits_to_alter
     
    idx=i+1    

    #handle the last channel 
    img_arr_flat[idx]=store_bits(img_arr_flat[idx],bin_file[file_idx:],lsb_last_channel)   
    idx+=1

    
    #store random values at the free channels 
    if random:
        print("[green]Storing random values.This may take some time...")
        r=np.random.randint(low = 0, high=2**bits_to_alter,size=free_channels) 
        random_numbers=[np.binary_repr(i,bits_to_alter) for i in r]    
        j=0
        for i in range(idx,total_channels):             
            img_arr_flat[i]=store_bits(img_arr_flat[i],random_numbers[j],bits_to_alter) 
            j+=1
       
    #Shape and save the modified png
    counter=0
    for root,dirs,files in walk(MODIFIED_IMAGES_PATH):
        for _ in files:counter+=1 
    img_arr = img_arr_flat.reshape(target_image.shape)
    im = Image.fromarray(img_arr)
    im.save(f"{MODIFIED_IMAGES_PATH}/mod_img_{counter+1}.png") 


def start_injection()->None:  
    prepare_folders(INPUT_IMAGES_PATH,MODIFIED_IMAGES_PATH,INPUT_DATA_PATH,EXTRACTED_FILES_PATH,ENCRYPTION_KEYS_PATH)     
    make_png(INPUT_IMAGES_PATH)
    image_path=get_image(INPUT_IMAGES_PATH) 
    file_path=get_file(INPUT_DATA_PATH)
    with open(file_path,"rb") as f: file=f.read() 
    clear() 
    if Confirm.ask("[blue]Encrypt file before injection?"):file=encrypt_file(file)
    img_array=np.array(Image.open(image_path))
    filename=Path(file_path).name 
    filename_bytes= filename.encode('utf-8')
    if Confirm.ask("[blue]Store random values?"):random=True 
    else:random=False
    inject_file(file,filename_bytes,img_array,random)





     


