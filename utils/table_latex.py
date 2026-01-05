from unittest import result
from util_latex_general import write_line, convert_expression_to_latex, convert_expression_to_postfix, parse_expression_with_parentheses, convert_tokens_to_latex
from itertools import product


def evaluate_postfix_logic_expression_with_steps(postfix_expression, variables_values):
    stack = []
    processing_values = [False] * len(postfix_expression)

    def add_to_stack(_id, value):
        stack.append((_id, value))
        processing_values[_id] = value

    for _id, token in postfix_expression:
        if token in ["&", "V", "=>", "<=", "<=>"]:
            if len(stack) >= 2:
                b = stack.pop()[1]
                a = stack.pop()[1]
                if token == "&":
                    result = a and b
                elif token == "V":
                    result = a or b
                elif token == "=>":
                    result = not a or b
                elif token == "<=":
                    result = a or not b
                elif token == "<=>":
                    result = a == b
                add_to_stack(_id, result)
        elif token == "~":
            if stack:
                add_to_stack(_id, not stack.pop()[1])
        else:
            clean_token = token.lstrip("(").rstrip(")")
            add_to_stack(_id, variables_values.get(clean_token, False))
    return stack[0] if stack else False, processing_values

def write_logic_table_latex(file, expression):
    with open(file, "w", encoding="utf-8") as f:
        write_line(f, r"\begin{table}[H]")
        write_line(f, r"\centering", 1)
        write_line(f, r"\caption{Bảng giá trị chân lí của $" + convert_expression_to_latex(expression) + r"$}", 1)

        postfix_expression = convert_expression_to_postfix(expression)
        variables = sorted(list(set([token for _id, token in postfix_expression if token not in ["&", "V", "~", "(", ")", "=>", "<=", "<=>"]])))
        column_format = "|" + "|".join("c" for _ in variables) + "|" + "c" * len(postfix_expression) + "|"
        write_line(f, r"\begin{tabular}{" + column_format + "}", 1)
        write_line(f, r"\hline", 2)
        header_line = " & ".join(variables) + " & " + " & ".join([token for token in convert_tokens_to_latex([token for _, token in parse_expression_with_parentheses(expression)], need_math_mode=True)]) + " \\\\"
        write_line(f, header_line, 2)
        write_line(f, r"\headerDivider", 2)
        for comb in product([True, False], repeat=len(variables)):
            variables_values = dict(zip(variables, comb))
            def convert_bool_to_vietnamese(value):
                return "Đ" if value else "S"
            
            row_values = [convert_bool_to_vietnamese(v) for v in comb]
            line_content = " & ".join(row_values) + " & "
            
            result, processing_values = evaluate_postfix_logic_expression_with_steps(postfix_expression, variables_values)
            for _id, v in enumerate(processing_values):
                if _id == result[0]:
                    line_content += r"\emphcolor{" + convert_bool_to_vietnamese(v) + "} & "
                else:
                    line_content += f"{convert_bool_to_vietnamese(v)} & "
            
            line_content = line_content.rstrip(" & ") + " \\\\"
            write_line(f, line_content, 2)
        write_line(f, r"\hline", 2)
        write_line(f, r"\end{tabular}", 1)
        write_line(f, r"\end{table}")
        