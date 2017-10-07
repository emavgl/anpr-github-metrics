import unittest
import sys
sys.path.insert(0, '..')
import githubapi as ghapi

USERNAME = "hackdevelopers2017@gmail.com"
PASSWORD = "Champagnone1"
ORGANIZATION = "italia"
	
class TestGithubApi(unittest.TestCase):

	def test_number_issues(self):
		g = ghapi.GithubApi(USERNAME, PASSWORD)
		organization = g.get_organization(ORGANIZATION)
		repository = g.get_repository(organization, "anpr")
		issues = g.get_issues(repository)
		self.assertEqual(issues['number_total'], 346)


if __name__ == '__main__':
    unittest.main()