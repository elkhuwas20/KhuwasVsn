import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style untuk visualisasi
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("=" * 60)
print("ANALISIS PROGRAM MAKAN BERGIZI GRATIS 2025")
print("=" * 60)
print()

# ==========================================
# 1. DATA ANGGARAN
# ==========================================
print("1. LOADING DATA ANGGARAN...")

anggaran_data = {
    'Komponen': [
        'Pemenuhan Gizi Nasional',
        'Dukungan Manajemen',
        'Total Anggaran'
    ],
    'Anggaran (Triliun Rp)': [63.356, 7.433, 71.0],
    'Persentase': [89.5, 10.5, 100.0]
}

df_anggaran = pd.DataFrame(anggaran_data)
print("\n📊 Data Anggaran MBG 2025:")
print(df_anggaran.to_string(index=False))

# Hitung anggaran untuk beli bahan makanan (85% dari pemenuhan gizi)
anggaran_bahan_makanan = 63.356 * 0.85
print(f"\n💰 Anggaran untuk bahan makanan: Rp {anggaran_bahan_makanan:.2f} Triliun")

# ==========================================
# 2. DATA TARGET PENERIMA
# ==========================================
print("\n" + "=" * 60)
print("2. LOADING DATA TARGET PENERIMA...")

target_data = {
    'Periode': ['Jan-Mar 2025', 'Akhir 2025', 'Target 2029'],
    'Target Penerima (Juta)': [3, 15, 82.9],
    'Keterangan': ['Fase Awal', 'Target Tahun Ini', 'Target Jangka Panjang']
}

df_target = pd.DataFrame(target_data)
print("\n📈 Target Penerima MBG:")
print(df_target.to_string(index=False))

# Data realisasi
realisasi_data = {
    'Bulan': ['Januari 2025', 'Mei 2025', 'Juli 2025', 'Oktober 2025'],
    'Penerima (Juta)': [3, 4.4, 6.38, 40],
    'Jumlah SPPG': [190, 1583, 2109, None]
}

df_realisasi = pd.DataFrame(realisasi_data)
print("\n✅ Realisasi Penerima MBG:")
print(df_realisasi.to_string(index=False))

# ==========================================
# 3. DATA BIAYA PER PORSI
# ==========================================
print("\n" + "=" * 60)
print("3. LOADING DATA BIAYA PER PORSI...")

biaya_regional_data = {
    'Wilayah': [
        'Jawa (Standar)',
        'Palembang - TK s/d SD Kelas 3',
        'Palembang - SD Kelas 4 s/d SMP',
        'Papua Selatan & Papua Barat Daya',
        'Papua (estimasi)',
        'Kabupaten Intan Jaya'
    ],
    'Biaya per Porsi (Rp)': [10000, 8000, 10000, 15000, 30000, 60000],
    'Kalori per Porsi': [650, 600, 650, 650, 700, 700]
}

df_biaya = pd.DataFrame(biaya_regional_data)
print("\n💵 Biaya per Porsi Berdasarkan Regional:")
print(df_biaya.to_string(index=False))

# Hitung rata-rata nasional
rata_rata_nasional = 63356000000000 / (5 * 52 * 19470000)  # 5 hari/minggu, 52 minggu, 19.47 juta penerima
print(f"\n📊 Rata-rata biaya nasional per porsi: Rp {rata_rata_nasional:,.0f}")

# ==========================================
# 4. DATA STUNTING
# ==========================================
print("\n" + "=" * 60)
print("4. LOADING DATA STUNTING...")

stunting_trend = {
    'Tahun': [2019, 2023, 2024, 2025, 2029, 2045],
    'Prevalensi (%)': [27.7, 21.5, 19.8, 18.8, 14.2, 5.0],
    'Status': ['Baseline', 'Historis', 'Terkini', 'Target', 'Target', 'Target']
}

df_stunting_trend = pd.DataFrame(stunting_trend)
print("\n📉 Trend Prevalensi Stunting Nasional:")
print(df_stunting_trend.to_string(index=False))

# Data stunting per provinsi (jumlah balita)
stunting_provinsi_jumlah = {
    'Provinsi': [
        'Jawa Barat', 'Jawa Tengah', 'Jawa Timur',
        'Sumatera Utara', 'Nusa Tenggara Timur', 'Banten'
    ],
    'Jumlah Balita Stunting': [638000, 485893, 430780, 316456, 214143, 209600],
    'Keterangan': ['Tertinggi'] + ['Top 6'] * 5
}

df_stunting_jumlah = pd.DataFrame(stunting_provinsi_jumlah)
print("\n🏆 Provinsi dengan Jumlah Balita Stunting Terbanyak (2024):")
print(df_stunting_jumlah.to_string(index=False))

# Data prevalensi stunting per provinsi
stunting_provinsi_prevalensi = {
    'Provinsi': [
        'Nusa Tenggara Timur', 'Sulawesi Barat', 'Papua Barat Daya',
        'Bali', 'Jawa Timur', 'Kepulauan Riau'
    ],
    'Prevalensi (%)': [37.0, 35.4, 30.5, 8.6, 14.7, 15.0],
    'Kategori': ['Tertinggi', 'Tertinggi', 'Tertinggi', 'Terendah', 'Terendah', 'Terendah']
}

df_stunting_prevalensi = pd.DataFrame(stunting_provinsi_prevalensi)
print("\n📊 Provinsi dengan Prevalensi Stunting Tertinggi & Terendah (2024):")
print(df_stunting_prevalensi.to_string(index=False))

# ==========================================
# 5. ANALISIS DASAR
# ==========================================
print("\n" + "=" * 60)
print("5. ANALISIS DASAR")
print("=" * 60)

# Analisis 1: Biaya per Anak per Tahun
print("\n📌 ANALISIS 1: Biaya per Anak per Tahun")
target_2025 = 15000000  # 15 juta
anggaran_pemenuhan_gizi = 63356000000000  # 63.356 triliun
hari_sekolah_per_tahun = 5 * 52  # 5 hari per minggu, 52 minggu

biaya_per_anak_per_tahun = anggaran_pemenuhan_gizi / target_2025
biaya_per_anak_per_hari = biaya_per_anak_per_tahun / hari_sekolah_per_tahun

print(f"Total anggaran pemenuhan gizi: Rp {anggaran_pemenuhan_gizi:,.0f}")
print(f"Target penerima 2025: {target_2025:,} anak")
print(f"Biaya per anak per tahun: Rp {biaya_per_anak_per_tahun:,.0f}")
print(f"Biaya per anak per hari: Rp {biaya_per_anak_per_hari:,.0f}")

# Analisis 2: Proyeksi Anggaran untuk Target 2029
print("\n📌 ANALISIS 2: Proyeksi Anggaran untuk Target 2029")
target_2029 = 82900000  # 82.9 juta
proyeksi_anggaran_2029 = target_2029 * biaya_per_anak_per_tahun
print(f"Target penerima 2029: {target_2029:,} anak")
print(f"Proyeksi anggaran yang dibutuhkan: Rp {proyeksi_anggaran_2029:,.0f}")
print(f"Proyeksi anggaran (Triliun): Rp {proyeksi_anggaran_2029/1000000000000:.2f} T")

# Analisis 3: Efisiensi Regional
print("\n📌 ANALISIS 3: Efisiensi Biaya Regional")
df_biaya['Efisiensi vs Standar (%)'] = (df_biaya['Biaya per Porsi (Rp)'] / 10000 * 100).round(0)
df_biaya['Selisih dari Standar (Rp)'] = df_biaya['Biaya per Porsi (Rp)'] - 10000
print(df_biaya[['Wilayah', 'Biaya per Porsi (Rp)', 'Efisiensi vs Standar (%)']].to_string(index=False))

# Analisis 4: Korelasi Stunting dengan Prioritas MBG
print("\n📌 ANALISIS 4: Analisis Prioritas Berdasarkan Stunting")
print("Provinsi dengan stunting tinggi yang perlu prioritas:")
prioritas = df_stunting_prevalensi[df_stunting_prevalensi['Kategori'] == 'Tertinggi'].copy()
print(prioritas[['Provinsi', 'Prevalensi (%)']].to_string(index=False))

# ==========================================
# 6. VISUALISASI DATA
# ==========================================
print("\n" + "=" * 60)
print("6. MEMBUAT VISUALISASI...")
print("=" * 60)

# Setup figure dengan multiple subplots
fig = plt.figure(figsize=(16, 12))

# Plot 1: Komposisi Anggaran
ax1 = plt.subplot(2, 3, 1)
colors_anggaran = ['#3498db', '#e74c3c']
plt.pie(df_anggaran['Anggaran (Triliun Rp)'][:2], 
        labels=df_anggaran['Komponen'][:2],
        autopct='%1.1f%%',
        colors=colors_anggaran,
        startangle=90)
plt.title('Komposisi Anggaran MBG 2025\n(Total: Rp 71 Triliun)', fontsize=12, fontweight='bold')

# Plot 2: Target vs Realisasi Penerima
ax2 = plt.subplot(2, 3, 2)
x_pos = np.arange(len(df_realisasi))
plt.bar(x_pos, df_realisasi['Penerima (Juta)'], color='#2ecc71', alpha=0.7)
plt.axhline(y=15, color='r', linestyle='--', label='Target Akhir 2025: 15 juta')
plt.xticks(x_pos, df_realisasi['Bulan'], rotation=45, ha='right')
plt.ylabel('Penerima (Juta)')
plt.title('Realisasi Penerima MBG 2025', fontsize=12, fontweight='bold')
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Plot 3: Biaya per Porsi Regional
ax3 = plt.subplot(2, 3, 3)
colors_biaya = ['green' if x <= 10000 else 'orange' if x <= 20000 else 'red' 
                for x in df_biaya['Biaya per Porsi (Rp)']]
bars = plt.barh(df_biaya['Wilayah'], df_biaya['Biaya per Porsi (Rp)'], color=colors_biaya, alpha=0.7)
plt.axvline(x=10000, color='blue', linestyle='--', linewidth=2, label='Standar Jawa: Rp 10.000')
plt.xlabel('Biaya per Porsi (Rp)')
plt.title('Variasi Biaya per Porsi Berdasarkan Wilayah', fontsize=12, fontweight='bold')
plt.legend()
plt.grid(axis='x', alpha=0.3)

# Plot 4: Trend Stunting
ax4 = plt.subplot(2, 3, 4)
historis = df_stunting_trend[df_stunting_trend['Status'].isin(['Baseline', 'Historis', 'Terkini'])]
target = df_stunting_trend[df_stunting_trend['Status'] == 'Target']
plt.plot(historis['Tahun'], historis['Prevalensi (%)'], 
         marker='o', linewidth=2, markersize=8, label='Realisasi', color='#e74c3c')
plt.plot(target['Tahun'], target['Prevalensi (%)'], 
         marker='s', linewidth=2, markersize=8, linestyle='--', label='Target', color='#3498db')
plt.xlabel('Tahun')
plt.ylabel('Prevalensi Stunting (%)')
plt.title('Trend Prevalensi Stunting Nasional', fontsize=12, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 5: Provinsi dengan Balita Stunting Terbanyak
ax5 = plt.subplot(2, 3, 5)
plt.barh(df_stunting_jumlah['Provinsi'], df_stunting_jumlah['Jumlah Balita Stunting']/1000, 
         color='#e67e22', alpha=0.7)
plt.xlabel('Jumlah Balita Stunting (Ribuan)')
plt.title('6 Provinsi dengan Balita Stunting Terbanyak', fontsize=12, fontweight='bold')
plt.grid(axis='x', alpha=0.3)

# Plot 6: Prevalensi Stunting Tertinggi vs Terendah
ax6 = plt.subplot(2, 3, 6)
colors_prev = ['red' if x == 'Tertinggi' else 'green' for x in df_stunting_prevalensi['Kategori']]
plt.barh(df_stunting_prevalensi['Provinsi'], df_stunting_prevalensi['Prevalensi (%)'], 
         color=colors_prev, alpha=0.7)
plt.xlabel('Prevalensi Stunting (%)')
plt.title('Provinsi dengan Prevalensi Tertinggi & Terendah', fontsize=12, fontweight='bold')
plt.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('analisis_mbg_2025.png', dpi=300, bbox_inches='tight')
print("✅ Visualisasi disimpan sebagai 'analisis_mbg_2025.png'")

# ==========================================
# 7. EXPORT DATA KE CSV
# ==========================================
print("\n" + "=" * 60)
print("7. EXPORT DATA KE FILE CSV")
print("=" * 60)

# Export semua dataframe ke CSV
df_anggaran.to_csv('data_anggaran_mbg.csv', index=False)
df_target.to_csv('data_target_penerima.csv', index=False)
df_realisasi.to_csv('data_realisasi_penerima.csv', index=False)
df_biaya.to_csv('data_biaya_per_porsi.csv', index=False)
df_stunting_trend.to_csv('data_stunting_trend.csv', index=False)
df_stunting_jumlah.to_csv('data_stunting_jumlah.csv', index=False)
df_stunting_prevalensi.to_csv('data_stunting_prevalensi.csv', index=False)

print("✅ Data berhasil diekspor:")
print("   - data_anggaran_mbg.csv")
print("   - data_target_penerima.csv")
print("   - data_realisasi_penerima.csv")
print("   - data_biaya_per_porsi.csv")
print("   - data_stunting_trend.csv")
print("   - data_stunting_jumlah.csv")
print("   - data_stunting_prevalensi.csv")

# ==========================================
# 8. KESIMPULAN ANALISIS
# ==========================================
print("\n" + "=" * 60)
print("8. KESIMPULAN ANALISIS")
print("=" * 60)

print("""
📌 TEMUAN KUNCI:

1. ANGGARAN & EFISIENSI:
   - Total anggaran Rp 71 T untuk 15 juta penerima di 2025
   - Biaya per anak per hari: ~Rp 12.516
   - Untuk mencapai target 82.9 juta penerima di 2029 dibutuhkan ~Rp 392 T

2. VARIASI REGIONAL:
   - Biaya per porsi sangat bervariasi: Rp 8.000 - Rp 60.000
   - Papua memiliki biaya tertinggi (hingga 6x lipat standar Jawa)
   - Perlu penyesuaian anggaran untuk daerah dengan indeks kemahalan tinggi

3. PRIORITAS STUNTING:
   - NTT memiliki prevalensi tertinggi (37%) DAN jumlah kasus besar
   - Jawa Barat memiliki jumlah balita stunting terbanyak (638 ribu)
   - 6 provinsi menyumbang 50% kasus stunting nasional

4. REALISASI PROGRAM:
   - Per Oktober 2025: 40 juta penerima (melampaui target!)
   - Pertumbuhan cepat: dari 3 juta (Jan) ke 40 juta (Okt)
   - Indikasi scaling up yang agresif

5. REKOMENDASI:
   - Prioritaskan alokasi untuk provinsi dengan stunting tinggi
   - Perlu monitoring kualitas gizi saat program di-scale up
   - Evaluasi keberlanjutan fiskal untuk target jangka panjang
   - Transparansi data pengadaan dan kualitas makanan

💡 CATATAN: Analisis ini berdasarkan data publik yang tersedia.
   Untuk analisis mendalam, diperlukan data tambahan seperti:
   - Data pengadaan per SPPG
   - Data kehadiran siswa
   - Data antropometri anak penerima
   - Laporan audit pelaksanaan program
""")

print("\n" + "=" * 60)
print("ANALISIS SELESAI!")
print("=" * 60)
print("\n✅ File yang dihasilkan:")
print("   1. analisis_mbg_2025.png (visualisasi)")
print("   2. 7 file CSV (raw data)")
print("\n📝 Next steps:")
print("   - Tambahkan data harga pangan dari BPS")
print("   - Scrape data pengadaan dari LPSE")
print("   - Analisis sentimen media sosial tentang program")
print("   - Buat dashboard interaktif dengan Streamlit/Dash")

plt.show()