from django.contrib import admin
from .models import Search, ProfileInfo, GroupInfo, Result

admin.site.register(Search)
admin.site.register(ProfileInfo)
admin.site.register(GroupInfo)
admin.site.register(Result)