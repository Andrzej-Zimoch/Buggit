from django.contrib import admin
from .models import( Project,Ticket,Team,Profile)




class TeamAdminInLine(admin.TabularInline):
    model=Team
class TeamAdmin(admin.ModelAdmin):
    list_display=("name",)

class ProjectAdmin(admin.ModelAdmin):
    list_display=("name",)

class TicketAdmin(admin.ModelAdmin):
    list_display=("name",)

# Register your models here.
admin.site.register(Profile)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Ticket,TicketAdmin)

admin.site.register(Team,TeamAdmin)


