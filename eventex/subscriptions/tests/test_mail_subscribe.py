from django.core import mail

from django.test import TestCase


class SubscribePostValid(TestCase):

    def setUp(self) -> None:
        data = dict(name='Wesley Borges', cpf='01234567891',
                    email='wesley@mail.com', phone='62999999999')
        self.client.post('/inscricao/', data=data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'djwesleyborges@gmail.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['djwesleyborges@gmail.com', 'wesley@mail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Wesley Borges',
            '01234567891',
            'wesley@mail.com',
            '62999999999'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
