import requests
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import json
import os

# Định nghĩa mật khẩu và API Key từ biến môi trường
PASSWORD = os.getenv("APP_PASSWORD", "12345")
API_KEY = os.getenv("WEATHER_API_KEY", "6d8b08472b1e48178f332905252503")

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
    plt.plot(dates, temps, marker='o', linestyle='-', color='red', linewidth=2, label=city)
    for i, txt in enumerate(temps):
        plt.text(dates[i], temps[i], f"{txt}°C", fontsize=12, ha='right', va='bottom')
    plt.xlabel("Ngày")
    plt.ylabel("Nhiệt độ (°C)")
    plt.title(f"Dự báo nhiệt độ tại {city}")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

def save_history(city, forecast_days):
    history_data = {"city": city, "forecast": []}
    for day in forecast_days:
        history_data["forecast"].append({
            "date": day['date'],
            "temperature": day['day']['avgtemp_c'],
            "condition": day['day']['condition']['text']
        })
    try:
        with open("weather_history.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
            data.append(history_data)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("weather_history.json", "w", encoding="utf-8") as file:
            json.dump([history_data], file, ensure_ascii=False, indent=4)

def show_history():
    try:
        with open("weather_history.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        st.subheader("📜 Lịch Sử Dự Báo Thời Tiết")
        for record in data:
            st.write(f"🌍 **{record['city']}**")
            for day in record["forecast"]:
                st.write(f"📅 {day['date']} - 🌡️ {day['temperature']}°C - ☁️ {day['condition']}")
            st.write("---")
    except (FileNotFoundError, json.JSONDecodeError):
        st.write("📌 Chưa có lịch sử dữ liệu.")

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
        if st.button("Xem lịch sử"):
            show_history()
    else:
        st.warning("⚠️ Mật khẩu không đúng. Hãy thử lại!")

if __name__ == "__main__":
    main()
