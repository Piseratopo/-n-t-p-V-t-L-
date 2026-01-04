from sympy import symbols, solve, sqrt, Eq, Expr, Float
import sympy


from util_latex_general import write_line

def substitute_in_expression(expression, x, value):
    # If it's a SymPy expression, use subs
    if isinstance(expression, Expr):
        return expression.subs(x, value)
    # Otherwise (constant, int, float, etc.), just return it
    return Float(expression)

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

def write_graph_code(
    file, functions, x_clips, y_clips, sample_sets=[], decimal=False, x_scale=1, y_scale=1,
    x_label="x", y_label="y", colors=["colorEmphasisCyan"]
):
    with open(file, "w", encoding="utf-8") as f:
        # Initialize the figure
        write_line(f, r"begin{figure}[H]")
        write_line(f, "centering", 1)
        write_line(f, r"begin{tikzpicture}", 1)

        # Draw the axis
        x_clip_starts = [xc[0] for xc in x_clips]
        x_clip_ends = [xc[1] for xc in x_clips]
        y_clip_starts = [yc[0] for yc in y_clips]
        y_clip_ends = [yc[1] for yc in y_clips]
        write_line(
            f,
            f"draw[->] ({min(x_clip_starts)}, 0) -- ({max(x_clip_ends)}, 0) node[right] " + "{$" + x_label + "$};",
            2,
        )
        write_line(
            f,
            f"draw[->] (0, {min(y_clip_starts)}) -- (0, {max(y_clip_ends)})  node[above] " + "{$" + y_label + "$};",
            2,
        )

        caption = ""

        for func_id, func in enumerate(functions):
            x_clip = x_clips[func_id % len(x_clips)]
            y_clip = y_clips[func_id % len(y_clips)]
            
            current_color = colors[func_id % len(colors)]
            x = symbols("x")
            
            pre_x_scale = func
            pre_expression = eval(pre_x_scale)
            post_x_scale = func.replace("x", f"(x/{x_scale})")
            expression = eval(post_x_scale)
                        
            # Adding function names to caption
            caption += "$" + sympy.latex(pre_expression) + "$"
            if func_id != len(functions) - 1:
                caption += ","

            # Get all the possible ending points by solving for the border cases
            ends = []
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
                value = substitute_in_expression(expression, x, ends[i] + 0.05)
                re_part, im_part = value.as_real_imag()
                is_real = abs(float(im_part)) < 1e-10
                if not is_real:
                    continue
                v = float(re_part) / float(y_scale)

                if v < y_clip[1] and v > y_clip[0]:
                    func = post_x_scale.replace("x", r"(\x)").replace("**", "^")
                    write_line(
                        f,
                        f"draw[graph thickness, samples=80, color={current_color}, domain={ends[i]:.3f}:{ends[i + 1]:.3f}] plot "
                        + r"(\x, {("
                        + func
                        + f") / {y_scale}"
                        + r"});",
                        2,
                    )

            sample_set = []
            if sample_sets:
                sample_set = sample_sets[func_id % len(sample_sets)]
            # Graph sample points
            for point in sample_set:
                if decimal:
                    if isinstance(point, tuple):
                        p = float(point[0]) / float(point[1])
                    else:
                        p = float(point)

                    value = float(sympy.N(substitute_in_expression(pre_expression, x, p)))
                    p_latex = f"{p:.2f}".replace(".", "{,}")
                    value_latex = f"{value:.2f}".replace(".", "{,}")
                    y_scale = float(y_scale)
                    if value / y_scale < y_clip[1] and value / y_scale > y_clip[0]:
                        write_line(
                            f,
                            f"filldraw[color={current_color}] (" 
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
                    value = substitute_in_expression(pre_expression, x, p_rational)
                    p_latex = sympy.latex(p_rational).replace(".", "{,}")
                    value_latex = sympy.latex(value).replace(".", "{,}")
                    # print(p_latex, value_latex)
                    if value / y_scale < y_clip[1] and value / y_scale > y_clip[0]:
                        write_line(
                            f,
                            f"filldraw[color={current_color}] ({{ {p * 1.0 * x_scale} }}, {{ {float(value / y_scale)} }}) circle (\pointSize) node[above] "
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