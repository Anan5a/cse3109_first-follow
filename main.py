from first_follow import *
from colored import fore,back,style

if __name__ == '__main__':
    prod_rules = take_input()
    if hasLeftRecursion(prod_rules):
        # cannot continue
        print(fore.RED+style.BOLD+"One or more production rules have left-recursion. Exiting..."+style.RESET)
        exit(-1)
    # Normal operation
    firsts_ = firsts(prod_rules.copy())
    follows_ = follows(prod_rules.copy(), firsts_.copy())

