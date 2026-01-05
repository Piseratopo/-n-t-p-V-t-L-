from enum import Flag


def write_line(opened_file, line, tab_count=0):
    opened_file.write("\t" * tab_count + line + "\n")

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

def add_token(token_list, current_pos, current_token):
    if current_token:
        token_list.append((current_pos, current_token))
        current_token = ""
    return current_token

def parse_expression(expression):
    tokens = []
    current_token = ""
    current_pos = 0
    current_is_digit = False
    for ch in expression:
        if ch == " ":
            if current_token:
                current_token = add_token(tokens, current_pos, current_token)
                current_pos += 1
            continue
        elif ch == "(" or ch == ")":
            if current_token:
                current_token = add_token(tokens, current_pos, current_token)
                current_pos += 1
            add_token(tokens, -1, ch)
            continue
        if ch.isalnum() != current_is_digit:
            if current_token:
                current_token = add_token(tokens, current_pos, current_token)
                current_pos += 1
            current_is_digit = ch.isalnum()
        current_token += ch
    add_token(tokens, current_pos, current_token)
    return tokens

def parse_expression_with_parentheses(expression):
    def is_in_component(ch):
        return ch.isalnum() or ch in "()"

    tokens = []
    current_token = ""
    current_pos = 0
    current_is_in_component = False
    for ch in expression:
        if ch == " ":
            if current_token:
                current_token = add_token(tokens, current_pos, current_token)
                current_pos += 1
            continue
        if is_in_component(ch) != current_is_in_component:
            if current_token:
                current_token = add_token(tokens, current_pos, current_token)
                current_pos += 1
            current_is_in_component = is_in_component(ch)
        current_token += ch
    add_token(tokens, current_pos, current_token)
    return tokens

def convert_expression_to_postfix(expression):
    stack = []
    postfix = []
    for _id, token in parse_expression(expression):
        if token in order_of_operation:
            while stack and stack[-1] in order_of_operation and order_of_operation[token] <= order_of_operation[stack[-1]]:
                postfix.append(stack.pop())
            stack.append((_id, token))
        elif token == "(":
            stack.append((_id, token))
        elif token == ")":
            while stack and stack[-1][1] != "(":
                postfix.append(stack.pop())
            stack.pop()
        else:
            postfix.append((_id, token))
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

def convert_tokens_to_latex(tokens, need_math_mode=False):
    for id, token in enumerate(tokens):
        if token in replacement:
            tokens[id] = replacement[token]
        if need_math_mode:
            tokens[id] = f"${tokens[id]}$"
    return tokens

def convert_expression_to_latex(expression):
    tokens = [t for _, t in parse_expression(expression)]
    return " ".join(convert_tokens_to_latex(tokens))

