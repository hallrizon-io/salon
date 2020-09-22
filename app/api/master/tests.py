# Create your tests here.
from datetime import datetime
from django.test import TestCase
from django.utils.crypto import get_random_string
from django.utils.formats import date_format
from faker import Faker
from rest_framework import status
from api.company.models import Company
from api.master.models import Master
from api.reception.models import Reception
from api.service.models import Service
from main.tests import BaseViewTest, CreateViewTest
from objects.nested_dict import set_nested_attribute, get_nested_attribute, pop_nested_attribute


class MasterListViewTest(BaseViewTest, TestCase):
    fixtures = ('profile.json', 'company.json', 'reception.json', 'master.json', 'service.json')

    def setUp(self):
        self.uri = 'masters'
        self.required_attributes = {
            'non_nested': ['id', 'profile', 'company', 'work_types', 'ratings'],
            'nested': {
                'profile': ['id', 'first_name', 'last_name', 'age'],
                'company': ['id', 'name', 'address', 'opening_hours',
                            'closing_hours', 'image', 'is_active'],
                'work_types': ['id', 'work_type_name', 'company_name', 'duration',
                               'price_from', 'price_to', 'company', 'service'],
                'ratings': ['company_name', 'service_name', 'rating',
                            'receptions', 'company_id', 'service_id']
            }
        }
        super(MasterListViewTest, self).setUp()

    def is_exist_required_attrs(self):
        return self.test_item.get('company') and self.test_item.get('work_types') and self.test_item.get('ratings')

    def set_test_item_with_required_attrs(self):
        for master in self.response.data.get('results'):
            if master.get('company') and master.get('work_types') and master.get('ratings'):
                self.test_item = master
                break

    def test_count_of_attributes(self):
        if not self.is_exist_required_attrs():
            self.set_test_item_with_required_attrs()
        super(MasterListViewTest, self).test_count_of_attributes()

    def test_attribute_matching(self):
        if not self.is_exist_required_attrs():
            self.set_test_item_with_required_attrs()
        super(MasterListViewTest, self).test_attribute_matching()


class MasterBookedHoursViewTest(BaseViewTest, TestCase):
    fixtures = ('profile.json', 'company.json', 'reception.json', 'master.json', 'service.json')

    def setUp(self):
        reception = Reception.objects.last()
        self.uri = f'masters/{reception.master.id}'
        self.uri_params = {'date': date_format(datetime.fromtimestamp(reception.start_timestamp), 'DATE_FORMAT')}
        self.required_attributes = {
            'non_nested': ['time_from', 'time_to', 'work_type', 'status'],
        }
        super(MasterBookedHoursViewTest, self).setUp()


class CreateMasterViewTest(CreateViewTest, TestCase):
    fixtures = ('profile.json', 'company.json', 'reception.json', 'master.json', 'service.json')

    def setUp(self):
        self.uri = 'profiles/master'
        self.login()
        self.faker = Faker()
        self.generate_request_params()

    def generate_request_params(self):
        profile = self.faker.profile(fields=('name', 'birthdate', ''))
        first_name, last_name, *other = profile['name'].split(' ', 2)
        email = self.faker.ascii_safe_email()
        self.request_params = {
            'profile': {
                'first_name': first_name,
                'last_name': last_name,
                'birth_date': date_format(profile['birthdate'], 'DATE_FORMAT'),
                'email': email,
                'password': get_random_string(length=12).lower()
            },
            'work_types': [{'name': service.name, 'duration': '01:30:00'} for service in Service.objects.all()],
            'company': {
                'name': self.faker.company(),
                'address': self.faker.street_address(),
                'opening_hours': '10:00',
                'closing_hours': '18:00'
            },
            'new_company': True
        }

    def test_blank_profile_first_name(self):
        self.check_blank_value('profile.first_name', self.expected_messages['blank'])

    def test_missing_profile_first_name(self):
        self.check_missing_value('profile.first_name', self.expected_messages['required'])

    def test_incorrect_profile_first_name(self):
        self.check_incorrect_value('profile.first_name', 123, 'The value contains numbers')

    def test_blank_profile_last_name(self):
        self.check_blank_value('profile.last_name', self.expected_messages['blank'])

    def test_missing_profile_last_name(self):
        self.check_missing_value('profile.last_name', self.expected_messages['required'])

    def test_incorrect_profile_last_name(self):
        self.check_incorrect_value('profile.last_name', 123, 'The value contains numbers')

    def test_unique_together_profile_fields(self):
        self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        set_nested_attribute('profile.email', self.faker.ascii_safe_email(), self.request_params)
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn('The fields first_name, last_name must make a unique set.',
                      [str(error) for error in get_nested_attribute('profile.non_field_errors', response.data)])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_profile_birth_date(self):
        self.check_incorrect_value('profile.birth_date', 'abc', 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.')
        self.check_incorrect_value('profile.birth_date', date_format(datetime.today(), 'DATE_FORMAT'), "Sorry, we think you're too young for that sh**")

    def test_blank_profile_email(self):
        self.check_blank_value('profile.email', self.expected_messages['blank'])

    def test_missing_profile_email(self):
        self.check_missing_value('profile.email', self.expected_messages['required'])

    def test_incorrect_profile_email(self):
        self.check_incorrect_value('profile.email', 123, 'Ensure this field has at least 8 characters.')
        self.check_incorrect_value('profile.email', 123, 'Enter a valid email address.')

    def test_unique_profile_email(self):
        self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.check_incorrect_value('profile.email', self.request_params['profile']['email'], 'This field must be unique.')

    def test_blank_profile_phone(self):
        self.check_blank_value('profile.phone', self.expected_messages['blank'])

    def test_incorrect_profile_phone(self):
        self.check_incorrect_value('profile.phone', 'abc', 'Incorrect phone number')
        self.check_incorrect_value('profile.phone', 123, 'Incorrect phone number')

    def test_blank_company_name(self):
        self.check_blank_value('company.name', self.expected_messages['blank'])

    def test_missing_company_name(self):
        self.check_missing_value('company.name', self.expected_messages['required'])

    def test_blank_company_address(self):
        self.check_blank_value('company.address', self.expected_messages['blank'])

    def test_missing_company_opening_hours(self):
        self.check_missing_value('company.opening_hours', self.expected_messages['required'])

    def test_incorrect_company_opening_hours(self):
        message = 'Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].'
        self.check_incorrect_value('company.opening_hours', '', message)
        self.check_incorrect_value('company.opening_hours', 'abc', message)
        self.check_incorrect_value('company.opening_hours', 123, message)

    def test_missing_company_closing_hours(self):
        self.check_missing_value('company.closing_hours', self.expected_messages['required'])

    def test_incorrect_company_closing_hours(self):
        message = 'Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].'
        self.check_incorrect_value('company.closing_hours', '', message)
        self.check_incorrect_value('company.closing_hours', 'abc', message)
        self.check_incorrect_value('company.closing_hours', 123, message)

    def test_blank_work_type_name(self):
        set_nested_attribute('name', '', self.request_params.get('work_types')[0])
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn(
            self.expected_messages['blank'],
            [str(error) for error in get_nested_attribute('name', response.data.get('work_types')[0])]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_work_type_name(self):
        pop_nested_attribute('name', self.request_params.get('work_types')[0])
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn(
            self.expected_messages['required'],
            [str(error) for error in get_nested_attribute('name', response.data.get('work_types')[0])]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_work_type_name(self):
        set_nested_attribute('name', 'abc', self.request_params.get('work_types')[0])
        set_nested_attribute('name', 123, self.request_params.get('work_types')[1])
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn(
            "The system doesn't support current service",
            [str(error) for error in get_nested_attribute('name', response.data.get('work_types')[0])]
        )
        self.assertIn(
            "The value contains numbers",
            [str(error) for error in get_nested_attribute('name', response.data.get('work_types')[1])]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blank_work_type_duration(self):
        set_nested_attribute('duration', '', self.request_params.get('work_types')[0])
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn(
            'Ensure this value is greater than or equal to 0:15:00.',
            [str(error) for error in get_nested_attribute('duration', response.data.get('work_types')[0])]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_work_type_duration(self):
        pop_nested_attribute('duration', self.request_params.get('work_types')[0])
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn(
            self.expected_messages['required'],
            [str(error) for error in get_nested_attribute('duration', response.data.get('work_types')[0])]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_work_type_duration(self):
        set_nested_attribute('duration', 'abc', self.request_params.get('work_types')[0])
        set_nested_attribute('duration', 123, self.request_params.get('work_types')[1])
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn(
            "Duration has wrong format. Use one of these formats instead: [DD] [HH:[MM:]]ss[.uuuuuu].",
            [str(error) for error in get_nested_attribute('duration', response.data.get('work_types')[0])]
        )
        self.assertIn(
            "Ensure this value is greater than or equal to 0:15:00.",
            [str(error) for error in get_nested_attribute('duration', response.data.get('work_types')[1])]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blank_company_enter_code(self):
        set_nested_attribute('new_company', False, self.request_params)
        self.check_blank_value('company.enter_code', self.expected_messages['blank'])

    def test_required_company_enter_code(self):
        set_nested_attribute('new_company', False, self.request_params)
        set_nested_attribute('company.enter_code', 'test', self.request_params)
        self.check_missing_value('company.enter_code', self.expected_messages['required'])

    def test_incorrect_company_enter_code(self):
        message = 'Not found company by current enter_code'
        set_nested_attribute('new_company', False, self.request_params)
        self.check_incorrect_value('company.enter_code', 'abc', message)
        self.check_incorrect_value('company.enter_code', 123, message)

    def test_blank_new_company(self):
        self.check_blank_value('new_company', 'Must be a valid boolean.')

    def test_missing_new_company(self):
        self.check_missing_value('new_company', self.expected_messages['required'])

    def test_incorrect_new_company(self):
        self.check_incorrect_value('new_company', 'abc', 'Must be a valid boolean.')
        self.check_incorrect_value('new_company', 123, 'Must be a valid boolean.')

    def test_create_master_for_exist_company(self):
        company = Company.objects.first()
        set_nested_attribute('new_company', False, self.request_params)
        set_nested_attribute('company.enter_code', company.enter_code, self.request_params)
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn('id', response.data)
        self.assertIn('date_joined', response.data)
        self.assertTrue(Master.objects.filter(pk=response.data.get('id')).exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_master_and_new_company(self):
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.assertIn('id', response.data)
        self.assertIn('date_joined', response.data)
        self.assertTrue(Master.objects.filter(pk=response.data.get('id')).exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
