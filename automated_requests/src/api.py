import json
import threading

import flask
from flask_cors import CORS
from flask import request, Response, abort

from src import scen_deployer
from src.scen_data import scen1_data, scen2_data, scen3_data, scen4_data

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config["DEBUG"] = True

# enable CORS to allow Cross Origin Resourcing Sharing (CORS)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/value-log', methods=['GET'])
def get_value_log():
    if "scenario_name" in request.args:
        scenario_name = request.args['scenario_name']

        scen = scen_deployer.get_scenario_by_name(scenario_name)

        if scen:
            return Response(json.dumps(scen_deployer.get_value_log(1, scenario_name)))
        else:
            abort(400)
    else:
        abort(400)


@app.route('/status', methods=['GET'])
def status():
    if "scenario_name" in request.args:
        scenario_name = request.args['scenario_name']

        scen = scen_deployer.get_scenario_by_name(scenario_name)

        if scen:
            return Response(json.dumps({"status": scen.deploy_status}), 200)
        else:
            abort(400)
    else:
        abort(400)

@app.route('/deploy-status', methods=['GET'])
def deploy_status():
    if "scenario_name" in request.args:
        scenario_name = request.args['scenario_name']

        scen = scen_deployer.get_scenario_by_name(scenario_name)

        if scen:
            return Response(json.dumps(scen_deployer.check_actuator_deployment_status(scenario_name)), 200)
        else:
            abort(400)
    else:
        abort(400)


@app.route('/deploy', methods=['POST'])
def deploy():
    if "scenario_name" in request.args:
        scenario_name = request.args['scenario_name']

        scen = None

        if scenario_name.lower() == "scen1":
            scen = scen1_data.scenario
        elif scenario_name.lower() == "scen2":
            scen = scen2_data.scenario
        elif scenario_name.lower() == "scen3":
            scen = scen3_data.scenario
        elif scenario_name.lower() == "scen4":
            scen = scen4_data.scenario

        if scen:
            t = threading.Thread(target=scen_deployer.deploy_scenario, args=[scen])
            t.start()
            return Response("", 202)
        else:
            abort(400)
    else:
        abort(400)



@app.route('/start', methods=['POST'])
def start():
    if "scenario_name" in request.args and "start_time" in request.args:
        scenario_name = request.args['scenario_name']

        scen = scen_deployer.get_scenario_by_name(scenario_name)

        if scen:
            start_time = request.args['start_time']
            t = threading.Thread(target=scen_deployer.start_actuators, args=[start_time, scenario_name])
            t.start()
            return Response("", 202)
        else:
            abort(400)
    else:
        abort(400)


def run():
    app.run(host="0.0.0.0", debug=False, port=8000)


run()
