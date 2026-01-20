from table_latex import write_logic_table_latex

latex_output_file = "output.tex"

write_logic_table_latex(latex_output_file, r"P ~& (Q ~\/ ~P)")
