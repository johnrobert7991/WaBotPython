# Ganti dengan versi Python yang sesuai
FROM python:3.9 

# Set direktori kerja
WORKDIR /app

# Salin requirements.txt ke dalam image
COPY requirements.txt .

# Instal dependensi dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin sisa kode aplikasi ke dalam image
COPY . .

# Tentukan perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]  # Ganti app.py dengan nama file aplikasi utama
