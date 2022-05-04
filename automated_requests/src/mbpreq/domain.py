from typing import List

class Actuator():

    def __init__(self, name: str, file_name: str) -> None:
        self.name = name
        self.id = ""
        self.file_name = file_name


class RuleAction():

    def __init__(self, actuator: Actuator,  suffix: str, msg: str) -> None:
        self.suffix = suffix
        self.id = ""
        self.msg = msg
        self.actuator = actuator

class RuleTrigger():

    def __init__(self,actuator: Actuator, name: str, time_start: str, time_end: str,  event_count: int) -> None:
        self.name = name
        self.actuator = actuator
        self.time_start = time_start
        self.time_end = time_end
        self.event_count = event_count
        self.id = ""


class RuleDefinition():
    def __init__(self, name: str, trigger: RuleTrigger, action: RuleAction) -> None:
        self.name = name
        self.id = ""
        self.trigger = trigger
        self.action = action


class Scenario():

    def __init__(self, name, operator, actuators: List[Actuator], rules: List[RuleDefinition]) -> None:
        self.name = name
        self.operator = operator
        self.actuators = actuators
        self.rules = rules
        self.id = ""
        self.deploy_status = "UNDEPLOYED"