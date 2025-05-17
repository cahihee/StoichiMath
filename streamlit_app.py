import streamlit as st
import re
from sympy import symbols, Eq, solve
from collections import defaultdict

st.title("🧪 StoichiMath: Aplikasi Perhitungan Stoikiometri")
st.write("Aplikasi ini membantu menghitung jumlah mol produk dan sisa reaktan berdasarkan persamaan reaksi kimia dan jumlah mol reaktan.")

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
import streamlit as st
import re
from sympy import symbols, Eq, solve
from sympy.parsing.sympy_parser import parse_expr
from collections import defaultdict

st.set_page_config(page_title="StoichiMath", layout="centered")
st.title("🧪 StoichiMath: Aplikasi Perhitungan Stoikiometri")

st.write("Masukkan reaksi kimia yang belum setara (misal: `H2 + O2 -> H2O`) dan jumlah mol salah satu reaktan:")

# Input dari pengguna
reaction_input = st.text_input("Persamaan Reaksi:", "H2 + O2 -> H2O")
mol_input = st.number_input("Masukkan mol dari salah satu reaktan:", min_value=0.0, format="%.2f")
known_species = st.text_input("Sebutkan spesies reaktan yang diketahui jumlah mol-nya:", "H2")

def parse_species(species_str):
    match = re.match(r"(\d*)\s*([A-Za-z0-9()]+)", species_str.strip())
    if match:
        coeff = int(match.group(1)) if match.group(1) else 1
        return coeff, match.group(2)
    return 1, species_str.strip()

def parse_equation(equation):
    lhs, rhs = equation.split("->")
    reactants = lhs.strip().split("+")
    products = rhs.strip().split("+")
    return [parse_species(r) for r in reactants], [parse_species(p) for p in products]

def get_element_count(species):
    element_pattern = r'([A-Z][a-z]*)(\d*)'
    counts = defaultdict(int)
    matches = re.findall(element_pattern, species)
    for elem, count in matches:
        counts[elem] += int(count) if count else 1
    return dict(counts)

def balance_reaction(reactants, products):
    species = [s for _, s in reactants + products]
    elements = set()
    for sp in species:
        elements.update(get_element_count(sp).keys())
    
    coeffs = symbols(f'a:{len(species)}')
    equations = []
    
    for elem in elements:
        lhs = sum(coeffs[i] * get_element_count(species[i]).get(elem, 0) for i in range(len(reactants)))
        rhs = sum(coeffs[i+len(reactants)] * get_element_count(species[i+len(reactants)]).get(elem, 0) for i in range(len(products)))
        equations.append(Eq(lhs, rhs))

    equations.append(Eq(coeffs[0], 1))  # Normalisasi: koefisien reaktan pertama = 1
    solution = solve(equations, coeffs)
    return [float(solution.get(c, 1)) for c in coeffs]

# Proses jika ada input reaksi
if reaction_input:
    try:
        reactants, products = parse_equation(reaction_input)
        all_species = reactants + products
        coeffs = balance_reaction(reactants, products)
        
        st.subheader("✅ Reaksi Setara:")
        species_str = []
        for coef, (_, name) in zip(coeffs, all_species):
            prefix = f"{int(coef)}" if coef != 1 else ""
            species_str.append(f"{prefix}{name}")
        
        st.latex(" + ".join(species_str[:len(reactants)]) + " \\rightarrow " + " + ".join(species_str[len(reactants):]))

        # Hitung stoikiometri
        if known_species:
            known_index = [name for _, name in reactants].index(known_species)
            known_coef = coeffs[known_index]
            st.subheader("📊 Hasil Stoikiometri:")
            for i, (coef, (_, name)) in enumerate(all_species):
                jumlah = (coef / known_coef) * mol_input
                st.write(f"{name}: {jumlah:.2f} mol")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses: {e}")
