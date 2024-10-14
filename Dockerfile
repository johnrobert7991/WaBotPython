# Ganti dengan versi Python yang sesuai
FROM python:3.11  

# RUN which python
RUN git clone https://github.com/johnrobert7991/WaBotPython.git /waBotPython

# Set direktori kerja
WORKDIR /waBotPython

# Instal dependensi dari requirements.txts
RUN pip install --no-cache-dir -r requirements.txt

# Menginformasikan Docker bahwa aplikasi mendengarkan pada port 80
EXPOSE 80

CMD ["python3", "app.py"]
