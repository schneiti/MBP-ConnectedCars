import json

import requests
from requests.structures import CaseInsensitiveDict

def create_operator_scen_one(session: requests.Session, data_model_id: str, operator_data):
    url = "http://host.docker.internal:8080/mbp/api/operators"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json;charset=UTF-8"
    headers["X-MBP-Access-Request"]= "requesting-entity-firstname=admin;;requesting-entity-lastname=admin;;requesting-entity-username=admin]"

    operator_data["dataModelId"] = str(data_model_id)

    resp = session.post(url, data=json.dumps(operator_data), headers=headers)
    return resp, session