# star-blazer-count
Application to get star count history for a Github Public Repo as CSV file.

### Prerequisites

Install [Docker](https://docs.docker.com/get-docker/).

Install [Curl](https://curl.se/dlwiz/?type=bin).

Please provide a github access token with read/write packages and repo.

To do this go to the:

`Github -> Settings -> Developer settings -> Personal access tokens -> Generate new token`


Save this token in your system in `GITHUB_ACCESS_TOKEN` variable


    export GITHUB_ACCESS_TOKEN=your_token
    
Info -> Without the Github access token, the application can only make fixed number of API calls in an hour .
Read more about [this](https://docs.github.com/en/developers/apps/rate-limits-for-github-apps). 


### Running the Application
	
Start Docker App and run the following commands :

	docker image build -t stargazer .
	docker run -v ${PWD}:/app -p 9300:9300 -d stargazer -.env GITHUB_ACCESS_TOKEN=your_token

*** PWD is the current working directory.

Use Curl to get the data as `output.csv` in the current directory.
    
    curl -H "Content-Type: application/json" \
           -X GET \
           -d '{"githubOwnerName":"REPO_OWNER_NAME","githubProjectName":"PROJECT_NAME"}' \
           http://0.0.0.0:9300/getStarCountData
           
The output will be the `output.csv` file in the current working directory.

### Usage

Example : Run -> 

    curl -H "Content-Type: application/json" \
           -X GET \
           -d '{"githubOwnerName":"github","githubProjectName":"platform-samples"}' \
           http://0.0.0.0:9300/getStarCountData
           
This will produce output.csv file in current working directory. 

#### The process of writing this application lies in [here](https://github.com/deppmish2/star-blazer-count/blob/main/PROCESS.md)
