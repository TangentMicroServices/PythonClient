[![Build Status](https://travis-ci.org/TangentMicroServices/PythonClient.svg?branch=master)](https://travis-ci.org/TangentMicroServices/PythonClient)


# PythonClient
A python client for interacting with the MicroServices

## Installation

	pip install microclient 


## Testing

**run the unit tests**

	nosetests

**Run the integration tests**

	nosetests microclient/integration_ITCase.py

# Clients

## Usage

For detailed examples see the tests 

### Connecting to a service

### Authentication

The process will be the same for any service. Using project service as an example

**Authentication with a token**

	from microservice.clients import ProjectService
	service = ProjectService(token=mytoken)

**Authentication with username and password**

	from microservice.clients import ProjectService

	service = ProjectService()
	response = service.authenticate(username=user, password=pass)
	is_logged_in, token = service.login(response)


# Fetchers

...
