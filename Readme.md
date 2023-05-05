# WeatherBot

Multilingual weather telegram-bot with PostgreSQL, SQLAlchemy and Docker.

## Features
- Weather forecast for three days
- Real time weather 
- Day length, sunrise and sunset
- Real time air quality
- English and Russian languages
- Geolocation of Telegram if a mobile application is used, otherwise by IP
- Recording weather and air quality data to a PostgreSQL database on a schedule
- Recording weather and air quality data to PostgreSQL database by admin command
- Database access via Adminer http://localhost:8080, or http://host-ip:8080
- Deployment via Docker

## Use
- Make your .env file by example .env.sample
- API can be found here https://www.weatherapi.com
- The files docker-compose_dev.yml, config_dev.py are made only for development on the local machine.
When using them, you need to change the imports in the files and in the .env DB_HOST=127.0.0.1
In this case, only PostgreSQL and Adminer will work in containers

## Server Deployment
- `install docker`
- `install docker compose`
- `git clone weatherbot`
- `cd weatherbot`
- `vi .env`   
- `vi config/your_location.py`    LOCALE = 'your coordinates'
- `docker compose -f docker-compose.yml build`
- `docker compose -f docker-compose.yml up -d`