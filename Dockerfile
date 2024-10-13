# Ganti dengan versi Python yang sesuai
FROM python:3.11  

CMD ["sh", "-c", "which python"]

# CMD which python
# RUN git clone https://github.com/johnrobert7991/WaBotPython.git /waBotPython

# # Set direktori kerja
# WORKDIR /waBotPython

# # Instal dependensi dari requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# CMD ["which" "python"]
# # Tentukan perintah untuk menjalankan aplikasi
# CMD ["python", "app.py"]  # Ganti app.py dengan nama file aplikasi utama
