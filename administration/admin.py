from django.contrib import admin

from administration.models import Department, Employment, Position
from logger.models import CustomLogEntry


class EmploymentInline(admin.TabularInline):
    model = Employment
    extra = 0
    # fields = ('user', 'position', 'is_head', 'is_active', )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = (EmploymentInline, )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    inlines = (EmploymentInline, )


@admin.register(CustomLogEntry)
class CustomLogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = ['user', 'content_type', 'action_flag', ]

    search_fields = ['object_repr', 'change_message', ]

    list_display = ['action_time', 'user', 'content_type', 'action_flag', ]
