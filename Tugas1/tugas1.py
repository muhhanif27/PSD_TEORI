# Muhammad Hanif
# 202210370311265
# Pemodelan dan Simulasi Data B

import simpy
import random
import numpy as np

# Parameter Simulasi
RANDOM_SEED = 42  # Seed untuk hasil random yang konsisten
JUMLAH_DRIVER = 5  # Jumlah driver tersedia dalam sistem
KECEPATAN_PESANAN_MASUK = 10  # Rata-rata jumlah pesanan masuk per jam
WAKTU_ANTAR = 15  # Waktu rata-rata antar pesanan dalam menit
DURASI_SIMULASI = 120  # Durasi total simulasi dalam menit
BATAS_KETERLAMBATAN = 30  # Pesanan dianggap terlambat jika lebih dari 30 menit

# Variabel untuk menyimpan data hasil simulasi
waktu_tunggu = []  # List untuk mencatat waktu tunggu pesanan
waktu_total = []  # List untuk mencatat total waktu pengantaran
pesanan_terlambat = 0  # Counter untuk jumlah pesanan yang mengalami keterlambatan

class GoFood:
    """Kelas untuk merepresentasikan sistem pengantaran makanan."""
    
    def __init__(self, env, jumlah_driver, waktu_antar):
        self.env = env
        self.drivers = simpy.Resource(env, jumlah_driver)  # Sumber daya driver
        self.waktu_antar = waktu_antar
        self.antrian = simpy.Store(env)  # Struktur data untuk menyimpan antrean pesanan

    def antar_pesanan(self, pesanan, driver_id, waktu_masuk):
        """Simulasi proses pengantaran makanan oleh driver tertentu."""
        
        # Waktu pengantaran pesanan diambil secara acak dari distribusi eksponensial
        waktu_pengantaran = random.expovariate(1 / self.waktu_antar)
        yield self.env.timeout(waktu_pengantaran)  # Driver melakukan pengantaran

        # Hitung total waktu dari pemesanan hingga makanan diterima pelanggan
        total_waktu = self.env.now - waktu_masuk
        waktu_total.append(total_waktu)

        # Jika total waktu lebih dari batas keterlambatan, hitung sebagai pesanan terlambat
        global pesanan_terlambat
        if total_waktu > BATAS_KETERLAMBATAN:
            pesanan_terlambat += 1

        print(f"[{self.env.now:.2f}] Driver {driver_id} mengantar {pesanan} dalam {waktu_pengantaran:.2f} menit. (Total: {total_waktu:.2f} menit)")

def pelanggan(env, nama_pesanan, gofood):
    """Proses pelanggan melakukan pemesanan."""
    
    waktu_masuk = env.now  # Catat waktu pesanan masuk ke sistem
    print(f"[{waktu_masuk:.2f}] {nama_pesanan} masuk.")

    with gofood.drivers.request() as request:
        yield request  # Menunggu driver tersedia
        
        # Hitung waktu tunggu hingga ada driver yang mengambil pesanan
        waktu_tunggu_pesanan = env.now - waktu_masuk
        waktu_tunggu.append(waktu_tunggu_pesanan)

        # ID driver yang menangani pesanan (berdasarkan jumlah driver yang sedang digunakan)
        driver_id = gofood.drivers.count  
        print(f"[{env.now:.2f}] {nama_pesanan} diambil oleh Driver {driver_id} setelah menunggu {waktu_tunggu_pesanan:.2f} menit.")

        # Proses pengantaran pesanan
        yield env.process(gofood.antar_pesanan(nama_pesanan, driver_id, waktu_masuk))

def generator_pesanan(env, gofood, kecepatan_pesanan):
    """Menghasilkan pesanan masuk secara acak berdasarkan distribusi eksponensial."""
    
    id_pesanan = 1
    while True:
        # Waktu antar pesanan berikutnya dihitung secara acak berdasarkan kecepatan pesanan masuk
        yield env.timeout(random.expovariate(1 / kecepatan_pesanan))
        
        # Proses pesanan baru
        env.process(pelanggan(env, f"Pesanan {id_pesanan}", gofood))
        id_pesanan += 1

# Inisialisasi simulasi
random.seed(RANDOM_SEED)
env = simpy.Environment()
gofood = GoFood(env, JUMLAH_DRIVER, WAKTU_ANTAR)

# simulasi
env.process(generator_pesanan(env, gofood, KECEPATAN_PESANAN_MASUK))
env.run(until=DURASI_SIMULASI)  # Simulasi berjalan hingga batas waktu yang ditentukan

# Analisis performa sistem berdasarkan data simulasi
print("\n=== Ringkasan Simulasi ===")
print(f"Rata-rata waktu tunggu: {np.mean(waktu_tunggu):.2f} menit")
print(f"Waktu tunggu maksimal: {np.max(waktu_tunggu):.2f} menit")
print(f"Waktu tunggu minimal: {np.min(waktu_tunggu):.2f} menit")
print(f"Rata-rata total waktu pesanan: {np.mean(waktu_total):.2f} menit")
print(f"Pesanan dengan total waktu maksimal: {np.max(waktu_total):.2f} menit")
print(f"Persentase pesanan terlambat: {(pesanan_terlambat / len(waktu_total)) * 100:.2f}%")
