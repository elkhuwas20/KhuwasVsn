import datetime

mahasiswa1 = {
    "nama": "Andi",
    "umur": 21,
    "jurusan": "Informatika",
    "Lahir": datetime.datetime(2002, 5, 17)
}
mahasiswa2 = {
    "nama": "Budi",
    "umur": 22,
    "jurusan": "Sistem Informasi",
    "Lahir": datetime.datetime(2001, 8, 24)
}
mahasiswa3 = {
    "nama": "Citra",
    "umur": 20,
    "jurusan": "Teknik Komputer",
    "Lahir": datetime.datetime(2003, 3, 12)
}
data_mahasiswa = {
    "mhs1": mahasiswa1,
    "mhs2": mahasiswa2,
    "mhs3": mahasiswa3
}
# print(data_mahasiswa)
print("Data Mahasiswa:")
print(f"{'KEY':<6} {'NAMA':<10} {'UMUR':<5} {'JURUSAN':<20} {'LAHIR':<15}")
print("=" * 60)
for mahasiswa in data_mahasiswa:
    KEY = mahasiswa
    NAMA = data_mahasiswa[mahasiswa]["nama"]
    UMUR = data_mahasiswa[mahasiswa]["umur"]
    JURUSAN = data_mahasiswa[mahasiswa]["jurusan"]
    LAHIR = data_mahasiswa[mahasiswa]["Lahir"].strftime("%d-%m-%Y")
    print(f"{KEY:<6} {NAMA:<10} {UMUR:<5} {JURUSAN:<20} {LAHIR:<15}")
