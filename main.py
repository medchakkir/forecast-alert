import requests
from twilio.rest import Client

api_endpoint = 'https://api.openweathermap.org/data/2.5/forecast'
api_key = '255c7549955d253fc1d5844f03a9b211'
account_sid = 'ACb33bbccadbd464eda31bf77d98fc406d'
auth_token = 'cc84a85e5195ca459e8b998d66a4b075'

weather_params = {
    # "lat": 51.759048,
    # "lon": 19.45,
    "lat": 11.600470,
    "lon": 43.150829,
    'appid': api_key
}


response = requests.get(url=api_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
# print(weather_data["list"])
# print(weather_data["list"][0]["weather"][0]["id"])

will_rain = False
for hour_data in weather_data["list"]:
    # print(hour_data["weather"][0]["id"])
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    # print("It's going to rain today, Remember to bring an ☔")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It's going to rain today, Remember to bring an ☔",
        from_='+12566023591',
        to='+252638114350'
    )
    print(message.status)

