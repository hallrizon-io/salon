# Create your tests here.
from datetime import time, datetime
from django.test import TestCase
from django.utils.formats import date_format
from faker import Faker
from rest_framework import status
from api.master.models import Master
from api.profile.models import Profile
from api.reception.models import Reception
from api.service.models import Service
from main.tests import BaseViewTest, CreateViewTest


class ReceptionListViewTest(BaseViewTest, TestCase):
    fixtures = ('profile.json', 'company.json', 'reception.json', 'master.json', 'service.json')

    def setUp(self):
        self.uri = 'receptions'
        self.required_attributes = {
            'non_nested': ['id', 'client', 'master', 'company', 'service', 'updated',
                           'created', 'time_from', 'time_to', 'description', 'status', 'price'],
            'nested': {
                'client': ['id', 'first_name', 'last_name', 'age'],
                'master': ['id', 'first_name', 'last_name', 'age'],
                'company': ['id', 'name', 'address', 'opening_hours', 'closing_hours']
            }
        }
        super(ReceptionListViewTest, self).setUp()


class CreateReceptionViewTest(CreateViewTest, TestCase):
    fixtures = ('profile.json', 'company.json', 'reception.json', 'master.json', 'service.json')

    def setUp(self):
        self.uri = 'receptions'
        self.login()
        self.faker = Faker()
        self.generate_request_params()

    def generate_request_params(self):
        profile = Profile.create_random_profile()
        master = Master.objects.create_random_master()
        service = Service.objects.first()
        dt = datetime.combine(self.faker.date_this_month(before_today=False, after_today=True), time(10, 0))

        self.request_params = {
            'company_id': master.company.first().id,
            'master_id': master.id,
            'client_id': profile.id,
            'service_id': service.id,
            'datetime': date_format(dt, 'DATETIME_FORMAT')
        }

    def test_blank_company_id(self):
        self.check_blank_value('company_id', self.expected_messages['blank'])

    def test_missing_company_id(self):
        self.check_missing_value('company_id', self.expected_messages['required'])

    def test_incorrect_company_id(self):
        self.check_incorrect_value('company_id', 'abc', self.expected_messages['positive_int'])
        self.check_incorrect_value('company_id', -999, "The current company doesn't exist")

    def test_blank_master_id(self):
        self.check_blank_value('master_id', self.expected_messages['blank'])

    def test_missing_master_id(self):
        self.check_missing_value('master_id', self.expected_messages['required'])

    def test_incorrect_master_id(self):
        self.check_incorrect_value('master_id', 'abc', self.expected_messages['positive_int'])
        self.check_incorrect_value('master_id', -999, "The current master doesn't exist")

    def test_blank_client_id(self):
        self.check_blank_value('client_id', self.expected_messages['blank'])

    def test_missing_client_id(self):
        self.check_missing_value('client_id', self.expected_messages['required'])

    def test_incorrect_client_id(self):
        self.check_incorrect_value('client_id', 'abc', self.expected_messages['positive_int'])
        self.check_incorrect_value('client_id', -999, "The current client doesn't exist")

    def test_blank_service_id(self):
        self.check_blank_value('service_id', self.expected_messages['blank'])

    def test_missing_service_id(self):
        self.check_missing_value('service_id', self.expected_messages['required'])

    def test_incorrect_service_id(self):
        self.check_incorrect_value('service_id', 'abc', self.expected_messages['positive_int'])
        self.check_incorrect_value('service_id', -999, "The system doesn't support current service")

    def test_master_unsupported_service(self):
        master = Master.objects.get(pk=self.request_params['master_id'])
        service_id = master.work_types.last().service.id
        master.work_types.last().delete()
        self.check_incorrect_value('service_id', service_id, "The current service doesn't support by this master")

    def test_blank_datetime(self):
        self.check_blank_value('datetime', self.expected_messages['blank'])

    def test_missing_datetime(self):
        self.check_missing_value('datetime', self.expected_messages['required'])

    def test_incorrect_datetime(self):
        message = "Date has wrong format. Use one of these formats instead: YYYY-MM-DD HH:MM."
        self.check_incorrect_value('datetime', 'abc', message)
        self.check_incorrect_value('datetime', 123, message)

    def test_incorrect_company_working_hours(self):
        message = 'Sorry, come to us when we are opening again'
        dt = date_format(datetime.combine(self.faker.date_this_month(after_today=True), time(8, 0)), 'DATETIME_FORMAT')
        self.request_params['datetime'] = dt
        self.check_response('other_reason', message)

        dt = date_format(datetime.combine(self.faker.date_this_month(after_today=True), time(22, 0)), 'DATETIME_FORMAT')
        self.request_params['datetime'] = dt
        self.check_response('other_reason', message)

    def test_incorrect_company_worker(self):
        master = Master.objects.create_random_master()
        self.request_params['master_id'] = master.id
        self.check_response('other_reason', "The current master doesn't work for this company")

    def test_already_booked_hours(self):
        self.client.post(f'/api/v1/{self.uri}/', self.request_params, content_type='application/json')
        self.check_response('other_reason', "Sorry, your hours are already booked")

    def test_create_reception(self):
        response = self.client.post(f'/api/v1/{self.uri}/', self.request_params)
        self.assertIn('id', response.data)
        self.assertIn('start_time', response.data)
        self.assertTrue(Reception.objects.filter(pk=response.data.get('id')).exists())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
