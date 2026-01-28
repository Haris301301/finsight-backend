# Menggunakan image Python resmi yang ringan
FROM python:3.10-slim

# Menentukan direktori kerja di dalam server
WORKDIR /app

# Menyalin daftar library dan menginstalnya
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tambahkan Gunicorn secara manual jika belum ada di requirements.txt
RUN pip install gunicorn

# Menyalin seluruh kode backend kamu
COPY . .

# Membuat folder uploads dan memberi izin akses (untuk simpan struk sementara)
RUN mkdir -p uploads && chmod 777 uploads

# Hugging Face Spaces mewajibkan aplikasi berjalan di port 7860
EXPOSE 7860

# Menjalankan Flask menggunakan Gunicorn di port 7860
# 'app:app' berarti file app.py dengan variabel app di dalamnya
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]