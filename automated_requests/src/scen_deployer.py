import time
from threading import Thread, Lock
from typing import Optional

from src.mbpreq.actuator_control import install_actuator, start_actuator, get_value_logs, get_actuator_state
from src.mbpreq.domain import Scenario
from src.mbpreq.generic_mbp_operations import *
from src.mbpreq.op_control import create_operator_scen_one
from src.mbpreq.rules import create_trigger, create_action, create_rule_definition, enable_rule_definition

deploy_status = "UNDEPLOYED"
session = None
access_lock = Lock()

scenarios = []

def deploy_scenario(scenario: Scenario):


    global scenarios, session
    if not session:
        session = login()[1]

    if (scenario not in scenarios):
        scenarios.append(scenario)

    resp, session = login()
    if resp.status_code == 200: print("Login successful")

    scenario.deploy_status = "Logged in"

    # Adapt settings
    #  resp, session = adapt_broker_settings(session, broker_ip="172.16.238.3")
    #  if resp.status_code == 200: print("Settings adaptions successful")

    # deploy_status = "Settings adapted"

    # Create device
    resp, session = create_device(session, ip_address="172.16.238.10")
    if resp.status_code == 200: print("Device creation successful")
    device_id = json.loads(str(resp.text))["id"]

    scenario.deploy_status = "Device created"

    # Create data model
    resp, session = create_data_model(session)
    if resp.status_code == 200: print("Data model creation successful")
    data_model_id = json.loads(str(resp.text))["id"]

    scenario.deploy_status = "Data model created"

    # Create operator
    resp, session = create_operator_scen_one(session, data_model_id, scenario.operator)
    if resp.status_code == 200: print("Operator creation successful")
    operator_id = json.loads(str(resp.text))["id"]
    print(resp.status_code, resp.text, resp.content)

    scenario.deploy_status = "Operator created"

    # Create actuators
    for act in scenario.actuators:
        resp, session = create_actuator(session, act.name, operatorId=operator_id, deviceId=device_id)
        print(data_model_id)
        if resp.status_code == 200: print("Actuator creation successful")
        act.id = json.loads(str(resp.text))["id"]
        print(resp.status_code, resp.text, resp.content)

    scenario.deploy_status = "Actuators created... Create rules..."

    # Create rules
    for rule in scenario.rules:
        # Action
        resp, session = create_action(session, rule.action.actuator.id, rule.action.suffix, rule.action.msg)
        if resp.status_code == 200: print("Action creation successful")
        rule.action.id = json.loads(str(resp.text))["id"]

        # Rule trigger
        resp, session = create_trigger(session, rule.trigger.event_count, rule.trigger.actuator.id, rule.trigger.time_start, rule.trigger.time_end, rule.trigger.name)
        if resp.status_code == 200: print("Rule trigger creation successful")
        rule.trigger.id = json.loads(str(resp.text))["id"]

        # Rule definition
        resp, session = create_rule_definition(session, rule.trigger.id, rule.action.id, rule.name)
        if resp.status_code == 200: print("Rule definition creation successful")
        rule.id = json.loads(str(resp.text))["id"]

        # Enable rule
        resp, session = enable_rule_definition(session, rule.id)

    scenario.deploy_status = "Installing operator scripts..."

    installing_threads = []
    for act in scenario.actuators:
        installing_threads.append(Thread(target=install_actuator, args=(session, act.id)))
    for thread in installing_threads:
        thread.start()
    for thread in installing_threads:
        thread.join()

    scenario.deploy_status = "INSTALLED."


def start_actuators(start_time, scen_name: str):
    global scenarios, session
    if not session:
        session = login()[1]

    scen = get_scenario_by_name(scen_name)

    if not scen:
        return

    scen.deploy_status = "Start operators at time "
    starting_threads = []
    for act in scen.actuators:
        starting_threads.append(Thread(target=start_actuator, args=(session, act.id, start_time, act.file_name), daemon=True))
    for thread in starting_threads:
        time.sleep(2)
        thread.start()

    scen.deploy_status = "All Actuators start process initialized."

def get_scenario_by_name(name: str) -> Optional[Scenario]:
    scen = None
    for scenario in scenarios:
        if scenario.name == name:
            scen = scenario
    return scen


def get_value_log(amount, scen_name: str):
    scen = get_scenario_by_name(scen_name)

    if not scen:
        return []

    value_log_list = []

    for act in scen.actuators:
        value_log_list.append({"name": act.name, "values": get_value_logs(session, act.id, amount)[0].json()})

    return value_log_list

def check_actuator_deployment_status(scen_name: str):
    scen = get_scenario_by_name(scen_name)
    if not scen:
        return []

    deplyoment_status_list = []

    for act in scen.actuators:
        deplyoment_status_list.append({"iov_object_name": act.name, "id": act.id, "status": get_actuator_state(session, act.id)[0].json()["content"]})

    return deplyoment_status_list

#deploy_scen_one()
