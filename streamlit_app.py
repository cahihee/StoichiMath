import streamlit as st
import re
from sympy import symbols, Eq, solve
from collections import defaultdict
from streamlit_lottie import st_lottie
import requests

st.title("🧪 StoichiMath")
st.sidebar.title("StoichiMath")
option = st.sidebar.selectbox(
    "Pilih opsi:", 
    [
        "Main Menu",
        "Perhitungan Mol", 
        "Perhitungan Massa", 
        "Perhitungan Volume Gas", 
        "Perhitungan Jumlah Partikel", 
        "Perbandingan Mol",
        "Reaktan Pembatas",
        "Perhitungan Yield",
        "About StoichiMath",
    ] 
) 

# Konten utama berubah sesuai pilihan di sidebar
if option == "Main Menu":
    st.write("Selamat Datang di StoichiMath!")
    st.markdown("""
    **StoichiMath** adalah aplikasi interaktif untuk membantu menghitung berbagai konsep dasar stoikiometri. Aplikasi ini kami rancang untuk membantu mempermudah perhitungan Stoikiometri yang juga akan membahas penyelesaian masalahnya:

    🔹 Perhitungan mol, massa, dan massa molar  
    🔹 Volume gas pada kondisi STP  
    🔹 Jumlah partikel menggunakan bilangan Avogadro  
    🔹 Perbandingan mol berdasarkan persamaan reaksi  
    🔹 Reaktan pembatas  
    🔹 Yield (hasil reaksi)

    ---
    Pilih fitur di sidebar kiri untuk mulai menggunakan!
    """)
def massa_ke_mol(massa, massa_molar):
    return massa / massa_molar

if option == "Perhitungan Mol":
    st.header("Perhitungan Mol dari Massa dan Massa Molar")
    massa = st.number_input("Masukkan massa zat (gram):", min_value=0.0, format="%.4f")
    massa_molar = st.number_input("Masukkan massa molar zat (g/mol):", min_value=0.0, format="%.4f")

    if st.button("Hitung Mol"):
        if massa > 0 and massa_molar > 0:
            mol = massa_ke_mol(massa, massa_molar)
            st.success(f"Jumlah mol = {mol:.4f} mol")

            # Penyelesaian dan rumus
            st.markdown("### 🧮 Penyelesaian")
            st.latex(r"n = \frac{massa}{massa\ molar}")
            st.latex(f"n = \\frac{{{massa}}}{{{massa_molar}}}")
            st.latex(f"n = {mol:.4f}~mol")
        else:
            st.error("Massa dan massa molar harus lebih dari nol.")
        
def mol_ke_massa(mol, massa_molar):
    return mol * massa_molar       
if option == "Perhitungan Massa":
    st.header("Perhitungan Massa")
    
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

def mol_ke_partikel(mol):
    avogadro = 6.022e23
    return mol * avogadro
if option == "Perhitungan Jumlah Partikel":
    st.header("Perhitungan Jumlah Partikel")
    mol = st.number_input("Masukkan jumlah mol zat (mol):", min_value=0.0, format="%.4f")
    
    if st.button("Hitung Jumlah Partikel"):
        if mol > 0:
            partikel = mol_ke_partikel(mol)
            st.success(f"Jumlah partikel = {partikel:.2e} partikel")

            st.markdown("### 🧮 Penyelesaian")
            st.latex(r"jumlah\ partikel = mol \times N_A")
            st.latex(f"jumlah\ partikel = {mol} \\times 6.022 \\times 10^{{23}}")
            st.latex(f"jumlah\ partikel = {partikel:.2e}")
        else:
            st.error("Jumlah mol harus lebih dari nol.")


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

if option == "Perbandingan Mol":
    st.header("Perbandingan Mol Reaktan dan Produk")
    mol_diketahui = st.number_input("Masukkan jumlah mol zat A (mol):", min_value=0.0, format="%.4f")
    koefisien_A = st.number_input("Koefisien zat A:", min_value=1)
    koefisien_B = st.number_input("Koefisien zat B:", min_value=1)
    
    if st.button("Hitung Mol B"):
        if mol_diketahui > 0:
            mol_B = mol_diketahui * (koefisien_B / koefisien_A)
            st.success(f"Mol zat B = {mol_B:.4f} mol")

            st.markdown("### 🧮 Penyelesaian")
            st.latex(r"mol_B = mol_A \times \frac{koef_B}{koef_A}")
            st.latex(f"mol_B = {mol_diketahui} \\times \\frac{{{koefisien_B}}}{{{koefisien_A}}}")
            st.latex(f"mol_B = {mol_B:.4f}~mol")
        else:
            st.error("Mol zat A harus lebih dari nol.")

def mol_ke_volume_gas(mol):
    volume_molar = 22.4  # L/mol pada STP
    return mol * volume_molar

if option == ("Perhitungan Volume Gas"):
    st.header("Perhitungan Volume Gas pada STP")
    mol = st.number_input("Masukkan jumlah mol gas (mol):", min_value=0.0, format="%.4f")

    if st.button("Hitung Volume Gas"):
        if mol > 0:
            volume = mol_ke_volume_gas(mol)
            st.success(f"Volume gas = {volume:.2f} liter")

            # Penyelesaian dan rumus
            st.markdown("### 🧮 Penyelesaian")
            st.latex(r"Volume = mol \times 22{,}4~L/mol")
            st.latex(f"Volume = {mol} \\times 22.4")
            st.latex(f"Volume = {volume:.2f}~L")
        else:
            st.error("Jumlah mol harus lebih dari nol.")

if option == "Reaktan Pembatas":
    st.header("Perhitungan Reaktan Pembatas")
    mol_A = st.number_input("Mol reaktan A:", min_value=0.0, format="%.4f")
    mol_B = st.number_input("Mol reaktan B:", min_value=0.0, format="%.4f")
    koef_A = st.number_input("Koefisien reaktan A:", min_value=1)
    koef_B = st.number_input("Koefisien reaktan B:", min_value=1)

    if st.button("Tentukan Reaktan Pembatas"):
        rasio_A = mol_A / koef_A
        rasio_B = mol_B / koef_B

        if rasio_A < rasio_B:
            pembatas = "Reaktan A"
        elif rasio_B < rasio_A:
            pembatas = "Reaktan B"
        else:
            pembatas = "Tidak ada, keduanya seimbang"

        st.success(f"Reaktan pembatas: {pembatas}")

        st.markdown("### 🧮 Penyelesaian")
        st.latex(f"\\text{{Rasio A}} = \\frac{{{mol_A}}}{{{koef_A}}} = {rasio_A:.4f}")
        st.latex(f"\\text{{Rasio B}} = \\frac{{{mol_B}}}{{{koef_B}}} = {rasio_B:.4f}")
        
if option == "Perhitungan Yield":
    st.header("Perhitungan Hasil (Yield) Reaksi")
    hasil_nyata = st.number_input("Masukkan hasil nyata (gram):", min_value=0.0, format="%.4f")
    hasil_teori = st.number_input("Masukkan hasil teori (gram):", min_value=0.0, format="%.4f")

    if st.button("Hitung Persen Yield"):
        if hasil_teori > 0:
            persen_yield = (hasil_nyata / hasil_teori) * 100
            st.success(f"Persen Yield = {persen_yield:.2f}%")

            st.markdown("### 🧮 Penyelesaian")
            st.latex(r"yield = \frac{hasil\ nyata}{hasil\ teori} \times 100\%")
            st.latex(f"yield = \\frac{{{hasil_nyata}}}{{{hasil_teori}}} \\times 100\%")
            st.latex(f"yield = {persen_yield:.2f}\\%")
        else:
            st.error("Hasil teori harus lebih dari nol.")

# Konten utama berubah sesuai pilihan di sidebar
if option == "About StoichiMath":
    st.write("**Tentang Aplikasi StoichiMath**")
    st.markdown("""
Stoikiometri adalah cabang kimia yang mempelajari dan menghitung hubungan kuantitatif antara reaktan dan produk dalam reaksi kimia.
Fungsinya adalah untuk menentukan jumlah zat (massa, mol, volume, atau jumlah partikel) yang terlibat dalam suatu reaksi kimia,
serta untuk memprediksi hasil reaksi dan memahami komposisi senyawa. Aplikasi ini dirancang untuk membantu mempermudah perhitungan
sekaligus membahas penyelesaian masalah terkait stoikiometri.
""")
    st.markdown("### 📚 Referensi:")

    col1, col2 = st.columns([0.1, 0.5])
    with col1:
        st.markdown("**Wikipedia:**")
    with col2:
        st.link_button("🌐 Klik disini", "https://id.wikipedia.org/wiki/Stoikiometri")

    col3, col4 = st.columns([0.1, 0.5])
    with col3:
        st.markdown("**Sciencedirect:**")
    with col4:
        st.link_button("🌐 Klik disini", "https://www.sciencedirect.com/topics/physics-and-astronomy/stoichiometry")

    st.markdown("""---
    Dikembangkan dengan Streamlit & Python.
    """)



st.markdown("---")
st.caption("🚀 Dibuat dengan ❤️ oleh Kelompok 11 | StoichiMath")


