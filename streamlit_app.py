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


elif option == "Perhitungan jumlah partikel dari mol":
    st.header("Perhitungan jumlah partikel dari mol")
    mol = st.number_input("Masukkan jumlah mol zat (mol):", min_value=0.0, format="%.4f")
    if st.button("Hitung Jumlah Partikel"):
        partikel = mol_ke_partikel(mol)
        st.success(f"Jumlah partikel = {partikel:.4e} partikel")


elif option == "Perhitungan perbandingan mol":
    st.header("Perhitungan perbandingan mol")
    mol_1 = st.number_input("Masukkan jumlah mol zat 1 (mol):", min_value=0.0, format="%.4f")
    koefisien_1 = st.number_input("Masukkan koefisien reaksi zat 1:", min_value=0.1, format="%.2f")
    koefisien_2 = st.number_input("Masukkan koefisien reaksi zat 2:", min_value=0.1, format="%.2f")
    if st.button("Hitung Mol Zat 2"):
        mol_2 = perbandingan_mol(mol_1, koefisien_1, koefisien_2)
        st.success(f"Jumlah mol zat 2 = {mol_2:.4f} mol")

# Fungsi untuk parsing persamaan reaksi
def parse_reaction(equation):
    reactants_part, products_part = equation.split("→")
    reactants = reactants_part.strip().split("+")
    products = products_part.strip().split("+")
    
    def parse_species(species_list):
        result = []
        for item in species_list:
            item = item.strip()
            match = re.match(r"(\d*)\s*([A-Za-z0-9()]+)", item)
            if match:
                coef = int(match.group(1)) if match.group(1) else 1
                chem = match.group(2)
                result.append((chem, coef))
        return result
    
    return parse_species(reactants), parse_species(products)

# Input dari pengguna
equation = st.text_input("Masukkan persamaan reaksi (misal: 2H2 + O2 → 2H2O)", "2H2 + O2 → 2H2O")

reactant_input = st.text_area("Masukkan jumlah mol reaktan (format: H2=4, O2=1)", "H2=4, O2=1")

if st.button("Hitung"):
    try:
        reactants, products = parse_reaction(equation)
        st.subheader("📘 Persamaan yang Diproses:")
        st.write("Reaktan:", reactants)
        st.write("Produk:", products)

        # Konversi input mol reaktan menjadi dict
        mol_reaktan = {}
        for item in reactant_input.split(","):
            chem, val = item.strip().split("=")
            mol_reaktan[chem.strip()] = float(val)

        # Hitung mol yang dapat bereaksi berdasarkan stoikiometri
        limiting_ratios = []
        for chem, coef in reactants:
            if chem in mol_reaktan:
                ratio = mol_reaktan[chem] / coef
                limiting_ratios.append(ratio)
            else:
                limiting_ratios.append(0)  # Jika tidak ada, diasumsikan 0 mol

        limiting_mol = min(limiting_ratios)

        st.subheader("⚗️ Hasil Perhitungan:")
        st.write(f"Reaksi terjadi sebanyak **{limiting_mol:.2f} kali** berdasarkan reaktan pembatas.")

        # Hitung sisa reaktan
        st.markdown("### 🔍 Sisa Reaktan:")
        for chem, coef in reactants:
            awal = mol_reaktan.get(chem, 0)
            sisa = awal - coef * limiting_mol
            st.write(f"{chem}: {sisa:.2f} mol")

        # Hitung mol produk
        st.markdown("### 🧪 Mol Produk yang Dihasilkan:")
        for chem, coef in products:
            hasil = coef * limiting_mol
            st.write(f"{chem}: {hasil:.2f} mol")
    except Exception as e:
        st.error(f"Terjadi kesalahan dalam pemrosesan: {e}")

st.markdown("---")
st.caption("🚀 Dibuat dengan ❤️ oleh StoichiMath")


