import requests
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import json
import os

# Định nghĩa mật khẩu và API Key từ biến môi trường
PASSWORD = os.getenv("APPWEATHER_PASSWORD")
API_KEY = os.getenv("WEATHER_API_KEY")

def apply_custom_style():
    st.markdown(
        """
        <style>
            body {
                background-color: #E3F2FD; /* Màu xanh dương nhạt */
                color: #2E3B55; /* Màu chữ tối dịu mắt */
            }
            .stApp {
                background-color: #E8F5E9; /* Xanh lá nhạt */
            }
            .stTextInput, .stButton, .stTitle, .stHeader, .stSubheader {
                color: #1E3A5F; /* Màu xanh đậm giúp dễ đọc */
            }
            .stPlotlyChart, .stImage, .stDataFrame {
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

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
        save_history(city, forecast_days)
    else:
        st.error("❌ Không thể lấy dữ liệu!")

def plot_temperature_chart(city, dates, temps):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker='o', linestyle='-', color='#00838F', linewidth=2, label=city)
    for i, txt in enumerate(temps):
        plt.text(dates[i], temps[i], f"{txt}°C", fontsize=12, ha='right', va='bottom', color='#004D40')
    plt.xlabel("Ngày", color="#004D40")
    plt.ylabel("Nhiệt độ (°C)", color="#004D40")
    plt.title(f"Dự báo nhiệt độ tại {city}", color="#004D40")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(plt)

def main():
    apply_custom_style()
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
