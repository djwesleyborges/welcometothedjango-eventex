from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect, Http404
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

    subscription = Subscription.objects.create(**form.cleaned_data)
    _send_mail(subject='Confirmação de Inscrição', from_=settings.DEFAULT_FROM_EMAIL, to=subscription.email,
               template_name='subscriptions/subscription_email.txt', context={'subscription': subscription})

    return HttpResponseRedirect(f'/inscricao/{subscription.pk}/')


def new(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscriptions_form.html', context)


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404
    return render(request=request, template_name='subscriptions/subscription_detail.html',
                  context={'subscription': subscription})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
