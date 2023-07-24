import re
import nltk

identifier ={
     "letvar": "identifier",
}

OPERATORS = {
    "letvar": "identifier",
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULTIPLY',
    '/': 'DIVIDE',
    '%': 'MODULO',
    '=': 'ASSIGN',
    '"':'str_identifier',
}

def is_valid_variable_name(variable_name):
    regex = r'^[a-zA-Z]{1}$'
    return re.match(regex, variable_name) is not None

def generate_tokens(code):

    tokens = []
    variables = {} 
    i = 0
    line_number = 1 

    while i < len(code):
        # Ignore whitespace characters
        if code[i].isspace():
            if code[i] == '\n':
                line_number += 1  # increment line number 
            i += 1
            continue

        # keep track of any word
        if code[i].isalpha():
            j = i + 1
            while j < len(code) and (code[j].isalnum() or code[j] == '_'):
                j += 1
            word = code[i:j]
           
        
            if word == "letvar":
                # get the variable name
                k = j + 1
                while k < len(code) and not code[k].isspace():
                    k += 1
                var_name = code[j+1:k]

                # check if variable name is already in dictionary
                if var_name in variables:
                    print(f"Error: Variable '{var_name}' already declared on line {variables[var_name]['line']}")
                else:
                    variables[var_name] = {'line': line_number, 'type': None, 'value': None}
                    
                if is_valid_variable_name(var_name):
                    print(f"Variable name '{var_name}' is valid.")
                else:
                    print(f"Variable name '{var_name}' is invalid.")
            
            else:
                tokens.append((word, 'Variable'))

            i = j
            continue

       
          # Check for numbers
        if code[i].isdigit():
            j = i + 1
            while j < len(code) and code[j].isdigit():
                j += 1
            tokens.append((code[i:j], 'NUMBER'))
            var_value = code[i:j]
            variables[var_name]['value'] = var_value
            variables[var_name]['type'] = 'NUMBER'
            i = j
            continue
        


        # Check for strings
        elif code[i] == '"':
            j = i + 1
            while j < len(code) and code[j] != '"':
                j += 1
           
            variables[var_name]['value'] = code[i+1:j]  # set the value of the variable
            tokens.append((variables[var_name]['value'], 'STRING'))  # add the variable to the tokens list
            variables[var_name]['type'] = 'STRING' 
            i = j + 1
        

        for operator in OPERATORS:
            if code.startswith(operator, i):
                tokens.append((code[i:i+len(operator)], OPERATORS[operator]))
                i += len(operator)
                break
        else:
            print(f"Error: Unrecognized character '{code[i]}' at position {i}")
            i += 1
    print("-------------------------------------------------------")
    
# Symbol Table
    mem_address = 0
    print("Symbol Table : ")
    for var_name, var_info in variables.items():
        # calculate the size of the variable based on its type
        if variables[var_name]['type'] == 'NUMBER':
            var_size = 2
        elif variables[var_name]['type'] == 'STRING':
            var_size = len(variables[var_name]['value']) * 2  # assuming 2 bytes per character
        else:
            var_size = 0  # unknown type
        no_ofDimension = 0 
        print(f"\tVar Name :{var_name}   Line Declaration : {var_info['line']},   Variable Type :{variables[var_name]['type']}, Memory Address: {mem_address}  , Number of Dimension : {no_ofDimension} ")
    
        mem_address += var_size

    return tokens



with open('code.mly', 'r') as file:
    code = file.read()

#lexical tokens
tokens = generate_tokens(code)
print("-------------------------------------------------------")

# Print the lexical tokens
print('Lexical tokens:')
for token in tokens:
    print(f'\t{token[0]}: {token[1]}')

print("-------------------------------------------------------")

# Define the grammar for compute the first 
'''
    Program->P
	statement -> S
	assignment -> A
	letvar -> L
	expression -> E
	term -> T
	op -> O
	identifier -> I
	number -> N
	letter -> R
	digit -> D
'''
mygrammar = {
    'P': ['S', 'SP'],
    'S': ['A','E'],
    'A': ['LI=E'],
    'L': ['l'],
    'E': ['T','TOE'],
    'T': ['I','N','E'],
    'O': ['+','-','*','/'],
    'I': ['R','D','IR','ID'],
    'N': ['D','ND'],
    'R': ['a','b','c'],
    'D': ['0','1','2'],
}

#First and Follow sets()
def find_first_set(non_terminal, visited=set()):
    if non_terminal in visited:
        #  skip the visited non-tereminal to avoid infinite loops
        return set()
    visited.add(non_terminal)
    first_set = set()
    productions = mygrammar[non_terminal]
    for production in productions:
        if not production:
            # If the production is empty, add the empty string to the first set 'epslon'
            first_set.add('')
            continue
        production = production.strip()#remove any white space
        first_symbol = production[0]
        if first_symbol in mygrammar:
            # If the first symbol is a non-terminal, add its first set to the first set of the current non-terminal
            first_set |= find_first_set(first_symbol, visited)
            # If the first set of the non-terminal contains the empty string, continue checking the next symbol in the production
            if '' in first_set:
                first_set.discard('')
                first_set |= find_first_set(non_terminal, visited)
        else:
            # If the first symbol is a terminal, add it to the first set of the current non-terminal
            first_set.add(first_symbol)

    visited.remove(non_terminal)
    return first_set
print('the First set() : ')
for non_terminal in mygrammar:
            first_set = find_first_set(non_terminal)
            print(f"First({non_terminal}) = {first_set}")

print("-------------------------------------------------------")


def find_follow_sets(grammar):
    follow_dict = {}
    for non_terminal in grammar:
        follow_dict[non_terminal] = set()
    start_symbol = list(grammar.keys())[0]
    follow_dict[start_symbol].add('$')

    # Iterate until follow sets converge
    while True:
        converged = True
        for non_terminal, productions in grammar.items():
            for production in productions:
                for i, symbol in enumerate(production):
                    if symbol in grammar:
                        follow_set = follow_dict[symbol]
                        if i == len(production) - 1:
                            # Last symbol in production
                            if follow_dict[non_terminal].update(follow_set):
                                converged = False
                        else:
                            next_symbol = production[i+1]
                            if next_symbol in grammar:
                                next_first_set = find_first_set(next_symbol)
                                if '' in next_first_set:
                                    next_first_set.discard('')
                                    if follow_dict[non_terminal].update(follow_set | next_first_set):
                                        converged = False
                                else:
                                    if follow_dict[non_terminal].update(next_first_set):
                                        converged = False
                            else:
                                if follow_dict[non_terminal].add(next_symbol):
                                    converged = False

        if converged:
            break

    return follow_dict



# Find the follow set of the start symbol
S_follow_set = find_follow_sets(mygrammar)
print('the Follow set() : ')
print(S_follow_set) 


# parse tree

grammar = nltk.CFG.fromstring("""
	program -> statement | statement program
	statement -> assignment | expression
	assignment -> "letvar" identifier '=' expression
	letvar -> "letvar"
	expression -> term | term op expression
	term -> identifier | number | '(' expression ')'
	op -> '+' | '-' | '*' | '/'
	identifier -> letter | digit | identifier letter | identifier digit
	number -> digit | number digit
	letter -> 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
	digit -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' |'10' | '11' | '12' | '13' | '14' | '15' | '16' | '17' | '18' | '19' | '20' | '21' | '22' | '23' | '24' | '25' | '26' | '27' | '28' | '29' | '30' | '31' | '32' | '33' | '34' | '35' | '36' | '37' | '38' | '39' | '40' | '41' | '42' | '43' | '44' | '45' | '46' | '47' | '48' | '49' | '50' | '51' | '52' | '53' | '54' | '55' | '56' | '57' | '58' | '59' | '60' | '61' | '62' | '63' | '64' | '65' | '66' | '67' | '68' | '69' | '70' | '71' | '72' | '73' | '74' | '75' | '76' | '77' | '78' | '79' | '80' | '81' | '82' | '83' | '84' | '85' | '86' | '87' | '88' | '89' | '90' | '91' | '92' | '93' | '94' | '95' | '96' | '97' | '98' | '99'
""")

parser = nltk.ChartParser(grammar)

try:
    tree = next(parser.parse(code.split()))
    tree.draw()
    
except Exception as e:
    print("Error:", e)

