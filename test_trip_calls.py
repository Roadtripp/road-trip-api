# from subprocess import call
import requests
import json


def smoke_test():
    assert True

# TODO: figure out how to run and kill server in file


def trip_post_test():
    head_post = {'title':'TITLE',
    'origin':'334 Blackwell Street B017, Durham, NC',
    'origin_date':'08/25/2004', 'origin_time':'12:00 PM',
    'destination':'New York, NY', 'destination_date':'08/28/2004',
    'destination_time':'12:00 PM'}
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
    assert j_post['origin_date'] =='08/25/2004'
    assert j_post['origin_date'] !='08/25/2005'
    assert j_post['destination_date'] == '08/28/2004'
    assert j_post['destination_date'] != '08/29/2004'
    assert j_post['destination_time'] == '12:00:00'
    assert j_post['destination_time'] != '12:01:00'

    head_patch = {'title':'TITLE2'}
    res_patch = requests.patch(url+str(j_post['id'])+'/', data=head_patch)
    j_patch = json.loads(res_patch.text)

    assert res_patch.status_code == 200
    assert j_patch['title'] != 'TITLE'
    assert j_patch['title'] == 'TITLE2'

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
    assert j_get['origin_date'] =='08/25/2004'
    assert j_get['origin_date'] !='08/25/2005'
    assert j_get['destination_date'] == '08/28/2004'
    assert j_get['destination_date'] != '08/29/2004'
    assert j_get['destination_time'] == '12:00:00'
    assert j_get['destination_time'] != '12:01:00'

    res_delete = requests.delete(url+str(j_post['id'])+'/')

    assert res_delete.status_code == 204
