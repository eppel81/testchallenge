from django.contrib import admin

from interview.models import Interview, InterElem, DoneInterview

class ElemInline(admin.TabularInline):
    model = InterElem
    extra = 1

class InterviewAdmin(admin.ModelAdmin):
    inlines = [ElemInline]


# class DoneInterviewAdmin(admin.ModelAdmin):
#     fields = [ elem_interview, user_id, response, user_meta]

admin.site.register(Interview, InterviewAdmin)
admin.site.register(InterElem)
admin.site.register(DoneInterview)

# admin.site.register(TypeInterElem)
