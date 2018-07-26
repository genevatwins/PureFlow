from flask import Flask, render_template
from flask import request

import os
import ast
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/provisioning')
def provisioning():
    return render_template('provisioning.html')

@app.route('/provisioning/openvswitch')
def openvswitch():
    return render_template('openvswitch.html')

@app.route('/provisioning/mikrotik')
def mikrotik():
    return render_template('mikrotik.html')

@app.route('/provisioning/api', methods = ['POST'])
def openvswitch_api():
    raw = request.form.to_dict(flat=True)
    data = {k.encode('utf8'): v.encode('utf8') for k, v in raw.items()}

    if data["device-type"] == "openvswitch":
        os.system('ansible-playbook -u %s -i %s, /opt/PureFlow/ansible/playbook/openvswitch.yaml --extra-vars "controller=%s bridge=%s"'%(data["username"],data["device-ip"],data["controller"],data["bridge"]))
        return "success!"
    
    if data["device-type"] == "mikrotik":
        os.system('ansible-playbook -i %s, /opt/PureFlow/ansible/playbook/mikrotik.yaml --extra-vars "user=%s ansible_paramiko_pass=%s port=%s controller=%s bridge=%s"'%(data["device-ip"],data["username"],data["password"],data["port"],data["controller"],data["bridge"]))
        return "success!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)

