# from subprocess import call
import requests
import json


def smoke_test():
    """Test to make sure nosetests works"""
    assert True

# TODO: figure out how to run and kill server in file


def trip_api_test():
    """Testing suite for Trip API calls
       (POST, PATCH, GET, DELETE)"""

    # POST a trip
    head_post = {'title': 'TITLE',
                 'origin': '334 Blackwell Street B017, Durham, NC',
                 'origin_date': '08/25/2004', 'origin_time': '12:00 PM',
                 'destination': 'New York, NY',
                 'destination_date': '08/28/2004',
                 'destination_time': '12:00 PM'}
    url = 'http://127.0.0.1:8000/api/trip/'
    res_post = requests.post(url, data=head_post)
    j_post = json.loads(res_post.text)

    assert res_post.status_code == 201
    assert j_post['title'] == 'TITLE'
    assert j_post['title'] != 'TITLE2'
    assert j_post['origin'] == '334 Blackwell Street B017, Durham, NC'
    assert j_post['origin'] != '335 Blackwell Street B017, Durham, NC'
    assert j_post['destination'] == 'New York, NY'
    assert j_post['destination'] != 'Miami, FL'
    assert j_post['origin_time'] == '12:00:00'
    assert j_post['origin_time'] != '12:00:01'
    assert j_post['origin_date'] == '08/25/2004'
    assert j_post['origin_date'] != '08/25/2005'
    assert j_post['destination_date'] == '08/28/2004'
    assert j_post['destination_date'] != '08/29/2004'
    assert j_post['destination_time'] == '12:00:00'
    assert j_post['destination_time'] != '12:01:00'

    # PATCH a trip
    head_patch = {'title': 'TITLE2'}
    res_patch = requests.patch(url+str(j_post['id'])+'/', data=head_patch)
    j_patch = json.loads(res_patch.text)

    assert res_patch.status_code == 200
    assert j_patch['title'] != 'TITLE'
    assert j_patch['title'] == 'TITLE2'

    # GET a trip
    res_get = requests.get(url+str(j_post['id'])+'/')
    j_get = json.loads(res_get.text)

    assert res_get.status_code == 200
    assert j_get['title'] == 'TITLE2'
    assert j_get['title'] != 'TITLE'
    assert j_get['origin'] == '334 Blackwell Street B017, Durham, NC'
    assert j_get['origin'] != '335 Blackwell Street B017, Durham, NC'
    assert j_get['destination'] == 'New York, NY'
    assert j_get['destination'] != 'Miami, FL'
    assert j_get['origin_time'] == '12:00:00'
    assert j_get['origin_time'] != '12:00:01'
    assert j_get['origin_date'] == '08/25/2004'
    assert j_get['origin_date'] != '08/25/2005'
    assert j_get['destination_date'] == '08/28/2004'
    assert j_get['destination_date'] != '08/29/2004'
    assert j_get['destination_time'] == '12:00:00'
    assert j_get['destination_time'] != '12:01:00'

    # DELETE a trip
    res_delete = requests.delete(url+str(j_post['id'])+'/')
    assert res_delete.status_code == 204


def city_api_test():
    """Testing suite for City API calls
       (POST, PATCH, GET, DELETE)"""
    # POST a trip
    head_trip_post = {'title': 'TITLE',
                      'origin': '334 Blackwell Street B017, Durham, NC',
                      'origin_date': '08/25/2004', 'origin_time': '12:00 PM',
                      'destination': 'New York, NY',
                      'destination_date': '08/28/2004',
                      'destination_time': '12:00 PM'}
    trip_url = 'http://127.0.0.1:8000/api/trip/'
    res_trip_post = requests.post(trip_url, data=head_trip_post)
    j_trip_post = json.loads(res_trip_post.text)
    trip_url += str(j_trip_post['id']) + '/'

    # POST a city
    head_city_post = {'city_name': 'Boston, MA', 'lat': 25, 'lon': 35}
    res_city_post = requests.post(trip_url+'city/', data=head_city_post)
    j_city_post = json.loads(res_city_post.text)
    city_url = trip_url+'city/' + str(j_city_post['id']) + '/'

    assert res_city_post.status_code == 201
    assert j_city_post['city_name'] == 'Boston, MA'
    assert j_city_post['trip_id'] == str(j_trip_post['id'])

    # PATCH a city
    head_city_patch = {'city_name': 'Cambridge, MA'}
    res_city_patch = requests.patch(city_url, data=head_city_patch)
    j_city_patch = json.loads(res_city_patch.text)

    assert res_city_patch.status_code == 200
    assert j_city_patch['city_name'] == 'Cambridge, MA'
    assert j_city_patch['city_name'] != 'Boston, MA'
    assert j_city_patch['trip_id'] == j_trip_post['id']

    # GET a city
    res_city_get = requests.get(city_url)
    j_city_get = json.loads(res_city_get.text)

    assert res_city_get.status_code == 200
    assert j_city_get['city_name'] == 'Cambridge, MA'
    assert j_city_get['city_name'] != 'Boston, MA'
    assert j_city_get['trip_id'] == j_trip_post['id']

    # DELETE a city
    res_delete_city = requests.delete(city_url)
    assert res_delete_city.status_code == 204

    # DELETE a trip
    res_delete = requests.delete(trip_url)
    assert res_delete.status_code == 204


def trip_creation_test():
    head_trip_post = {'title': 'TITLE',
                      'origin': '334 Blackwell Street B017, Durham, NC',
                      'origin_date': '08/25/2004', 'origin_time': '12:00 PM',
                      'destination': 'New York, NY',
                      'destination_date': '08/28/2004',
                      'destination_time': '12:00 PM'}
    url_trip_post = 'http://127.0.0.1:8000/api/trip/'
    res_trip_post = requests.post(url_trip_post, head_trip_post)
    j_trip_post = json.loads(res_trip_post.text)

    url_trip_suggestions = url_trip_post + str(j_trip_post['id']) + '/suggestions/'
    suggestions = json.loads(requests.get(url_trip_suggestions).text)

    assert res_trip_post.status_code == 201
    assert {'location': "Washington, District of Columbia",
            'stopover': False,
            'activities': []
            } in suggestions['waypoints']
    assert {'location': "Fayetteville, NC"} not in suggestions['waypoints']
