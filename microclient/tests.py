from mock import patch
import unittest, responses

##
# Clients
##
from microclient.clients import ProjectService, HoursService, UserService, ServiceBase

mock_service_definitions = {
	
	"FooService": {
		"base": "..", 
		"resources": {
			"someresource" : {
				"endpoint": "/someresource/",
				"required_params": ['foo', 'bar'],
				"optional_params": ['baz'],
			}, 
			"someotherresource": {}
		}
	},	
}

class ServiceBaseTestCase(unittest.TestCase):

	def setUp(self):
		pass 

	def test_init_specifying_all_args(self):

		service = ServiceBase('SomeService', 'token:123', tld='example.com', protocol='https')

		assert service.service_name == 'SomeService'
		assert service.token == 'token:123'
		assert service.tld == 'example.com'
		assert service.protocol == 'https'

	def test__get_base_url(self):

		service = ServiceBase('SomeService', 'token:123', tld='example.com')
		url = service._get_base_url()

		assert url == 'http://someservice.example.com/api/v1'

	def test__get_url(self):
		
		service = ServiceBase('SomeService', 'token:123', tld='example.com')
		url = service._get_url('/path/to/somewhere/')

		assert url == 'http://someservice.example.com/api/v1/path/to/somewhere/'

	def test_login(self):

		class MockResponse:
			status_code = 200
			def json(self):
				return {
					"token": "123"
				}

		service = ServiceBase('SomeService', tld='example.com')
		response = service.login(MockResponse())

		assert response == True, 'Expect response to be true'
		assert service.token == "123"

	def test_login_failure(self):

		class MockResponse:
			status_code = 405
			def json(self):
				return {
					"token": "123"
				}

		service = ServiceBase('SomeService', tld='example.com')
		response = service.login(MockResponse())

		assert service.token == None, 'Clear the token if login fails'
		assert response == False, 'Not logged in'

	
	@unittest.skip("Not yet in use, can't work out how to magically pass the resource in")
	def test_init_creates_fluent_methods(self):

		with patch.dict("microclient.clients.service_definitions", mock_service_definitions):
			service = ServiceBase('FooService', 'token:123')

			assert getattr(service, 'list_someresource', None) is not None
			assert getattr(service, 'get_someresource', None) is not None
			assert getattr(service, 'create_someresource', None) is not None
			assert getattr(service, 'update_someresource', None) is not None
			assert getattr(service, 'delete_someresource', None) is not None
			

	@patch.object(ServiceBase, 'call')
	def test_list(self, mock_call):

		service = ServiceBase('ProjectService', 'token:123')
		service.list("project")

		mock_call.assert_called_with('/projects/')

	@patch.object(ServiceBase, 'call')
	def test_get(self, mock_call):

		service = ServiceBase('ProjectService', 'token:123')
		service.get("project", 1)

		mock_call.assert_called_with('/projects/1/')

	@patch.object(ServiceBase, 'call')
	def test_create(self, mock_call):

		mock_data = {"foo": "1", "bar": 2}

		with patch.dict("microclient.clients.service_definitions", mock_service_definitions):
			service = ServiceBase('FooService', 'token:123')
			service.create("someresource", mock_data)

		mock_call.assert_called_with('/someresource/', mock_data, 'post')

	@patch.object(ServiceBase, 'call')
	def test_create_will_raise_error_if_required_params_are_missing(self, mock_call):

		mock_data = {"foo": "1"}

		with patch.dict("microclient.clients.service_definitions", mock_service_definitions):
			service = ServiceBase('FooService', 'token:123')
			with self.assertRaises(ValueError) as cm:
				service.create("someresource", mock_data)

	@patch.object(ServiceBase, 'call')
	def test_update(self, mock_call):

		mock_data = {"foo": "1", "bar": 2}

		with patch.dict("microclient.clients.service_definitions", mock_service_definitions):
			service = ServiceBase('FooService', 'token:123')
			service.update("someresource", 1, mock_data)

		mock_call.assert_called_with('/someresource/1/', mock_data, 'patch')

	@patch.object(ServiceBase, 'call')
	def test_delete(self, mock_call):
		
		with patch.dict("microclient.clients.service_definitions", mock_service_definitions):
			service = ServiceBase('FooService', 'token:123')
			service.delete("someresource", 1)

		mock_call.assert_called_with('/someresource/1/', 'delete')
		

class ProjectServiceTestCase(unittest.TestCase):

	def setUp(self):
		self.service = ProjectService()

	def test_project_service_init(self):

		assert self.service.service_name == 'ProjectService', \
			'Expect service_name to be properly setup'

		
class HoursServiceTestCase(unittest.TestCase):

	def setUp(self):
		self.service = HoursService()

	def test_hours_service_init(self):

		assert self.service.service_name == 'HoursService', \
			'Expect service_name to be properly setup'

		
class UserServiceTestCase(unittest.TestCase):

	def setUp(self):
		self.service = UserService(tld="example.com")

	def test_userservice_init(self):

		assert self.service.service_name == 'UserService', \
			'Expect service_name to be properly setup'

	@responses.activate
	def test_userservice_authenticate(self):

		expected_url = "http://userservice.example.com/api-token-auth/"

		responses.add(responses.POST, expected_url,
                  body='{"token": "123"}', status=200,
                  content_type='application/json')

		response = self.service.authenticate(username="test", password="test")

		assert response.status_code == 200

##
# Fetchers
##
from microclient.fetchers import ProjectFetcher, FetcherBase

class BaseFetcherTestCase(unittest.TestCase):

	def setUp(self):
		self.fetcher = FetcherBase()

	def test_create_index(self):

		test_data = [
			{"id": 1, "text": "a"},
			{"id": 2, "text": "b"},
			{"id": 2, "text": "b"},
			{"id": 3, "text": "c"},
		]

		print self.fetcher.create_index(test_data, "id")





class ProjectFetcherTestCase(unittest.TestCase):

	def setUp(self):
		pass 

	def test_project_fetcher_init(self):

		fetcher = ProjectFetcher()			
		#assert getattr(fetcher, 'service_api', None) is not None,\
		#			'Expect service_api to be globally defined on the object'


