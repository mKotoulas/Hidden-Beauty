from rich.console import Console  
from rich.table import Table    
from rich import box,print 
from os import system,get_terminal_size 
 
console=Console() 

def main_menu()->None: 
    title="[bold yellow]Welcome to\n[red]:secret:[/]Hidden Beauty[red]:secret:" 
    caption="[white on red]Because everyone has something to hide\nDon't you?"
    width=round(get_terminal_size().columns*0.8)
    style="yellow bold" 
    table=Table(title=title,box=box.DOUBLE_EDGE,caption=caption,width=width,style=style) 
    table.add_column("[cyan]Function code",justify="center")  
    table.add_column("[cyan]Function description",justify="center")   
    table.add_row("(Type) 1 (to)","Inject file",style="magenta") 
    table.add_row("(Type) 2 (to)","Extract file",style="magenta")  
    table.add_row("(Type) 3 (to)","Exit",style="magenta")  
    console.print(table)  

def clear()->None: system("cls") 
 
def get_choice()->str:
    choice=input("Select:") 
    while choice not in ["1","2","3"]: 
        clear() 
        main_menu()  
        print("[red]Invalid operation.Please type again")      
        choice=input()
    return choice

def draw_line(mode:str)->None:  
    if mode=="1":msg="Injection"
    else:msg="Extraction"
    right_padding=round((get_terminal_size().columns-len("Injetion"))/2) 
    msg=msg.rjust(right_padding,"-")
    msg=msg.ljust(get_terminal_size().columns-1,"-")  
    print("[blue]"+msg+"\n")


def encryption_menu()->None:
    print("[blue]Procced with:")
    print("[green]1.Existing key(type 1 to select)")
    print("[green]2.Generate new key(type 2 to select)") 
       



  