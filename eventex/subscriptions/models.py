from django.db import models


class Subscription(models.Model):
    name = models.CharField('nome', max_length=50)
    cpf = models.CharField('cpf', max_length=11)
    email = models.EmailField('e-Mail')
    phone = models.CharField('Telefone', max_length=20)
    created_at = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'inscrições'
        verbose_name = 'inscrição'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
