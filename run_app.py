from menu_items import * 
from injection import start_injection
from extraction import start_extraction 
from time import sleep
from sys import exit
MENU_FUNCTIONS={"1":start_injection,"2":start_extraction,"3":exit} 

def run_app()->None:
    clear()
    sleep(0.1) 
    main_menu()  
    choice=get_choice() 
    clear()
    if choice=="3":MENU_FUNCTIONS[choice]() 
    draw_line(choice)  
    MENU_FUNCTIONS[choice]()

run_app()      

 
    
