from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Course)
admin.site.register(Classes)
admin.site.register(Session_Year)
admin.site.register(Student)
admin.site.register(Section)
admin.site.register(Staff)
admin.site.register(SchoolSubjects)
admin.site.register(CollegeSubjects)
admin.site.register(Stafftype)
admin.site.register(Staff_Notification)
admin.site.register(Staff_Leave)
admin.site.register(Staff_Feedback)
admin.site.register(Student_Notification)
admin.site.register(Student_Feedback)
admin.site.register(Student_Leave)
admin.site.register(Attendence)
admin.site.register(Attendence_Report)
admin.site.register(SchoolTeacher)
admin.site.register(CollegeTeacher)
admin.site.register(StudentResult)
# admin.site.register(ClassRoutine)
admin.site.register(RoutineSubjects)
admin.site.register(Period)
admin.site.register(Notice)
admin.site.register(webNotice)
admin.site.register(admissionForm)

