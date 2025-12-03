import datetime

class Mahasiswa:
    def __init__(self, nama, umur, jurusan, lahir):
        self.nama = nama
        self.umur = umur
        self.jurusan = jurusan
        self.lahir = lahir

class MahasiswaWEB3(Mahasiswa):
    def __init__(self, nama, umur, jurusan, lahir, proyek_web3):
        super().__init__(nama, umur, jurusan, lahir)
        self.proyek_web3 = proyek_web3

class MahasiswaBlockchain(Mahasiswa):
    def __init__(self, nama, umur, jurusan, lahir, proyek_blockchain):
        super().__init__(nama, umur, jurusan, lahir)
        self.proyek_blockchain = proyek_blockchain

class MahasiswaDeFi(Mahasiswa):
    def __init__(self, nama, umur, jurusan, lahir, proyek_defi):
        super().__init__(nama, umur, jurusan, lahir)
        self.proyek_defi = proyek_defi

class MahasiswaNFT(Mahasiswa):
    def __init__(self, nama, umur, jurusan, lahir, proyek_nft):
        super().__init__(nama, umur, jurusan, lahir)
        self.proyek_nft = proyek_nft

class MahasiswaMetaverse(Mahasiswa):
    def __init__(self, nama, umur, jurusan, lahir, proyek_metaverse):
        super().__init__(nama, umur, jurusan, lahir)
        self.proyek_metaverse = proyek_metaverse

class MahasiswaDAO(Mahasiswa):
    def __init__(self, nama, umur, jurusan, lahir, proyek_dao):
        super().__init__(nama, umur, jurusan, lahir)
        self.proyek_dao = proyek_dao
        self.data_mahasiswa_web3 = []  # Inisialisasi di sini

    def run_menu(self):
        while True:
            print("\nManajemen Mahasiswa WEB3")
            print("=" * 30)
            print("1. Tambah Mahasiswa WEB3")
            print("2. Lihat Data Mahasiswa WEB3")
            print("3. Update Data Mahasiswa WEB3")
            print("4. Hapus Data Mahasiswa WEB3")
            print("5. Keluar")
            pilihan = input("Masukkan pilihan Anda (1-5): ")
            
            if pilihan == '1':
                self.tambah_mahasiswa_web3()
            elif pilihan == '2':
                self.lihat_data_mahasiswa_web3()
            elif pilihan == '3':
                self.update_data_mahasiswa_web3()
            elif pilihan == '4':
                self.hapus_data_mahasiswa_web3()
            elif pilihan == '5':
                print("Keluar dari program.")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

    def tambah_mahasiswa_web3(self):
        while True:
            nama = input("Masukkan nama mahasiswa: ")
            umur = int(input("Masukkan umur mahasiswa: "))
            jurusan = input("Masukkan jurusan mahasiswa: ")
            hari = int(input("Masukkan hari lahir (DD): "))
            bulan = int(input("Masukkan bulan lahir (MM): "))
            tahun = int(input("Masukkan tahun lahir (YYYY): "))
            lahir = datetime.datetime(tahun, bulan, hari)
            proyek_web3 = input("Masukkan proyek WEB3 yang sedang dikerjakan: ")
            
            mahasiswa_web3 = MahasiswaWEB3(nama, umur, jurusan, lahir, proyek_web3)
            self.data_mahasiswa_web3.append(mahasiswa_web3)
            print(f"Mahasiswa WEB3 {mahasiswa_web3.nama} berhasil ditambahkan.")
            
            lagi = input("Apakah Anda ingin menambahkan mahasiswa WEB3 lagi? (y/n): ")
            if lagi.lower() != 'y':
                break

    def lihat_data_mahasiswa_web3(self):
        if not self.data_mahasiswa_web3:
            print("Belum ada data mahasiswa WEB3.")
            return
            
        print("\nData Mahasiswa WEB3:")
        print(f"{'NAMA':<15} {'UMUR':<5} {'JURUSAN':<20} {'LAHIR':<15} {'PROYEK WEB3':<30}")
        print("=" * 90)
        for mahasiswa in self.data_mahasiswa_web3:
            nama = mahasiswa.nama
            umur = mahasiswa.umur
            jurusan = mahasiswa.jurusan
            lahir = mahasiswa.lahir.strftime("%d-%m-%Y")
            proyek_web3 = mahasiswa.proyek_web3
            print(f"{nama:<15} {umur:<5} {jurusan:<20} {lahir:<15} {proyek_web3:<30}")

    def update_data_mahasiswa_web3(self):
        if not self.data_mahasiswa_web3:
            print("Belum ada data mahasiswa WEB3.")
            return
            
        nama_cari = input("Masukkan nama mahasiswa WEB3 yang akan diupdate: ")
        for mahasiswa in self.data_mahasiswa_web3:
            if mahasiswa.nama == nama_cari:
                print("Data ditemukan. Masukkan data baru:")
                mahasiswa.nama = input("Masukkan nama mahasiswa: ")
                mahasiswa.umur = int(input("Masukkan umur mahasiswa: "))
                mahasiswa.jurusan = input("Masukkan jurusan mahasiswa: ")
                hari = int(input("Masukkan hari lahir (DD): "))
                bulan = int(input("Masukkan bulan lahir (MM): "))
                tahun = int(input("Masukkan tahun lahir (YYYY): "))
                mahasiswa.lahir = datetime.datetime(tahun, bulan, hari)
                mahasiswa.proyek_web3 = input("Masukkan proyek WEB3 yang sedang dikerjakan: ")
                print(f"Data mahasiswa WEB3 {mahasiswa.nama} berhasil diupdate.")
                return
        print("Mahasiswa WEB3 tidak ditemukan.")

    def hapus_data_mahasiswa_web3(self):
        if not self.data_mahasiswa_web3:
            print("Belum ada data mahasiswa WEB3.")
            return
            
        nama_cari = input("Masukkan nama mahasiswa WEB3 yang akan dihapus: ")
        for i, mahasiswa in enumerate(self.data_mahasiswa_web3):
            if mahasiswa.nama == nama_cari:
                del self.data_mahasiswa_web3[i]
                print(f"Data mahasiswa WEB3 {nama_cari} berhasil dihapus.")
                return
        print("Mahasiswa WEB3 tidak ditemukan.")

if __name__ == "__main__":
    manajemen = MahasiswaDAO("", 0, "", datetime.datetime.now(), "")
    manajemen.run_menu()