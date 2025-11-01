import datetime
import os
mahasiswa1 = {
    "nama": "Andi",
    "umur": 21,
    "jurusan": "Informatika",
    "Lahir": datetime.datetime(1111, 1, 1)
} 
data_mahasiswa = {}
os.system ("cls")
print(f"{"Data Mahasiswa Sebelum Ditambahkan:":^30}")
print(f"{"Selamat Datang Admin":^30}")
print("=" * 30)
mahasiswa = dict.fromkeys(mahasiswa1.keys())
print(mahasiswa)
mahasiswa ["nama"] = (input("Masukkan nama anda: "))
mahasiswa ["umur"] = int(input("Masukkan umur anda: "))
mahasiswa ["jurusan"] = input("Masukkan jurusan anda: ")
hari_tanggal_lahir = int(input("Masukkan  tanggal lahir anda: "))
bulan_lahir = int(input("Masukkan bulan lahir anda: "))
tahun_lahir = int(input("Masukkan tahun lahir anda: "))
mahasiswa ["Lahir"] = datetime.datetime(tahun_lahir, bulan_lahir, hari_tanggal_lahir)
data_mahasiswa ["mhs1"] = mahasiswa
os.system ("cls")
print(f"{"Data Mahasiswa Setelah Ditambahkan:":^30}")
print("=" * 30)

print(mahasiswa)
