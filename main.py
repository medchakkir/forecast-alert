import os
import smtplib
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
latitude = os.getenv("LATITUDE")
longitude = os.getenv("LONGITUDE")
api_key = os.getenv("API_KEY")
api_endpoint = os.getenv("API_ENDPOINT")
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")


# Validate all required environment variables
required_vars = {
    "LATITUDE": latitude,
    "LONGITUDE": longitude,
    "API_KEY": api_key,
    "API_ENDPOINT": api_endpoint,
    "SENDER_EMAIL": sender_email,
    "RECEIVER_EMAIL": receiver_email,
    "SENDER_PASSWORD": sender_password,
}

missing_vars = [var for var, value in required_vars.items() if value is None]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

weather_params = {
    "lat": latitude,
    "lon": longitude,
    "appid": api_key
}

# Fetch weather forecast from API
try:
    response = requests.get(url=api_endpoint, params=weather_params, timeout=10)
    response.raise_for_status()
    weather_data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching weather forecast: {e}")
    exit(1)
except ValueError as e:
    print(f"Error parsing JSON response: {e}")
    exit(1)

# Validate response structure
if "list" not in weather_data:
    print("Error: API response missing 'list' key")
    print(f"Response structure: {list(weather_data.keys())}")
    exit(1)

if not weather_data["list"] or len(weather_data["list"]) == 0:
    print("Error: Weather data list is empty")
    exit(1)

# Check for rain conditions
will_rain = False
for hour_data in weather_data["list"]:
    # Safely access weather data
    if "weather" not in hour_data or not hour_data["weather"]:
        print("Warning: Missing weather data for hour, skipping...")
        continue
    
    condition_code = hour_data["weather"][0].get("id")
    if condition_code is None:
        print("Warning: Missing condition code, skipping...")
        continue
    
    # Check specifically for rain (5xx codes)
    if 500 <= int(condition_code) < 600:
        will_rain = True
        break  # Found rain, no need to check further

# Send Email if rain is expected
if will_rain:
    try:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=sender_email, password=sender_password)
            connection.sendmail(
                from_addr=sender_email, 
                to_addrs=receiver_email, 
                msg=f"Subject: Rain Alert\n\nIt's going to rain today. Remember to bring an umbrella."
            )
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP authentication failed: {e}")
        exit(1)
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error sending email: {e}")
        exit(1)
else:
    print("No rain expected today! ☀️")
