from sympy import symbols, solve, Eq, Abs
import sympy


def write_line(opened_file, line, tab_count=0):
    opened_file.write("\t" * tab_count + "\\" + line + "\n")


def write_graph_code(
    file, functions, x_clip, y_clip, samples=None, decimal=False, x_scale=1, y_scale=1,
    x_label="x", y_label="y"
):
    color_order = ["colorEmphasisCyan", "colorEmphasis"]

    with open(file, "w", encoding="utf-8") as f:
        write_line(f, r"begin{figure}[H]")
        write_line(f, "centering", 1)
        write_line(f, r"begin{tikzpicture}", 1)

        write_line(
            f,
            f"draw[->] ({x_clip[0]}, 0) -- ({x_clip[1]}, 0) node[right] " + "{$" + x_label + "$};",
            2,
        )
        write_line(
            f,
            f"draw[->] (0, {y_clip[0]}) -- (0, {y_clip[1]})  node[above] " + "{$" + y_label + "$};",
            2,
        )

        caption = ""

        for func_id, func in enumerate(functions):
            x = symbols("x")

            # Get all the possible ending points
            ends = []
            pre_x_scale = func
            pre_expression = eval(pre_x_scale)
            caption += "$" + sympy.latex(pre_expression) + "$"
            post_x_scale = func.replace("x", f"(x/{x_scale})")
            expression = eval(post_x_scale)
            if func_id != len(functions) - 1:
                caption += ","

            solutions = solve(Eq(expression, y_clip[0] * y_scale), x)
            solutions = [
                sol.evalf().as_real_imag()[0]
                for sol in solutions
                if abs(sol.as_real_imag()[1]) < 1e-10
            ]
            ends += solutions

            solutions = solve(Eq(expression, y_clip[1] * y_scale), x)
            solutions = [
                sol.evalf().as_real_imag()[0]
                for sol in solutions
                if abs(sol.as_real_imag()[1]) < 1e-10
            ]
            ends += solutions

            ends += list(set(x_clip))

            # Sort and filter the ending points
            ends.sort()
            ends = [x for x in ends if x_clip[0] <= x <= x_clip[1]]
            # print(ends)

            for i in range(len(ends) - 1):
                value = expression.subs(x, ends[i] + 0.05)
                # print(value)

                if value / float(y_scale) < y_clip[1] and value / float(y_scale) > y_clip[0]:
                    func = post_x_scale.replace("x", r"(\x)").replace("**", "^")
                    write_line(
                        f,
                        f"draw[graph thickness, samples=80, color={color_order[func_id]}, domain={ends[i]:.3f}:{ends[i + 1]:.3f}] plot "
                        + r"(\x, {("
                        + func
                        + f") / {y_scale}"
                        + r"});",
                        2,
                    )

            # Graph sample points
            for point in samples or []:
                if decimal:
                    if isinstance(point, tuple):
                        p = float(point[0]) / float(point[1])
                    else:
                        p = float(point)

                    value = float(sympy.N(pre_expression.subs(x, p)))
                    p_latex = f"{p:.2f}".replace(".", "{,}")
                    value_latex = f"{value:.2f}".replace(".", "{,}")
                    y_scale = float(y_scale)
                    if value / y_scale < y_clip[1] and value / y_scale > y_clip[0]:
                        write_line(
                            f,
                            f"filldraw[color={color_order[func_id]}] (" 
                            + "{"
                            + f"{p * x_scale}" + "}" 
                            + f", {{ {value / y_scale} }}) circle (\pointSize) node[above] "
                            + r"{$\left("
                            + f"{p_latex};{value_latex}"
                            + r"\right)$};",
                            2,
                        )
                else:
                    if isinstance(point, tuple):
                        p = float(point[0]) / float(point[1])
                        p_rational = sympy.Rational(*point)
                    elif isinstance(point, float):
                        p = point
                        p_rational = sympy.Rational(point)
                    else:
                        p = point
                        p_rational = point
                    value = pre_expression.subs(x, p_rational)
                    p_latex = sympy.latex(p_rational).replace(".", "{,}")
                    value_latex = sympy.latex(value).replace(".", "{,}")
                    # print(p_latex, value_latex)
                    if value / y_scale < y_clip[1] and value / y_scale > y_clip[0]:
                        write_line(
                            f,
                            f"filldraw[color={color_order[func_id]}] ({{ {p * 1.0 * x_scale} }}, {{ {float(value / y_scale)} }}) circle (\pointSize) node[above] "
                            + r"{$\left({"
                            + p_latex
                            + "};{"
                            + value_latex
                            + r"}\right)$};",
                            2,
                        )

        write_line(f, r"end{tikzpicture}", 1)
        write_line(f, r"caption{Đồ thị của " + caption + "}", 1)
        write_line(f, r"end{figure}")

def write_scatter_plot_latex(
    file, x_clip, y_clip, caption,
    points, x_scale=1, y_scale=1, decimal=True, color="colorEmphasisCyan",
    x_label="x", y_label="y"
):
    x_clip = [x / x_scale for x in x_clip]
    y_clip = [y / y_scale for y in y_clip]
    
    with open(file, "w", encoding="utf-8") as f:
        write_line(f, r"begin{figure}[H]")
        write_line(f, "centering", 1)
        write_line(f, r"begin{tikzpicture}", 1)
        write_line(
            f,
            f"draw[->] ({x_clip[0]}, 0) -- ({x_clip[1]}, 0) node[right] " + "{$" + x_label + "$};",
            2,
        )
        write_line(
            f,
            f"draw[->] (0, {y_clip[0]}) -- (0, {y_clip[1]})  node[above] " + "{$" + y_label + "$};",
            2,
        )
        for point in points:
            if decimal:
                x_scaled = point[0] / x_scale
                y_scaled = point[1] / y_scale
                x_latex = f"{point[0]:.2f}".replace(".", "{,}")
                y_latex = f"{point[1]:.2f}".replace(".", "{,}")
            else:
                x_scaled = sympy.Rational(point[0]) / x_scale
                y_scaled = sympy.Rational(point[1]) / y_scale
                x_latex = sympy.latex(sympy.Rational(point[0]))
                y_latex = sympy.latex(sympy.Rational(point[1]))
            if x_scaled < x_clip[0] or x_scaled > x_clip[1] or y_scaled < y_clip[0] or y_scaled > y_clip[1]:
                continue
            write_line(
                f,
                f"filldraw[color={color}] ({x_scaled}, {y_scaled}) circle (\pointSize) node[above] "
                + r"{$\left(" + x_latex + ";" + y_latex + r"\right)$};",
                2,
            )
        write_line(f, r"end{tikzpicture}", 1)
        write_line(f, r"caption{Đồ thị của " + caption + "}", 1)
        write_line(f, r"end{figure}")