from enum import Flag


def write_line(opened_file, line, tab_count=0):
    opened_file.write("\t" * tab_count + "\\" + line + "\n")

order_of_operation = {
    "^": 3,
    "*": 2,
    "/": 2,
    "+": 1,
    "-": 1,
    "~": 0,
    "&": -1,
    "V": -2,
    "=>": -3,
    "<=": -3,
    "<=>": -3 
}

def add_token(token_list, current_token):
    if current_token:
        token_list.append(current_token)
        current_token = ""
    return current_token

def parse_expression(expression):
    tokens = []
    current_token = ""
    current_is_digit = False
    for ch in expression:
        if ch == " ":
            current_token = add_token(tokens, current_token)
            continue
        if ch == "(" or ch == ")":
            current_token = add_token(tokens, current_token)
            tokens.append(ch)
            continue
        if ch.isdigit() != current_is_digit:
            current_token = add_token(tokens, current_token)
            current_is_digit = ch.isdigit()
        current_token += ch
    add_token(tokens, current_token)
    return tokens

def convert_expression_to_postfix(expression):
    stack = []
    postfix = []
    for token in parse_expression(expression):
        if token in order_of_operation:
            while stack and stack[-1] in order_of_operation and order_of_operation[token] <= order_of_operation[stack[-1]]:
                postfix.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                postfix.append(stack.pop())
            stack.pop()
        else:
            postfix.append(token)
    while stack:
        postfix.append(stack.pop())
    return postfix

replacement = {
    "~": r"\neg",
    "&": r"\land",
    "V": r"\lor",
    "=>": r"\implies",
    "<=": r"\impliedby",
    "<=>": r"\iff" 
}

def convert_expression_to_latex(expression):
    tokens = parse_expression(expression)
    for id, token in enumerate(tokens):
        if token in replacement:
            tokens[id] = replacement[token]
    return " ".join(tokens)