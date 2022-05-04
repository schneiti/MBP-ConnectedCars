import json

import requests
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json;charset=UTF-8"
headers[
    "X-MBP-Access-Request"] = "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin"


def install_sensor(session: requests.Session, sens_id):
    url = "http://host.docker.internal:8080/mbp/api/deploy/sensor/" + sens_id

    resp = session.post(url, headers=headers)
    return resp, session

def get_sensor_state(session: requests.Session, sens_id):
    url = "http://host.docker.internal:8080/mbp/api/devices/{}/state/".format(sens_id)

    resp = session.get(url, headers=headers)
    return resp, session

def delete_value_logs(session: requests.Session, sens_id):
    url = "http://host.docker.internal:8080/mbp/api/sensors/{}/valueLogs".format(sens_id)

    resp = session.delete(url, headers=headers)
    return resp, session

def start_sensor(session: requests.Session, sens_id: str, start_time: str, car_file_name: str):
    url = "http://host.docker.internal:8080/mbp/api/start/sensor/{}".format(sens_id)

    data = [{"name":"startTime","value":start_time},{"name":"car_data_file_name","value":car_file_name}]

    resp = session.post(url, data=json.dumps(data), headers=headers)
    return resp, session

def get_value_logs(session: requests.Session, sens_id: str, amount: int):
    url = "http://host.docker.internal:8080/mbp/api/sensors/{}/valueLogs?sort=time%2Cdesc&size={}&startTime=-1&endTime=-1".format(sens_id, amount)

    resp = session.get(url, headers=headers)
    return resp, session