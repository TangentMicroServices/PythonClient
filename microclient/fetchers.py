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
            entry_merge_data = lookup.get(id)

            if entry_merge_data is not None:
                for field in merge_fields:
                    new_field = "{0}_{1}" . format (prefix, field)
                    entry[new_field] = entry_merge_data.get(field)
            else:
                print \
("Cannot find entry for {0}. Cannot find match for key: {1}:{2}" . format (prefix, merge_key, id))

        return original_data


class ProjectFetcher(FetcherBase):

    def __init__(self, token, tld="tangentmicroservices.com", protocol="http"):
        self.project_service = ProjectService(token, tld, protocol)
        self.user_service = UserService(token, tld, protocol)
        
    def get_projects(self, with_users=True):

        users = json.loads(self.user_service.get_users().content)
        projects = json.loads(self.project_service.get_projects().content)

        if with_users:
            for resource in projects.get("resource_set", []):
                self.merge(resource, "user", users, "id", "resource", ["first_name", "last_name"])
        else:
            return projects


class EntryFetcher(FetcherBase):

    def __init__(self, token, tld="tangentmicroservices.com", protocol="http"):
        self.project_service = ProjectService(token, tld, protocol)
        self.user_service = UserService(token, tld, protocol)
        self.hours_service = HoursService(token, tld, protocol)


    def get_entries(self, filter_params=None, with_users=True, with_projects=True, with_tasks=True):
        
        users = json.loads(self.user_service.get_users().content)
        projects = json.loads(self.project_service.get_projects().content)      
        entries = json.loads(self.hours_service.get_entries(filter_params=filter_params).content)      
        tasks = json.loads(self.project_service.get_tasks().content)

        if with_users:
            self.merge(entries, "user", users, "id", "user", ["first_name", "last_name"])
        
        if with_projects:
            self.merge(entries, "project_id", projects, "pk", "project", ["title"])

        if with_tasks:
            self.merge(entries, "project_task_id", tasks, "id", "task", ["title"])

        return entries

