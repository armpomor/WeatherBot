"""
Ranges of gas concentrations in air.
Green - excellent AQI = 0-50
Yellow - moderate AQI = 51-100
Orange - unhealthy AQI = 101-150
Brown - bad AQI = 151-200
Purple - very bad AQI = 201-300
Red - dangerous AQI = >300
In the dictionary they are increased by 10 times,
because then divide by 10 to make list[float]
https://www.pranaair.com/blog/what-is-air-quality-index-aqi-and-its-calculation/
"""

GASES = {
    'CO': {tuple([x / 10 for x in range(0, 8500)]): 'green',
           tuple([x / 10 for x in range(8500, 17000)]): 'yellow',
           tuple([x / 10 for x in range(17000, 85000)]): 'orange',
           tuple([x / 10 for x in range(85000, 146000)]): 'brown',
           tuple([x / 10 for x in range(146000, 290000)]): 'purple',
           tuple([x / 10 for x in range(290000, 300000)]): 'red'},
    'NO2': {tuple([x / 10 for x in range(0, 400)]): 'green',
            tuple([x / 10 for x in range(400, 800)]): 'yellow',
            tuple([x / 10 for x in range(800, 1800)]): 'orange',
            tuple([x / 10 for x in range(1800, 2800)]): 'brown',
            tuple([x / 10 for x in range(2800, 4000)]): 'purple',
            tuple([x / 10 for x in range(4000, 6000)]): 'red'},
    'O3': {tuple([x / 10 for x in range(0, 500)]): 'green',
           tuple([x / 10 for x in range(500, 1000)]): 'yellow',
           tuple([x / 10 for x in range(1000, 1680)]): 'orange',
           tuple([x / 10 for x in range(1680, 2080)]): 'brown',
           tuple([x / 10 for x in range(2080, 7480)]): 'purple',
           tuple([x / 10 for x in range(7480, 8000)]): 'red'},
    'SO2': {tuple([x / 10 for x in range(0, 400)]): 'green',
            tuple([x / 10 for x in range(400, 800)]): 'yellow',
            tuple([x / 10 for x in range(800, 3800)]): 'orange',
            tuple([x / 10 for x in range(3800, 8000)]): 'brown',
            tuple([x / 10 for x in range(8000, 16000)]): 'purple',
            tuple([x / 10 for x in range(16000, 17000)]): 'red'},
    'pm2_5': {tuple([x / 10 for x in range(0, 120)]): 'green',
              tuple([x / 10 for x in range(120, 354)]): 'yellow',
              tuple([x / 10 for x in range(354, 554)]): 'orange',
              tuple([x / 10 for x in range(554, 1504)]): 'brown',
              tuple([x / 10 for x in range(1504, 2504)]): 'purple',
              tuple([x / 10 for x in range(2504, 5005)]): 'red'},
    'pm10': {tuple([x / 10 for x in range(0, 540)]): 'green',
             tuple([x / 10 for x in range(540, 1540)]): 'yellow',
             tuple([x / 10 for x in range(1540, 2540)]): 'orange',
             tuple([x / 10 for x in range(2540, 3540)]): 'brown',
             tuple([x / 10 for x in range(3540, 4240)]): 'purple',
             tuple([x / 10 for x in range(4240, 6040)]): 'red'}
}

# Colored plates
CIRCLE_COLOR = {'green': '&#128994;',
                'yellow': '&#128993;',
                'orange': '&#128992;',
                'brown': '&#128996;',
                'purple': '&#128995;',
                'red': '&#128308;'
                }
