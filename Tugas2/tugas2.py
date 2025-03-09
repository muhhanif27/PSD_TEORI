import numpy as np  # Library untuk operasi numerik
import matplotlib.pyplot as plt  # Library untuk visualisasi
import time  # Library untuk mengukur waktu eksekusi

# Fungsi untuk membuat subplot visualisasi

def plot_construction():
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # Membuat dua subplot dalam satu baris dengan ukuran 12x6

    # Subplot pertama untuk menampilkan titik acak
    axes[0].set_title('Random Generated Dots')  # Judul grafik pertama
    axes[0].set_aspect('equal')  # Menjaga rasio sumbu X dan Y tetap sama
    axes[0].set_xlim([-1, 1])  # Batas sumbu X
    axes[0].set_ylim([-1, 1])  # Batas sumbu Y

    # Subplot kedua untuk menampilkan estimasi π vs jumlah titik
    axes[1].set_title('Estimasi π vs Jumlah Titik')  # Judul grafik kedua
    axes[1].set_xlim([0, 100000])  # Batas sumbu X sesuai jumlah sampel
    axes[1].set_ylim([3.10, 3.20])  # Batas sumbu Y untuk nilai π
    axes[1].set_xlabel('Jumlah Titik')  # Label sumbu X
    axes[1].set_ylabel('Estimasi π')  # Label sumbu Y
    axes[1].grid(True)  # Menampilkan grid pada grafik kedua
    axes[1].set_yticks(np.arange(3.10, 3.21, 0.02))  # Menentukan interval pada sumbu Y
    
    return axes  # Mengembalikan objek subplot

# Memanggil fungsi untuk membuat subplot
axes = plot_construction()
ax1, ax2 = axes  # Menyimpan subplot dalam variabel terpisah

N_samples = np.arange(1, 100_001)  # Array dari 1 hingga 100000 sebagai jumlah titik acak
pi_counter = 0  # Variabel untuk menghitung titik yang masuk ke dalam lingkaran

# List untuk menyimpan data titik dan hasil estimasi π

dots_x, dots_y, dots_color = [], [], []  # List untuk menyimpan koordinat dan warna titik
pi_array = []  # List untuk menyimpan estimasi nilai π
n_points = []  # List untuk menyimpan jumlah titik yang digunakan

# Membuat scatter plot awal
scatter = ax1.scatter(dots_x, dots_y, color=dots_color, marker='o', s=5)  # Menampilkan titik-titik acak
plot, = ax2.plot([], [], 's-', color='blue', label='Estimasi π')  # Membuat garis estimasi π

# Menambahkan garis horizontal sebagai referensi nilai π asli
ax2.axhline(y=np.pi, color='r', linestyle='--', label='π sebenarnya')

start_time = time.time()  # Mulai pengukuran waktu eksekusi

# Looping untuk menjalankan simulasi Monte Carlo
for N in N_samples:
    x, y = np.random.uniform(-1, 1), np.random.uniform(-1, 1)  # Menghasilkan titik acak dalam rentang [-1,1]
    dots_x.append(x)  # Menyimpan koordinat X
    dots_y.append(y)  # Menyimpan koordinat Y

    # Menentukan apakah titik masuk dalam lingkaran (x^2 + y^2 ≤ 1)
    if np.sqrt(x**2 + y**2) <= 1:
        pi_counter += 1  # Jika dalam lingkaran, tambah hitungan
        dots_color.append('red')  # Beri warna merah untuk titik dalam lingkaran
    else:
        dots_color.append('blue')  # Beri warna biru untuk titik di luar lingkaran

    # Menghitung estimasi π berdasarkan perbandingan titik dalam lingkaran terhadap total titik
    approx_pi = 4 * (pi_counter / N)
    pi_array.append(approx_pi)  # Simpan nilai estimasi π
    n_points.append(N)  # Simpan jumlah titik yang sudah digunakan

    # Memperbarui plot setiap 5000 iterasi agar lebih interaktif
    if N % 5000 == 0:
        scatter.set_offsets(np.column_stack((dots_x, dots_y)))  # Memperbarui posisi titik pada plot
        scatter.set_facecolors(dots_color)  # Memperbarui warna titik
        ax1.set_title(f"Titik merah: {pi_counter}, Titik Biru: {N - pi_counter}")  # Update judul dengan info titik

        # Memperbarui plot estimasi π dengan data subsampling (ambil setiap 200 titik)
        plot.set_data(n_points[::200], pi_array[::200])  
        ax2.set_title(f'Estimasi π ~ {approx_pi}')  # Perbarui judul dengan estimasi terkini
        ax2.legend()  # Menampilkan legenda

        # Menampilkan informasi di terminal
        exec_time_so_far = time.time() - start_time
        print(f"Jumlah titik merah: {pi_counter}, Jumlah titik biru: {N - pi_counter}, "
              f"Jumlah titik: {N}, Estimasi π: {approx_pi}, "
              f"Error: {abs(approx_pi - np.pi):.6f}, Waktu: {exec_time_so_far:.4f} detik")

        plt.draw()
        plt.pause(0.01)  # Pause agar visualisasi dapat diperbarui

# Menampilkan hasil akhir di terminal
execution_time = time.time() - start_time  # Menghitung total waktu eksekusi
print(f"\nSimulasi Monte Carlo untuk π:")
print(f"Jumlah titik: {len(N_samples)}")
print(f"Estimasi π: {approx_pi}")
print(f"π asli: {np.pi}")
print(f"Error: {abs(approx_pi - np.pi)}")
print(f"Waktu eksekusi: {execution_time} detik")

# Menyimpan gambar hasil simulasi
plt.savefig("Tugas2/estimasi_pi.png", dpi=300)
plt.show()  # Menampilkan plot akhir
