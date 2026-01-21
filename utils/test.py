from table_latex import write_logic_table_latex
from util_latex_general import parse_expression

latex_output_file = "output.tex"

write_logic_table_latex(latex_output_file, r"Q <= R *@ ~P & Q")
expr = "3 + π * (α + β) ∑漢字"
print(parse_expression(expr))

