# VulnLab Academy

Platform lab cybersecurity yang sengaja dibuat rentan, terinspirasi alur
PortSwigger Web Security Academy: **pilih kategori → pilih level → baca
tutorial lengkap → klik "Akses Lab" → serang labnya**.

⚠️ **Hanya untuk lab pribadi/training.** Jangan deploy ke internet publik —
aplikasi ini SENGAJA berisi kerentanan sungguhan (SQL injection, XSS, command
injection ke shell asli, path traversal ke filesystem asli).

## Instalasi

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 database.py           # inisialisasi database (opsional, otomatis saat run)
python3 app.py
```

Buka `http://<ip-server>:5000` dari mesin Kali Linux kamu, atau
`http://127.0.0.1:5000` kalau dijalankan lokal. Jalankan dengan `host="0.0.0.0"`
(sudah default di `app.py`) supaya bisa diakses dari mesin Kali terpisah
dalam jaringan lab yang sama.

## Status kategori

16 kategori serangan tersedia di menu, mengikuti struktur PortSwigger.
**4 kategori sudah punya lab yang benar-benar bisa diserang** (12 lab total,
3 level tiap kategori):

| Kategori | Apprentice | Practitioner | Expert |
|---|---|---|---|
| SQL injection | Auth bypass (UNION) | Blind boolean-based | Blind time-based |
| XSS | Reflected | Stored (filter bypass) | DOM-based (location.hash) |
| OS command injection | Langsung via `;` | Blind (delay) | Filter bypass (`\|`, `$IFS`) |
| Path traversal | Tanpa filter | Filter non-recursive | Bypass ekstensi + encoding |

12 kategori sisanya (CSRF, Clickjacking, DOM-based lain, CORS, XXE, SSRF,
HTTP request smuggling, SSTI, Access control, Authentication, Insecure
deserialization, File upload) sudah punya **struktur katalog + slot tutorial**
di `data/catalog.py`, tinggal ditambahkan tutorial teks dan lab Flask
sungguhan mengikuti pola 4 kategori di atas.

## Struktur proyek

```
app.py                  # routing utama: index, /category/<slug>, /category/<slug>/<level>
database.py              # skema SQLite + seed data
data/catalog.py          # 16 kategori x 3 level: judul, tujuan, tutorial lengkap
labs/                    # blueprint Flask berisi lab vulnerable sungguhan
  sql_injection.py
  xss.py
  command_injection.py
  path_traversal.py
templates/               # tampilan (base, index, category, tutorial) + templates/labs/*
static/css/style.css     # desain
lab_files/                # file contoh untuk lab path traversal
```

## Menambah lab baru

1. Tambahkan tutorial di `data/catalog.py` pada `LABS["slug-kategori"]["level"]`.
2. Set `"implemented": True` pada kategori di `CATEGORIES`.
3. Buat `labs/nama_kategori.py` berisi Blueprint dengan 3 route (satu per level),
   sengaja tulis kode yang vulnerable (tanpa parameterized query / tanpa
   escaping / tanpa validasi input, sesuai jenis kerentanannya).
4. Buat template di `templates/labs/nama_kategori_<level>.html`.
5. Daftarkan blueprint di `app.py` (`app.register_blueprint(...)`) dan tambah
   entri di `LAB_ROUTE_MAP`.

## Menyerang dengan tools Kali Linux

Setiap halaman tutorial mencantumkan endpoint persis dan contoh perintah
`sqlmap`/`curl`. Untuk Burp Suite: arahkan proxy browser ke Burp, jelajahi
lab lewat browser, lalu gunakan Proxy History / Repeater / Intruder seperti
biasa — tidak ada proteksi CSRF/anti-automation yang menghalangi.

Contoh cepat:
```bash
# SQL injection apprentice - dump user via sqlmap
sqlmap -u "http://TARGET:5000/lab/sql-injection/apprentice/login" \
  --data="username=admin&password=admin" -p username --batch --dump

# Command injection apprentice
curl "http://TARGET:5000/lab/command-injection/apprentice/ping?host=127.0.0.1;whoami"

# Path traversal apprentice
curl "http://TARGET:5000/lab/path-traversal/apprentice/image?filename=../../../../etc/passwd"
```
