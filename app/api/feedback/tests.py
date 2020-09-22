# Create your tests here.
from datetime import datetime, time
from django.db.models import Q
from django.test import TestCase
from datetime import date
from rest_framework import status
from api.company.models import Company
from api.profile.models import Profile
from api.reception.models import Reception
from api.reception.serializers import CreateReceptionSerializer
from main.tests import CreateViewTest


class CreateFeedbackViewTest(CreateViewTest, TestCase):
    fixtures = ('profile.json', 'company.json', 'service.json', 'master.json', 'reception.json')

    def setUp(self):
        self.uri = 'feedbacks'
        self.profile = Profile.create_random_profile()
        self.company = Company.objects.filter(Q(receptions__gt=0)).first()
        self.master = self.company.masters.first()
        serializer = CreateReceptionSerializer(data={
            'company_id': self.company.id,
            'master_id': self.master.id,
            'client_id': self.profile.id,
            'service_id': self.master.work_types.filter(company=self.company).first().service.id,
            'datetime': datetime.combine(date.today(), time(10, 0)).strftime("%Y-%m-%d %H:%M:%S")
        })
        serializer.is_valid()

        self.reception = serializer.save()
        self.reception.status = Reception.Status.ACCEPTED
        self.reception.save(update_fields=['status'])
        self.login()

    def test_incorrect_reception_id(self):
        response = self.client.post(f'/api/v1/{self.uri}/', {'reception_id': 999, 'mark': 5})
        self.assertEqual("The current reception doesn't exist", str(response.data.get('reception_id')))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reception_feedback_value(self):
        response = self.client.post(f'/api/v1/{self.uri}/', {'reception_id': self.reception.id, 'mark': 2.2})
        self.assertEqual("Incorrect mark value", response.data.get('mark'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reception_feedback(self):
        response = self.client.post(f'/api/v1/{self.uri}/', {'reception_id': self.reception.id, 'mark': 2})
        self.assertTrue(self.reception.feedback.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_reception_feedback(self):
        self.client.post(f'/api/v1/{self.uri}/', {'reception_id': self.reception.id, 'mark': 2})
        old_mark = self.reception.feedback.mark
        response = self.client.post(f'/api/v1/{self.uri}/', {'reception_id': self.reception.id, 'mark': 5})
        self.reception.refresh_from_db()
        self.assertTrue(old_mark != self.reception.feedback.mark)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incorrect_client_id(self):
        params = {'client_id': 999, 'company_id': self.company.id, 'mark': 5}
        response = self.client.post(f'/api/v1/{self.uri}/', params)
        self.assertEqual("The current client doesn't exist", str(response.data.get('client_id')))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_company_id(self):
        response = self.client.post(f'/api/v1/{self.uri}/', {'client_id': self.profile.id, 'company_id': 999, 'mark': 5})
        self.assertEqual("The current company doesn't exist", str(response.data.get('company_id')))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_company_feedback_value(self):
        response = self.client.post(f'/api/v1/{self.uri}/', {
            'client_id': self.profile.id,
            'company_id': self.company.id,
            'mark': 2.2
        })
        self.assertEqual("Incorrect mark value", response.data.get('mark'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_company_feedback(self):
        response = self.client.post(f'/api/v1/{self.uri}/', {
            'client_id': self.profile.id,
            'company_id': self.company.id,
            'mark': 2
        })
        self.assertTrue(self.company.feedbacks.get(client=self.profile).id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_company_feedback(self):
        self.client.post(f'/api/v1/{self.uri}/', {
            'client_id': self.profile.id,
            'company_id': self.company.id,
            'mark': 2
        })
        old_mark = self.company.feedbacks.get(client=self.profile).mark
        response = self.client.post(f'/api/v1/{self.uri}/', {
            'client_id': self.profile.id,
            'company_id': self.company.id,
            'mark': 5
        })
        self.reception.refresh_from_db()
        self.assertTrue(old_mark != self.company.feedbacks.get(client=self.profile).mark)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
