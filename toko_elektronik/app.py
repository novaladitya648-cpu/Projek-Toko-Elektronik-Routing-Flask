from flask import Flask, render_template, abort, redirect, url_for

app = Flask(__name__)

# Data produk (key = id produk)
PRODUK = {
    1: {"nama": "Nova A12", "kategori": "HP", "harga": 1899000,
        "deskripsi": "HP entry level, layar 6,5 inci, baterai 5000 mAh."},
    2: {"nama": "Nova X5 Pro", "kategori": "HP", "harga": 4599000,
        "deskripsi": "HP kelas menengah, RAM 8 GB, kamera 50 MP."},
    3: {"nama": "Luma S9", "kategori": "HP", "harga": 7999000,
        "deskripsi": "HP flagship, layar AMOLED, penyimpanan 256 GB."},
    4: {"nama": "Kiro Book 14", "kategori": "Laptop", "harga": 6299000,
        "deskripsi": "Laptop ringan untuk kuliah, RAM 8 GB, SSD 256 GB."},
    5: {"nama": "Kiro Book Pro 15", "kategori": "Laptop", "harga": 9499000,
        "deskripsi": "Laptop 15 inci, RAM 16 GB, SSD 512 GB."},
    6: {"nama": "Arka G15", "kategori": "Laptop", "harga": 12999000,
        "deskripsi": "Laptop gaming, RAM 16 GB, kartu grafis terpisah."},
}

# Username yang sudah terdaftar
TERDAFTAR = ["andi", "budi", "citra", "dewi"]

# Informasi pengguna (sesuai username di atas)
DATA_USER = {
    "andi": {"nama": "Andi Pratama", "email": "andi@email.com", "status": "Member"},
    "budi": {"nama": "Budi Santoso", "email": "budi@email.com", "status": "Member"},
    "citra": {"nama": "Citra Lestari", "email": "citra@email.com", "status": "Pelanggan"},
    "dewi": {"nama": "Dewi Anggraini", "email": "dewi@email.com", "status": "Admin Toko"},
}


# ---------- Route statis ----------
@app.route("/")
def beranda():
    return render_template("beranda.html")


@app.route("/tentang")
def tentang():
    return render_template("tentang.html")


@app.route("/produk")
def produk():
    return render_template("produk.html", daftar=PRODUK)


@app.route("/kontak")
def kontak():
    return render_template("kontak.html")


# ---------- Redirect ----------
@app.route("/home")
def home_lama():
    # URL lama dialihkan ke beranda
    return redirect(url_for("beranda"))


# ---------- Dynamic route ----------
@app.route("/cek/<username>")
def cek_username(username):
    username = username.lower()

    # Validasi: minimal 4 karakter
    if len(username) < 4:
        pesan = "Username minimal 4 karakter."
        return render_template("cek.html", username=username, pesan=pesan, status="error"), 400

    if username in TERDAFTAR:
        pesan = "Username sudah dipakai."
        status = "dipakai"
    else:
        pesan = "Username masih tersedia."
        status = "tersedia"

    return render_template("cek.html", username=username, pesan=pesan, status=status)


@app.route("/user/<username>")
def user(username):
    username = username.lower()

    # Validasi: minimal 4 karakter
    if len(username) < 4:
        pesan = "Username minimal 4 karakter."
        return render_template("user.html", username=username, data=None, pesan=pesan), 400

    # Validasi: username harus terdaftar
    if username not in DATA_USER:
        abort(404)

    return render_template("user.html", username=username, data=DATA_USER[username])


# ---------- Dynamic route dengan converter int ----------
@app.route("/produk/<int:id>")
def detail_produk(id):
    p = PRODUK.get(id)
    if p is None:
        abort(404)
    return render_template("detail_produk.html", id=id, p=p)


# ---------- Custom error 404 ----------
@app.errorhandler(404)
def halaman_tidak_ditemukan(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
