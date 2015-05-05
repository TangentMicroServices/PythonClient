from django.test import TestCase

from microclient.fetchers import ProjectFetcher, EntryFetcher
from microclient.clients import ProjectService, UserService, HoursService
import json

class ProjectServiceTestCase(TestCase):

	def setUp(self):
		self.service = ProjectService()

	def test_get_projects(self):

		projects = self.service.get_projects()		
		assert projects.status_code == 200, 'Expect 200 OK'

class HoursServiceTestCase(TestCase):

	def setUp(self):
		self.service = HoursService()

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

class UserServiceTestCase(TestCase):

	def setUp(self):
		self.service = UserService()

	def test_get_projects(self):

		projects = self.service.get_users()		
		assert projects.status_code == 200, 'Expect 200 OK'


class EntryFetcherTestCase(TestCase):

	def setUp(self):
		self.fetcher = EntryFetcher()

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

class ProjectFetcherTestCase(TestCase):

	def setUp(self):
		self.fetcher = ProjectFetcher()

	'''
	@unittest.skip("Not working for nested items yet")
	def test_get_projects(self):
		projects = self.fetcher.get_projects()		
		print projects
	'''