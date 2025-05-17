import streamlit as st
from sympy import symbols, Eq, solve
from sympy.parsing.sympy_parser import parse_expr
import re

st.set_page_config(
    page_title="StoichiMath",
    page_icon="🧪",
    layout="centered"
)

st.title("🧪 StoichiMath - Kalkulator Stoikiometri")

st.markdown("Masukkan reaksi kimia, dan StoichiMath akan menyetarakannya serta menghitung berdasarkan stoikiometri.")

# =====================
# 🔄 Fungsi Penyamaan
# =====================
def balance_equation(equation):
    try:
        reactants, products = equation.split("->")
        reactants = reactants.strip().split("+")
        products = products.strip().split("+")

        species = [s.strip() for s in reactants + products]
        elements = set(re.findall(r'[A-Z][a-z]*', equation))
        element_list = list(elements)

        coeffs = symbols(f'a1:{len(species)+1}')
        eqs = []

        for element in element_list:
            lhs = sum(coeffs[i] * species[i].count(element) for i in range(len(reactants)))
            rhs = sum(coeffs[i+len(reactants)] * species[i+len(reactants)].count(element) for i in range(len(products)))
            eqs.append(Eq(lhs, rhs))

        eqs.append(Eq(coeffs[0], 1))  # Fix satu koefisien agar hasil tidak trivial
        sol = solve(eqs, coeffs)
        if not sol:
            return "Tidak bisa disetarakan otomatis."

        result = []
        for i, s in enumerate(species):
            c = sol.get(coeffs[i], 1)
            result.append(f"{int(c) if c != 1 else ''}{s}")

        return " + ".join(result[:len(reactants)]) + " -> " + " + ".join(result[len(reactants):])

    except:
        return "Format salah. Contoh: H2 + O2 -> H2O"

# =====================
# 🧮 Fungsi Stoikiometri
# =====================
def calculate_stoichiometry(mol_input, ratio_from, ratio_to):
    try:
        mol = float(mol_input)
        return mol * (ratio_to / ratio_from)
    except:
        return "Input tidak valid."

# =====================
# 🔧 Input User
# =====================
reaction_input = st.text_input("Masukkan persamaan reaksi (contoh: H2 + O2 -> H2O):")

if reaction_input:
    st.subheader("📘 Persamaan yang Disetarakan:")
    balanced = balance_equation(reaction_input)
    st.success(balanced)

    st.subheader("🔢 Hitung Stoikiometri:")
    col1, col2 = st.columns(2)
    with col1:
        mol_awal = st.number_input("Mol zat yang diketahui", value=1.0)
        koef_awal = st.number_input("Koefisien zat diketahui", min_value=1)
    with col2:
        koef_tujuan = st.number_input("Koefisien zat ditanya", min_value=1)

    if st.button("Hitung"):
        mol_hasil = calculate_stoichiometry(mol_awal, koef_awal, koef_tujuan)
        st.info(f"Jumlah mol produk/zat tujuan = {mol_hasil} mol")

# =====================
# ℹ️ Footer
# =====================
st.markdown("---")
st.caption("Dibuat dengan ❤️ oleh StoichiMath | 2025")

