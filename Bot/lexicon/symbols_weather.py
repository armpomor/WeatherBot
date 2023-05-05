"""
First dict - Key=Unique weather code; value=Description of the weather.
The second dict is key=Unique weather code; value=Unicode Characters
"""

CONDITIONS = {1000: "Sunny", 1003: "Partly cloudy", 1006: "Cloudy", 1009: "Overcast",
              1030: "Mist", 1063: "Patchy rain possible", 1066: "Patchy snow possible",
              1069: "Patchy sleet possible", 1072: "Patchy freezing drizzle possible",
              1087: "Thundery outbreaks possible", 1114: "Blowing snow", 1117: "Blizzard",
              1135: "Fog", 1147: "Freezing fog", 1150: "Patchy light drizzle",
              1153: "Light drizzle", 1168: "Freezing drizzle", 1171: "Heavy freezing drizzle",
              1180: "Patchy light rain", 1183: "Light rain", 1186: "Moderate rain at times",
              1189: "Moderate rain", 1192: "Heavy rain at times", 1195: "Heavy rain",
              1198: "Light freezing rain", 1201: "Moderate or heavy freezing rain",
              1204: "Light sleet", 1207: "Moderate or heavy sleet", 1210: "Patchy light snow",
              1213: "Light snow", 1216: "Patchy moderate snow", 1219: "Moderate snow",
              1222: "Patchy heavy snow", 1225: "Heavy snow", 1237: "Ice pellets", 1240: "Light rain shower",
              1243: "Moderate or heavy rain shower", 1246: "Torrential rain shower",
              1249: "Light sleet showers", 1252: "Moderate or heavy sleet showers", 1255: "Light snow showers",
              1258: "Moderate or heavy snow showers", 1261: "Light showers of ice pellets",
              1264: "Moderate or heavy showers of ice pellets", 1273: "Patchy light rain with thunder",
              1276: "Moderate or heavy rain with thunder", 1279: "Patchy light snow with thunder",
              1282: "Moderate or heavy snow with thunder"}

SYMBOLS = {1000: "\u2600", 1003: "\u2601", 1006: "\u2601", 1009: "\u2602",
           1030: "\u2601", 1063: "\u2614", 1066: "\u2614", 1069: "\u2614",
           1072: "\u2614", 1087: "\u2608", 1114: "\u2603", 1117: "\u2603",
           1135: "\u2601", 1147: "\u2601", 1150: "\u2614", 1153: "\u2614",
           1168: "\u2601", 1171: "\u2614", 1180: "\u2614", 1183: "\u2614",
           1186: "\u2614", 1189: "\u2614", 1192: "\u2614", 1195: "\u2614",
           1198: "\u2614", 1201: "\u2614", 1204: "\u2603", 1207: "\u2603", 1210: "\u2603",
           1213: "\u2603", 1216: "\u2603", 1219: "\u2603", 1222: "\u2603", 1225: "\u2603",
           1237: "\u2602", 1240: "\u2614", 1243: "\u2614", 1246: "\u2614", 1249: "\u2614",
           1252: "\u2603", 1255: "\u2603", 1258: "\u2603", 1261: "\u2614",
           1264: "\u0001F327", 1273: "\u2614", 1276: "\u0001F327", 1279: "\u2603", 1282: "\u2603"}
