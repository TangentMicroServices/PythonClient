[![Build Status](https://travis-ci.org/TangentMicroServices/PythonClient.svg?branch=master)](https://travis-ci.org/TangentMicroServices/PythonClient)
[![Code Climate](https://codeclimate.com/github/TangentMicroServices/PythonClient/badges/gpa.svg)](https://codeclimate.com/github/TangentMicroServices/PythonClient)


# PythonClient
A python client for interacting with the MicroServices

## Installation

	pip install microclient 


# Developing/Contributing

Target Pythons is: 2.7, 3.4

## Setup

	#clone the repo:
	git@github.com:TangentMicroServices/PythonClient.git

	virtualenv env
	# use virtualenv-3.4 fr python 3


## Testing

**run the unit tests**

	nosetests

**Run the integration tests**

	nosetests microclient/integration_ITCase.py -s

**Run specific test case**

    nosetests microclient/integration_ITCase.py:EntryFetcherTestCase.test_get_entries -s

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
