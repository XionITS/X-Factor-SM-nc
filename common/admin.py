from django.contrib import admin
from .models import XFactor_User
from .models import XFactor_Group
from .models import XFactor_Auth
from .models import XFactor_UserAuth

class Search_XFactor_User(admin.ModelAdmin):
    search_fields = ['User name']

admin.site.register(XFactor_User, Search_XFactor_User)
admin.site.register(XFactor_Group)
admin.site.register(XFactor_Auth)
admin.site.register(XFactor_UserAuth)



# Register your models here.
