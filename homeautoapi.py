import json
import os
from flask import Flask, render_template, session, redirect, request, send_from_directory, url_for
import bdsconfig

#Application variables 
app = Flask(__name__, static_url_path='')
app.secret_key = "kasivoretest"
 


@app.route('/device_status')
def device_status():
    
   
    return json.dump()