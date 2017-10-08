import requests
import json
import datetime
from dateutil import parser
from github import Github
import numpy as np
import time

class GithubApi:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.g = Github(self.username, self.password)

    # ORGANIZATION

    def get_organization(self, organization_name):
        """
        It returns an organization object given the organization name
        """
        return self.g.get_organization(organization_name)

    def get_organization_info(self, organization):
        org_info = {}
        org_info['number_of_collaborators'] = organization.collaborators
        org_info['number_of_followers'] = organization.followers
        org_info['number_of_following'] = organization.following
        org_info['id'] = organization.id
        org_info['email'] = organization.email
        org_info['owner'] = organization.name
        return org_info

    def get_issues(self, organization_name, repository_name):
        issues_list = []
        counter = 1
        base_url = 'https://api.github.com/repos/'
        base_url += organization_name + '/'
        base_url += repository_name + '/issues?'

        while True:
            payload = 'state=all&page=' + str(counter)
            payload += '&client_id=adad1b3c3e2a4e2796dd'
            payload += '&client_secret=9c8391e0f0d014d30dc629fa0e1af681493ab28b'
            req_url = base_url + payload
            json_res = requests.get(req_url).json()
            issues_list += json_res
            counter += 1
            if len(json_res) == 0:
                break
        
        return issues_list

    def get_comments(self, organization_name, repository_name):
        base_url = 'https://api.github.com/repos/'
        base_url += organization_name + '/'
        base_url += repository_name + '/issues/comments?'
        comments_list = []
        counter = 1
        while True:
            payload = 'page=' + str(counter)
            payload += '&client_id=adad1b3c3e2a4e2796dd'
            payload += '&client_secret=9c8391e0f0d014d30dc629fa0e1af681493ab28b'
            req_url = base_url + payload
            json_res = requests.get(req_url).json()
            comments_list += json_res
            counter += 1
            if len(json_res) == 0:
                break
        return comments_list

    def get_issue(self, issues_list, issue_url):
        """
        Return a list with the issue
        or empty list if issues_list does not contain the issue
        with the matching issue_url
        """
        return [ x for x in issues_list if x['url'] == issue_url]

    def get_closing_times(self, issues_list):
        closing_times = []
        for issue in issues_list:
            status = issue['state']
            if status == 'closed':
                created_at = parser.parse(issue['created_at'])
                closed_at = parser.parse(issue['closed_at'])
                delta_t = (closed_at - created_at).total_seconds()
                closing_times.append(delta_t)
        return closing_times

    def get_closing_rate(self, issues_list):
        if len(issues_list) == 0:
            return 0
        closed_issue = [x for x in issues_list if x['state'] == 'closed']
        return len(closed_issue) / len(issues_list)

    def get_comments_rate(self, comments_list, issues_list):
        if len(issues_list) == 0:
            return 0
        return len(comments_list) / len(issues_list)

    def get_first_response_times(self, comments_list, issues_list):

        # organize comments by issues
        comments_by_issues = {}
        for comment in comments_list:
            issue_url = comment['issue_url']
            if issue_url in comments_by_issues:
                comments_by_issues[issue_url].append(comment)
            else:
                comments_by_issues[issue_url] = []
                comments_by_issues[issue_url].append(comment)

        first_response_times = []
        for issue_url, comments in comments_by_issues.items():
            if len(comments) > 0:
                issue_result = self.get_issue(issues_list, issue_url)
                if len(issue_result) > 0:
                    issue = issue_result[0]
                    first = parser.parse(issue['created_at'])
                    second = parser.parse(comments[0]['created_at'])
                    delta_t = (second - first).total_seconds()
                    first_response_times.append(delta_t)
        
        return first_response_times

    def create_issues_info(self, organization_name, repository_name, issues_list):
        """
        It returns a dictionary containing some infos on the issues
        """
        issues = {}
        issues['entries'] = issues_list
        issues['number_total'] = len(issues['entries'])
        issues['number_open'] = len([x for x in issues['entries'] if x['state'] == "open"])
        issues['number_closed'] = issues['number_total'] - issues['number_open']

        issues['comments'] = self.get_comments(organization_name, repository_name)
        issues['first_response_times'] = self.get_first_response_times(issues['comments'], issues_list)
        issues['closing_times'] = self.get_closing_times(issues_list)

        issues['average_first_response_time'] = None
        if len(issues['first_response_times']) > 0:
            issues['average_first_response_time'] = sum(issues['first_response_times']) / len(issues['first_response_times'])
        
        issues['average_closing_time'] = None
        if len(issues['closing_times']) > 0:
            issues['average_closing_time'] = sum(issues['closing_times']) / len(issues['closing_times'])

        issues['closing_rate'] = self.get_closing_rate(issues_list)
        issues['comments_rate'] = self.get_comments_rate(issues['comments'], issues_list)

        return issues

    def get_issues_and_pull_requests(self, organization_name, repository_name):
        """
        Returns dictionaries of issues and pull requests
        which contain a list of issues (or pull-requests)
        and other metrics
        """
        # temp lists
        issues_list = []
        pull_requests_list = []

        # get both issues and pull requests (open and closed)
        issues_and_pr = self.get_issues(organization_name, repository_name)
        issues_list = [x for x in issues_and_pr if 'pull_request' not in x]
        pull_requests_list = [x for x in issues_and_pr if 'pull_request' in x]
        
        # create an dictinary issues with list of issues and extra-info
        issues = self.create_issues_info(organization_name, repository_name, issues_list)

        # create a dictinary pull_requests with list of issues and extra-info
        pull_requests = self.create_issues_info(organization_name, repository_name, pull_requests_list)

        return  issues, pull_requests

    def get_repositories_list(self, organization):
        """
        It gets a list of repositories infos
        """
        repositories = []
        
        for r in organization.get_repos():
            repo_info = {}
            repo_info['id'] = r.id
            repo_info['name'] = r.name
            repo_info['description'] = r.description
            repo_info['organization_name'] = organization.name
            repo_info['url'] = r.git_url
            repositories.append(repo_info)
            
        return repositories

    def get_repository(self, organization, repository_name):
        """
        It returns a repository object 
        given the organization and the name
        """
        return organization.get_repo(repository_name)

    def get_repository_info(self, organization, repository):
        """
        It returns a dictionary containing some info on the repo
        """
        repo_info = {}
        
        repo_info['issues'], repo_info['pull_requests'] = self.get_issues_and_pull_requests(organization.login, repository.name)
        repo_info['name'] = repository.name
        repo_info['owner'] = organization.name
        repo_info['created_at'] = repository.created_at
        repo_info['url'] = repository.git_url
        repo_info['description'] = repository.description
        repo_info['tags'] = [x.name for x in repository.get_tags()]
        repo_info['branches'] = [x.name for x in repository.get_branches()]
        repo_info['number_of_issues'] = len(repo_info['issues'])
        repo_info['number_of_pull_requests'] = len(repo_info['pull_requests'])
        repo_info['number_of_branches'] = len(repo_info['branches'])

        # sum all the commits if present
        commit_stat_info = repository.get_stats_commit_activity()
        repo_info['commits'] = None
        if commit_stat_info:			
            repo_info['commits'] = sum([x.total for x in commit_stat_info])
        
        return repo_info
