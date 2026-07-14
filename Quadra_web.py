from fractions import Fraction
import os
import sys
from sympy import sympify, Symbol
import math
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import io


def get_image_bytes(format_type):
    buf = io.BytesIO()
    plt.gcf().savefig(buf, format=format_type, bbox_inches="tight", dpi=300)
    buf.seek(0)
    return buf


def reset_form():
    st.session_state["coefficient_a"] = ""
    st.session_state["coefficient_b"] = ""
    st.session_state["coefficient_c"] = ""


def validate_and_convert(user_input):

    cleaned_input = user_input.replace('√', 'sqrt').strip()

    if not cleaned_input:
        raise ValueError("Порожнє поле")

    expr = sp.sympify(cleaned_input)

    if not expr.is_number:
        raise ValueError("Введення містить змінні або текст замість числа")

    return expr


def show_data():

    raw_a = entry_1
    raw_b = entry_2
    raw_c = entry_3

    try:

        a = validate_and_convert(raw_a)
        b = validate_and_convert(raw_b)
        c = validate_and_convert(raw_c)

        if a == 0:
            st.error(txt["error_a"])
            return

    except (sp.SympifyError, TypeError, ValueError, Exception):
        st.error(txt["error_input"])
        return

    if a == 1:
        term_a = "x²"
    elif a == -1:
        term_a = "-x²"
    elif a == float(a):
        term_a = f"{a:.1f}x²"
    else:
        term_a = f"{a}x²"

    try:
        b_negative = b < 0

    except:
        b_negative = False
    if b == 0:
        term_b = ""
    elif b == 1:
        term_b = " + x"
    elif b == -1:
        term_b = " - x"
    elif b_negative:
        if isinstance(b, sp.Integer):
            term_b = f" - {abs(b)}x"
        elif isinstance(b, sp.Rational):
            term_b = f" - {abs(b)}x"
        elif isinstance(b, sp.Float):
            b = b * -1
            term_b = f" - {b:.1f}x"
            b = b * -1
        else:
            term_b = f"{b}"
    elif b == float(b):
        term_b = f"+{b:.1f}x"
    else:
        term_b = f" + {b}x"

    try:
        is_c_negative = float(c.evalf()) < 0
    except:
        is_c_negative = False

    if c == 0:
        term_c = ""
    elif is_c_negative:
        if isinstance(c, sp.Integer):
            term_c = f" - {abs(c)}"
        elif isinstance(c, sp.Rational):
            term_c = f" - {abs(c)}"
        elif isinstance(c, sp.Float):
            c = c * -1
            term_c = f" - {c:.1f}"
            c = c * -1
        else:
            term_c = f"{c}"
    elif c == float(c):
        term_c = f"+{c:.1f}"
    else:
        term_c = f" + {c}"
    x0 = (-b/(2*a))
    y0 = (-b**2 + 4*a*c)/(4*a)

    Oy = c
    d = float(b**2 - 4*a*c)
    if d > 0:
        x_1 = float((-b + d**0.5) / (2*a))
        x_2 = float((-b - d**0.5) / (2*a))
        if x_1 > x_2:
            x_max = x_1
            x_min = x_2
        else:
            x_min = x_1
            x_max = x_2
        term_x = f"**x₁  = ({x_min:.1f} ; 0) , x₂ = ({x_max:.1f} ; 0)** "
    elif d == 0:
        x_0 = -b / 2*a
        term_x = f" **x_₁_₂ = ({x_0:.1f} ; 0)**"
    else:
        term_x = txt["x_axis"]

    equation_text = f"{term_a}{term_b}{term_c}"
    equation_text_2 = f"{x0:.1f}"
    equation_text_3 = f"{y0:.1f}"

    equation_text = equation_text.replace('sqrt', '√')
    equation_text_2 = equation_text_2.replace('sqrt', '√')
    equation_text_3 = equation_text_3.replace('sqrt', '√')

    st.button(txt["reset_btn"], on_click=reset_form)

    st.success(f"{txt["calc_func"]} **y = {equation_text}**")
    st.success(
        f"{txt["find_vertex_formula"]} &nbsp;&nbsp;**x₀ = - b / 2a,&nbsp;&nbsp;&nbsp;y₀ = (-b² + 4ac) / 4a** ")
    st.success(
        f"{txt["vertex"]}&nbsp;**x₀ = {equation_text_2} ;&nbsp; y₀ = {equation_text_3}**, {txt["point"]} **({equation_text_2}; {equation_text_3})**")
    st.success(f"{txt["point_0y"]}  **(0 ; {Oy:.1f})**")
    st.success(f"{txt["calc_disc"]}&nbsp;**D = b² - 4ac**")
    st.success(f"{txt["discr_D"]} **D = {d:.1f}**")
    st.success(f"{txt["find_roots_formula"]} &nbsp; **x₁,₂= -b±√D / 2a**")
    st.success(f"{txt["points_0x"]}: {term_x}")

    fig, ax = plt.subplots(figsize=(6, 6))
    x = np.linspace(-10, 10, 200)
    y = a * x**2 + b * x + c

    func_label = f"y = {equation_text}"

    ax.plot(x, y, label=func_label, color='red', linewidth=1)

    if d > 0:
        if a > 0:
            ax.plot(x0, y0, marker='o', color='blue', markersize=1.5)
            annotation_text = f'        А    \n({x0:.1f}; {y0:.1f})'
            ax.annotate(annotation_text, fontsize=10,
                        xy=(x0, y0),
                        xytext=(x0-1.2, y0-1.2), color='blue')

            ax.plot(x_1, 0, marker='o', color='blue', markersize=1.5)
            annotation_text = f'({x_1:.1f}; 0)'
            ax.annotate(annotation_text, fontsize=10,
                        xy=(x_1, 0),
                        xytext=(x_1 + 0.4, 0.2), color='blue')
            ax.plot(x_2, 0, marker='o', color='blue', markersize=1.5)
            annotation_text = f'({x_2:.1f}; 0)'
            ax.annotate(annotation_text, fontsize=10,
                        xy=(x_2, 0),
                        xytext=(x_2 - 2.2, 0.2), color='blue')
        if a < 0:
            ax.plot(x0, y0, marker='o', color='blue', markersize=1.5)
            annotation_text = f'        А    \n({x0:.1f}; {y0:.1f})'
            ax.annotate(annotation_text, fontsize=10,
                        xy=(x0, y0),
                        xytext=(x0-1.2, y0+0.2), color='blue')

            ax.plot(x_1, 0, marker='o', color='blue', markersize=1.5)
            annotation_text = f'({x_1:.1f}; 0)'
            ax.annotate(annotation_text, fontsize=10,
                        xy=(x_1, 0),
                        xytext=(x_1 - 2.2, 0.2), color='blue')
            ax.plot(x_2, 0, marker='o', color='blue', markersize=1.5)
            annotation_text = f'({x_2:.1f}; 0)'
            ax.annotate(annotation_text, fontsize=10,
                        xy=(x_2, 0),
                        xytext=(x_2 + 0.4, 0.2), color='blue')
    if d <= 0:
        if a > 0:
            ax.plot(x0, y0, marker='o', color='blue', markersize=1.5)
            annotation_text = f'        А    \n({x0:.1f}; {y0:.1f})'
            ax.annotate(annotation_text, fontsize=10,
                        xy=(x0, y0),
                        xytext=(x0-1.2, y0-1.2), color='blue')

        if a < 0:
            ax.plot(x0, y0, marker='o', color='blue', markersize=1.5)
            annotation_text = f'        А    \n({x0:.1f}; {y0:.1f})'
            ax.annotate(annotation_text, fontsize=10,
                        xy=(x0, y0),
                        xytext=(x0-1.2, y0+0.2), color='blue')

    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xticks(np.arange(-10, 11, 1))
    ax.set_yticks(np.arange(-10, 11, 1))

    ax.grid(True, linestyle='-.', alpha=0.1)
    ax.legend()
    ax.set_title(f"{txt["graph_title"]} {func_label}")

    st.pyplot(fig)

    st.write("---")
    st.subheader(f"{txt["export_header"]}")

    col1, col2 = st.columns([1, 2], gap="small")

    png_bytes = get_image_bytes("png")
    pdf_bytes = get_image_bytes("pdf")

    plt.close(fig)

    col1.download_button(
        label=txt["download_png"],
        data=png_bytes,
        file_name="q_function.png",
        mime="image/png",)

    col2.download_button(
        label=txt["download_pdf"],
        data=pdf_bytes,
        file_name="q_function.pdf",
        mime="application/pdf",)


LANGUAGES = {
    "🇺🇦 Українська": {
        "title": "Калькулятор квадратичної функції",
        "coef_a": "Коефіцієнт a",
        "coef_b": "Коефіцієнт b",
        "coef_c": "Коефіцієнт c",
        "calc_btn": "Розрахувати",
        "export_header": "📥 Експорт",
        "download_png": "📷 Завантажити як PNG",
        "download_pdf": "📄 Завантажити як PDF",
        "donate_btn": "☕ Пригостити автора кавою",
        "reset_btn": "Скинути значення",
        "error_a": "Увага! Коефіцієнт 'a' не може дорівнювати 0 для квадратичної функції!",
        "error_input": "Помилка! Дозволено лише: цілі, дробові та числа з коренем (√).\nПідкореневі числа записуються в душках √(n)\n де n потрібне число.",
        "x_axis": "Графік функції не перетинає вісь 0х.",
        "points_0x": "Точки перетину з віссю 0х:",
        "calc_func": "Обчислюємо функцію:",
        "find_vertex_formula": "Знаходимо вершину параболи(Х₀;У₀) за формулами:",
        "vertex": "Вершина параболи",
        "point": "Точка А",
        "point_0y": "Точка перетину з віссю 0у:",
        "calc_disc": "Обчислюємо Дискримінант за формулою:",
        "discr_D": "Дискримінант:",
        "find_roots_formula": "Знаходимо корені функції за формулою:",
        "graph_title": "Графік функції:",
        "footer_text": """Copyright © 2026 Babiuk Alex.
        Цей проєкт є програмним забезпеченням з відкритим вихідним кодом і поширюється під ліцензією GNU AGPLv3.
        Ви можете вільно використовувати, поширювати та модифікувати цей код, за умови збереження авторства та відкриття вихідного коду ваших похідних проєктів.
        
        Програма надається "ЯК Є", без жодних гарантій. Автор не несе відповідальності за будь-які наслідки її використання.""",

    },
    "🇬🇧 English": {
        "title": "Quadratic Function Calculator",
        "coef_a": "Coefficient a",
        "coef_b": "Coefficient b",
        "coef_c": "Coefficient c",
        "calc_btn": "Calculate",
        "export_header": "📥 Export",
        "download_png": "📷 Download as PNG",
        "download_pdf": "📄 Download as PDF",
        "donate_btn": "☕ Buy me a coffee",
        "reset_btn": "Reset",
        "error_a": "Attention! The coefficient 'a' cannot be equal to 0 for a quadratic function!",
        "error_input": "Error! Only integers, decimals, and square root numbers (√) are allowed.\nNumbers under the root must be written in parentheses as √(n), where n is the desired number.",
        "x_axis": "The graph of the function does not intersect the x-axis.",
        "points_0x": "x-intercepts",
        "calc_func": "Calculating the function:",
        "find_vertex_formula": "Finding the parabola vertex (X₀, Y₀) using formulas:",
        "vertex": "Parabola vertex",
        "point": "Point A",
        "point_0y": "y-intercept:",
        "calc_disc": "Calculating the Discriminant using the formula:",
        "discr_D": "Discriminant:",
        "find_roots_formula": "Finding the roots of the function using the formula:",
        "graph_title": "Graph of the function:",
         "footer_text": """Copyright © 2026 Babiuk Alex.
         This project is open-source software licensed under the GNU AGPLv3.
         You are free to use, distribute, and modify this code, provided that authorship is preserved and the source code of your derivative projects remains open.
         
         The program is provided "AS IS", without warranties of any kind. The author shall not be liable for any consequences arising from its use.""",

    },
}

st.session_state.setdefault("coefficient_a", "")
st.session_state.setdefault("coefficient_b", "")
st.session_state.setdefault("coefficient_c", "")

col_title, col_lang = st.columns([4, 1.5])
with col_lang:
    #st.write("")
    selected_lang = st.selectbox(
        "Language",
        list(LANGUAGES.keys()),
        label_visibility="collapsed",
        key="app_language_selector",
    )

txt = LANGUAGES[selected_lang]

with col_title:
    st.title(txt["title"])

label = st.subheader("y = ax² + bx + c")

entry_1 = st.text_input(txt["coef_a"], key="coefficient_a")


entry_2 = st.text_input(txt["coef_b"], key="coefficient_b")


entry_3 = st.text_input(txt["coef_c"], key="coefficient_c")

if st.button(txt["calc_btn"], type="primary"):
    show_data()
