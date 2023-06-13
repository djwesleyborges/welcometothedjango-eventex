from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):

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
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)  # 5 e a quantidade de inputs que deseja encontrar
        self.assertContains(self.response, 'type="text"', 4)
        self.assertContains(self.response, 'type="text"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """HTML must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Content must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields."""
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):

    def setUp(self) -> None:
        data = dict(name='Wesley Borges', cpf='01234567891',
                    email='wesley@mail.com', phone='62999999999')
        self.resp = self.client.post('/inscricao/', data=data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""

        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'wesley@mail.com']
        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]
        self.assertIn('Wesley Borges', email.body)
        self.assertIn('01234567891', email.body)
        self.assertIn('wesley@mail.com', email.body)
        self.assertIn('62999999999', email.body)


class SubscribeInvalidPost(TestCase):
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


class SubscribeSuccessMessage(TestCase):

    def setUp(self) -> None:
        data = dict(name='Wesley Borges', cpf='01234567891',
                    email='wesley@mail.com', phone='62999999999')
        self.resp = self.client.post('/inscricao/', data=data, follow=True)

    def test_message(self):
        self.assertContains(self.resp, 'Inscrição realizada com sucesso!')
