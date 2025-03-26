import requests
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import json
import os

# Định nghĩa mật khẩu và API Key từ biến môi trường
PASSWORD = os.getenv("APPWEATHER_PASSWORD")
API_KEY = os.getenv("WEATHER_API_KEY")

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
            col2.image(icon_url, width=50)
            col3.write(f"🌡️ **{temp}°C**")
            col4.write(f"☁️ {weather_desc}")

        plot_temperature_chart(city, dates, temps)
    else:
        st.error("❌ Không thể lấy dữ liệu!")

def plot_temperature_chart(city, dates, temps):
    st.markdown("""
        <style>
            .stPlotlyChart {border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);}
        </style>
    """, unsafe_allow_html=True)
    
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker='o', linestyle='-', color='cyan', linewidth=2, label=city)
    plt.xlabel("Ngày")
    plt.ylabel("Nhiệt độ (°C)")
    plt.title(f"Dự báo nhiệt độ tại {city}")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(plt)

def main():
    st.set_page_config(page_title="Dự Báo Thời Tiết", page_icon="⛅", layout="centered")
    
    st.markdown("""
        <style>
            body {
                background-color: #2E2E2E;
                color: #EAEAEA;
                font-family: Arial, sans-serif;
            }
            .stTextInput, .stButton {
                border-radius: 10px;
            }
        </style>
    """, unsafe_allow_html=True)
    
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
