# import pickle
import json
# import pandas as pd
import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from models import Trip
import os
from city_selector import find_haversine, make_df


def w(data):
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))


def p():
    return pickle.load(open('data.pkl', 'rb'))


def pic(city, state):
    pass







def main():
    key = os.environ['GOOGLE_MAPS']
    location = "Vancouver MA"
    url = 'https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}'.format(key, location)
    resp = requests.get(url)
    j = json.loads(resp.text)['results'][0]['geometry']['location']
    df = make_df()
    print([row.img_url for index, row in df[abs(j['lng']-df['longitude']) < .45][abs(j['lat']-df['latitude']) < .45].iterrows()][0])
        # print(find_haversine(row['latitude'], row['longitude'], j['lat'], j['lng']))
        # print(row.City)


    # print(j)
    # print(resp.status_code)

    # driver = webdriver.Chrome('/Documents/')
    # driver.get("http://www.python.org")
    # assert "Python" in driver.title
    # elem = driver.find_element_by_name("q")
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source
    # driver.close()
    # df = pd.read_csv("road_trip/trip/best_us_cities.csv", encoding="latin-1")
    # print(df.iloc[0::2][["City", "State"]])
    # pic("Seattle", "WA")
    # resp = driver.get('http://www.google.com/search?q=Seattle+WA')
    # resp = requests.get('https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=seattle+wa')
    # city = BeautifulSoup(resp.content, 'html.parser').find_all("img", {"class": "iuth"})
    # print(city)
    # print(resp.status_code)


if __name__ == '__main__':
    main()
