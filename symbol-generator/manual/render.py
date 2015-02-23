#!/usr/bin/env python

import os


def formula_as_file(formula, file_path, packages=""):
    # assert file_path.endswith(".svg")
    with open("formula.template.tex") as f:
        template = f.read()

    template = template.replace("{{formula}}", formula)
    template = template.replace("{{packages}}", packages)
    print(template)

    with open("formulatmp.tex", "w") as f:
        f.write(template)

    os.system("pdflatex formulatmp.tex -output-format=pdf")
    os.system("pdf2svg formulatmp.pdf formulatmp.svg")
    os.system("inkscape formulatmp.svg -h 40 --export-png=%s" % file_path)


def main():
    """Run examples."""
    formulas = []
    formula = (r"\bold H = \begin{bmatrix}"
               r"\dfrac{\partial^2 f}{\partial x_1^2} & "
               r"\dfrac{\partial^2 f}{\partial x_1\,\partial x_2} & "
               r"\cdots & "
               r"\dfrac{\partial^2 f}{\partial x_1\,\partial x_n} \\[2.2ex]"
               r"\dfrac{\partial^2 f}{\partial x_2\,\partial x_1} & "
               r"\dfrac{\partial^2 f}{\partial x_2^2} & "
               r"\cdots & "
               r"\dfrac{\partial^2 f}{\partial x_2\,\partial x_n} \\[2.2ex]"
               r"\vdots & \vdots & \ddots & \vdots \\[2.2ex]"
               r"\dfrac{\partial^2 f}{\partial x_n\,\partial x_1} & "
               r"\dfrac{\partial^2 f}{\partial x_n\,\partial x_2} & "
               r"\cdots & \dfrac{\partial^2 f}{\partial x_n^2}"
               r"\end{bmatrix}.")
    formulas.append(("hesse-matrix.png", formula))
    formula = (r"\int x^a\,dx = \frac{x^{a+1}}{a+1} + "
               r"C \qquad\text{(for } a\neq -1\text{)}\,\!")
    formulas.append(("cavalieri-quadrature-formula.png", formula))
    for file_path, formula in formulas:
        formula_as_file(formula, file_path)

if __name__ == '__main__':
    main()
