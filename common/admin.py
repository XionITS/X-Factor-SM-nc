from django.contrib import admin
from .models import Xfactor_Common
from .models import Xfactor_Group
from .models import Xfactor_Auth
from .models import Xfactor_Xuser_Auth

class Search_Xfactor_Common(admin.ModelAdmin):
    search_fields = ['User name']

admin.site.register(Xfactor_Common, Search_Xfactor_Common)
admin.site.register(Xfactor_Group)
admin.site.register(Xfactor_Auth)
admin.site.register(Xfactor_Xuser_Auth)



# Register your models here.
