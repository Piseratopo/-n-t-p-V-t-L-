from table_latex import write_logic_table_latex
from util_latex_general import parse_expression_with_parentheses

latex_output_file = "output.tex"

write_logic_table_latex(latex_output_file, r"(A *@ B) & (B +@ C) & (C *@ D) & (D <=> A)")

