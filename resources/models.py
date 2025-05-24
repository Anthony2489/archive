from django.db import models
from student.models import Student

# Create your models here.

class Departments(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Departments"
        ordering = ['name']

class Courses(models.Model):
    course_code = models.CharField(max_length=5, unique=True, primary_key=True)
    course_name = models.CharField(max_length=100, unique=True)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(blank=True, null=True)
    credits = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #instructor = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.course_name} ({self.course_code})"

    class Meta:
        verbose_name_plural = "Courses"
        ordering = ['course_name']

class CourseGroup(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='groups')
    group_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.group_name} - {self.course.course_name}"

    class Meta:
        verbose_name_plural = "Course Groups"
        ordering = ['group_name']

class Assignments(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(CourseGroup, max_length=50, blank=True, null=True, on_delete=models.CASCADE)
    course_id= models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    version = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('custom.User', on_delete=models.CASCADE, related_name='assignments_created', blank=True, null=True)
    updated_by = models.ForeignKey('custom.User', on_delete=models.CASCADE, related_name='assignments_updated', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    max_score = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.title} - {self.course.course_name}"

    class Meta:
        verbose_name_plural = "Assignments"
        ordering = ['due_date']

class AssignmentSubmissions(models.Model):
    id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submission_date = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(default=0)
    feedback = models.TextField(blank=True, null=True)
    is_graded = models.BooleanField(default=False)
    attempt_number = models.PositiveIntegerField(default=1)
    file_checksum = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.assignment.title} - {self.student.user.username}"

    class Meta:
        verbose_name_plural = "Assignment Submissions"
        ordering = ['submission_date']

class resources(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(CourseGroup, max_length=50, blank=True, null=True, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='resources')
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.CharField(max_length=50)  # e.g., 'document', 'video', 'link'
    resource_url = models.URLField(max_length=200, blank=True, null=True)
    resource_file = models.FileField(upload_to='resources/', blank=True, null=True)
    uploaded_by = models.ForeignKey('custom.User', on_delete=models.CASCADE, related_name='resources_uploaded', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.resource_type} - {self.course_id.course_name} - {self.assignment.title}"
    class Meta:
        verbose_name_plural = "Resources"
        ordering = ['uploaded_at']

