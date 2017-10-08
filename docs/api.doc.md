# __APIs__

## Structure
The back-end is composed of just one python file (_api/modules/githubapi.py_).
It contains a GithubApi class, which allows a Flask application to call its method to extract some data and some statistics on the GitHub repositories of Developers Italia (it can be used for different GitHub accounts, though).

## Endpoints
From _api/runapi.py_ it is possible to call 3 endpoints, which return JSON strings as responses:

### GET /stats
It is used to extract some basic organization infos. It returns a JSON structured like the following:

### GET /repositories
It is used to get a list of the repositories of the current organization. After calling it, a JSON file like whe following is returned:

### GET /repositories/<_repository_name_\>
It is used to get all the needed informations about a chosen repository of the chosen organization.
In particular, we obtain statistics about:

- Issues
- Pull requests
- Comments
- First response times
- Issues closing times
- Others...

After calling it, we obtain a JSON like the following: