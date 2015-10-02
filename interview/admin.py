from django.contrib import admin

from interview.models import Interview, TypeInterElem, InterElem

admin.site.register(Interview)
admin.site.register(InterElem)
admin.site.register(TypeInterElem)
