# What it does
This is python script with a basic CLI that allows you to hide any type of file inside an RGB image using steganography with an additional option to encrypt the file before hiding it. 

# How it works
To accomplish that,the script alters 1 to 4 lsb's of the image channels based on the size of the input image and file. This is a common steganographic technique. 

If the file is too big to fit inside the image a related error message is displayed and the script terminates.   

# How to use it 

In the folder files/input files place the file you want to hide. It can be of any type (.zip,.png,.pdf etc).

In the folder files/input images place the image that will be used to hide the file. Make sure the image is indeed an RGB image. If the format of the image is not png the script will automatically convert it to png. 

Note: You can create subfolders in the above folders for your input images and files if you wish. 

Type python run_app.py in your terminal to run the script. 
I suggest you run it through VS code at this point because the colors will not be good if you run it from your terminal. 

To encrypt the file select that option from the menu. It will ask you if you want to use an existing key or create a new one. The first time you run the script select 
"create new key" from the menu. The keys will be stored in the folder files/encryption key. You will need that key to decrypt the file so make sure you don't delete it if you plan to use it. 

The script will ask you if you want to store random values in the image. When the file is hidden inside the image it is most likely that there are channels in the image that have not been modified at all. I suggest for better results to store random values in those channels. Have in mind that this option will increase execution time. 

You can find the modified image in the folder files/modified images.  

# Important notice 
Even the slightest modifiction to the image will make the decryption process not possible.   

#Example 

The picture below is 26.1 MB and contains a rar file (16,4 MB) of "The Rebublic", a work of the Greek philosopher Plato.  
 
![image](https://user-images.githubusercontent.com/40547620/204315782-1be332ee-3a2c-44ea-8886-82b424e75a76.png) 



You can find the above file and 4 more sample images to use in the related folders.  





