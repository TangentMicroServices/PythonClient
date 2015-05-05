from microclient.fetchers import ProjectFetcher, EntryFetcher
from microclient.clients import ProjectService, UserService, HoursService
import json, unittest, uuid

testing_tld = "staging.tangentmicroservices.com"
testing_admin_username = "admin"
testing_admin_password = "tangentsolutions"


def do_crud(service, resource, data):
	# create:
	response = service.create(resource, data)
	resource_id = response.json().get("id", None)
	if resource_id is None:
		resource_id = response.json().get("pk", None)

	assert response.status_code == 201, '{0} Expect 201 created' . format (resource)

	# get		
	response = service.get(resource, resource_id)
	assert response.status_code == 200, '{0} Expect 200 OK' . format (resource)

	# delete:
	response = service.delete(resource, resource_id)		
	assert response.status_code == 204, '{0} Expect 204 DELETED' . format (resource)

	response = service.get(resource, resource_id)
	assert response.status_code == 404, '{0} Expect 404 not found - item deleted' . format (resource)


class ProjectServiceTestCase(unittest.TestCase):

	def setUp(self):
		self.service = ProjectService(tld=testing_tld)
		
		response = self.service.authenticate(username=testing_admin_username, password=testing_admin_password)
		self.service.login(response)

		self.user_service = UserService(tld=testing_tld)
		response = self.user_service.authenticate(username=testing_admin_username, password=testing_admin_password)
		self.user_service.login(response)

		# create a project:
		project_data = {
			"title": "Test project",
			"description": "lorum ipsum",
			"start_date": "2015-04-24",
		}
		self.project = self.service.create("project", project_data)		
		self.project_id = self.project.json().get("pk")

		# create a 
		user_data = {
			"username": str(uuid.uuid4()).split("-")[0],
			"first_name": "joe",
			"last_name": "soap",
		}
		self.user = self.user_service.create("user", user_data)
		self.user_id = self.user.json().get("id")


	def tearDown(self):

		self.service.delete("project", self.project_id)
		self.user_service.delete("user", self.user_id)

	def test_get_projects(self):

		projects = self.service.get_projects()		
		assert projects.status_code == 200, 'Expect 200 OK'

	def test_crud_project(self):
		"""
		TODO: refactor into do_crud
		"""

		project_data = {
			"title": "Test project",
			"description": "lorum ipsum",
			"start_date": "2015-04-24",
		}

		do_crud(self.service, "project", project_data)

	def test_crud_resource(self):
		"""
		TODO: refactor into do_crud
		"""

		data = {
			"user": self.user_id,
			"start_date": "2015-04-24",
			"rate": 200,
			"agreed_hours_per_month": 0.00,
			"project": self.project_id
		}

		do_crud(self.service, "resource", data)

	
class HoursServiceTestCase(unittest.TestCase):

	def setUp(self):
		self.service = HoursService(tld=testing_tld)
		response = self.service.authenticate(username=testing_admin_username, password=testing_admin_password)
		self.service.login(response)

		data={
		    "user": 10,
		    "project_id": 0,
		    "project_task_id": 3,
		    "status": "Open",
		    "day": "2015-04-27",
		    "comments": "comment",
		    "hours": "5.00"		    
		}

		response = self.service.create("entry", data)		
		self.entry = response.json()
		

	def tearDown(self):
		entry_id = self.entry.get("id")
		self.service.delete("entry", entry_id)

	def test_get_entries(self):

		entries = self.service.get_entries()		
		assert entries.status_code == 200, 'Expect 200 OK'

	def test_create_entry(self):

		data={
		    "user": 10,
		    "project_id": 0,
		    "project_task_id": 3,
		    "status": "Open",
		    "day": "2015-04-27",
		    "start_time": None,
		    "end_time": None,
		    "comments": "comment",
		    "hours": "5.00",
		    "created": "2015-04-27T14:01:18.649643Z",
		    "updated": "2015-05-04T10:16:34.917113Z",
		    "overtime": False,
		    "tags": ""
		}

		entry = self.service.create("entry", data)
		self.create_id = entry.json()['id']

		assert entry.status_code == 201, 'Expect 201 CREATE OK'
		assert self.create_id is not None, 'Entry Id is not None'


	def test_update_entry(self):

		entry_id = self.entry.get('id')
		data = {"project_id": 99}
		entry_response = self.service.update("entry", entry_id, data)
		entry_data = entry_response.json()
		
		assert entry_response.status_code == 200, 'Expect 200 UPDATE OK'

		assert entry_data.get("project_id") == 99, 'Expect project_id to be updated'
		assert entry_data.get('comments') == "comment", 'Expect comment to be unchanged'

class UserServiceTestCase(unittest.TestCase):

	def setUp(self):		
		self.service = UserService(tld=testing_tld)

	def test_login(self):		

		assert self.service.token is None, 'Expect token to be none to start with'
		response = self.service.authenticate(username=testing_admin_username, password=testing_admin_password)

		assert response.status_code == 200, 'Expect 200 OK'
		

	"""
	def test_get_users(self):

		users = self.service.get_users()		
		assert users.status_code == 200, 'Expect 200 OK'
	"""

class EntryFetcherTestCase(unittest.TestCase):

	def setUp(self):
		user_service = UserService(tld=testing_tld)
		response = user_service.authenticate(username=testing_admin_username, password=testing_admin_password)
		is_logged_in, token = user_service.login(response)
		
		self.fetcher = EntryFetcher(token=token, tld=testing_tld)

	def test_get_entries(self):
		entries = self.fetcher.get_entries()		
		entry = entries[0]

		expected_fields = [
			# user_fields
			'user_first_name', 'user_last_name', 

			# project_fields
			'project_title',

			# task fields:
			'task_title'
		]

		for field in expected_fields:
			assert entry.get(field, None) is not None, \
				'Expect field to be added to data'

class ProjectFetcherTestCase(unittest.TestCase):

	def setUp(self):
		self.fetcher = ProjectFetcher()

	
	@unittest.skip("Not working for nested items yet")
	def test_get_projects(self):
		projects = self.fetcher.get_projects()		
		print projects
	