# Ganti dengan versi Python yang sesuai
FROM python:3.11  

# RUN which python
RUN git clone https://github.com/johnrobert7991/WaBotPython.git /waBotPython

# Set direktori kerja
WORKDIR /waBotPython

# Instal dependensi dari requirements.txts
RUN pip install --no-cache-dir -r requirements.txt

# Menginformasikan Docker bahwa aplikasi mendengarkan pada port 80
EXPOSE 3000

# CMD ["ls"]
CMD ["gunicorn", "--bind" , ":3000", "--workers", "2", "app:main"]
# CMD ["python3", "app.py"]
