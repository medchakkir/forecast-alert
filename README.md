# Forecast Alert

An automated weather monitoring service that checks weather forecasts and sends email alerts when rain is expected. This project uses Python to fetch weather data from a weather API and sends email notifications via Gmail SMTP.

## Features

- Weather forecast API integration
- Automatic rain detection (checks for weather condition codes 500-599)
- Email alert system via Gmail SMTP
- Environment variable configuration for secure credential management
- Comprehensive error handling for API and email operations
- Easy to automate with task schedulers

## Requirements

- Python 3.x
- Gmail account with App Password enabled
- Weather API access (OpenWeatherMap or compatible API with API key)
- Required Python packages (see `requirements.txt`):
  - `python-dotenv` - For loading environment variables
  - `requests` - For making API calls to fetch weather forecasts
  - `smtplib` - Built into Python standard library for email sending

## Installation

1. Clone this repository:

```bash
git clone https://github.com/<username>/forecast-alert.git
cd forecast-alert
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate # On Windows
source venv/bin/activate # On macOS/Linux
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:

```env
API_KEY=your_weather_api_key_here
API_ENDPOINT=https://api.openweathermap.org/data/2.5/forecast
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=recipient@example.com
SENDER_PASSWORD=your_gmail_app_password
LATITUDE=your_latitude
LONGITUDE=your_longitude
```

**Important:**

- Replace all placeholder values with your actual credentials
- Never commit the `.env` file to version control
- For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password
- Get a free API key from [OpenWeatherMap](https://openweathermap.org/api) or use a compatible weather API

## Usage

To run the script:

```bash
python main.py
```

### How It Works

1. The script loads environment variables from `.env` file
2. Validates that all required environment variables are present
3. Fetches weather forecast data from the configured API endpoint using the API key
4. Checks the forecast for rain conditions (weather codes 500-599 indicate rain)
5. If rain is detected in the forecast, sends an email alert via Gmail SMTP
6. The email includes:
   - Subject: "Rain Alert"
   - Body: A reminder to bring an umbrella ☔
7. If no rain is expected, displays a message: "No rain expected today! ☀️"

### Error Handling

The script includes comprehensive error handling for:

- Missing environment variables
- API request failures (network errors, timeouts, HTTP errors)
- JSON parsing errors
- Missing or invalid API response structure
- SMTP authentication failures
- General SMTP errors
- Unexpected exceptions

## Setting Up Automated Execution

To run this script automatically on a schedule, you can:

1. **Windows Task Scheduler**: Create a scheduled task to run the script daily (e.g., in the morning to check the day's forecast)
2. **Linux/Mac Cron Jobs**: Add a cron job to execute the script at specified intervals
3. **Cloud Services**: Deploy to AWS Lambda, Google Cloud Functions, or similar services
4. **GitHub Actions**: Set up a scheduled workflow to run the script

Example cron job (runs daily at 8 AM):

```bash
0 8 * * * /usr/bin/python3 /path/to/forecast-alert/main.py
```

## Security Notes

- **Never commit your `.env` file** to version control - it contains sensitive credentials
- Use Gmail's App Passwords instead of your main account password
- Keep your API key secure and rotate it periodically if compromised
- Consider using a secrets management service for production deployments
- The `.env` file is already included in `.gitignore` to prevent accidental commits

## API Compatibility

This script is designed to work with OpenWeatherMap's 5-day/3-hour forecast API. The API response should include:

- A `list` key containing an array of forecast data
- Each item should have a `weather` array with condition codes
- Weather condition codes follow the OpenWeatherMap standard (5xx codes indicate rain)

If using a different weather API, you may need to adjust the response parsing logic in `main.py`.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is for educational purposes.
