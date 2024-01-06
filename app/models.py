from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings


# Create your models here.


class CustomUser(AbstractUser):
    USER = (
        ('1', 'HOD'),
        ('2', 'STAFF'),
        ('3', 'STUDENT'),      
        ('4', 'STAFF2'),      
    )

    user_type = models.CharField(choices=USER, max_length=10, default=1)
    profile_pic = models.ImageField(upload_to='profile_pic/User', default="profile_pic/User/user.png")


class Course(models.Model):
    name = models.CharField(max_length=50, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.name
    
    
    




class Session_Year(models.Model):
    session_start = models.CharField(max_length=10, default="")
    session_end = models.CharField(max_length=10, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.session_start + " to " + self.session_end


class Classes(models.Model):
    name = models.CharField(max_length=4, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.name



class Stafftype(models.Model):
    name = models.CharField(max_length=50, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.name



class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, default="", null=True)
    date_of_birth = models.DateField(null=True)
    birth_certificate = models.CharField(max_length=50 , default="", null=True)
    religion = models.CharField(max_length=20, default="", null=True)
    joining_date = models.DateField(null=True)
    mobile_number = models.CharField(max_length=15, default="", null=True)
    present_address = models.TextField(default="", null=True)
    permanent_address = models.TextField(default="", null=True)
    staff_type = models.ForeignKey(Stafftype, on_delete=models.CASCADE, default="", null=True)
    blood_group = models.CharField(max_length=10, default="", null=True)
    qualification = models.CharField(max_length=20, default="", null=True)
    nid = models.CharField(max_length=20, default="")
    
    fathers_name = models.CharField(max_length=50, default="", null=True)
    mothers_name = models.CharField(max_length=50, default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name
    




class SchoolTeacher(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name_eng = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=10, default="", null=True)
    date_of_birth = models.DateField()
    birth_certificate = models.CharField(max_length=50 , default="", null=True)
    religion = models.CharField(max_length=20)
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    present_address = models.TextField()
    permanent_address = models.TextField()
    staff_type = models.ForeignKey(Stafftype, on_delete=models.DO_NOTHING, default="", null=True)
    blood_group = models.CharField(max_length=10)
    qualification = models.CharField(max_length=50)
    nid = models.CharField(max_length=20, default="")
    fathers_name = models.CharField(max_length=50)
    mothers_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, default="", null=True)
    short_name = models.CharField(max_length=10)
    sallery = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.admin.username

    



# Define the CollegeTeacher model
class CollegeTeacher(Staff):
    department = models.CharField(max_length=50, default="", null=True)
    academic_rank = models.CharField(max_length=20, default="", null=True)
    sallery = models.IntegerField(default=0, null=True)
    short_name = models.CharField(max_length=20, default="", null=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name + " (College Teacher)"


class Section(models.Model):
    section_name = models.CharField(max_length=50, default="",null=True,)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default="", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default="", null=True)
    teacher_id = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True, related_name='sections_taught')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.section_name

    



class Student(models.Model):
    
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default="", null=True)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    name_eng = models.CharField(max_length=50, default="")
    student_id = models.CharField(max_length=20, unique=True, default="")
    roll = models.CharField(max_length=20, unique=True, default="")
    session_year_id = models.ForeignKey(Session_Year, on_delete=models.DO_NOTHING, default="")
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, default="")
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, default="")
    gender = models.CharField(max_length=10, default="")
    date_of_birth = models.DateField()
    class_name = models.ForeignKey(Classes, on_delete=models.DO_NOTHING, default="")
    religion = models.CharField(max_length=20, default="")
    mobile_number = models.CharField(max_length=15, default="")
    attendence_status = models.IntegerField(default=0, null=True)
    attendence_date = models.DateField(null=True)
    update_status = models.IntegerField(default=0, null=True)
    
    fathers_name = models.CharField(max_length=50, default="")
    fathers_mobile = models.CharField(max_length=15, default="")
    fathers_email = models.EmailField(default="")
    mothers_name = models.CharField(max_length=50, default="")
    mothers_mobile = models.CharField(max_length=15, default="")
    mothers_email = models.EmailField(default="")
    present_address = models.TextField(default="")
    permanent_address = models.TextField(default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name







class SchoolSubjects(models.Model):
    name = models.CharField(max_length=50, default="")
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE, default="")
    teacher = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.name
     
     
     
class CollegeSubjects(models.Model):
    name = models.CharField(max_length=50, default="")
    teacher = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.name
     




class Staff_Notification(models.Model):
    school_teacehr_id = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.staff_id.admin.first_name


    
    
    
class Student_Notification(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default="")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.student_id.admin.first_name




class Staff_Leave(models.Model):
    school_teacher_id = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="")
    data = models.CharField(max_length=50, default="")
    message = models.TextField()
    status = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.staff_id.admin.first_name + " " + self.staff_id.admin.last_name
     
     
     
class Staff_Feedback(models.Model):
    school_teacher_id = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.staff_id.admin.first_name + ' ' + self.staff_id.admin.first_name


class Student_Feedback(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.student_id.admin.first_name + ' ' + self.student_id.admin.first_name
    
    
class Student_Leave(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, default="")
    data = models.CharField(max_length=50, default="")
    message = models.TextField()
    status = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.student_id.admin.first_name + " " + self.student_id.admin.last_name
    

class Attendence(models.Model):
    section_id = models.ForeignKey(Section, on_delete=models.DO_NOTHING, default="")
    session_year_id = models.ForeignKey(Session_Year, on_delete=models.DO_NOTHING, default="")
    attendence_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.section_id) + " " + str(self.attendence_date)
    
    
class Attendence_Report(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendence_id = models.ForeignKey(Attendence, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.student_id.admin.first_name) + "  " + str(self.attendence_id.attendence_date)
    

    
# class ResultPlan(models.Model):
#     subject = models.ForeignKey(SchoolSubjects, on_delete=models.CASCADE, default="", null=True)
#     pi_no = models.CharField(max_length=20, default="", null=True)
#     pi_name = models.CharField(max_length=20, default="", null=True)
#     bi_name = models.CharField(max_length=20, default="", null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#          return str(self.pi_no)


'''
class StudentResult(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(SchoolSubjects, on_delete=models.CASCADE)
    result = models.ForeignKey(ResultPlan, on_delete=models.CASCADE, default="", null=True)
    pi_no = models.CharField(max_length=20, default="", null=True)
    grade = models.CharField(default=0, null=True, max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.student_id.admin.first_name) + "  " + str(self.subject_id.name)
'''


class StudentResult(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    session_year_id = models.ForeignKey(Session_Year, on_delete=models.CASCADE, default="", null=True)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE, default="", null=True)
    result = models.CharField(default=0, null=True, max_length=50)
    result_link = models.CharField(default="#", max_length=500)

    def __str__(self):
        return str(self.student_id.admin.first_name) + "  " + str(self.class_id)



class Period(models.Model):
    name = models.CharField(max_length=10, default="", null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    
    def __str__(self):
        return str(self.name)+ "  " + str(self.start_time)+ "  " + str(self.end_time)
    



class RoutineSubjects(models.Model):
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE, default="", null=True)
    session_year_id = models.ForeignKey(Session_Year, on_delete=models.CASCADE, default="", null=True)
    class_day = models.CharField(max_length=10 ,default="", null=True)
    
    
    first_subject = models.ForeignKey(SchoolSubjects, on_delete=models.CASCADE, default="", null=True, related_name='first_subject')
    fitst_subject_teacher = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True, related_name='first_subject_teacher')
    first_period = models.ForeignKey(Period, on_delete=models.CASCADE, default="", null=True, related_name='first_period')
    
    second_subject = models.ForeignKey(SchoolSubjects, on_delete=models.CASCADE, default="", null=True, related_name='second_subject')
    second_subject_teacher = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True, related_name='second_subject_teacher')
    second_period = models.ForeignKey(Period, on_delete=models.CASCADE, default="", null=True, related_name='second_period')
    
    
    third_subject = models.ForeignKey(SchoolSubjects, on_delete=models.CASCADE, default="", null=True, related_name='third_subject')
    third_subject_teacher = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True, related_name='third_subject_teacher')
    third_period = models.ForeignKey(Period, on_delete=models.CASCADE, default="", null=True, related_name='third_period')
    
    
    
    fourth_subject = models.ForeignKey(SchoolSubjects, on_delete=models.CASCADE, default="", null=True, related_name='fourth_subject')
    fourth_subject_teacher = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True, related_name='fourth_subject_teacher')
    fourth_period = models.ForeignKey(Period, on_delete=models.CASCADE, default="", null=True, related_name='fourth_period')
    
    fifth_subject = models.ForeignKey(SchoolSubjects, on_delete=models.CASCADE, default="", null=True, related_name='fifth_subject')
    fifth_subject_teacher = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True, related_name='fifth_subject_teacher')
    fifth_period = models.ForeignKey(Period, on_delete=models.CASCADE, default="", null=True, related_name='fifth_period')
    
    
    sixth_subject = models.ForeignKey(SchoolSubjects, on_delete=models.CASCADE, default="", null=True, related_name='sixth_subject')
    sixth_subject_teacher = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True, related_name='sixth_subject_teacher')
    sixth_period = models.ForeignKey(Period, on_delete=models.CASCADE, default="", null=True, related_name='sixth_period')
    
    
    seventh_subject = models.ForeignKey(SchoolSubjects, on_delete=models.CASCADE, default="", null=True, related_name='seventh_subject')
    seventh_subject_teacher = models.ForeignKey(SchoolTeacher, on_delete=models.CASCADE, default="", null=True, related_name='seventh_subject_teacher')
    seventh_period = models.ForeignKey(Period, on_delete=models.CASCADE, default="", null=True, related_name='seventh_period')
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.section_id)
    
    
    
class Notices(models.Model):
    headline = models.CharField(max_length=20, default="", null=True)
    notice = models.TextField(default="", null=True)
    notice_link = models.CharField(default="", null=True, max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


    def __str__(self):
        return str(self.headline)



class admissionForm(models.Model):
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE, default="", null=True)
    form_name = models.CharField(max_length=200, default="", null=True)
    form_link = models.TextField(default="", null=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.form_name + " " + str(self.class_name))