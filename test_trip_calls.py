# from subprocess import call
import requests
import json


def smoke_test():
    assert True

# TODO: figure out how to run and kill server in file


def trip_post_test():
    head = {'title':'TITLE', 'origin':'334 Blackwell Street B017, Durham, NC',
    'origin_date':'08/25/2004', 'origin_time':'12:00 PM',
    'destination':'New York, NY', 'destination_date':'08/28/2004',
    'destination_time':'12:00 PM'}
    url = 'http://127.0.0.1:8000/api/trip/'
    res_post = requests.post(url, data=head)
    j = json.loads(res_post.text)

    assert j['title'] == 'TITLE'
    assert j['title'] != 'TITLE2'
    assert j['origin'] == '334 Blackwell Street B017, Durham, NC'
    assert j['origin'] != '335 Blackwell Street B017, Durham, NC'
    assert j['destination'] == 'New York, NY'
    assert j['destination'] != 'Miami, FL'
    assert j['origin_time'] == '12:00:00'
    assert j['origin_time'] != '12:00:01'
    assert j['origin_date'] =='08/25/2004'
    assert j['origin_date'] !='08/25/2005'
    assert j['destination_date'] == '08/28/2004'
    assert j['destination_date'] != '08/29/2004'
    assert j['destination_time'] == '12:00:00'
    assert j['destination_time'] != '12:01:00'
