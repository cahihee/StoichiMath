stoichimath_streamlit/
└── app.py
import streamlit as st

# Header
st.title("🧪 StoichiMath - Kalkulator Stoikiometri")

# Input
reaction = st.text_input("Masukkan persamaan reaksi (misal: 2H2 + O2 -> 2H2O)")
mol_input = st.text_input("Masukkan mol reaktan (misal: H2 = 4)")

# Tombol Hitung
if st.button("Hitung"):
    try:
        if "H2 + O2" in reaction:
            h2_mol = float(mol_input.split('=')[1])
            h2o_mol = h2_mol  # Berdasarkan rasio 2:2
            st.success(f"Mol H2O yang dihasilkan: {h2o_mol} mol")
        else:
            st.warning("Reaksi belum didukung dalam versi ini.")
    except:
        st.error("Format input salah. Gunakan format seperti: H2 = 4")
