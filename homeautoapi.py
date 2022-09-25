import json
import os
from flask import Flask, render_template, session, redirect, request, send_from_directory, url_for
import bdsconfig

#Application variables 
app = Flask(__name__, static_url_path='')
app.secret_key = "bdsHomeAuto"
 


@app.route('/device_status')
def device_status():
    req = request.get_json()
    db_status={'LED2':req.get('LED2')}
    print(req)
    
    
    return json.dumps(db_status)

@app.route('/')
@app.route('/index')
def index():
   return  'Where do you think you are going?'

if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="192.168.178.1", port=8080)
    app.run(host="192.168.8.128", port=8080)