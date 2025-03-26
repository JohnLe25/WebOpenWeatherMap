import requests
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import json
import os

# 🔹 Thiết lập style cho ứng dụng
st.set_page_config(page_title="Dự Báo Thời Tiết", page_icon="🌦️", layout="centered")

# 🎨 Tuỳ chỉnh màu nền bằng CSS
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
        font-family: Arial, sans-serif;
    }
    .stApp {
        background: linear-gradient(to right, #74ebd5, #acb6e5);
        border-radius: 15px;
        padding: 20px;
    }
    .stTitle {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
    }
    .stTextInput>div>div>input {
        font-size: 18px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🔑 Lấy API từ biến môi trường
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
        
        st.markdown(f"<h3 style='color: #ffffff;'>📍 {city}</h3>", unsafe_allow_html=True)
        for day in forecast_days:
            date = day['date']
            temp = day['day']['avgtemp_c']
            weather_desc = day['day']['condition']['text']
            icon_url = "https:" + day['day']['condition']['icon']

            dates.append(date)
            temps.append(temp)

            # 🖼️ Hiển thị thời tiết với bố cục rõ ràng
            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
            col1.markdown(f"<p style='font-size:18px; color:#ffffff;'>📅 <b>{date}</b></p>", unsafe_allow_html=True)
            col2.image(icon_url, width=50)
            col3.markdown(f"<p style='font-size:18px; color:#ffcc00;'>🌡️ <b>{temp}°C</b></p>", unsafe_allow_html=True)
            col4.markdown(f"<p style='font-size:18px; color:#ffffff;'>☁️ {weather_desc}</p>", unsafe_allow_html=True)

        plot_temperature_chart(city, dates, temps)
    else:
        st.error("❌ Không thể lấy dữ liệu!")

def plot_temperature_chart(city, dates, temps):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, temps, marker='o', linestyle='-', color='#ff5733', linewidth=2, label=city)
    ax.fill_between(dates, temps, color="#ffcccb", alpha=0.3)
    
    for i, txt in enumerate(temps):
        ax.text(dates[i], temps[i], f"{txt}°C", fontsize=12, ha='right', va='bottom')

    ax.set_xlabel("Ngày")
    ax.set_ylabel("Nhiệt độ (°C)")
    ax.set_title(f"📊 Biểu đồ nhiệt độ tại {city}")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

def main():
    st.markdown("<h1 class='stTitle'>🌤️ Dự Báo Thời Tiết 3 Ngày</h1>", unsafe_allow_html=True)
    st.write("💡 Nhập tên thành phố để xem dự báo thời tiết!")

    password_input = st.text_input("🔒 Nhập mật khẩu:", type="password")
    if password_input == PASSWORD:
        cities = st.text_input("🏙️ Nhập thành phố (cách nhau bằng dấu phẩy):")
        if st.button("🚀 Lấy dữ liệu"):
            city_list = [city.strip() for city in cities.split(",")]
            for city in city_list:
                get_weather(city)
    else:
        st.warning("⚠️ Mật khẩu không đúng. Hãy thử lại!")

if __name__ == "__main__":
    main()
