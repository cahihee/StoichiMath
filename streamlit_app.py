stoichimath/
│
├── index.html          → Halaman utama (frontend)
├── style.css           → (opsional) Tampilan
├── app.py              → Backend Flask (Python)
└── requirements.txt    → Daftar dependensi Python

<!DOCTYPE html>
<html>
<head>
    <title>StoichiMath</title>
</head>
<body>
    <h1>StoichiMath - Kalkulator Stoikiometri</h1>
    <form action="/calculate" method="post">
        <label>Persamaan reaksi (misal: 2H2 + O2 -> 2H2O):</label><br>
        <input type="text" name="reaction" required><br><br>
        <label>Mol reaktan utama (misal: H2 = 4):</label><br>
        <input type="text" name="mol_input" required><br><br>
        <input type="submit" value="Hitung">
    </form>
</body>
</html>
