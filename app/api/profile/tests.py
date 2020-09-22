# Create your tests here.
from datetime import datetime
from django.test import TestCase
from django.utils.crypto import get_random_string
from django.utils.formats import date_format
from faker import Faker
from rest_framework import status
from api.profile.models import Profile
from main.tests import BaseViewTest, CreateViewTest


class ProfileListViewTest(BaseViewTest, TestCase):
    fixtures = ('profile.json',)

    def setUp(self):
        self.uri = 'profiles'
        self.required_attributes = {'non_nested': [
            'username', 'first_name', 'last_name', 'birth_date', 'email', 'last_login', 'is_active', 'date_joined'
        ]}
        super(ProfileListViewTest, self).setUp()


class CreateProfileViewTest(CreateViewTest, TestCase):
    fixtures = ('profile.json',)

    def setUp(self):
        self.uri = 'profiles'
        self.login()
        self.faker = Faker()
        self.generate_request_params()

    def generate_request_params(self):
        profile = self.faker.profile(fields=('name', 'birthdate', 'ssn'))
        first_name, last_name, *other = profile['name'].split(' ', 2)
        self.request_params = {
            'first_name': first_name,
            'last_name': last_name,
            'birth_date': date_format(profile['birthdate'], 'DATE_FORMAT'),
            'email': self.faker.ascii_safe_email(),
            'password': get_random_string(length=12).lower(),
            'phone': f'+380{profile["ssn"].replace("-", "")}'
        }

    def test_blank_first_name(self):
        self.check_blank_value('first_name', self.expected_messages['blank'])

    def test_missing_first_name(self):
        self.check_missing_value('first_name', self.expected_messages['required'])

    def test_incorrect_first_name(self):
        self.check_incorrect_value('first_name', 123, 'The value contains numbers')

    def test_blank_last_name(self):
        self.check_blank_value('last_name', self.expected_messages['blank'])

    def test_missing_last_name(self):
        self.check_missing_value('last_name', self.expected_messages['required'])

    def test_incorrect_last_name(self):
        self.check_incorrect_value('last_name', 123, 'The value contains numbers')

    def test_unique_together_fields(self):
        self.client.post(f'/api/v1/{self.uri}/', self.request_params)
        self.request_params['email'] = self.faker.ascii_safe_email()
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params)
        self.assertEqual('The fields first_name, last_name must make a unique set.',
                         str(response.data.get('non_field_errors')[0]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_birth_date(self):
        self.check_incorrect_value('birth_date', 'abc', 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.')
        self.check_incorrect_value('birth_date', date_format(datetime.today(), 'DATE_FORMAT'), "Sorry, we think you're too young for that sh**")

    def test_blank_email(self):
        self.check_blank_value('email', self.expected_messages['blank'])

    def test_missing_email(self):
        self.check_missing_value('email', self.expected_messages['required'])

    def test_incorrect_email(self):
        self.check_incorrect_value('email', 123, 'Ensure this field has at least 8 characters.')
        self.check_incorrect_value('email', 123, 'Enter a valid email address.')

    def test_unique_email(self):
        self.client.post(f'/api/v1/{self.uri}/', self.request_params)
        self.check_incorrect_value('email', self.request_params['email'], 'This field must be unique.')

    def test_blank_phone(self):
        self.check_blank_value('phone', self.expected_messages['blank'])

    def test_incorrect_phone(self):
        self.check_incorrect_value('phone', 'abc', 'Incorrect phone number')
        self.check_incorrect_value('phone', 123, 'Incorrect phone number')

    def test_create_profile(self):
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn('id', response.data)
        self.assertIn('date_joined', response.data)
        self.assertTrue(Profile.is_profile_exist(response.data.get('id')))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
