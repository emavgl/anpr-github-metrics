import unittest
import sys
sys.path.insert(0, '..')
import githubapi as ghapi

USERNAME = "hackdevelopers2017@gmail.com"
PASSWORD = "Champagnone1"
ORGANIZATION = "italia"
	
class TestGithubApi(unittest.TestCase):

	def test_organization_name(self):
		g = ghapi.GithubApi(USERNAME, PASSWORD)
		organization = g.get_organization(ORGANIZATION)
		self.assertEqual(organization.name, "Developers Italia")

	def test_number_repositories(self):
		g = ghapi.GithubApi(USERNAME, PASSWORD)
		organization = g.get_organization(ORGANIZATION)
		repositories = g.get_repositories_list(organization)
		self.assertEqual(len(repositories), 119)

	def test_number_issues(self):
		g = ghapi.GithubApi(USERNAME, PASSWORD)
		organization = g.get_organization(ORGANIZATION)
		repository = g.get_repository(organization, "daf")
		issues, pull_requests = g.get_issues_and_pull_requests(organization.login, repository.name)
		self.assertEqual(issues['number_total'], 12)

	def test_first_response_times(self):
		g = ghapi.GithubApi(USERNAME, PASSWORD)
		organization = g.get_organization(ORGANIZATION)
		repository = g.get_repository(organization, "daf")
		issues, pull_requests = g.get_issues_and_pull_requests(organization.login, repository.name)
		comments_list = g.get_comments(ORGANIZATION, repository.name)
		first_response_times = g.get_first_response_times(comments_list, issues['entries'])
		self.assertEqual(len(first_response_times), 3)
		
	def test_closing_times(self):
		g = ghapi.GithubApi(USERNAME, PASSWORD)
		organization = g.get_organization(ORGANIZATION)
		repository = g.get_repository(organization, "daf")
		issues, pull_requests = g.get_issues_and_pull_requests(organization.login, repository.name)
		closing_times = g.get_closing_times(issues['entries'])
		self.assertEqual(len(closing_times), 6)

	def test_closing_rate(self):
		g = ghapi.GithubApi(USERNAME, PASSWORD)
		organization = g.get_organization(ORGANIZATION)
		repository = g.get_repository(organization, "daf")
		issues, pull_requests = g.get_issues_and_pull_requests(organization.login, repository.name)
		closing_rate = g.get_closing_rate(issues['entries'])
		self.assertEqual(closing_rate, 0.5)

	def test_comments_rate(self):
		g = ghapi.GithubApi(USERNAME, PASSWORD)
		organization = g.get_organization(ORGANIZATION)
		repository = g.get_repository(organization, "daf")
		issues, pull_requests = g.get_issues_and_pull_requests(organization.login, repository.name)
		comments_list = g.get_comments(ORGANIZATION, repository.name)
		comments_rate = g.get_comments_rate(comments_list, issues['entries'])
		self.assertEqual(comments_rate, 0.4166666666666667)

if __name__ == '__main__':
    unittest.main()