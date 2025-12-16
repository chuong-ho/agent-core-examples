## How to run the demos

Prerequisite:
- Create a virtual environment for python by executing:    `python3 -m venv ./.venv`
- Activate virtual environment:  `source ./.venv/bin.activate`
- Install requirements:      `pip install -r requirements.txt`
- Install jupyter kernel:  `pip install jupyter ipykernel`
- then run jupyter cells block by block

IAM authentication has to be in an .env file or in environmental variables



### Root
erxample of agent on ec2 using python and fast mcp

### 10-strands-agent-on-agentcore
Example of simple strands agent on agentcore. Shows how much easier it is to write agent logic

### 20-agentcore-identity
Example of using IAM permissions to verify agent. 
To Do: Octa integration. I have an okta example working, but obviouysly requires okta server and identity provider set up. Will try to include Okta terraform code in the future

### 30-Agentcore-Gateway
Agent running on agentcore gateway. Shows how we can enable agents to be built once, and used many times. Has identity built in. 
To Do: write example to host mcp on agentcore gateway

