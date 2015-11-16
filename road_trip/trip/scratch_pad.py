import pickle
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
# from models import Trip


def w(data):
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))


def p():
    return pickle.load(open('data.pkl', 'rb'))


def pic(city, state):
    pass


def main():
    df = pd.read_csv("road_trip/trip/best_us_cities.csv", encoding="latin-1")
    # print(df.iloc[0::2][["City", "State"]])
    # pic("Seattle", "WA")
    resp = requests.get('http://www.google.com/search?q=Seattle+WA')
    print(resp.text)
    print(resp.status_code)


if __name__ == '__main__':
    main()
