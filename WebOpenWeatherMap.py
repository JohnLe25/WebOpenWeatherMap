import requests
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import json
import os

# Lấy API Key và mật khẩu từ biến môi trường
API_KEY = os.getenv("WEATHER_API_KEY")
PASSWORD = os.getenv("APPWEATHER_PASSWORD")

# Kiểm tra API Key
if not API_KEY:
    st.error("❌ Lỗi: API Key chưa được thiết lập. Hãy đặt biến môi trường WEATHER_API_KEY.")

# Kiểm tra mật khẩu
if not PASSWORD:
    st.error("❌ Lỗi: Chưa thiết lập mật khẩu. Hãy đặt biến môi trường APP_PASSWORD.")

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=4"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_days = data['forecast']['forecastday']

        dates = []
        temps = []
        
        st.subheader(f"📍 {city}")
        for day in forecast_days:
            date = day['date']
            temp = day['day']['avgtemp_c']
            weather_desc = day['day']['condition']['text']
            icon_url = "https:" + day['day']['condition']['icon']

            dates.append(date)
            temps.append(temp)

            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
            col1.write(f"📅 **{date}**")
            col2.image(icon_url, width=40)
            col3.write(f"🌡️ **{temp}°C**")
            col4.write(f"☁️ {weather_desc}")

        plot_temperature_chart(city, dates, temps)
    else:
        st.error("❌ Không thể lấy dữ liệu!")

def plot_temperature_chart(city, dates, temps):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker='o', linestyle='-', color='red', linewidth=2, label=city)
    for i, txt in enumerate(temps):
        plt.text(dates[i], temps[i], f"{txt}°C", fontsize=12, ha='right', va='bottom')
    plt.xlabel("Ngày")
    plt.ylabel("Nhiệt độ (°C)")
    plt.title(f"Dự báo nhiệt độ tại {city}")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

def main():
    st.title("🌤️ Dự Báo Thời Tiết 3 Ngày")
    st.write("Nhập tên thành phố để xem dự báo!")

    password_input = st.text_input("🔒 Nhập mật khẩu:", type="password")
    if password_input == PASSWORD:
        cities = st.text_input("Nhập tên các thành phố (cách nhau bằng dấu phẩy):")
        if st.button("Lấy dữ liệu"):
            city_list = [city.strip() for city in cities.split(",")]
            for city in city_list:
                get_weather(city)
    else:
        st.warning("⚠️ Mật khẩu không đúng. Hãy thử lại!")

if __name__ == "__main__":
    main()
