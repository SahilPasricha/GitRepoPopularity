from giturlparse import parse, validate
from fastapi import HTTPException

def parseGitRepoStr(git_repo_str):
    if not git_repo_str:
        raise HTTPException(status_code=400, detail="Please provide a valid repository name.")
    # Check if its a complete URL
    repo_host, repo_owner, repo_name = None, None, None
    url_parsed = parse(git_repo_str)
    if  url_parsed.valid:
        repo_host, repo_owner, repo_name = url_parsed.host, url_parsed.owner, url_parsed.repo
        if repo_host != "github.com":
            raise HTTPException(status_code=400, detail="Please provide a valid repository name.")

    elif len(git_repo_str.split('/')) == 2:
        repo_owner = git_repo_str.split('/')[0]
        repo_name = git_repo_str.split('/')[1]
        if ".git" in repo_name:
            repo_name.replace('.git','')
        if len(repo_name) > 100 or len(repo_owner) > 30:
            raise HTTPException(status_code=400, detail="Please provide a valid repository name.")
    else:
        raise HTTPException(status_code=400, detail="Please provide unique identifier for repo name. "
                                                    "Either owner name or repo name is missing.")
    return repo_owner + "/" + repo_name