#!/usr/bin/env python3

class ConColor:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INVERSE = '\33[7m'

    PURPLE = '\033[95m'
    GREY = '\033[90m'
    WHITE = '\033[97m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


print(f"{ConColor.PURPLE}Purple{ConColor.RESET}")
print(f"{ConColor.GREY}Grey{ConColor.RESET}")
print(f"{ConColor.WHITE}White{ConColor.RESET}")
print(f"{ConColor.BLUE}Blue{ConColor.RESET}")
print(f"{ConColor.CYAN}Cyan{ConColor.RESET}")
print(f"{ConColor.GREEN}Green{ConColor.RESET}")
print(f"{ConColor.YELLOW}Yellow{ConColor.RESET}")
print(f"{ConColor.RED}Red{ConColor.RESET}")
print(f"{ConColor.RED}{ConColor.BOLD}Red BOLD combo{ConColor.RESET}")
print(f"{ConColor.UNDERLINE}Underline{ConColor.RESET}")
print(f"{ConColor.INVERSE}Inverse{ConColor.RESET}")
