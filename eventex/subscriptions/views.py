from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscriptions_form.html', context={'form': form})

    _send_mail(subject='Confirmação de Inscrição', from_=settings.DEFAULT_FROM_EMAIL, to=form.cleaned_data['email'],
               template_name='subscriptions/subscription_email.txt', context=form.cleaned_data)

    Subscription.objects.create(**form.cleaned_data)

    messages.success(request, 'Inscrição realizada com sucesso!')
    return HttpResponseRedirect('/inscricao/')


def new(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscriptions_form.html', context)


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context, subject)
    mail.send_mail(subject, body, from_, [from_, to])
