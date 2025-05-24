from django.contrib import admin

# Register your models here
from .models import Departments, Courses, CourseGroup, Assignments, AssignmentSubmissions, resources

admin.site.register(Departments)
admin.site.register(Courses)
admin.site.register(CourseGroup)
admin.site.register(Assignments)
admin.site.register(AssignmentSubmissions)
admin.site.register(resources)
                    