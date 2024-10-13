FROM python:3.11  # Ganti dengan versi Python yang sesuai

RUN git clone https://github.com/johnrobert7991/WaBotPython.git /

# Set direktori kerja
WORKDIR /

# Instal dependensi dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Tentukan perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]  # Ganti app.py dengan nama file aplikasi utama
