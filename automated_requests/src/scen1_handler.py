import json
import time
from threading import Thread, Lock
import requests

from src.mbpreq.actuator_control import install_actuator, start_actuator, get_value_logs, get_actuator_state
from src.mbpreq.generic_mbp_operations import *
from src.mbpreq.op_control import create_operator_scen_one
from src.mbpreq.rules import create_trigger, create_action, create_rule_definition, enable_rule_definition

ACTION_CAR2_SLOWDOWN_MSG = "{\"from\": \"car1\", \"to\": \"car2\", \"msg\": \"Emergency braking on opposite lane. Slow down with acceleration = -3,55 m/s^2 to velocity = 29 km/h.\"}"
ACTION_CAR2_SLOWDOWN_SUFFIX = "slowdown_cartwo"

ACTION_CAR3_SLOWDOWN_MSG = "{\"from\": \"car1\", \"to\": \"car3\", \"msg\": \"Emergency braking on your lane ahead. Slow down with acceleration = -2.57 m/s^2 to 13 km/h.\"}"
ACTION_CAR3_SLOWDOWN_SUFFIX = "slowdown_carthree"

deploy_status = "UNDEPLOYED"
act_id_one = ""
act_id_two = ""
act_id_three = ""
session = login()[1]

access_lock = Lock()


def deploy_scen_one():
    global deploy_status
    global act_id_one, act_id_two, act_id_three
    global deploy_status

    resp, session = login()
    if resp.status_code == 200: print("Login successful")

    deploy_status = "Logged in"

    # Adapt settings
    #  resp, session = adapt_broker_settings(session, broker_ip="172.16.238.3")
    #  if resp.status_code == 200: print("Settings adaptions successful")

    # deploy_status = "Settings adapted"

    # Create device
    resp, session = create_device(session, ip_address="172.16.238.10")
    if resp.status_code == 200: print("Device creation successful")
    device_id = json.loads(str(resp.text))["id"]

    deploy_status = "Device created"

    # Create data model
    resp, session = create_data_model(session)
    if resp.status_code == 200: print("Data model creation successful")
    data_model_id = json.loads(str(resp.text))["id"]

    deploy_status = "Data model created"

    # Create operator
    resp, session = create_operator_scen_one(session, data_model_id)
    print(data_model_id)
    if resp.status_code == 200: print("Operator creation successful")
    operator_id = json.loads(str(resp.text))["id"]
    print(resp.status_code, resp.text, resp.content)

    deploy_status = "Operator created"

    # Create sensors
    #   resp, session = create_sensor(session, "Car1", operatorId=operator_id, deviceId=device_id)
    #   print(data_model_id)
    #    if resp.status_code == 200: print("Sensor creation successful")
    #    sensor_id_one = json.loads(str(resp.text))["id"]
    #    print(resp.status_code, resp.text, resp.content)

    # Create actuators
    resp, session = create_actuator(session, "Car1", operatorId=operator_id, deviceId=device_id)
    print(data_model_id)
    if resp.status_code == 200: print("Actuator creation successful")
    act_id_one = json.loads(str(resp.text))["id"]
    print(resp.status_code, resp.text, resp.content)

    resp, session = create_actuator(session, "Car2", operatorId=operator_id, deviceId=device_id)
    print(data_model_id)
    if resp.status_code == 200: print("Actuator creation successful")
    act_id_two = json.loads(str(resp.text))["id"]
    print(resp.status_code, resp.text, resp.content)

    resp, session = create_actuator(session, "Car3", operatorId=operator_id, deviceId=device_id)
    print(data_model_id)
    if resp.status_code == 200: print("Actuator creation successful")
    act_id_three = json.loads(str(resp.text))["id"]
    print(resp.status_code, resp.text, resp.content)

    deploy_status = "Actuators created... Create actions..."

    # Action1 for car2
    resp, session = create_action(session, act_id_two, ACTION_CAR2_SLOWDOWN_SUFFIX, ACTION_CAR2_SLOWDOWN_MSG)
    if resp.status_code == 200: print("Action creation successful")
    action_one_id = json.loads(str(resp.text))["id"]

    # Action2 for car3
    resp, session = create_action(session, act_id_three, ACTION_CAR3_SLOWDOWN_SUFFIX, ACTION_CAR3_SLOWDOWN_MSG)
    if resp.status_code == 200: print("Action creation successful")
    action_two_id = json.loads(str(resp.text))["id"]

    deploy_status = "Actions created... Create rule conditions..."

    # Rule trigger1 for action1
    resp, session = create_trigger(session, 0, act_id_one, "27.37", "28.5", "slowdown_car2")
    if resp.status_code == 200: print("Rule trigger creation successful")
    rule_trigger_one_id = json.loads(str(resp.text))["id"]

    # Rule trigger2 for action2
    resp, session = create_trigger(session, 1, act_id_one, "28.82", "30", "slowdown_car3")
    if resp.status_code == 200: print("Rule trigger creation successful")
    rule_trigger_two_id = json.loads(str(resp.text))["id"]

    deploy_status = "Creating rule definitions..."

    # Rule definition1
    resp, session = create_rule_definition(session, rule_trigger_one_id, action_one_id, "slowdown_car2")
    if resp.status_code == 200: print("Rule definition creation successful")
    rule_definition_one_id = json.loads(str(resp.text))["id"]

    resp, session = enable_rule_definition(session, rule_definition_one_id)

    # Rule definition2
    resp, session = create_rule_definition(session, rule_trigger_two_id, action_two_id, "slowdown_car3")
    if resp.status_code == 200: print("Rule definition creation successful")
    rule_definition_two_id = json.loads(str(resp.text))["id"]
    resp, session = enable_rule_definition(session, rule_definition_two_id)


    deploy_status = "Installing operator scripts..."

    t1 = Thread(target=install_actuator, args=(session, act_id_one))
    t2 = Thread(target=install_actuator, args=(session, act_id_two))
    t3 = Thread(target=install_actuator, args=(session, act_id_three))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    deploy_status = "INSTALLED."


def start_actuators(start_time):
    global deploy_status

    deploy_status = "Start operators at time "
    t1 = Thread(target=start_actuator, args=(session, act_id_one, start_time, "car1.txt"), daemon=True)
    t2 = Thread(target=start_actuator, args=(session, act_id_two, start_time, "car2.txt"), daemon=True)
    t3 = Thread(target=start_actuator, args=(session, act_id_three, start_time, "car3.txt"), daemon=True)

    t1.start()
    time.sleep(2)
    t2.start()
    time.sleep(2)
    t3.start()

    deploy_status = "All Actuators start process initialized."


def get_value_log(amount):
    return [{"name": "CAR_1", "values": get_value_logs(session, act_id_one, amount)[0].json()},
    {"name": "CAR_2", "values": get_value_logs(session, act_id_two, amount)[0].json()},
    {"name": "CAR_3", "values": get_value_logs(session, act_id_three, amount)[0].json()}]


def check_actuator_deployment_status():
    arr = [
        {"iov_object_name": "Car1", "id": act_id_one, "status": get_actuator_state(session, act_id_one)[0].json()["content"]},
        {"iov_object_name": "Car2", "id": act_id_two, "status": get_actuator_state(session, act_id_two)[0].json()["content"]},
        {"iov_object_name": "Car3", "id": act_id_three, "status": get_actuator_state(session, act_id_three)[0].json()["content"]},
    ]


    # READY, DEPLOYED,
    return arr

#deploy_scen_one()
