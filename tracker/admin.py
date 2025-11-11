from django.contrib import admin
from .models import Student, Performance


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name', 'roll_no', 'gender')
    search_fields = ('name', 'roll_no')
    list_filter = ('class_name', 'gender')


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'subject', 'score', 'attendance', 'term', 'date_recorded'
    )
    search_fields = ('student__name', 'subject')
    list_filter = ('subject', 'term', 'date_recorded')
    date_hierarchy = 'date_recorded'
