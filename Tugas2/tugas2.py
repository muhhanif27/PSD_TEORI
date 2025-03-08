import numpy as np
import matplotlib.pyplot as plt
import time

def plot_construction():
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Generated Dots
    axes[0].set_title('Random Generated Dots')
    axes[0].set_aspect('equal')
    axes[0].set_xlim([-1, 1])
    axes[0].set_ylim([-1, 1])

    # Plot Estimasi π
    axes[1].set_title('Estimasi π vs Jumlah Titik')
    axes[1].set_xlim([0, 100000])  # Sesuaikan dengan N_samples
    axes[1].set_ylim([3.10, 3.20])  # Sesuaikan dengan kebutuhan
    axes[1].set_xlabel('Jumlah Titik')
    axes[1].set_ylabel('Estimasi π')
    axes[1].grid(True)
    axes[1].set_yticks(np.arange(3.10, 3.21, 0.02))  # Atur interval sesuai gambar
    
    return axes

axes = plot_construction()
ax1, ax2 = axes
N_samples = np.arange(1, 100_001)
pi_counter = 0

# Data titik
dots_x, dots_y, dots_color = [], [], []
pi_array = []
n_points = []

scatter = ax1.scatter(dots_x, dots_y, color=dots_color, marker='o', s=5)
plot, = ax2.plot([], [], 's-', color='blue', label='Estimasi π')

# Tambahkan garis horizontal merah putus-putus di nilai π sebenarnya
ax2.axhline(y=np.pi, color='r', linestyle='--', label='π sebenarnya')

start_time = time.time()

for N in N_samples:
    x, y = np.random.uniform(-1, 1), np.random.uniform(-1, 1)
    dots_x.append(x)
    dots_y.append(y)

    if np.sqrt(x**2 + y**2) <= 1:
        pi_counter += 1
        dots_color.append('red')
    else:
        dots_color.append('blue')

    approx_pi = 4 * (pi_counter / N)
    pi_array.append(approx_pi)
    n_points.append(N)

    # Update plot tiap 5000 iterasi
    if N % 5000 == 0:
        scatter.set_offsets(np.column_stack((dots_x, dots_y)))
        scatter.set_facecolors(dots_color)
        ax1.set_title(f"Titik merah: {pi_counter}, Titik Biru: {N - pi_counter}")

        # Update plot estimasi π dengan subsampling
        plot.set_data(n_points[::200], pi_array[::200])  
        ax2.set_title(f'Estimasi π ~ {approx_pi}')
        ax2.legend()

        # Tampilkan proses di terminal
        exec_time_so_far = time.time() - start_time
        print(f"Jumlah titik merah: {pi_counter}, Jumlah titik biru: {N - pi_counter}, Jumlah titik: {N}, Estimasi π: {approx_pi}, Error: {abs(approx_pi - np.pi):.6f}, Waktu: {exec_time_so_far:.4f} detik")

        plt.draw()
        plt.pause(0.01)

# Tampilkan hasil akhir di terminal
execution_time = time.time() - start_time
print(f"\nSimulasi Monte Carlo untuk π:")
print(f"Jumlah titik: {len(N_samples)}")
print(f"Estimasi π: {approx_pi}")
print(f"π asli: {np.pi}")
print(f"Error: {abs(approx_pi - np.pi)}")
print(f"Waktu eksekusi: {execution_time} detik")

plt.savefig("Tugas2/estimasi_pi.png", dpi=300)
plt.show()
