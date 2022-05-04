import json

import requests
from requests.structures import CaseInsensitiveDict

def login():
    s = requests.Session()
    url = "http://host.docker.internal:8080/mbp/api/users/login"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers[
        "X-MBP-Access-Request"] = "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin"
    data = '{"username":"admin","password":"12345"}'

    resp = s.post(url, data=data, headers=headers)

    return resp, s

def adapt_broker_settings(session: requests.Session, broker_ip: str):
    url = "http://host.docker.internal:8080/mbp/api/settings"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json;charset=UTF-8"
    headers["X-MBP-Access-Request"] = "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin"

    data = {"senderName":"MBP","brokerLocation":"REMOTE","brokerIPAddress":broker_ip,"brokerPort":1883,"demoMode":False}

    resp = session.post(url, data=json.dumps(data), headers=headers)
    return resp, session

def create_device(session: requests.Session, ip_address: str):
    url = "http://host.docker.internal:8080/mbp/api/devices"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json;charset=UTF-8"
    headers["X-MBP-Access-Request"] = "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin"


    data = '{"username":"mbp","password":"password","ipAddress":"' + ip_address + '","componentType":"Virtual Machine","name":"CarSimDevice","errors":{}}'

    resp = session.post(url, data=data, headers=headers)
    return resp, session

def create_data_model(session: requests.Session):
    url = "http://host.docker.internal:8080/mbp/api/data-models"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json;charset=UTF-8"
    headers["X-MBP-Access-Request"] = "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin"


    data_raw = {"name": "CarDataModel", "description": "Data model for simulating car data", "errors": {},
                "treeNodes": [{"name": "make", "type": "string", "parent": "car_info", "children": []},
                              {"name": "model", "type": "string", "parent": "car_info", "children": []},
                              {"name": "license_num", "type": "string", "parent": "car_info", "children": []},
                              {"name": "type_of_drive", "type": "string", "parent": "car_info", "children": []},
                              {"name": "kilometrage_val", "type": "decimal128", "parent": "kilometrage", "children": []},
                              {"name": "kilometrage_unit", "type": "string", "parent": "kilometrage", "children": []},
                              {"name": "kilometrage", "type": "object", "parent": "car_info",
                               "children": ["kilometrage_val", "kilometrage_unit"]},
                              {"name": "car_info", "type": "object", "parent": "RootObj",
                               "children": ["make", "model", "license_num", "type_of_drive", "kilometrage"]},
                              {"name": "latitude", "type": "decimal128", "unit": "°", "parent": "position", "children": []},
                              {"name": "longitude", "type": "decimal128", "unit": "°", "parent": "position",
                               "children": []},
                              {"name": "bearing", "type": "decimal128", "unit": "°", "parent": "position", "children": []},
                              {"name": "nmea", "type": "string", "parent": "position", "children": []},
                              {"name": "position", "type": "object", "parent": "RootObj",
                               "children": ["latitude", "longitude", "bearing", "nmea"]},
                              {"name": "speed_val", "type": "decimal128", "parent": "speed", "children": []},
                              {"name": "speed_unit", "type": "string", "parent": "speed", "children": []},
                              {"name": "speed", "type": "object", "parent": "motion",
                               "children": ["speed_val", "speed_unit"]},
                              {"name": "acc_val", "type": "decimal128", "parent": "acceleration", "children": []},
                              {"name": "acc_unit", "type": "string", "parent": "acceleration", "children": []},
                              {"name": "acceleration", "type": "object", "parent": "motion",
                               "children": ["acc_val", "acc_unit"]},
                              {"name": "motion", "type": "object", "parent": "RootObj",
                               "children": ["speed", "acceleration"]},
                              {"name": "left_turn_signal", "type": "boolean", "parent": "light_status", "children": []},
                              {"name": "right_turn_signal", "type": "boolean", "parent": "light_status",
                               "children": []},
                              {"name": "light_status", "type": "object", "parent": "RootObj",
                               "children": ["left_turn_signal", "right_turn_signal"]},
                              {"name": "time", "type": "decimal128", "unit": "s", "parent": "scenario_meta",
                               "children": []},
                              {"name": "last_message_received", "type": "string", "parent": "scenario_meta",
                               "children": []},
                              {"name": "scenario_meta", "type": "object", "parent": "RootObj",
                               "children": ["time", "last_message_received"]},
                              {"name": "RootObj", "description": "", "type": "object", "unit": "", "parent": "",
                               "children": ["car_info", "position", "motion", "light_status", "scenario_meta"]}]}

    resp = session.post(url, data=json.dumps(data_raw), headers=headers)
    return resp, session

def create_actuator(session: requests.Session, act_name: str, operatorId: str, deviceId: str):
    url = "http://host.docker.internal:8080/mbp/api/actuators"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json;charset=UTF-8"
    headers["X-MBP-Access-Request"] = "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin"


    data = {"name":act_name,"componentType":"Motor","operatorId": operatorId,"deviceId": deviceId,"errors":{}}

    resp = session.post(url, data=json.dumps(data), headers=headers)
    return resp, session

def create_sensor(session: requests.Session, sens_name: str, operatorId: str, deviceId: str):
    url = "http://host.docker.internal:8080/mbp/api/sensors"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json;charset=UTF-8"
    headers["X-MBP-Access-Request"] = "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin"

    data = {"name":sens_name,"componentType":"Motor","operatorId": operatorId,"deviceId": deviceId,"errors":{}}

    resp = session.post(url, data=json.dumps(data), headers=headers)
    return resp, session

def delete_sensor(session: requests.Session, sens_id):
    url = "http://host.docker.internal:8080/mbp/api/sensor/" + sens_id

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json;charset=UTF-8"
    headers["X-MBP-Access-Request"] = "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin"


    resp = session.delete(url, headers=headers)
    return resp, session