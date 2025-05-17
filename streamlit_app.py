import streamlit as st
import re
from sympy import symbols, Eq, solve
from collections import defaultdict

st.title("🧪 StoichiMath")
st.write("Aplikasi ini membantu kamu untuk menghitung jumlah mol produk dan sisa reaktan berdasarkan persamaan reaksi kimia dan jumlah mol reaktan secara otomatis.")
st.sidebar.title("Perhitungan Stoikiometeri")
option = st.sidebar.selectbox(
    "Pilih opsi:", 
    [
        "Perhitungan Massa dan mol", 
        "Perhitungan mol dari massa", 
        "perhitungan volume gas", 
        "perhitungan jumlah partikel dari mol", 
        "perhitungan perbandingan mol",
    ] 
) 
st.write(f"Kamu memilih: {option}")
# Konten utama berubah sesuai pilihan di sidebar
if option == "Perhitungan Massa dan mol":
    st.header("Perhitungan Massa dan mol")
    massa = st.number_input("Masukkan massa (gram):", min_value=0.0)
    molar_mass = st.number_input("Masukkan massa molar (g/mol):", min_value=0.0)
    if massa > 0 and molar_mass > 0:
        mol = massa / molar_mass
        st.write(f"Jumlah mol = {mol}")

elif option == "Perhitungan mol dari massa":
    st.header("Perhitungan mol dari massa")
    mol = st.number_input("Masukkan jumlah mol zat (mol):", min_value=0.0, format="%.4f")
    massa_molar = st.number_input("Masukkan massa molar zat (g/mol):", min_value=0.0, format="%.4f")
    if st.button("Hitung Massa"):
        massa = mol_ke_massa(mol, massa_molar)
        st.success(f"Massa zat = {massa:.4f} gram")

elif option == "Perhitungan volume gas":
    st.header("Perhitungan volume gas")
    mol = st.number_input("Masukkan jumlah mol gas (mol):", min_value=0.0, format="%.4f")
    if st.button("Hitung Volume Gas"):
        volume = mol_ke_volume(mol)
        st.success(f"Volume gas pada STP = {volume:.4f} liter")

        # Penyelesaian
        st.markdown("### 🧮 Penyelesaian")
        st.latex(r"V = n \times 22.4\ L")
        st.latex(f"V = {mol} \\times 22.4")
        st.latex(f"V = {volume:.4f}~L")


elif option == "Perhitungan jumlah partikel dari mol":
    st.header("Perhitungan jumlah partikel dari mol")
    mol = st.number_input("Masukkan jumlah mol zat (mol):", min_value=0.0, format="%.4f")
    if st.button("Hitung Jumlah Partikel"):
        partikel = mol_ke_partikel(mol)
        st.success(f"Jumlah partikel = {partikel:.4e} partikel")

        # Penyelesaian
        st.markdown("### 🧮 Penyelesaian")
        st.latex(r"N = n \times N_A")
        st.latex(r"N_A = 6.022 \times 10^{23}")
        st.latex(f"N = {mol} \\times 6.022 \\times 10^{{23}}")
        st.latex(f"N = {partikel:.4e}~partikel")

elif option == "Perhitungan perbandingan mol":
    st.header("Perhitungan perbandingan mol")
    mol_1 = st.number_input("Masukkan jumlah mol zat 1 (mol):", min_value=0.0, format="%.4f")
    koefisien_1 = st.number_input("Masukkan koefisien reaksi zat 1:", min_value=0.1, format="%.2f")
    koefisien_2 = st.number_input("Masukkan koefisien reaksi zat 2:", min_value=0.1, format="%.2f")
    if st.button("Hitung Mol Zat 2"):
        mol_2 = perbandingan_mol(mol_1, koefisien_1, koefisien_2)
        st.success(f"Jumlah mol zat 2 = {mol_2:.4f} mol")

st.markdown("---")
st.caption("🚀 Dibuat dengan ❤️ oleh StoichiMath")


