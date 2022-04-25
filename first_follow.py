from colored import style, fore


def take_input():
    prod_rules = {}

    print("Enter production rules. Type end to stop input process.\nFormat A->B|cD|#")
    while True:
        input_ = input()
        if input_.find('end') != -1:
            break
        NT, Rules = input_.split('->')
        prod_rules.update({NT: Rules.split('|')})
    return prod_rules


def hasLeftRecursion(prod_rules: dict):
    for NT in prod_rules:
        for Rule in prod_rules[NT]:
            if Rule.find(NT) == 0:  # Production rule found in first position, Left recursion!!
                return True
    return False


def findFirst(NT, prod_rules: "dict[list,str]"):
    firsts0 = []
    for rule in prod_rules[NT]:  # loop all rules of the NT
        if rule == '#':
            firsts0.extend(['#'])
            continue
        for i in range(len(rule)):
            if (ord(rule[i]) < 65 or ord(rule[i]) > 90) and rule[i] != "'":
                firsts0.extend([rule[i]])
                break
            ff = []
            if i < len(rule) - 1 and rule[i + 1] == "'":  # 2 char NT
                ff = findFirst(rule[i:i + 1], prod_rules)
            elif rule[i] == "'":
                continue
            ff = findFirst(rule[i], prod_rules)
            try:
                ff.index('#')
                firsts0.extend(ff)
            except:
                firsts0.extend(ff)
                break
    return unique(firsts0)


def findFollow(NT,prod_rules: "dict[list,str]", follows_, firsts_):
    for nt in prod_rules:
        for rule in prod_rules[nt]:
            for i in range(len(rule)):
                if len(NT) >= 1 and rule[i] == NT[0]:
                    if i != len(rule)-1 and rule[i+1] == "'":
                        i+=1
                    if i == len(rule)-1:
                        follows_[NT].extend(follows_[nt])
                    elif 'A' <= rule[i + 1] <= 'Z':
                        NT_ = rule[i+1]
                        if rule[i+2] == "'":
                            NT_ += rule[i+2]
                        follows_[NT].extend(firsts_[NT_])
                        follows_[NT].extend(follows_[nt])
                    elif rule[i+1] != '' and rule[i+1] != "'":
                        follows_[NT].extend([rule[i+1]])



def firsts(prod_rules: dict):
    firsts_ = {}

    for NT in prod_rules:
        firsts_[NT] = findFirst(NT, prod_rules)
    for NT in firsts_:
        print(fore.BLUE + style.BOLD + f"FIRST({NT}) = " + '{' + f"{','.join(firsts_[NT])}" + '}' + style.RESET)
    return firsts_


def follows(prod_rules: dict, firsts_: dict):
    follows_ = {}
    non_terminals = list(prod_rules.keys())
    start_symbol = non_terminals[0]

    for NT in non_terminals:
        follows_[NT] = []
    follows_[start_symbol].append("$")
    for NT in non_terminals:
        findFollow(NT,prod_rules, follows_, firsts_)
    for NT in follows_:
        follows_[NT] = unique(follows_[NT],removeNull=True)
    for NT in follows_:
        print(fore.GREEN + style.BOLD + f"FOLLOW({NT}) = " + '{' + f"{','.join(follows_[NT])}" + '}' + style.RESET)
    return follows_


def unique(sequence, removeNull = False):
    seen = set()
    rlist = [x for x in sequence if not (x in seen or seen.add(x))]
    if removeNull:
        return list(filter(("#").__ne__, rlist))
    return rlist
