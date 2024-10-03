import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Memuat data yang sudah dibersihkan
day_data = pd.read_csv('dashboard/day_data.csv')
hour_data = pd.read_csv('dashboard/hour_data.csv')

# Judul proyek
st.title("Proyek Analisis Data: Bike-sharing-dataset")

# Menampilkan identitas diri
st.write("### Identitas Diri")
st.write("- **Nama:** Muhammad Haikal Batubara")
st.write("- **Email:** m248b4ky2870@bangkit.academy")
st.write("- **ID Dicoding:** haikal_batubara")

# Menampilkan beberapa baris pertama dari masing-masing dataset untuk verifikasi
st.subheader("Data Day")
st.write(day_data.head())

st.subheader("Data Hour")
st.write(hour_data.head())

# Statistik Deskriptif
st.subheader("Statistik Deskriptif")
st.write("Statistik Deskriptif untuk day_data:")
st.write(day_data.describe())

st.write("Statistik Deskriptif untuk hour_data:")
st.write(hour_data.describe())

# Histogram dan Boxplot untuk day_data
st.subheader("Histogram dan Boxplot untuk day_data")
variables_to_plot_day = ['cnt', 'temp', 'hum', 'windspeed']
fig, axs = plt.subplots(2, 4, figsize=(15, 10))

for i, variable in enumerate(variables_to_plot_day):
    # Histogram
    sns.histplot(day_data[variable], bins=30, kde=True, ax=axs[0, i])
    axs[0, i].set_title(f'Histogram {variable} (day)')
    axs[0, i].set_xlabel(variable)
    axs[0, i].set_ylabel('Frequency')

    # Boxplot
    sns.boxplot(x=day_data[variable], ax=axs[1, i])
    axs[1, i].set_title(f'Boxplot {variable} (day)')
    axs[1, i].set_xlabel(variable)

plt.tight_layout()
st.pyplot(fig)

# Heatmap untuk korelasi variabel
st.subheader("Heatmap Korelasi (day_data)")

# Select only numeric columns for correlation
numeric_columns = day_data.select_dtypes(include=['number']).columns
correlation_matrix = day_data[numeric_columns].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f',
            cmap='coolwarm', square=True, cbar_kws={'shrink': .8})
plt.title('Heatmap Korelasi (day_data)')
st.pyplot(plt)

# Analisis Penyewaan Berdasarkan Musim
st.subheader("Jumlah Penyewaan Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=day_data, x='season', y='cnt', estimator=sum, ax=ax)
ax.set_title('Total Penyewaan Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Total Penyewaan')
st.pyplot(fig)

# Tren Penyewaan Harian
st.subheader("Tren Penyewaan Harian")
daily_rentals = day_data.groupby('dteday')['cnt'].sum().reset_index()

# Pastikan kolom 'dteday' bertipe datetime
daily_rentals['dteday'] = pd.to_datetime(daily_rentals['dteday'])

fig, ax = plt.subplots(figsize=(15, 5))
plt.plot(daily_rentals['dteday'], daily_rentals['cnt'], marker='o')
ax.set_title('Tren Penyewaan Harian')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Total Penyewaan')
plt.xticks(rotation=45)
plt.grid()
st.pyplot(fig)

# Scatter Plots untuk variabel cuaca dan cnt
st.subheader("Hubungan antara Variabel Cuaca dan Jumlah Penyewaan")
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

sns.scatterplot(data=day_data, x='temp', y='cnt', alpha=0.6, ax=axs[0, 0])
axs[0, 0].set_title('Hubungan antara Suhu dan Jumlah Penyewaan')
axs[0, 0].set_xlabel('Temperature')
axs[0, 0].set_ylabel('Jumlah Penyewaan (cnt)')

sns.scatterplot(data=day_data, x='hum', y='cnt', alpha=0.6, ax=axs[0, 1])
axs[0, 1].set_title('Hubungan antara Kelembapan dan Jumlah Penyewaan')
axs[0, 1].set_xlabel('Humidity')
axs[0, 1].set_ylabel('Jumlah Penyewaan (cnt)')

sns.scatterplot(data=day_data, x='windspeed', y='cnt', alpha=0.6, ax=axs[1, 0])
axs[1, 0].set_title('Hubungan antara Kecepatan Angin dan Jumlah Penyewaan')
axs[1, 0].set_xlabel('Windspeed')
axs[1, 0].set_ylabel('Jumlah Penyewaan (cnt)')

sns.boxplot(data=day_data, x='weathersit', y='cnt', ax=axs[1, 1])
axs[1, 1].set_title('Jumlah Penyewaan Berdasarkan Situasi Cuaca')
axs[1, 1].set_xlabel('Situasi Cuaca')
axs[1, 1].set_ylabel('Jumlah Penyewaan (cnt)')

plt.tight_layout()
st.pyplot(fig)

# Segmentasi berdasarkan jenis cuaca
st.subheader("Jumlah Penyewaan Berdasarkan Jenis Cuaca")
weather_counts = day_data.groupby('weathersit')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=weather_counts, x='weathersit', y='cnt',
            hue='weathersit', palette='viridis', dodge=False, ax=ax)
ax.set_title('Jumlah Penyewaan Berdasarkan Jenis Cuaca')
ax.set_xlabel('Jenis Cuaca')
ax.set_ylabel('Jumlah Penyewaan')
plt.xticks(rotation=0)
ax.legend(title='Jenis Cuaca')
st.pyplot(fig)

# Segmentasi berdasarkan hari kerja vs. libur
st.subheader("Jumlah Penyewaan Berdasarkan Hari Kerja vs. Libur")
workingday_counts = day_data.groupby('workingday')['cnt'].sum().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=workingday_counts, x='workingday', y='cnt', ax=ax)
ax.set_title('Jumlah Penyewaan Berdasarkan Hari Kerja vs. Libur')
ax.set_xlabel('Hari Kerja (0 = Tidak, 1 = Ya)')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Menampilkan kesimpulan
st.subheader("Kesimpulan")
st.write("""
### 1. Pengaruh Faktor Cuaca terhadap Jumlah Penyewaan Sepeda
Dari analisis regresi yang dilakukan, ditemukan bahwa faktor cuaca, seperti suhu dan kelembapan, memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda. Secara khusus, peningkatan suhu berbanding lurus dengan jumlah penyewaan sepeda, menunjukkan bahwa hari yang lebih hangat cenderung mendorong lebih banyak orang untuk menggunakan sepeda. Sebaliknya, kelembapan yang tinggi cenderung mengurangi minat masyarakat untuk menyewa sepeda.

### 2. Tren Penyewaan Sepeda Berdasarkan Musim dan Hari Kerja/Libur
Analisis menunjukkan bahwa tren penyewaan sepeda bervariasi antara musim dan hari kerja/libur. Musim panas dan musim semi mencatatkan jumlah penyewaan yang lebih tinggi dibandingkan musim dingin, mencerminkan preferensi masyarakat untuk bersepeda pada suhu yang lebih nyaman. Selain itu, penyewaan sepeda lebih tinggi pada hari kerja dibandingkan hari libur, yang menunjukkan bahwa sepeda digunakan tidak hanya untuk rekreasi tetapi juga sebagai sarana transportasi oleh pekerja.

### 3. Waktu Puncak Penggunaan Sepeda dalam Satu Hari
Analisis data menunjukkan bahwa waktu puncak penggunaan sepeda terjadi pada pagi hari (antara pukul 7 hingga 9) dan sore hari (antara pukul 17 hingga 19). Waktu-waktu ini biasanya bertepatan dengan jam berangkat dan pulang kerja, yang menunjukkan bahwa sepeda digunakan sebagai moda transportasi utama di waktu-waktu tersebut. Selain itu, perbedaan signifikan terlihat antara hari kerja dan akhir pekan, di mana penyewaan lebih tinggi pada hari kerja dibandingkan dengan akhir pekan.

### Rangkuman
Secara keseluruhan, hasil analisis menunjukkan bahwa faktor cuaca, musim, dan waktu berperan penting dalam memengaruhi jumlah penyewaan sepeda. Memahami pola ini dapat membantu dalam perencanaan dan pengelolaan layanan penyewaan sepeda, termasuk pengembangan infrastruktur dan promosi untuk meningkatkan penggunaan sepeda di masyarakat.
""")
