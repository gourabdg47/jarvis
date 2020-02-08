from colorama import Fore, Back, Style, init

init(convert=True)

def prRed(text):print(Fore.RED + text) 
def with_green_background(text):print(Back.GREEN + text) 
def reset_colour_style():print(Style.RESET_ALL) 
