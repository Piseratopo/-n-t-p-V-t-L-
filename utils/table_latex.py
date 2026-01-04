from util_latex_general import write_line, convert_expression_to_latex, convert_expression_to_postfix

def write_logic_table_latex(file, expression):
    with open(file, "w", encoding="utf-8") as f:
        write_line(f, r"begin{table}[H]")
        write_line(f, r"centering", 1)
        write_line(f, r"caption{Bảng giá trị chân lí của $" + convert_expression_to_latex(expression) + r"$}", 1)
        print(convert_expression_to_postfix(expression))
        write_line(f, r"begin{tabular}{|c|c|c" + "c" * len(convert_expression_to_postfix(expression)) + r"|}", 1)
        write_line(f, r"hline", 2)
        write_line(f, r"end{tabular}", 1)
        write_line(f, r"end{table}")
        