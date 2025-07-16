from django.contrib import admin

# Register your models here.
from .models import Siparis, SipPerCapita, SipDensityPerHood  # Example table

admin.site.register(Siparis)
admin.site.register(SipPerCapita)
admin.site.register(SipDensityPerHood)