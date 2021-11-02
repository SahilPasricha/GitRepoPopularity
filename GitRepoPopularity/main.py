import multiprocessing
import re
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
import uvicorn
import requests
from decouple import config
from ErrorCodes import ErrorCode
from ValidateGitRepo import parseGitRepoStr

api_token : str = config('api_token')
timeout : float = float(config('timeout'))
API_GITHUB_URL = "https://api.github.com"
SEARCH_ENDPOINT = "/search/repositories"
DEFAULT_REPO = "CSSEGISandData/COVID-19"
headers = {'Authorization': 'token %s' % api_token,
           'Accept': 'application/vnd.github.v3+json'}
#All characters must be either a hyphen (-) or alphanumeric
regex_repo_owner = re.compile("^[\w\.@\:/\-]+$")
#All characters must be either a hyphen (-), a period (.), or alphanumeric
regex_repo_name = re.compile("^[a-zA-Z0-9.-]*$")
repo_score = 0
ret_status_code, ret_message = None,None
req_resp = {}
app = FastAPI()

def github_api_call(params,github_api = API_GITHUB_URL+SEARCH_ENDPOINT, headers  = headers):
    global req_resp
    req_resp = requests.get(github_api, headers=headers, params=params)

def call_search_repo_api_with_timeout(params,timeout = timeout, headers = headers):
    """Spawn process to make the git api call and kill the thread after timeout."""
    p = multiprocessing.Process(target=github_api_call(params, API_GITHUB_URL+SEARCH_ENDPOINT, headers, ))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.kill()
        raise HTTPException(status_code=408, detail="Request Timeout.")

@app.get("/v1/checkRepo")
async def check_repo(repo_url: str = Header(DEFAULT_REPO)):
    """API endpoint to fetch data(Stars,forks) for given repository from Github."""
    #Check if git repo name provided is valid
    str_url = parseGitRepoStr(repo_url)
    params = {'q': 'repo:' + str_url,
              'per_page': 1}
    #Call the git search api endpoint with timeout of the environment
    call_search_repo_api_with_timeout(params, headers)
    ret_str_json = req_resp.json()
    if req_resp.status_code != 200:
        ErrorCode(req_resp.status_code,ret_str_json)
    else:
        num_forks = ret_str_json['items'][0]['forks']
        num_stars = ret_str_json['items'][0]['stargazers_count']
        score = num_stars * 1 + num_forks * 2
        ret_status_code = 200
        if score >= 500:
            ret_message = "Repository is popular."
        else:
            ret_message = "Repository is not popular."

    return JSONResponse(
        status_code = ret_status_code,
        content= {"Response" : ret_message}
    )

@app.head("/v1/healthCheck")
async def validate_service():
    """API endpoint to check if the service is up and running end-to-end."""
    params = {'q': 'repo:' + DEFAULT_REPO,
              'per_page': 1}
    call_search_repo_api_with_timeout(params, headers)
    return JSONResponse(
        status_code = req_resp.status_code
    )

@app.get("/")
async def root_endpoint():
    """Lists exposed endpoints """
    return JSONResponse(
        status_code=200,
        content={"Publicly Available APIs" : "/v1/healthCheck, /v1/checkRepo.",
                 "Documentation" : "/docs"
                }
    )

if __name__ == '__main__':
    uvicorn.run(app , host='0.0.0.0', port=8000)