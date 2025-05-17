import streamlit as st
import re
from sympy import symbols, Eq, solve
from collections import defaultdict

st.title("🧪 StoichiMath")
st.sidebar.title("Perhitungan Stoikiometeri")
option = st.sidebar.selectbox(
    "Pilih opsi:", 
    [
        "Perhitungan Mol", 
        "Perhitungan Massa", 
        "perhitungan volume gas", 
        "perhitungan jumlah partikel dari mol", 
        "perhitungan perbandingan mol",
    ] 
) 

# Konten utama berubah sesuai pilihan di sidebar
if option == "Perhitungan Mol":
    st.header("Perhitungan Mol")
    st.write("kamu bisa menghitung jumlah mol dari massa dan massa molar")
    massa = st.number_input("Masukkan massa (gram):", min_value=0.0)
    molar_mass = st.number_input("Masukkan massa molar (g/mol):", min_value=0.0)
    if massa > 0 and molar_mass > 0:
        mol = massa / molar_mass
        st.write(f"Jumlah mol = {mol}")
        
        # Penyelesaian dan rumus
        st.markdown("🧮 Penyelesaian")
        st.latex(r"n = \frac{massa}{massa\ molar}")
        st.latex(f"n = \\frac{{{massa}~gram}}{{{molar_mass}~g/mol}}")
        st.latex(f"n = {mol:.4f}~mol")
    else:
        st.error("Massa molar harus lebih besar dari nol.")
        
def mol_ke_massa(mol, massa_molar):
    return mol * massa_molar       
if option == "Perhitungan Massa":
    st.header("Perhitungan Massa")
    st.write("Kamu bisa menghitung massa dari mol dan massa molar")
    
    mol = st.number_input("Masukkan jumlah mol zat (mol):", min_value=0.0, format="%.4f")
    massa_molar = st.number_input("Masukkan massa molar zat (g/mol):", min_value=0.0, format="%.4f")
    
    if st.button("Hitung Massa"):
        if mol > 0 and massa_molar > 0:
            massa = mol_ke_massa(mol, massa_molar)
            st.success(f"Massa zat = {massa:.4f} gram")

            # Penyelesaian
            st.markdown("### 🧮 Penyelesaian")
            st.latex(r"massa = mol \times massa\ molar")
            st.latex(f"massa = {mol} \\times {massa_molar}")
            st.latex(f"massa = {massa:.4f}~gram")
        else:
            st.error("Jumlah mol dan massa molar harus lebih dari nol.")


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


