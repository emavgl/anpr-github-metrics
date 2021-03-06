import json, datetime
from flask import Flask, request, g, url_for
from flask.ext.cache import Cache
from modules.githubapi import GithubApi
app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

def make_cache_key(*args, **kwargs):
    print(request.full_path)
    return request.full_path 

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type " + str(type(x)))

USERNAME = "hackdevelopers2017@gmail.com"
PASSWORD = "Champagnone1"
ORGANIZATION = "italia"

ghapi = GithubApi(USERNAME, PASSWORD)
organization = ghapi.get_organization(ORGANIZATION)

@app.route("/stats")
@cache.memoize(120)
def get_organization_info():
    """
    Get basic organization info
    """
    res = {'organization_info': ghapi.get_organization_info(organization)}
    json_res = json.dumps(res)
    return json_res, 200, {'Content-Type': 'application/json'}

@app.route("/repositories")
@cache.memoize(120)
def get_repositories():
    """
    Get list of repositories
    """
    repositories = ghapi.get_repositories_list(organization)
    res = {'repositories': repositories}
    json_res = json.dumps(res, default=datetime_handler)
    return json_res, 200, {'Content-Type': 'application/json'}

@app.route("/repositories/<repository_name>")
@cache.cached(timeout=3600, key_prefix=make_cache_key)
def get_repository_info(repository_name):
    """
    Get repository info
    """
    repository = ghapi.get_repository(organization, repository_name)
    repo_info = ghapi.get_repository_info(organization, repository)
    res = {'repository': repo_info}
    json_res = json.dumps(res, default=datetime_handler)
    return json_res, 200, {'Content-Type': 'application/json'}