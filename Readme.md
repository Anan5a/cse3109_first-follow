# Program to calculate First and Follow sets of given grammar
## Abstract:

## Algorithm for calculating First:
To compute First(X) for all grammar symbols X, apply following rules until no more terminals or ɛ can be added to any First set:

    1. If X is a terminal then First(X) = {X}.
    2. If X is a nonterminal and X→Y1 Y2 … Y𝑘 is a production for some k>=1, then place a in First(X) if for some ‘I’ a is in First(Y𝑖) and ɛ is in all of First(Y1) ...First(Y𝑖−1) that is Y1 … Y𝑖−1 => ɛ. if ɛ is in First(Y𝑗) for j=1…k then add ɛ to First(X).
    3. If X → ɛ is a production then add ɛ to First(X)

## Algorithm for calculating Follow:
To compute Follow(A) for all non-terminals A, apply following rules until nothing can be added to any follow set:

    1. Place $ in Follow(S) where S is the start symbol
    2. If there is a production A→ αBβ then everything in First(β) except ɛ is in Follow(B).
    3. If there is a production A → B or a production A → αBβ where First(β) contains ɛ, then everything in Follow(A) is in Follow(B)

### Input format:
    1. A→bc
    2. A→Bcd|ef
    3. # and $ should not be used, they are reserved for internal use
    4. typing end will quit input process
## Working procedure:
    1. Take input
    2. Check validity (presence of left recursion)
    3. Compute first
    4. Compute follow
## Code explanation:
### 1. Take input
Code:
```
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
```
Returns a dictionary of production rules in this format

	{“NT”:[“Rule1”,”Rule2”,”RuleN”}
### 2. Check validity (left recursion):
```
def hasLeftRecursion(prod_rules: dict):
    for NT in prod_rules:
        for Rule in prod_rules[NT]:
            if Rule.find(NT) == 0:  # Production rule found in first position, Left recursion!!
                return True
    return False
```

### 3. Compute first:
```
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

def firsts(prod_rules: dict):
    firsts_ = {}

    for NT in prod_rules:
        firsts_[NT] = findFirst(NT, prod_rules)
    for NT in firsts_:
        print(fore.BLUE + style.BOLD + f"FIRST({NT}) = " + '{' + f"{','.join(firsts_[NT])}" + '}' + style.RESET)
    return firsts_
```
### Output:
#### Input
    E->TE'
    E'->+TE'|#
    T->FT'
    T'->*FT'|#
    F->(E)|i
    end

### Explanation:
We loop through all non terminals in firsts() function. Which calls findFirst() for each non-terminal.
Inside the findFirst() function 

    1. If we encounter # aka epsilon we push it into a list and continue the loop
    2. Otherwise, If the first item in the rule is a terminal we push it in the list and terminate the loop
    3. If item is non terminal we find First of the item recursively
    4. If the recursion result has # in the list, we remove it push result in list and keep the loop going otherwise we push result in the list and terminate the loop

### 4. Compute Follow:
```
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
```
### Output
#### Input
    E->TE'
    E'->+TE'|#
    T->FT'
    T'->*FT'|#
    F->(E)|i
    end
### Explanation:
We loop through all non terminals in follows() function. Which calls findFollow() for each non-terminal.
Inside the findFollow() function
    1. We iterate through all production rules for each Non terminals
    2. If right side of the Non terminal  (NT, the one we are working with) has a terminal we push it to the list
    3. If we find non terminal we keep finding follow
[Link to this page: https://github.com/Anan5a/cse3109_first-follow](https://github.com/Anan5a/cse3109_first-follow)