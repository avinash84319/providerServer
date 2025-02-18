from flask import Flask, request, jsonify
import base64
import logging
import requests
from flask_cors import CORS, cross_origin

# environment imports
import dotenv
dotenv.load_dotenv()


# internal imports
import virt
from mngt_server_controllers import heartbeats
from virt_controllers import telemetry,vmcrud

app = Flask(__name__)
CORS(app)

# home route
@app.route('/')
def home():
    return "Welcome to the server"

#heartbeat routes
app.add_url_rule('/heartbeat', 'heartbeat', heartbeats.check_provider_server, methods=['GET'])


#vm routes

##telemetry
app.add_url_rule("/vm/runningvms","listvms",telemetry.list_running_vms,methods=['GET'])
app.add_url_rule("/vm/inactivevms","listingactivevms",telemetry.list_inactive_vms,methods=['GET'])
app.add_url_rule("/vm/getinfo/<name>","getinfo",telemetry.get_vm_info,methods=['GET'])

##creation
app.add_url_rule("/vm/create/<name>/<vcpus>/<memory>","createvm",vmcrud.create_vm,methods=['GET'])
app.add_url_rule("/vm/delete/<name>","deletevm",vmcrud.delete_vm,methods=['GET'])



if __name__ == '__main__':

    # check connection to libvirt daemon
    virt.check_connection()

    # check connection to management server
    # if not heartbeats.check_managment_server(environ.get('MNGT_URL')):
    #     print("Failed to connect to the management server")
    #     exit(1)

    app.run(debug=True)