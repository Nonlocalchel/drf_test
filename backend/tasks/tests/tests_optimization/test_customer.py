import json

from django.urls import reverse

from services.APITestCaseWithJWT import APITestCaseWithJWT
from users.models import User


class CustomerOptimizationTestCase(APITestCaseWithJWT):
    """Тестирование запросов работника с привилегиями"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('\nCustomer optimization test:')

    @classmethod
    def setUpTestUser(cls):
        cls.clean_password = 'customer_super_ps_387'
        cls.user = User.objects.get(username='customer_2')

    def test_get_all_tasks(self):
        url = reverse('tasks-list')
        with self.assertNumQueries(2):
            self.client.get(url)

    def test_get_task(self):
        url = reverse('tasks-detail', args=(61,))
        with self.assertNumQueries(2):
            self.client.get(url)

    def test_post_task(self):
        url = reverse('tasks-list')
        data = {
            "title": "test_task"
        }
        json_data = json.dumps(data)

        with self.assertNumQueries(3):
            self.client.post(url, data=json_data,
                             content_type='application/json')
