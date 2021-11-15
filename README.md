# Quickstart

## Pre-requistive

Creating Virtual Environment
```
$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirments.txt
```
## Run Server/hosting service - Using Docker 

```
# Build the docker container
$ docker build -t flask-app:latest .

# Run the docker container
$ docker run -d -p 5000:5000 flask-app

```

## Run Server/hosting service - Directly

```
# Hosting Service
$ python3 app/autoapp.py
```

## Run Clients

Run these in different terminal/bash window.

```
# Client - 1  Endpoint '/policy/<int>policy_id'
$ python3 test.py

# Client - 2  Endpoint '/checkpolicy'
$ python3 test2.py
```

# Information

## Flask App functionalities/method

### Methods:

*Endpoint /policy/<int>policy_id*

- GET     - get the existing policy (if stored in database).
- PUT     - put a new policy to the database.
- PATCH   - update the existing policy or attributes of the policy.
- DELETE  - delete the policy (if exists in database).
- POST    - validate the current policy - either ACCEPT or REJECT. 
    
*Endpoint /checkpolicy*

- POST    - validate the policy given as a input.
    

## Status Codes

- 200 OK *The request action was sucessful*
- 201 Created *A new resoure was created*
- 204 No Content *The request was sucessful, but response has no content*
- 400 Bad Request *The request was malformed*
- 404 Not Found *The requested resource was not found*
- 409 Conflict *Conflict between the current state and target state*
- 415 Unsupported Media Type *The request data format is not supported by the app*
- 500 Internal Server Error *Server threw error while processing the request*
