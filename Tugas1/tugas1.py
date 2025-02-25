import simpy
import random
import numpy as np

# Parameter Simulasi
RANDOM_SEED = 42
JUMLAH_DRIVER = 5  # Jumlah driver tersedia
KECEPATAN_PESANAN_MASUK = 10  # Rata-rata pesanan masuk per jam
WAKTU_ANTAR = 15  # Waktu antar dalam menit
DURASI_SIMULASI = 120  # Durasi simulasi dalam menit
BATAS_KETERLAMBATAN = 30  # Pesanan dianggap terlambat jika lebih dari 30 menit

# Simpan data waktu tunggu
waktu_tunggu = []
waktu_total = []
pesanan_terlambat = 0  # Jumlah pesanan yang mengalami keterlambatan

class GoFood:
    def __init__(self, env, jumlah_driver, waktu_antar):
        self.env = env
        self.drivers = simpy.Resource(env, jumlah_driver)
        self.waktu_antar = waktu_antar
        self.antrian = []  # Antrian pesanan jika semua driver sibuk

    def antar_pesanan(self, pesanan, driver_id, waktu_masuk):
        """Simulasi proses pengantaran makanan oleh driver tertentu."""
        waktu_pengantaran = random.expovariate(1 / self.waktu_antar)
        yield self.env.timeout(waktu_pengantaran)

        total_waktu = env.now - waktu_masuk  # Total waktu dari pemesanan hingga diterima pelanggan
        waktu_total.append(total_waktu)

        if total_waktu > BATAS_KETERLAMBATAN:
            global pesanan_terlambat
            pesanan_terlambat += 1

        print(f"Driver {driver_id} mengantar {pesanan} dalam {waktu_pengantaran:.2f} menit. (Total: {total_waktu:.2f} menit)")

def pelanggan(env, nama_pesanan, gofood):
    """Proses pelanggan melakukan pemesanan."""
    waktu_masuk = env.now
    print(f"{nama_pesanan} masuk pada {waktu_masuk:.2f} menit.")

    with gofood.drivers.request() as request:
        yield request  # Menunggu driver tersedia
        
        # Jika driver sedang sibuk, pesanan harus menunggu
        waktu_tunggu_pesanan = env.now - waktu_masuk
        waktu_tunggu.append(waktu_tunggu_pesanan)

        # Identifikasi driver yang mengambil pesanan
        driver_id = len(gofood.drivers.users)
        print(f"{nama_pesanan} diambil oleh Driver {driver_id} setelah menunggu {waktu_tunggu_pesanan:.2f} menit.")

        yield env.process(gofood.antar_pesanan(nama_pesanan, driver_id, waktu_masuk))

def generator_pesanan(env, gofood, kecepatan_pesanan):
    """Menghasilkan pesanan masuk secara acak."""
    id_pesanan = 1
    while True:
        yield env.timeout(random.expovariate(1 / kecepatan_pesanan))
        env.process(pelanggan(env, f"Pesanan {id_pesanan}", gofood))
        id_pesanan += 1

# Jalankan simulasi
random.seed(RANDOM_SEED)
env = simpy.Environment()
gofood = GoFood(env, JUMLAH_DRIVER, WAKTU_ANTAR)

env.process(generator_pesanan(env, gofood, KECEPATAN_PESANAN_MASUK))
env.run(until=DURASI_SIMULASI)

# Analisis performa
print("\n=== Ringkasan Simulasi ===")
print(f"Rata-rata waktu tunggu: {np.mean(waktu_tunggu):.2f} menit")
print(f"Waktu tunggu maksimal: {np.max(waktu_tunggu):.2f} menit")
print(f"Waktu tunggu minimal: {np.min(waktu_tunggu):.2f} menit")
print(f"Rata-rata total waktu pesanan: {np.mean(waktu_total):.2f} menit")
print(f"Pesanan dengan total waktu maksimal: {np.max(waktu_total):.2f} menit")
print(f"Persentase pesanan terlambat: {(pesanan_terlambat / len(waktu_total)) * 100:.2f}%")
