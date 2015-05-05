from microclient.clients import ServiceBase
import json
from datetime import datetime
from microclient.clients import ProjectService, HoursService, UserService


class FetcherBase():
	
	def __init__(self):
		pass

	def create_index(self, data_list, index_name):

		lookup = {}
		return { item[index_name]: item for item in data_list }

	def merge(self, original_data, original_key, merge_data, merge_key, prefix, merge_fields):

		lookup = self.create_index(merge_data, merge_key)
		
		for entry in original_data:

			id = entry.get(original_key)
			merge_data = lookup.get(id)

			for field in merge_fields:
				new_field = "{0}_{1}" . format (prefix, field)
				entry[new_field] = merge_data.get(field)

		return original_data


class ProjectFetcher(FetcherBase):

	def __init__(self):
		self.project_service = ProjectService()
		self.user_service = UserService()
		
	def get_projects(self, with_users=True):

		users = json.loads(self.user_service.get_users().content)
		projects = json.loads(self.project_service.get_projects().content)

		if with_users:
			for resource in projects.get("resource_set", []):
				self.merge(resource, "user", users, "id", "resource", ["first_name", "last_name"])
		else:
			return projects


class UserFetcher(FetcherBase):

	def get_users(self):
		#Users
		users_response = self.service_api.get_users()
		return json.loads(users_response.content)

class EntryFetcher(FetcherBase):

	def __init__(self):
		self.project_service = ProjectService()
		self.user_service = UserService()
		self.hours_service = HoursService()


	def get_entries(self, project_id=None, user_id=None, with_users=True, with_projects=True, with_tasks=True):

		users = json.loads(self.user_service.get_users().content)
		projects = json.loads(self.project_service.get_projects().content)		
		entries = json.loads(self.hours_service.get_entries().content)
		import pdb;pdb.set_trace()
		tasks = json.loads(self.project_service.get_tasks().content)

		if with_users:
			self.merge(entries, "user", users, "id", "user", ["first_name", "last_name"])
		
		if with_projects:
			self.merge(entries, "project_id", projects, "pk", "project", ["title"])

		if with_tasks:
			self.merge(entries, "project_task_id", tasks, "id", "task", ["title"])

		return entries

