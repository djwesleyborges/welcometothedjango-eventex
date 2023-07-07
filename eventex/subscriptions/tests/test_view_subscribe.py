from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):

    def setUp(self) -> None:
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """Get inscricao/ must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must return subscriptions/subscriptions_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscriptions_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 4),
                ('type="text"', 4),
                ('type="submit"', 1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

        # self.assertContains(self.response, '<form')
        # self.assertContains(self.response, '<input', 6)  # 5 e a quantidade de inputs que deseja encontrar
        # self.assertContains(self.response, 'type="text"', 4)
        # self.assertContains(self.response, 'type="text"')
        # self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """HTML must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Content must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):

    def setUp(self) -> None:
        data = dict(name='Wesley Borges', cpf='01234567891',
                    email='wesley@mail.com', phone='62999999999')
        self.resp = self.client.post('/inscricao/', data=data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        # self.assertEqual(302, self.resp.status_code)
        self.assertRedirects(self.resp, '/inscricao/1/')

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribePostInvalid(TestCase):
    def setUp(self) -> None:
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscriptions_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
