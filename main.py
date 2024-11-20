import streamlit as st
from weather import get_weather_data
from datetime import datetime
import folium
from streamlit_folium import st_folium
import requests
from PIL import Image
import io

# Dictionary mapping weather conditions to icons
WEATHER_ICONS = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '🌨️',
    'Mist': '🌫️',
    'Smoke': '🌫️',
    'Haze': '🌫️',
    'Dust': '🌫️',
    'Fog': '🌫️',
}

# Custom CSS with dark theme
def get_custom_css():
    return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
            
            /* Base styles */
            [data-testid="stAppViewContainer"] {
                background-color: #1A1A1A;
                color: #FFFFFF;
                font-family: 'Poppins', sans-serif;
            }
            
            /* App title */
            .app-title {
                font-family: 'Poppins', sans-serif;
                font-weight: 600;
                font-size: 2.5rem;
                color: #E0E0E0;  /* Light gray */
                text-align: center;
                margin: 2rem 0;
                letter-spacing: 1px;
            }
            
            /* Section headers */
            h1, h2, h3 {
                font-family: 'Poppins', sans-serif;
                text-align: center;
                color: #F5F5F5;  /* Off-white */
                margin: 1rem 0;
                font-weight: 500;
                letter-spacing: 0.5px;
            }
            
            /* Metric styling */
            [data-testid="stMetricValue"] {
                color: #FFFFFF !important;
                font-size: 1.5rem !important;
                font-weight: 600 !important;
                font-family: 'Poppins', sans-serif !important;
            }
            
            [data-testid="stMetricLabel"] {
                color: #E0E0E0 !important;  /* Light gray */
                font-family: 'Poppins', sans-serif !important;
                font-weight: 500 !important;
            }
            
            /* Container styling */
            [data-testid="stVerticalBlock"] {
                background-color: #2C2C2C;
                border-radius: 15px;
                padding: 1.5rem;
                margin: 0.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            /* Button styling */
            .stButton>button {
                width: 100%;
                max-width: 300px;
                border-radius: 8px;
                height: 3em;
                background-color: #F5F5F5;  /* Off-white */
                color: #1A1A1A;  /* Dark background */
                font-family: 'Poppins', sans-serif;
                font-weight: 500;
                transition: all 0.3s ease;
                margin: 1rem auto;
                display: block;
                border: none;
            }
            
            .stButton>button:hover {
                background-color: #FFFFFF;  /* Pure white on hover */
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
            }
            
            /* Input styling */
            .stTextInput>div>div>input {
                color: #FFFFFF;
                background-color: #2C2C2C;
                border: 2px solid #404040;
                border-radius: 8px;
                text-align: center;
                max-width: 300px;
                margin: 0 auto;
                font-family: 'Poppins', sans-serif;
                padding: 0.5rem;
            }
            
            .stTextInput>div>div>input:focus {
                border-color: #64B5F6;  /* Material Blue */
                box-shadow: 0 0 0 1px #64B5F6;
            }
            
            /* Temperature display */
            .temperature {
                font-size: 4rem;
                font-weight: 600;
                color: #FFFFFF;
                text-align: center;
                margin: 1rem 0;
                font-family: 'Poppins', sans-serif;
            }
            
            /* Weather description */
            .weather-description {
                font-size: 1.5rem;
                color: #E0E0E0;  /* Light gray */
                text-align: center;
                margin-bottom: 2rem;
                font-weight: 500;
                font-family: 'Poppins', sans-serif;
            }
            
            /* Forecast cards */
            .forecast-card {
                background-color: #2C2C2C;
                border-radius: 15px;
                padding: 1.5rem;
                margin: 0.5rem;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .forecast-card h4 {
                color: #E0E0E0;  /* Light gray */
                font-family: 'Poppins', sans-serif;
                font-weight: 500;
                margin-bottom: 0.5rem;
            }
            
            .forecast-card h3 {
                color: #FFFFFF;
                font-family: 'Poppins', sans-serif;
                font-weight: 600;
                margin: 0.5rem 0;
            }
            
            /* Footer */
            footer {
                text-align: center;
                padding: 2rem;
                color: #BDBDBD;  /* Lighter gray */
                font-family: 'Poppins', sans-serif;
                font-weight: 400;
            }
        </style>
    """

def get_weather_icon_url(icon_code):
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

def load_weather_icon(icon_code):
    url = get_weather_icon_url(icon_code)
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    return img

def create_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker(
        [lat, lon],
        popup="Weather Location",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)
    return m

def get_forecast_data(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching forecast data: {str(e)}")
        return None

def main():
    # Set page config
    st.set_page_config(
        page_title="Weather App",
        page_icon="🌤️",
        layout="wide"
    )
    
    # Initialize session state
    if 'weather_data' not in st.session_state:
        st.session_state.weather_data = None
    if 'forecast_data' not in st.session_state:
        st.session_state.forecast_data = None

    # Inject custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Main container with centered content
    with st.container():
        # Header
        st.markdown("""
            <h1 class="app-title">
                🌤️ Weather Information App
            </h1>
        """, unsafe_allow_html=True)
        
        # Search section - centered
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            city = st.text_input(
                label="City Name",
                value="Mumbai",
                placeholder="Enter city name...",
                label_visibility="collapsed"
            )
            API_KEY = "82005d27a116c2880c8f0fcb866998a0"
            
            if st.button("Get Weather Info", use_container_width=True):
                if not city:
                    st.error("Please enter a city name")
                else:
                    with st.spinner('Fetching weather data...'):
                        try:
                            st.session_state.weather_data = get_weather_data(city, API_KEY)
                            if st.session_state.weather_data:
                                st.session_state.forecast_data = get_forecast_data(city, API_KEY)
                            else:
                                st.error("Unable to fetch weather data. Please check the city name.")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")

        # Display weather data if available
        if st.session_state.weather_data and st.session_state.forecast_data:
            weather = st.session_state.weather_data
            forecast = st.session_state.forecast_data
            
            try:
                # Current Weather Section
                st.markdown("""<div class="weather-card">""", unsafe_allow_html=True)
                
                # Weather icon and temperature
                icon_url = get_weather_icon_url(weather['icon'])
                st.markdown(f"""
                    <div style='display: flex; justify-content: center; align-items: center; flex-direction: column;'>
                        <img src="{icon_url}" alt="Weather Icon" style="width: 100px; height: 100px;">
                        <h1 style='font-size: 3rem; margin: 1rem;'>{weather['temperature']}°C</h1>
                        <p style='font-size: 1.5rem;'>{weather['description'].capitalize()}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Metrics Section with proper styling
                col1, col2 = st.columns(2)
                
                # Left Metrics Card
                with col1:
                    with st.container():
                        st.markdown("### 📊 Basic Metrics")
                        st.metric(
                            label="Feels Like",
                            value=f"{weather['feels_like']}°C",
                            delta=None
                        )
                        st.metric(
                            label="Humidity",
                            value=f"{weather['humidity']}%",
                            delta=None
                        )
                        st.metric(
                            label="Wind Speed",
                            value=f"{weather['wind_speed']} m/s",
                            delta=None
                        )
                
                # Right Metrics Card
                with col2:
                    with st.container():
                        st.markdown("### 🌅 Additional Info")
                        st.metric(
                            label="Pressure",
                            value=f"{weather['pressure']} hPa",
                            delta=None
                        )
                        st.metric(
                            label="Cloudiness",
                            value=f"{weather['clouds']}%",
                            delta=None
                        )
                        
                        # Sunrise and Sunset times
                        sunrise_time = datetime.fromtimestamp(weather['sunrise']).strftime('%H:%M')
                        sunset_time = datetime.fromtimestamp(weather['sunset']).strftime('%H:%M')
                        
                        st.markdown(f"""
                            <div style='text-align: center; padding: 10px;'>
                                <p style='margin: 5px;'>🌅 <b>Sunrise:</b> {sunrise_time}</p>
                                <p style='margin: 5px;'>🌇 <b>Sunset:</b> {sunset_time}</p>
                            </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Map Section - centered
                st.markdown("""<div class="map-container">""", unsafe_allow_html=True)
                st.markdown("### 📍 Location")
                if 'coord' in weather:
                    map_data = create_map(weather['coord']['lat'], weather['coord']['lon'])
                    st_folium(map_data, height=300, width=800)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Forecast Section - with corrected day calculation
                st.markdown("### 📅 5-Day Forecast")
                
                # Process forecast data to get one entry per day
                daily_forecasts = []
                seen_dates = set()
                
                for item in forecast['list']:
                    date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                    if date not in seen_dates:
                        daily_forecasts.append(item)
                        seen_dates.add(date)
                    if len(daily_forecasts) >= 5:  # Limit to 5 days
                        break
                
                # Display forecast
                forecast_cols = st.columns(len(daily_forecasts))
                for idx, daily in enumerate(daily_forecasts):
                    with forecast_cols[idx]:
                        date = datetime.fromtimestamp(daily['dt']).strftime('%A')
                        temp = round(daily['main']['temp'], 1)
                        icon = daily['weather'][0]['icon']
                        description = daily['weather'][0]['description']
                        
                        icon_url = get_weather_icon_url(icon)
                        st.markdown(f"""
                            <div class="forecast-card">
                                <h4>{date}</h4>
                                <img src="{icon_url}" alt="Weather Icon" style="width: 50px; height: 50px;">
                                <h3>{temp}°C</h3>
                                <p>{description.capitalize()}</p>
                            </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error displaying weather data: {str(e)}")
        
        # Footer
        st.markdown("""
            <footer>
                <p>Made with ❤️ using Streamlit</p>
            </footer>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 