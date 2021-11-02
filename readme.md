#**Github Repo Polularity Caclulator**

REST API app to fetch repository information from Githib and calculate it's populaity based on forks and stars.


## Table of contents


<p>
  <a href = "#GeneralInfo">General info</a><br>
  <a href = "#technologie">Technologies</a><br>
  <a href = "#endpoint">Endpoints</a><br>
  <a href = "#instruction">Instructions to run</a><br>
  <a href = "#assumption">Assumptions</a><br>
  <a href = "#improvement">Improvements</a><br>
</p>

<a name="GeneralInfo"></a>
## General Information
This application calls Github API server to access data about given Repo.
Based on this data(Forks, Stars) polularity score is then calculate using a simple formula
i.e. 

score = num_stars * 1 + num_forks * 2

The Repository is a popular if it's score is greater then or equal to 500 , otherwise its not a popular repository.
Further to take user input and return the popularity status, API endpoints are exposed.
The exposed APIs are versioned(v1) for future enhancements.


<a name="technologie"></a>
## Technologies
* Runtime environment: Python (Version: 3.9.4)
  * API Framework: FastAPI
  * Authentication: Access Token (Amongst Github App, OAUTH App, Vault authentication token is deemed best fit)
  * Documentation: Swagger
  * Key Libraries: uvicorn, Requests, multiprocessing(To handle timeout)


##Endpoints
<a name="endpoint"></a>
* HTTP Method:GET
  * Endpoint: v1/checkRepo: API endpoint to fetch data(Stars,forks) for given repository from Github and check if its popular or not
  * Endpoint: Root Endpoint: Lists exposed endpoints
  * HTTP Method: HEAD
    * v1/healthCheck: API endpoint to check if the service is up and running end-to-end.


## Instructions to run
<a name="instruction"></a>
* .env file: Contains the access credentials and timeout vars is not included in repo and would be sent to authorized person via email.

####Install Dependencies
```bash
pip install -r requirements.txt
```

#### Run Test Cases
```bash
python OrderDeskTest/test.py
```

#### Run the application server
```bash
python OrderDeskTest/main.py
```

#### Access the swagger documentation
Make sure your application server is running 
```bash
<localhost:port>/docs
```

<a name="assumption"></a>
## Assumptions
* Input String would either be in form owner/repository or https//www.github.com/owner/repository
  * Expected http errors are returned with custom message and for the rest error message from git is passed as it is.

<a name="improvement"></a>
## Improvements
* Encrypted access token 
  * A frontend for users to access the application directly 
  * Added scenarios for customer HTTP error code
  * More test cases and more testing approaches could have been tried