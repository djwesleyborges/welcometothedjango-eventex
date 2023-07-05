from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):

    def setUp(self) -> None:
        self.obj = Subscription(
            name="Wesley",
            cpf="12365478932",
            email="wesley@wesley.com",
            phone="62999999999"
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)
