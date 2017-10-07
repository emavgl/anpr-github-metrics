import json
from flask import Flask, request, g, url_for
app = Flask(__name__)

@app.route("/hello")
def hello_world():
    """
    Hello World!
    """
    res = {'res': 'ciao'}
    json_res = json.dumps(res)
    return json_res, 200, {'Content-Type': 'application/json'}