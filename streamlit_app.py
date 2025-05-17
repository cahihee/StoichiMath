import streamlit as st
from chempy import balance_stoichiometry
from pint import UnitRegistry
import matplotlib.pyplot as plt

ureg = UnitRegistry()

st.set_page_config(page_title="StoichiMath", layout="centered")

st.title("⚗️ StoichiMath")
st.subheader("Alat bantu stoikiometri reaksi kimia")

# Input reaksi
reaction_input = st.text_input("Masukkan reaksi kimia (contoh: H2 + O2 -> H2O):")

if reaction_input:
    try:
        reac_str, prod_str = reaction_input.split("->")
        reac = {r.strip() for r in reac_str.split('+')}
        prod = {p.strip() for p in prod_str.split('+')}
        reac_bal, prod_bal = balance_stoichiometry(reac, prod)
        
        st.success("✅ Reaksi Tersetarakan:")
        st.write(" + ".join(f"{v} {k}" for k, v in reac_bal.items()), "→", 
                 " + ".join(f"{v} {k}" for k, v in prod_bal.items()))

        # Pilih zat diketahui
        st.markdown("---")
        st.subheader("🔢 Hitung Stoikiometri")
        all_species = list(reac_bal.keys()) + list(prod_bal.keys())
        selected_species = st.selectbox("Pilih zat yang diketahui jumlahnya:", all_species)
        known_value = st.number_input(f"Masukkan jumlah {selected_species}:", min_value=0.0)

        unit = st.selectbox("Satuan:", ["mol", "gram", "partikel", "liter (gas)"])

        # Molar massa dummy (kamu bisa ganti dengan yang lebih akurat)
        molar_masses = {
            "H2": 2.02, "O2": 32.00, "H2O": 18.02, "CO2": 44.01, "CH4": 16.04,
            "NaCl": 58.44, "C6H12O6": 180.16
        }

        if st.button("Hitung"):
            try:
                known_mol = None

                if unit == "mol":
                    known_mol = known_value
                elif unit == "gram":
                    known_mol = known_value / molar_masses[selected_species]
                elif unit == "partikel":
                    known_mol = known_value / (6.022e23)
                elif unit == "liter (gas)":
                    known_mol = known_value / 22.4

                hasil_mol = {}
                for species in all_species:
                    ratio = (prod_bal if species in prod_bal else reac_bal)[species] / \
                            (prod_bal if selected_species in prod_bal else reac_bal)[selected_species]
                    mol_target = known_mol * ratio
                    hasil_mol[species] = mol_target

                st.markdown("### 📊 Hasil Perhitungan")
                for species, mol in hasil_mol.items():
                    massa = mol * molar_masses.get(species, 0)
                    partikel = mol * 6.022e23
                    volume = mol * 22.4  # gas STP
                    st.markdown(f"**{species}**:")
                    st.markdown(f"- Mol: `{mol:.4f}` mol")
                    st.markdown(f"- Massa: `{massa:.2f}` gram")
                    st.markdown(f"- Partikel: `{partikel:.2e}`")
                    st.markdown(f"- Volume (gas): `{volume:.2f}` L")

                # Visualisasi
                st.markdown("### 📈 Diagram Perbandingan Mol")
                fig, ax = plt.subplots()
                ax.bar(hasil_mol.keys(), hasil_mol.values(), color='skyblue')
                ax.set_ylabel("Mol")
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Terjadi kesalahan perhitungan: {e}")

    except Exception as e:
        st.error(f"❌ Gagal menyetarakan reaksi: {e}")

st.markdown("---")
st.caption("🚀 Dibuat dengan ❤️ oleh StoichiMath")


