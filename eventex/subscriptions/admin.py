from django.contrib import admin
from django.utils.timezone import now

from eventex.subscriptions.models import Subscription


class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'cpf', 'created_at',
                    'subscribed_today')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'email', 'phone', 'cpf', 'created_at',)
    list_filter = ('created_at',)

    @admin.display(description='inscrito hoje ?', boolean=True)
    def subscribed_today(self, obj):
        return obj.created_at == now().date()


admin.site.register(Subscription, SubscriptionModelAdmin)
