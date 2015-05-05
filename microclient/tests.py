from django.test import TestCase
from django.conf import settings
from django.forms import ValidationError
from mock import patch
import unittest


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

class ServiceBaseTestCase(TestCase):

	def setUp(self):
		pass 

	def test_init_specifying_all_args(self):

		service = ServiceBase('SomeService', 'token:123')

		assert service.service_name == 'SomeService'
		assert service.token == 'token:123'

	def test_init_with_defaults(self):

		setattr(settings, 'TOKEN', 'settings_token')
		service = ServiceBase('SomeService')

		assert service.token == 'settings_token', \
			'Expect TOKEN to be set from settings.py if not explicitly passed in'

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
			with self.assertRaises(ValidationError) as cm:
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
		

class ProjectServiceTestCase(TestCase):

	def setUp(self):
		self.service = ProjectService()

	def test_project_service_init(self):

		assert self.service.service_name == 'ProjectService', \
			'Expect service_name to be properly setup'

		assert getattr(self.service, 'token', None) is not None, \
			'Expect token to be set'

class HoursServiceTestCase(TestCase):

	def setUp(self):
		self.service = HoursService()

	def test_hours_service_init(self):

		assert self.service.service_name == 'HoursService', \
			'Expect service_name to be properly setup'

		assert getattr(self.service, 'token', None) is not None, \
			'Expect token to be set'

class UserServiceTestCase(TestCase):

	def setUp(self):
		self.service = UserService()

	def test_userservice_init(self):

		assert self.service.service_name == 'UserService', \
			'Expect service_name to be properly setup'

		assert getattr(self.service, 'token', None) is not None, \
			'Expect token to be set'


##
# Fetchers
##
from microclient.fetchers import ProjectFetcher, FetcherBase

class BaseFetcherTestCase(TestCase):

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





class ProjectFetcherTestCase(TestCase):

	def setUp(self):
		pass 

	def test_project_fetcher_init(self):

		fetcher = ProjectFetcher()			
		#assert getattr(fetcher, 'service_api', None) is not None,\
		#			'Expect service_api to be globally defined on the object'


