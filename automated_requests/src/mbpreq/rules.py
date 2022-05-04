import json
from typing import List

import requests
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json;charset=UTF-8"
headers[
    "X-MBP-Access-Request"] = "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin"

def create_action(session: requests.Session, actuator_id: str, topic_suffix: str, data: str):
    url = "http://host.docker.internal:8080/mbp/api/rule-actions"

    data = {"type": "ACTUATOR_ACTION", "parameters": {"actuator": actuator_id, "action": topic_suffix, "data": data},
            "name": topic_suffix}

    resp = session.post(url, data=json.dumps(data), headers=headers)
    return resp, session

def create_trigger(session: requests.Session, event_count: int, actuator_id: str, time: str, time_two:str, name: str):
    url = "http://host.docker.internal:8080/mbp/api/rule-triggers"

    data = {"name":name,"description":"","query":"SELECT * FROM pattern [every(event_{event_num}=actuator_{act_id})] WHERE ((event_{event_num}.`['scenario_meta']['time']`>= {time}) AND (event_{event_num}.`['scenario_meta']['time']`<{time_two}))".format(event_num=event_count, time=time, time_two=time_two, act_id=actuator_id)}

    resp = session.post(url, data=json.dumps(data), headers=headers)
    return resp, session

def create_rule_definition(session: requests.Session, trigger_id: str, action_id: str, name:str):
    url = "http://host.docker.internal:8080/mbp/api/rules"

    data = {"name": name,"trigger":trigger_id,"actions":["{}".format(action_id)]}

    resp = session.post(url, data=json.dumps(data), headers=headers)
    return resp, session

def enable_rule_definition(session: requests.Session, rule_def_id: str):
    url = "http://host.docker.internal:8080/mbp/api/rules/enable/{}".format(rule_def_id)

    resp = session.post(url, headers=headers)
    return resp, session