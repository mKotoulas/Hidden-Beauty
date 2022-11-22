from folders import get_image 
from constants import MODIFIED_IMAGES_PATH,MAX_FILENAME_SIZE,EXTRACTED_FILES_PATH
from PIL import Image
import numpy as np 
from math import ceil 
from rich import print 
from cryptograph import decrypt_file 

def retrieve_bits(channel:int,n_bits:int): 
    return (str(bin(channel)[2:]).zfill(8))[-n_bits:]  

def extract_file(mod_img_arr:np.array)->dict:
    mod_img_arr_flat = mod_img_arr.flatten()         
    total_channels=len(mod_img_arr_flat) 
    channels_after_fn=total_channels-(MAX_FILENAME_SIZE+1)
    max_file_size=4*channels_after_fn
    channels_for_size=len(bin(max_file_size)[2:]) 
    available_channels=channels_after_fn-channels_for_size 
    
    print("[green]Extracting...") 
    #restore number of lsb changed  
    bits_to_alter=int(retrieve_bits(mod_img_arr_flat[0],3),2) 
     
    idx=1 
    #restore filename 
    filename="".join( [retrieve_bits(mod_img_arr_flat[i],1) for i in range(idx,MAX_FILENAME_SIZE+1)] )  
    idx+=MAX_FILENAME_SIZE 
    
    #restore file_size  
    file_size_inbits=int( "".join([retrieve_bits(mod_img_arr_flat[i],1) for i in range(idx,idx+channels_for_size)]),2)
    idx+=channels_for_size #points to first channel that holds the file 
    
    channels_used_float=file_size_inbits/bits_to_alter
    channels_used=int(channels_used_float) if file_size_inbits%bits_to_alter==0 else int(channels_used_float)+1
    last_channel=ceil(bits_to_alter*(channels_used_float%1))  
    lsb_last_channel=last_channel if last_channel!=0 else bits_to_alter
    #free_channels=available_channels-channels_used # channels left for random values 
     
    
  
    
    #restore file
    file="".join([retrieve_bits(mod_img_arr_flat[i],bits_to_alter) for i in range(idx,idx+channels_used-1)]) 
    idx=idx+channels_used
    #handle last channel
    file_last_bits=retrieve_bits(mod_img_arr_flat[idx],lsb_last_channel) 
    #merge
    final_file=file+file_last_bits 
    
    filename_hex=f"{int(filename,2):x}" 
    filename_bytes=bytes.fromhex(filename_hex)   
    file_hex=f"{int(final_file,2):x}"
    file_bytes=bytes.fromhex(file_hex)
    return {"filename":filename_bytes, 
            "file":file_bytes
           }  




def start_extraction():
    img=get_image(MODIFIED_IMAGES_PATH)
    mod_img_arr= np.array(Image.open(img))
    content=extract_file(mod_img_arr)
    filename=content["filename"]
    file=content["file"] 
    filename = filename.decode("utf-8")
    save_path = f"{EXTRACTED_FILES_PATH}/{filename}"

    if file.startswith(b'gAAAAA'): file=decrypt_file(file) 
    with open(save_path, 'wb') as f:f.write(file)  
