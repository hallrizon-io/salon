from abc import abstractmethod
from collections import OrderedDict
from django.test import Client
from rest_framework import status
from functools import reduce
from api.profile.models import Profile
from objects.nested_dict import set_nested_attribute, get_nested_attribute, pop_nested_attribute


class BaseViewTest:
    def get_response(self):
        return self.client.get(f'/api/v1/{self.uri}/', self.uri_params if hasattr(self, 'uri_params') else {})

    def login(self):
        self.client = Client()
        self.client.force_login(Profile.objects.get(username='admin'))

    def setUp(self):
        self.login()
        self.response = self.get_response()
        self.test_item = self.response.data.get('results')[0]

    def test_status_code(self):
        self.assertEqual(status.HTTP_200_OK, self.response.status_code)

    def test_count_of_attributes(self):
        self.check_count_of_attributes(self.test_item, self.required_attributes.get('non_nested'))

    def check_count_of_attributes(self, item, required_attributes):
        self.assertEqual(len(item), len(required_attributes))
        for key in item:
            value = item.get(key)
            if isinstance(value, (OrderedDict, dict)):
                self.check_count_of_attributes(value, self.required_attributes.get('nested').get(key))
            elif isinstance(value, list):
                self.check_count_of_attributes(value[0], self.required_attributes.get('nested').get(key))

    def test_attribute_matching(self):
        self.match_nested_attributes(self.test_item, self.required_attributes.get('non_nested'))

    def match_nested_attributes(self, item, required_attributes):
        for key in item:
            value = item.get(key)
            if isinstance(value, (OrderedDict, dict)):
                self.match_nested_attributes(value, self.required_attributes.get('nested').get(key))
            elif isinstance(value, list):
                self.match_nested_attributes(value[0], self.required_attributes.get('nested').get(key))

            self.assertIn(key, required_attributes)


class CreateViewTest:
    expected_messages = {
        'blank': "This field may not be blank.",
        'required': "This field is required.",
        'positive_int': "Expected a positive integer value"
    }

    @abstractmethod
    def generate_request_params(self):
        pass

    def login(self):
        self.client = Client()
        self.client.force_login(Profile.objects.get(username='admin'))

    def set_nested_attribute(self, path, value):
        path_list = path.split('.')
        reduce(dict.get, path_list[:-1], self.request_params)[path_list[-1]] = value

    def pop_nested_param(self, path):
        path_list = path.split('.')
        del reduce(dict.get, path_list[:-1], self.request_params)[path_list[-1]]

    def check_response(self, path, message):
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn(message, [str(error) for error in get_nested_attribute(path, response.data)])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def check_blank_value(self, path, message):
        set_nested_attribute(path, '', self.request_params)
        self.check_response(path, message)

    def check_missing_value(self, path, message):
        pop_nested_attribute(path, self.request_params)
        self.check_response(path, message)

    def check_incorrect_value(self, path, value, message):
        set_nested_attribute(path, value, self.request_params)
        self.check_response(path, message)
