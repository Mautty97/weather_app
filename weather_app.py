'''
This program will allow a use to either allow access to their location or ask them for a zip code.
It will then fetch the current weather in that area displaying 
current temp, real feel, high/low, wind speed, humidity, and UV index

https://geocoder.readthedocs.io/api.html#ip-addresses
https://weather.com/weather/today/l/78741

Libraries used:
-requests
-bs4
-geocoder
-re

'''

import requests
import bs4
import geocoder
import re

#check if user wants to use a zip code or their current location
def zip_or_ip():
    response = ''
    print('\n')
    print('You can check the weather by putting in a zip code or just use your current location.')
    print('\n')
    while response not in ['Y','y','N','n']:
        response = input('Would you like to use a zip code or jsut use your current location? (y/n): ')
        if response not in ['Y','y','N','n']:
            print('Sorry, please choose y or n')
        elif response in ['Y','y']:
            return True
        else:
            return False

#get a zip code from the user
def get_zip():
        valid_zip = re.compile(r'\d\d\d\d\d')
        location = input('Please enter a zip code (ex: 94043): ')
        while not(valid_zip.match(location)):
            location = input('Please enter a valid zip code (ex: 94043): ')
        return location

#gets users ip address and returns a zip code from that
def get_location():
    g = geocoder.ip('me')
    return g.postal

#get current temp data from weather soup
def get_curr_temp(soup):
    temp = soup.select('.CurrentConditions--tempValue--3a50n')
    return(temp[0].text)

#get real feel temp from weather soup
def get_real_feel(soup):
    all_tags = soup.select('.removeIfEmpty')
    real_feel = re.search(r'\d+\W', all_tags[13].text)
    return real_feel[0]

#get high and low temps from weather soup (have to use tuple unpacking to separate them)
def get_high_low(soup):
    high_low = soup.select('.WeatherDetailsListItem--wxData--2s6HT')
    return high_low[0].text

#get wind speed from weather soup as a long string
def get_wind_speed(soup):
    wind_speed = soup.select('.WeatherDetailsListItem--wxData--2s6HT')
    return wind_speed[1].text

#get humidity from weather soup
def get_humidity(soup):
    humidity = soup.select('.WeatherDetailsListItem--wxData--2s6HT')
    return humidity[2].text

#get UV index from weather soup
def get_uv_index(soup):
    uv_index = soup.select('.WeatherDetailsListItem--wxData--2s6HT')
    return uv_index[5].text

#pass in weather conditions and print them out (if the high or low has already happend it will return -- for the temp)
def show_weather(location, curr_temp, real_feel, high, low, wind_speed, humidity, uv_index):
    if high == '--':
        print(f""" 

        Here are the local weather conditions in {location}:

        The current temperature is {curr_temp}
        The real feel temperature is {real_feel}
        The low will be {low}
        The wind speed is {wind_speed}
        The humidity is {humidity}
        The UV index is at {uv_index}
        """)

    elif low =='--':
        print(f""" 

        Here are the local weather conditions in {location}:

        The current temperature is {curr_temp}
        The real feel temperature is {real_feel}
        The high will be {high}
        The wind speed is {wind_speed}
        The humidity is {humidity}
        The UV index is at {uv_index}
        """)

    else:
        print(f""" 

        Here are the local weather conditions in {location}:

        The current temperature is {curr_temp}
        The real feel temperature is {real_feel}
        The high will be {high} and the low will be {low}
        The wind speed is {wind_speed}
        The humidity is {humidity}
        The UV index is at {uv_index}
        """)

"""
Main Code:
Ask user if they want to input a zip code or just use their location.
Then use their location to get the zip code or use the zip code the input to fetch weather data from weather.com
"""
again = True

while again:

    base_url = 'https://weather.com/weather/today/l/{}'

    if zip_or_ip():
        location = get_zip()
    else:
        location = get_location()

    res = requests.get(base_url.format(location))
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    try:
        curr_temp = get_curr_temp(soup)
        real_feel = get_real_feel(soup)
        high,low = get_high_low(soup).split('/')
        wind_speed = get_wind_speed(soup)[14:]
        humidity = get_humidity(soup)
        uv_index = get_uv_index(soup)

        show_weather(location, curr_temp, real_feel, high, low, wind_speed, humidity, uv_index)

    except Exception as e:
        print('There was an error')
        print(e)

    response = ''

    while response not in ['Y','y','N','n']:
        response = input('Would you like to check a different location? (y/n): ')
        if response not in ['Y','y','N','n']:
            print('Sorry, please choose y or n')
        elif response in ['Y','y']:
            again = True
        else:
            again = False

