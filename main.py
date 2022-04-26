from first_follow import *

if __name__ == '__main__':
    prod_rules = take_input()
    if hasLeftRecursion(prod_rules):
        # cannot continue
        print("One or more production rules have left-recursion. Exiting...")
        exit(-1)
    # Normal operation
    firsts_ = firsts(prod_rules.copy())
    follows_ = follows(prod_rules.copy(), firsts_.copy())

