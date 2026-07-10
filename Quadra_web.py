"""
Copyright © 2026 Babiuk Alex. Всі права захищені.

Ця програма є об'єктом інтелектуальної власності автора.
Користувачеві надається обмежена, невиключна ліцензія на використання
програми суто в особистих або внутрішніх комерційних цілях.

КАТЕГОРИЧНО ЗАБОРОНЯЄТЬСЯ:
1. Копіювати, поширювати або передавати програму третім особам.
2. Проводити реверс-инжиніринг, декомпіляцію або модифікацію коду.
3. Використовувати програму для створення конкуруючих продуктів.

ПРОГРАМА НАДАЄТЬСЯ "ЯК Є" (AS IS), БЕЗ ЖОДНИХ ГАРАНТІЙ. АВТОР НЕ НЕСЕ
ВІДПОВІДАЛЬНОСТІ ЗА БУДЬ-ЯКІ ЗБИТКИ ВНАСЛІДОК ЇЇ ВИКОРИСТАННЯ.
"""

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
            st.error(
                "Увага! Коефіцієнт 'a' не може дорівнювати 0 для квадратичної функції!")
            return

    except (sp.SympifyError, TypeError, ValueError, Exception):
        st.error("Помилка! Дозволено лише: цілі, дробові та числа з коренем (√).\nПідкореневі числа записуються в душках √(n)\n де n потрібне число."
                 )
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
        term_x = f"**Графік функції не перетинає вісь 0х.**"

    equation_text = f"{term_a}{term_b}{term_c}"
    equation_text_2 = f"{x0:.1f}"
    equation_text_3 = f"{y0:.1f}"

    equation_text = equation_text.replace('sqrt', '√')
    equation_text_2 = equation_text_2.replace('sqrt', '√')
    equation_text_3 = equation_text_3.replace('sqrt', '√')

    st.success(f"Обчислюємо функцію: **y = {equation_text}**")
    st.success(
        "Знаходимо вершину параболи(Хо;Уо) за формулами: &nbsp;&nbsp;**x₀ = - b / 2a,&nbsp;&nbsp;&nbsp;y₀ = (-b² + 4ac) / 4a** ")
    st.success(
        f"Вершина параболи:&nbsp;**x₀ = {equation_text_2} ;&nbsp; y₀ = {equation_text_3}**, точка А **({equation_text_2}; {equation_text_3})**")
    st.success(f"Точка перетину з віссю 0у:  **(0 ; {Oy:.1f})**")
    st.success("Обчислюємо Дискримінант за формулою:&nbsp;**D = b² - 4ac**")
    st.success(f"Дискримінант **D = {d:.1f}**")
    st.success("Знаходимо корені функції за формулою: &nbsp; **x₁,₂= -b±√D / 2a**")
    st.success(f"Точки перетину з віссю 0х: {term_x}")

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
    ax.set_title(f"Графік функції: {func_label}")

    st.pyplot(fig)

    st.write("---")
    st.subheader("📥 Експорт")

    col1, col2 = st.columns([1, 2], gap="small")

    png_bytes = get_image_bytes("png")
    pdf_bytes = get_image_bytes("pdf")

    plt.close(fig)

    col1.download_button(
        label="📷 Завантажити графік як PNG",
        data=png_bytes,
        file_name="quadratic_function.png",
        mime="image/png",)

    col2.download_button(
        label="📄 Завантажити графік як PDF",
        data=pdf_bytes,
        file_name="quadratic_function.pdf",
        mime="application/pdf",)


st.session_state.setdefault("coefficient_a", "")
st.session_state.setdefault("coefficient_b", "")
st.session_state.setdefault("coefficient_c", "")


label = st.subheader("y = ax² + bx + c")

entry_1 = st.text_input("Введіть значення a:", key="coefficient_a")


entry_2 = st.text_input("Введіть значення b:", key="coefficient_b")


entry_3 = st.text_input("Введіть значення c:", key="coefficient_c")

if st.button("Розрахувати", type="primary"):
    show_data()


st.button("Скинути значення", on_click=reset_form)
