import unicodedata

from enum import Flag
from abc import ABC, abstractmethod


def write_line(opened_file, line, tab_count=0):
    opened_file.write("\t" * tab_count + line + "\n")


class MathOperation(ABC):
    def __init__(self, symbol, latex_symbol, precedence, input_count=2):
        self.symbol = symbol
        self.latex_symbol = latex_symbol
        self.precedence = precedence
        self.input_count = input_count
    
    @abstractmethod
    def compute(self, *values):
        pass


class NotOperation(MathOperation):
    def __init__(self):
        super().__init__("~", r"\neg", 0, 1)
    
    def compute(self, value):
        return not value


class AndOperation(MathOperation):
    def __init__(self):
        super().__init__("&", r"\land", -1)
    
    def compute(self, a, b):
        return a and b

class NandOperation(MathOperation):
    def __init__(self):
        super().__init__("~&", r"\uparrow", -1)
    
    def compute(self, a, b):
        return not(a and b)



class OrOperation(MathOperation):
    def __init__(self):
        super().__init__("V", r"\lor", -2)
    
    def compute(self, a, b):
        return a or b


class NorOperation(MathOperation):
    def __init__(self):
        super().__init__(r"~\/", r"\downarrow", -2)
    
    def compute(self, a, b):
        return not(a or b)

class XorOperation(MathOperation):
    def __init__(self):
        super().__init__("+@", r"\oplus", -3)
    
    def compute(self, a, b):
        return a ^ b

class NxorOperation(MathOperation):
    def __init__(self):
        super().__init__("*@", r"\odot", -3)
    
    def compute(self, a, b):
        return not(a ^ b)

class ImpliesOperation(MathOperation):
    def __init__(self):
        super().__init__("=>", r"\implies", -4)
    
    def compute(self, a, b):
        return (not a) or b

class NimpliesOperation(MathOperation):
    def __init__(self):
        super().__init__("~=>", r"\nRightarrow", -4)
    
    def compute(self, a, b):
        return a and (not b)

class ImpliedByOperation(MathOperation):
    def __init__(self):
        super().__init__("<=", r"\impliedby", -4)
    
    def compute(self, a, b):
        return a or (not b)

class NimpliedByOperation(MathOperation):
    def __init__(self):
        super().__init__("~<=", r"\nLeftarrow", -4)
    
    def compute(self, a, b):
        return (not a) and b


class IffOperation(MathOperation):
    def __init__(self):
        super().__init__("<=>", r"\iff", -4)
    
    def compute(self, a, b):
        return a == b


# Create operation instances
operations = {
    "~": NotOperation(),
    "&": AndOperation(),
    "\\/": OrOperation(),
    "=>": ImpliesOperation(),
    "<=": ImpliedByOperation(),
    "<=>": IffOperation(),
    "~&": NandOperation(),
    "~\\/": NorOperation(),
    "+@": XorOperation(),
    "*@": NxorOperation(),
    "~=>": NimpliesOperation(),
    "~<=": NimpliedByOperation()
}

# Maintain backward compatibility
order_of_operation = {op.symbol: op.precedence for op in operations.values()}

def add_token(token_list, current_pos, current_token):
    if current_token:
        token_list.append((current_pos, current_token))
        current_token = ""
    return current_token

# def parse_expression(expression):
#     tokens = []
#     current_token = ""
#     current_pos = 0
#     current_is_digit = False
#     for ch in expression:
#         if ch == " ":
#             if current_token:
#                 current_token = add_token(tokens, current_pos, current_token)
#                 current_pos += 1
#             continue
#         elif ch == "(" or ch == ")":
#             if current_token:
#                 current_token = add_token(tokens, current_pos, current_token)
#                 current_pos += 1
#             add_token(tokens, -1, ch)
#             continue
#         if ch.isalnum() != current_is_digit:
#             if current_token:
#                 current_token = add_token(tokens, current_pos, current_token)
#                 current_pos += 1
#             current_is_digit = ch.isalnum()
#         current_token += ch
#     add_token(tokens, current_pos, current_token)
#     return tokens


def parse_expression(expression):
    tokens = []
    current_token = ""
    current_pos = 0
    current_is_alnum = False

    def is_alnum_or_unicode(ch):
        # Treat letters, digits, and other Unicode categories as "alphanumeric"
        return ch.isalnum() or unicodedata.category(ch).startswith(('L', 'N'))

    for ch in expression:
        if ch.isspace():
            if current_token:
                current_token = add_token(tokens, current_pos, current_token)
                current_pos += 1
            continue
        elif ch in ("(", ")"):
            if current_token:
                current_token = add_token(tokens, current_pos, current_token)
                current_pos += 1
            add_token(tokens, -1, ch)
            continue

        if is_alnum_or_unicode(ch) != current_is_alnum:
            if current_token:
                current_token = add_token(tokens, current_pos, current_token)
                current_pos += 1
            current_is_alnum = is_alnum_or_unicode(ch)

        current_token += ch

    if current_token:
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
            while stack and stack[-1][1] in order_of_operation and order_of_operation[token] <= order_of_operation[stack[-1][1]]:
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
    print(postfix)
    return postfix

def convert_tokens_to_latex(tokens, need_math_mode=False):
    for id, token in enumerate(tokens):
        if token in operations:
            tokens[id] = operations[token].latex_symbol
        if need_math_mode:
            tokens[id] = f"${tokens[id]}$"
    return tokens

def convert_expression_to_latex(expression):
    tokens = [t for _, t in parse_expression(expression)]
    return " ".join(convert_tokens_to_latex(tokens))

