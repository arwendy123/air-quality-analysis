import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("all_data.csv")

# Konversi kolom datetime ke tipe data datetime
df['datetime'] = pd.to_datetime(df['datetime']).dt.date

# Sidebar
st.sidebar.title("Streamlit Dashboard")

# Tambahkan filter berdasarkan stasiun
station_options = ["Semua Stasiun"] + list(df['station'].unique())  # Tambahkan "Semua Stasiun" ke opsi
selected_station = st.sidebar.selectbox("Pilih Stasiun:", station_options)

# Tambahkan filter berdasarkan rentang tanggal
start_date = st.sidebar.date_input("Pilih Tanggal Awal:", df['datetime'].min())
end_date = st.sidebar.date_input("Pilih Tanggal Akhir:", df['datetime'].max())

# Filter data berdasarkan stasiun dan rentang tanggal
if selected_station == "Semua Stasiun":
    filtered_df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]
else:
    filtered_df = df[(df['station'] == selected_station) & (df['datetime'] >= start_date) & (df['datetime'] <= end_date)]

# Main content
st.title("Analisis Data Kualitas Udara")

# Tambahkan deskripsi atau penjelasan singkat
st.write("Dashboard ini memberikan analisis data kualitas udara berdasarkan pertanyaan bisnis yang dipilih.")

selected_question = st.sidebar.selectbox("Pilih Pertanyaan Bisnis:", ["1. Kualitas Udara Stasiun", "2. Tren Polusi Udara"])

if selected_question == "1. Kualitas Udara Stasiun":
    # Visualisasi perbandingan kualitas udara antar stasiun menggunakan boxplot
    st.subheader("Visualisasi Perbandingan Kualitas Udara Antar Stasiun")
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='station', y='PM2.5', data=filtered_df, palette='Set3')
    plt.title('Perbandingan Kualitas Udara Antar Stasiun')
    plt.xlabel('Stasiun')
    plt.ylabel('PM2.5 Concentration')
    st.pyplot(plt.gcf())

    # Analisis Statistik Deskriptif
    st.subheader("Analisis Statistik Deskriptif")
    station_stats = filtered_df.groupby('station')['PM2.5'].describe()
    st.write(station_stats)

elif selected_question == "2. Tren Polusi Udara":
    # Ensure 'datetime' column is datetime type
    filtered_df['datetime'] = pd.to_datetime(filtered_df['datetime'])

    # Analisis Tren Harian
    st.subheader("Analisis Tren Harian Polusi Udara")
    daily_mean = filtered_df.groupby(filtered_df['datetime'].dt.date)['PM2.5'].mean()
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=daily_mean.index, y=daily_mean.values)
    plt.title('Tren Harian Polusi Udara')
    plt.xlabel('Tanggal')
    plt.ylabel('Rata-rata PM2.5')
    st.pyplot(plt.gcf())

    # Analisis Tren Mingguan
    st.subheader("Analisis Tren Mingguan Polusi Udara")
    weekly_mean = filtered_df.groupby(filtered_df['datetime'].apply(lambda x: x.isocalendar()[1]))['PM2.5'].mean()
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=weekly_mean.index, y=weekly_mean.values)
    plt.title('Tren Mingguan Polusi Udara')
    plt.xlabel('Minggu ke-')
    plt.ylabel('Rata-rata PM2.5')
    st.pyplot(plt.gcf())