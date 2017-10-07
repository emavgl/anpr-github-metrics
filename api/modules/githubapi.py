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

	# ISSUES

	def get_issue_info(self, entry):
		"""
		Extract baseline info (infos and pull requests)
		"""
		issue_info = {}
		issue_info['id'] = entry.id
		issue_info['created_at'] = entry.created_at
		issue_info['state'] = entry.state
		issue_info['closed_at'] = entry.closed_at
		issue_info['author'] = entry.user.id
		issue_info['labels'] = [x.name for x in entry.labels]
		
		# get the first response time
		if entry.comments > 0:
			diff_dt = entry.get_comments()[0].created_at - entry.created_at
			issue_info['first_response_time'] = diff_dt.total_seconds()
		else:
			issue_info['first_response_time'] = None

		# get time between close event and creation event
		if issue_info['closed_at']:
			diff_dt = issue_info['closed_at'] - issue_info['created_at']
			issue_info['closed_at_time'] = diff_dt.total_seconds()
		else:
			issue_info['closed_at_time'] = None
		
		return issue_info

	def get_issues_list(self, repo):
		"""
		It returns a list of issues (open and closed)
		"""
		issues_list = []
		for entry in repo.get_issues():
			if not entry.pull_request:
				info = self.get_issue_info(entry)
				issues_list.append(info)

		for entry in repo.get_issues(state="closed"):
			if not entry.pull_request:
				info = self.get_issue_info(entry)
				issues_list.append(info)
				
		return issues_list

	def get_issues(self, repo):
		"""
		It returns a dictionary containing some infos on the issues
		"""
		issues = {}
		issues['entries'] = self.get_issues_list(repo)
		issues['number_total'] = len(issues['entries'])
		issues['number_open'] = len([x for x in issues['entries'] if x['state'] == "open"])
		issues['number_closed'] = issues['number_total'] - issues['number_open']
		issues['first_response_times'] = [x['first_response_time'] for x in issues['entries'] if x['first_response_time'] != None]
		issues['closed_at_times'] = [x['closed_at_time'] for x in issues['entries'] if x['closed_at_time'] != None ]

		if len(issues['first_response_times']) > 0:
			issues['average_first_response_time'] = np.mean(issues['first_response_times'])
		else:
			issues['average_first_response_time'] = None

		if len(issues['closed_at_times']) > 0:
			issues['average_closed_at'] = np.mean(issues['closed_at_times'])
		else:
			issues['average_closed_at'] = None
		
		return issues

			
	# PULL REQUESTS

	def get_pull_requests(self, repo):
		"""
		It returns a list of pull requests
		"""
		pull_requests = []
		for entry in repo.get_issues():
			if entry.pull_request:
				pull_request = self.get_issue_info(entry)
				pull_requests.append(pull_request)
		
		return pull_requests
	
	# REPOS

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
			repo_info['url'] = r.git_url
			repositories.append(repo_info)
			
		return repositories

	def get_repository(self, organization, repository_name):
		"""
		It returns a repository object 
		given the organization and the name
		"""
		return organization.get_repo(repository_name)

	def get_repository_info(self, repository):
		"""
		It returns a dictionary containing some info on the repo
		"""
		repo_info = {}
		
		repo_info['issues'] = self.get_issues(repository)
		repo_info['pull_requests'] = self.get_pull_requests(repository)
		repo_info['name'] = repository.name
		repo_info['created_at'] = repository.created_at
		repo_info['url'] = repository.git_url
		repo_info['description'] = repository.description
		repo_info['tags'] = [x.name for x in repository.get_tags()]
		repo_info['branches'] = [x.name for x in repository.get_branches()]

		# sum all the commits if present
		commit_stat_info = repository.get_stats_commit_activity()
		repo_info['commits'] = None
		if commit_stat_info:			
			repo_info['commits'] = sum([x.total for x in commit_stat_info])
		
		return repo_info