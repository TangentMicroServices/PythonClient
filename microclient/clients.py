import requests
import json

"""
TODO: prefix (e.g.: /api/v1/) should not be hardcoded
"""

service_definitions = {

    "ProjectService": {
        #"base": settings.PROJECTSERVICE_BASE_URL,
        "resources": {
            "project": {
                "endpoint": "/projects/",
                "required_params": ["title", "description", "start_date"],
                "optional_params": [],
            },
            "task": {
                "endpoint": "/tasks/",
                "required_params": [],
                "optional_params": [],
            },
            "resource": {
                "endpoint": "/resources/",
                "required_params": [
                    "user", "start_date", "rate", "project"
                ],
                "optional_params": [
                    "end_date", "agreed_hours_per_month",
                ],
            }
        }
    },
    "HoursService": {
        #"base": settings.HOURSSERVICE_BASE_URL,
        "resources": {
            "entry": {
                "endpoint": "/entry/",
                "required_params": [
                    'user', 'project_id', 'project_task_id', 'day', 'hours', 'comments'
                ],
                "optional_params": [
                    'status', 'start_time', 'end_time', 'overtime', 'tags'
                ]
            }
        }
    },
    "UserService": {
        #"base": settings.USERSERVICE_BASE_URL,
        "resources": {
            "user": {
                "endpoint": "/users/",
                "required_params": [],
                "optional_params": []
            }
        }
    }

}


class ServiceBase(object):

    def __init__(self, service_name, token=None, tld="tangentmicroservices.com", protocol="http"):

        self.token = token
        self.tld = tld
        self.protocol = protocol
        # if token is None:
        #    self.token = settings.TOKEN

        self.service_name = service_name
        # self._make_api(service_name)

    def call(self, path, data={}, method="get"):

        url = self._get_url(path)

        headers = {
            'content-type': 'application/json',
        }
        if self.token is not None:
            headers.update({
                'Authorization': 'Token {0}' . format(self.token)
            })

        http_method = getattr(requests, method)

        return http_method(url, data=json.dumps(data), headers=headers)

    def authenticate(self, username, password):
        userservice = UserService(tld=self.tld, protocol=self.protocol)
        return userservice.authenticate(username, password)

    def login(self, userservice_response):

        is_logged_in = False

        if userservice_response.status_code == 200:
            self.token = userservice_response.json().get("token")
            is_logged_in = True
        else:
            self.token = None

        return (is_logged_in, self.token)

    def as_json(self, response):
        return json.loads(response.content)

    def info(self, resource):
        '''
        prints information/documentation on a provided resource
        '''
        service_def, resource_def, path = self._get_service_information(
            resource)

        print (resource)
        print ("*******************************************")
        print ("Base URL: {0}" . format (self.tld))
        print ("Resource path: {0}" . format (resource_def.get("endpoint")))
        print ("Required parameters: {0}" . format (resource_def.get("required_params")))
        print ("Optional parameters" . format (resource_def.get("optional_params")))
        

    def list(self, resource):

        service_def, resource_def, path = self._get_service_information(
            resource)
        return self.call(path)

    def get(self, resource, resource_id):
        service_def, resource_def, path = self._get_service_information(
            resource)

        get_path = "{0}{1}/" . format(path, resource_id)
        return self.call(get_path)

    def create(self, resource, data):
        '''
        A base function that performs a default create POST request for a given object
        '''

        service_def, resource_def, path = self._get_service_information(
            resource)
        self._validate(resource, data)

        return self.call(path, data, 'post')

    def update(self, resource, resource_id, data):
        '''
        A base function that performs a default create PATCH request for a given object
        '''
        service_def, resource_def, path = self._get_service_information(
            resource)

        update_path = "{0}{1}/" . format(path, resource_id)
        return self.call(update_path, data, 'patch')

    def delete(self, resource, resource_id):
        '''
        A base function that performs a default delete DELETE request for a given object
        '''

        service_def, resource_def, path = self._get_service_information(
            resource)
        delete_path = "{0}{1}/" . format(path, resource_id)
        return self.call(delete_path, method="delete")

    def _make_api(self, service_name):
        '''
        not yet in use ..
        '''

        resources = [resource for resource, resource_details in
                     service_definitions.get(service_name, {}).get("resources", {}).items()]

        for resource in resources:
            setattr(self, 'list_{0}' . format(resource), self.list)
            setattr(self, 'get_{0}' . format(resource), self.get)
            setattr(self, 'create_{0}' . format(resource), self.create)
            setattr(self, 'update_{0}' . format(resource), self.update)
            setattr(self, 'delete_{0}' . format(resource), self.delete)

    def _validate(self, resource, data):

        service_def, resource_def, path = self._get_service_information(
            resource)

        required_params = resource_def.get("required_params", [])
        optional_params = resource_def.get("optional_params", [])

        for param in required_params:
            if data.get(param, None) is None:

                required_params_string = (", ").join(required_params)
                err_message = "{0} is a required parameter for create on {1}. Required parameters are: {2}"\
                    . format(param, resource, required_params_string)
                raise ValueError(err_message)

    def _get_service_information(self, resource):
        service_def = service_definitions.get(self.service_name)
        resource_def = service_def.get("resources", {}).get(resource)
        path = resource_def.get("endpoint")
        return service_def, resource_def, path

    def _get_url(self, path):
        return "{0}{1}" . format(self._get_base_url(), path)

    def _get_base_url(self):
        return "{0}://{1}.{2}/api/v1" . format(self.protocol, self.service_name.lower(), self.tld)

    def _get_headers(self):

        headers = {
            'content-type': 'application/json',
        }

        if self.token is not None:
            headers.update({
                'Authorization': 'Token {0}' . format(self.token)
            })

        return headers


class ProjectService(ServiceBase):

    def __init__(self, token=None, tld="tangentmicroservices.com", protocol="http"):

        super(ProjectService, self).__init__(
            'ProjectService', token, tld, protocol)

    def get_projects(self):
        '''
        @DeprecationWarning("Rather just use: ProjectService.list('project') directly")
        '''

        return self.list("project")

    def get_tasks(self):
        '''
        @DeprecationWarning("Rather just use: ProjectService.list('task') directly")
        '''
        return self.list("task")


class HoursService(ServiceBase):

    def __init__(self, token=None, tld="tangentmicroservices.com", protocol="http"):

        super(HoursService, self).__init__(
            'HoursService', token, tld, protocol)

    def as_json(self, response):
        return json.loads(response.content)

    def get_entries(self, project_id=None, user_id=None):

        path = '/entry/'

        if(user_id or project_id):
            path = "{0}?user={1}&project_id={2}" .format(
                path, user_id, project_id)

        return self.call(path)

    def get_overview(self):
        return self.call(self.service_name, '/entry/overview/')


class UserService(ServiceBase):

    def __init__(self, token=None, tld="tangentmicroservices.com", protocol="http"):

        super(UserService, self).__init__('UserService', token, tld, protocol)

    def authenticate(self, username, password):

        data = {
            "username": username,
            "password": password,
        }

        url = "{0}://{1}.{2}/api-token-auth/" . format(
            self.protocol, self.service_name.lower(), self.tld)
        response = requests.post(url, data)

        return response

    def get_users(self):
        return self.list('user')
