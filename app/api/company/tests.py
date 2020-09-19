# Create your tests here.
from decimal import Decimal, ROUND_UP

from django.test import TestCase
from api.company.models.company import Company
from main.tests import BaseViewTest


class CompanyListViewTest(BaseViewTest, TestCase):
    fixtures = ('profile.json', 'company.json',)

    def setUp(self):
        self.uri = 'companies'
        self.required_attributes = {'non_nested': [
            'id', 'name', 'address', 'rating', 'opening_hours', 'closing_hours', 'image', 'enter_code', 'is_active'
        ]}
        super(CompanyListViewTest, self).setUp()

    def test_company_best_rating(self):
        response = self.client.get(f'/api/v1/{self.uri}/?sort_by_rating=desc')
        company = Company.all_with_calculated_rating(order='desc').first()
        self.assertEqual(
            str(company.rating.quantize(Decimal('1.0'), rounding=ROUND_UP)),
            response.data.get('results')[0].get('rating')
        )

    def test_company_worst_rating(self):
        response = self.client.get(f'/api/v1/{self.uri}/?sort_by_rating=asc')
        company = Company.all_with_calculated_rating(order='asc').first()
        rating = company.rating
        if company.rating:
            rating = str(company.rating.quantize(Decimal('1.0'), rounding=ROUND_UP))
        self.assertEqual(rating, response.data.get('results')[0].get('rating'))


class CompanyDetailViewTest(BaseViewTest, TestCase):
    fixtures = ('profile.json', 'company.json', 'master.json', 'service.json')

    def setUp(self):
        self.uri = 'companies/1'
        self.required_attributes = {
            'non_nested': ['id', 'masters', 'name', 'address', 'opening_hours',
                           'closing_hours', 'image', 'enter_code', 'is_active'],
            'nested': {
                'masters': ['id', 'profile', 'work_types'],
                'profile': ['id', 'first_name', 'last_name', 'age'],
                'work_types': ['id', 'work_type_name', 'company_name', 'duration',
                               'price_from', 'price_to', 'company', 'service']
            }
        }
        self.login()
        self.response = self.get_response()
        self.test_item = self.response.data
