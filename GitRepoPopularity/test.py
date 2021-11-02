
import unittest
import ValidateGitRepo
from fastapi.responses import JSONResponse
from main import github_api_call, call_search_repo_api_with_timeout, validate_service
import sys
import unittest

fill_url = "https://github.com/CSSEGISandData/COVID-19"
time_out = 0.5

class TestClass(unittest.TestCase):


    def test_validate_plain_string(self):
        erroneous_url = "CSSEGISandData/COVID-19"
        try:
            ValidateGitRepo.parseGitRepoStr(erroneous_url)
        except:
            self.assertEqual(True,False,"Error: Failed to parse input username/repository string")


    def test_validate_full_url(self):
        try:
            ValidateGitRepo.parseGitRepoStr(fill_url)
        except:
            self.assertEqual(True,False,"Error: Failed to parse URL")

    def test_validate_erroneous_full_url(self):
        erroneous_url = "https://git.com/CSSEGISandData/sdfjhaJSHJHGDJG"
        try:
            ValidateGitRepo.parseGitRepoStr(erroneous_url)
            self.assertEqual(True,False,"Error: erroneous url should not be parsed")
        except:
            pass


    def test_time_out(self):
        fill_url = "j"
        params = {'q': 'repo:' + fill_url,
                               'per_page': 100}
        time_out_code = 408
        return_code = None
        try:
            call_search_repo_api_with_timeout(params)
        except():
            return_code = sys.exc_info()[1].status_code
            self.assertEqual(return_code,time_out_code,"Error: Request Timeout")


if __name__ == '__main__':
    unittest.main()
