from django.contrib import admin

from api.models.delivery_address import DeliveryAddress
from api.models.email_verification import ECOMEmailVerification
from api.models.user import ECOMUser

admin.site.register(ECOMUser)
admin.site.register(DeliveryAddress)
admin.site.register(ECOMEmailVerification)
