import json

import requests
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json;charset=UTF-8"
headers[
    "X-MBP-Access-Request"] = "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin"


def install_actuator(session: requests.Session, act_id):
    url = "http://host.docker.internal:8080/mbp/api/deploy/actuator/" + act_id

    resp = session.post(url, headers=headers)
    return resp, session

def get_actuator_state(session: requests.Session, act_id):
    url = "http://host.docker.internal:8080/mbp/api/actuators/{}/state/".format(act_id)

    resp = session.get(url, headers=headers)
    return resp, session

def delete_value_logs(session: requests.Session, act_id):
    url = "http://host.docker.internal:8080/mbp/api/actuators/{}/valueLogs".format(act_id)

    resp = session.delete(url, headers=headers)
    return resp, session

def start_actuator(session: requests.Session, act_id: str, start_time: str, car_file_name: str):
    url = "http://host.docker.internal:8080/mbp/api/start/actuator/{}".format(act_id)

    data = [{"name":"startTime","value":start_time},{"name":"car_data_file_name","value":car_file_name}]

    resp = session.post(url, data=json.dumps(data), headers=headers)
    return resp, session

def get_value_logs(session: requests.Session, act_id: str, amount: int):
    url = "http://host.docker.internal:8080/mbp/api/actuators/{}/valueLogs?sort=time%2Cdesc&size={}&startTime=-1&endTime=-1".format(act_id, amount)

    resp = session.get(url, headers=headers)
    return resp, session

def get_actuator_state(session: requests.Session, act_id: str):
    url = "http://host.docker.internal:8080/mbp/api/actuators/state/{}".format(act_id)

    resp = session.get(url, headers=headers)
    return resp, session