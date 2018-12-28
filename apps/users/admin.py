from django.contrib import admin
from .models import UserProfile
from users.models import *

# Register your models here.

admin.site.register(EmailVerifyRecord)
admin.site.register(Banner)
admin.site.register(UserProfile)

