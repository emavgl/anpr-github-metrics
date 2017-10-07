import json, datetime
from flask import Flask, request, g, url_for
from modules.githubapi import GithubApi
app = Flask(__name__)

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type " + str(type(x)))

USERNAME = "hackdevelopers2017@gmail.com"
PASSWORD = "Champagnone1"
ORGANIZATION = "italia"

ghapi = GithubApi(USERNAME, PASSWORD)
organization = ghapi.get_organization(ORGANIZATION)

@app.route("/hello")
def hello_world():
    """
    Hello World!
    """
    res = {'res': 'ciao'}
    json_res = json.dumps(res)
    return json_res, 200, {'Content-Type': 'application/json'}

@app.route("/repositories")
def get_repositories():
    """
    Hello World!
    """
    repositories = ghapi.get_repositories_list(organization)
    res = {'repositories': repositories}
    json_res = json.dumps(res, default=datetime_handler)
    return json_res, 200, {'Content-Type': 'application/json'}

@app.route("/repositories/<repository_name>")
def get_repository_info(repository_name):
    """
    Hello World!
    """
    repository = ghapi.get_repository(organization, repository_name)
    repo_info = ghapi.get_repository_info(repository)
    res = {'respository': repo_info}
    json_res = json.dumps(res, default=datetime_handler)
    return json_res, 200, {'Content-Type': 'application/json'}