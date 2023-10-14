from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
import csv
from app.models import *
from django.contrib import messages
import pandas as pd
from django.http import JsonResponse
from datetime import datetime, timezone
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import re
import os




#===================================    EMAIL CHECKER    =====================================

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_email(email):
    if(re.fullmatch(regex, email)):
        return 1
    else:
        return 0



def oops(request):
    return render(request, 'oops.html')





@login_required(login_url='login')
def admin_home(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = SchoolSubjects.objects.all().count()
    notice_obj = Notice.objects.all()[:5]

    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()
    
    

    context = {
        "student_count":student_count,
        "staff_count":staff_count,
        "course_count":course_count,
        "subject_count":subject_count,
        "student_gender_male":student_gender_male,
        "student_gender_female":student_gender_female,
        "notice_obj" : notice_obj,
        
    }

    return render(request,"hod/home.html", context)





@login_required(login_url='login')
def addStudent(request):

    student_obj = Student.objects.all()
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    customuser = CustomUser.objects.all()
    section_obj = Section.objects.all()
    class_obj = Classes.objects.all()


    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        roll = request.POST.get('roll')
        session_year_id = request.POST.get('session_year_id')
        course_id = request.POST.get('course_id')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        class_name = request.POST.get('class_name')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section_id = request.POST.get('section')
        fathers_name = request.POST.get('fathers_name')
        fathers_mobile = request.POST.get('fathers_mobile')
        fathers_email = request.POST.get('fathers_email')
        mothers_name = request.POST.get('mothers_name')
        mothers_mobile = request.POST.get('mothers_mobile')
        mothers_email = request.POST.get('mothers_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        profile_pic = request.FILES.get('profile_pic')
        username=str(first_name+"  ( Student )")
        password="student"
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f"{email} - Email Already Exists")
            return redirect('add_student')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, f"{first_name}__student - Username Already Exists.")
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3
            )
            
            user.set_password(password)
            user.save()

            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)
            section = Section.objects.get(id=section_id)
            class_id = Classes.objects.get(id=class_name)
            student_data = Student(
                admin=user,
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                roll=roll,
                session_year_id=session_year,
                course_id=course,
                gender = gender,
                date_of_birth= date_of_birth,
                class_name= class_id,
                religion= religion,
                joining_date= joining_date,
                mobile_number= mobile_number,
                admission_number= admission_number,
                section= section,
                fathers_name= fathers_name,
                fathers_mobile= fathers_mobile,
                fathers_email= fathers_email,
                mothers_name= mothers_name,
                mothers_mobile= mothers_mobile,
                mothers_email= mothers_email,
                present_address= present_address,
                permanent_address= permanent_address,
                update_status = 0,

            )
            student_data.save()
            messages.success(request, f"{first_name} {last_name} Added Successfully")
            return redirect('add_student')



    context = {
        "student_obj":student_obj,
        "courses":course,
        "session_years":session_year,
        "section_obj":section_obj,
        'class_obj' : class_obj,
    }

    return render(request,"Hod/add_student.html", context)




@login_required(login_url='login')
def viewStudent(request):
    student_obj = Student.objects.all()
    context = {
        "student_obj":student_obj,
    }
    return render(request,"Hod/view_student.html", context)





@login_required(login_url='login')
def editStudent(request, id):
    student = Student.objects.filter(id=id)
    section_obj = Section.objects.all()
    session_year = Session_Year.objects.all()
    course = Course.objects.all()
    class_obj = Classes.objects.all()


    context = {
        "student":student,
        "section_obj":section_obj,
        "session_year":session_year,
        "course":course,
        'class_obj':class_obj,
    }
    
    return render(request, 'hod/edit_student.html', context)

@login_required(login_url='login')
def updateStudent(request):
    if request.method == "POST":
        customUserId = request.POST.get('customUserId')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        roll = request.POST.get('roll')
        session_year_id = request.POST.get('session_year_id')
        course_id = request.POST.get('course_id')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        class_id = request.POST.get('class_id')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        password=request.POST.get('password')
        admission_number = request.POST.get('admission_number')
        section_id = request.POST.get('section')
        fathers_name = request.POST.get('fathers_name')
        fathers_mobile = request.POST.get('fathers_mobile')
        fathers_email = request.POST.get('fathers_email')
        mothers_name = request.POST.get('mothers_name')
        mothers_mobile = request.POST.get('mothers_mobile')
        mothers_email = request.POST.get('mothers_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        profile_pic = request.FILES.get('profile_pic')
        username=str(first_name+"__student")



        student = Student.objects.get(admin=customUserId)
        student.first_name=first_name
        student.last_name=last_name
        student.student_id=student_id
        student.roll=roll

        course = Course.objects.get(id=course_id)
        student.course_id=course
        # if course_id != None and course_id != "":
        
        session = Session_Year.objects.get(id=session_year_id)
        student.session_year_id=session
        # if session != None and session != "":
        
        section = Section.objects.get(id=section_id)
        student.section=section
        # if section_id != None and section_id != "":
        
        classes = Classes.objects.get(id=class_id)
        student.name = classes

        
        if gender != None and gender != "":
            student.gender = gender

        if date_of_birth != None and date_of_birth != "":
            student.date_of_birth = date_of_birth

    
        student.religion = religion

        if joining_date != None and joining_date != "":
            student.joining_date = joining_date

        student.mobile_number = mobile_number
        student.password = password
        student.admission_number = admission_number
        student.section_id = section_id
        student.fathers_name = fathers_name
        student.fathers_mobile = fathers_mobile
        student.fathers_email = fathers_email
        student.mothers_name = mothers_name
        student.mothers_mobile = mothers_mobile
        student.mothers_email = mothers_email
        student.present_address = present_address
        student.permanent_address = permanent_address
        student.profile_pic = profile_pic
        student.username = username

        student.save()
        
        
        user = CustomUser.objects.get(id=customUserId)
        user.first_name=first_name
        user.last_name=last_name
        user.username=username
        user.email=email
        if profile_pic != None and profile_pic != "":
            user.profile_pic=profile_pic
        if password != None and password != "":
            user.set_password(password)
        user.save()
        
        
        messages.success(request, f"{first_name} {last_name} Updated Successfully")
        return redirect('view_student')
    return render (request, 'hod/edit_student.html')




@login_required(login_url='login')
def deleteStudent(request, admin):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            student = CustomUser.objects.get(id=admin)

            # Handle foreign key relationships before deleting
            # Example: Set related foreign key references to None
            student.class_name = None
            student.save()

            student.delete()
            messages.success(request, f"{student.first_name} {student.last_name} Deleted Successfully")
            return redirect('view_student')
        else:
            messages.error(request, "Please Type CONFIRM to Delete Student")
            return redirect('view_student')

    
    

@login_required(login_url='login')
def approveStudent(request, id):
    student = Student.objects.get(id=id)
    student.update_status = 1
    student.save()
    messages.success(request, f"{student.admin.first_name} {student.admin.last_name} Approved Successfully")
    return redirect('view_student')



@login_required(login_url='login')
def downloadStudentCsv(request):
    # Replace 'queryset' with the actual queryset you want to export as CSV (e.g., Student.objects.all())
    student_obj = Student.objects.all()
    data = []
    
    for i in student_obj:
        Date_of_Birth = str(i.date_of_birth)
        Joining = str(i.joining_date)
        Create = str(i.created_at)
        Update = str(i.updated_at)
        
        data.append({
            'id': i.student_id,
            'Name': i.first_name  + i.last_name,
            'Roll': i.roll,
            'Class' : i.class_name,
            'Section' : i.section,
            'Session Year': i.session_year_id,
            'Course': i.course_id,
            'Mobile Number' : i.mobile_number,
            'Gender' : i.gender,
            'Date of Birth' : Date_of_Birth,
            'Religion' : i.religion,
            'Joining Date' : Joining,
            'Admission Number' : i.admission_number,
            'Fathers Name' : i.fathers_name,
            'Fathers Mobile' : i.fathers_mobile,
            'Fathers Email' : i.fathers_email,
            'Mothers Name' : i.mothers_name,
            'Mothers Mobile' : i.mothers_mobile,
            'Mothers Email' : i.mothers_email,
            'Present Address' : i.present_address,
            'Permanent Address' : i.permanent_address,
            'Created At' : Create,
            'Updated At' : Update
            
        })
                # Define the folder path where you want to save the file
    folder_path = os.path.join(os.path.expanduser("~"), "Downloads")  # For PC
    # For Android, you may need to specify a different path

    # Ensure the folder exists, create it if it doesn't
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    excel_file_path = os.path.join(folder_path, 'student.xlsx')
        
    pd.DataFrame(data).to_excel(excel_file_path)
    messages.success(request, "Student Data Downloaded Successfully")
    return redirect('view_student')

    
    
    
    
    
    
    
    
    
    

# course start here ===========================================================================

@login_required(login_url='login')
def addCourse(request):
    if request.method=='POST':
        course_name=request.POST.get('course_name')
        course = Course(
            name=course_name
        )
        course.save()
        messages.success(request, f"{course_name} Added Successfully")
        return redirect('add_course')

    return render(request, 'hod/add_course.html')



@login_required(login_url='login')
def viewCourse(request):
    course_obj = Course.objects.all()
    context={
        "course_obj":course_obj,
    }

    return render(request, 'hod/view_course.html', context)



@login_required(login_url='login')
def editCourse(request, id):
    course = Course.objects.filter(id=id)

    context = {
        "course":course,
    }

    return render(request, 'hod/edit_course.html', context)




@login_required(login_url='login')
def updateCourse(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')

        course = Course.objects.get(id=course_id)
        course.name = course_name
        course.save()

        messages.success(request, f"{course_name} Updated Successfully!")

        return redirect('view_Course')


    return render(request, 'hod/edit_course.html')



@login_required(login_url='login')
def deleteCourse(request, id):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            course = Course.objects.get(id=id)
            course.delete()
            messages.success(request, f"{course.name} Deleted Successfully!")

            return redirect('view_Course')
        else:
            messages.error(request, "Please Type CONFIRM to Delete Course")
            return redirect('view_Course')




#===================================    STAFF START HERE    =====================================

@login_required(login_url='login')
def addStaff(request):
    staff_type_obj = Stafftype.objects.all()

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        birth_certificate_no = request.POST.get('birth_certificate_no')
        blood_group = request.POST.get('blood_group')
        Qualification = request.POST.get('Qualification')
        nid_no = request.POST.get('nid_no')
        permanent_address = request.POST.get('permanent_address')
        present_address = request.POST.get('present_address')
        gender = request.POST.get('gender')
        joining_date = request.POST.get('joining_date')
        religion = request.POST.get('religion')
        mobile_number = request.POST.get('mobile_number')
        staff_type_id = request.POST.get('staff_type')
        fathers_name = request.POST.get('fathers_name')
        mothers_name = request.POST.get('mothers_name')

        profile_pic = request.FILES.get('profile_pic')
        username = str(first_name + " (Staff)")
        password = "staff"

        staff_type = Stafftype.objects.get(id=staff_type_id)

        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f"{email} - Email Already Exists")
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, f"{first_name}_staff - Username Already Exists.")
            return redirect('add_staff')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=4
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
                gender=gender,
                date_of_birth = date_of_birth,
                birth_certificate = birth_certificate_no,
                religion = religion,
                joining_date = joining_date,
                mobile_number = mobile_number,
                present_address = present_address,
                permanent_address = permanent_address,
                staff_type = staff_type,
                blood_group = blood_group,
                qualification = Qualification,
                nid = nid_no,
                fathers_name = fathers_name,
                mothers_name = mothers_name,
                
            )
            staff.save()
            messages.success(request, f"{first_name} {last_name} Added Successfully")
            return redirect('add_staff')
    
    
    
    context = {
        "staff_type_obj":staff_type_obj,
    }

    return render(request, 'hod/add_staff.html', context)



@login_required(login_url='login')
def downloadStaffxlsx(request):
    # Replace 'queryset' with the actual queryset you want to export as CSV (e.g., Student.objects.all())
    staff_obj = Staff.objects.all()
    data = []
    
    for i in staff_obj:
        Date_of_Birth = str(i.date_of_birth)
        Joining = str(i.joining_date)
        Create = str(i.created_at)
        Update = str(i.updated_at)
        
        data.append({

            'name' : i.admin.first_name + i.admin.last_name,
            'email' : i.admin.email,
            'Gender': i.gender,
            'Qualification' : i.qualification,
            "Date of Birth" : Date_of_Birth,
            'Birth Certificate' : i.birth_certificate,
            'Religion' : Joining,
            'Mobile Number' : i.mobile_number,
            'Present Address' : i.present_address,
            'Permanent Address' :i.permanent_address,
            'Staff Type' : i.staff_type,
            'Blood Group' : i.blood_group,
            'NID' : i.nid,
            'Fathers Name' : i.fathers_name,
            'Mothers Name' : i.mothers_name,
            
        })
        
        # Define the folder path where you want to save the file
    folder_path = os.path.join(os.path.expanduser("~"), "Downloads")  # For PC
    # For Android, you may need to specify a different path

    # Ensure the folder exists, create it if it doesn't
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    excel_file_path = os.path.join(folder_path, 'staff.xlsx')
        
    pd.DataFrame(data).to_excel(excel_file_path)
    messages.success(request, "Staff Data Downloaded Successfully")
    return redirect('view_staff')




@login_required(login_url='login')
def staffView(request):
    staff_obj = Staff.objects.all()

    context = {
        "staff_obj":staff_obj,
    }


    return render(request, 'hod/view_staff.html', context)





@login_required(login_url='login')
def editStaff(request, id):
    staff = Staff.objects.filter(id=id)
    staff_type = Stafftype.objects.all()
    

    get_gender = None
    get_date_of_birth = None
    get_birth_certificate = None
    get_religion = None
    get_joining_date = None
    get_staff_type = None
    for i in staff:
        get_gender = i.gender
        get_date_of_birth = i.date_of_birth
        get_joining_date = i.joining_date
        get_staff_type = i.staff_type
        get_staff_type_id = i.staff_type.id



    context = {
        "staff":staff,
        "staff_type" : staff_type,
        'get_gender' : get_gender,
        'get_date_of_birth' : get_date_of_birth,
        'get_joining_date' : get_joining_date,
        'get_staff_type' : get_staff_type,
        'get_staff_type_id' : get_staff_type_id,
    }
    
    return render(request, 'hod/edit_staff.html', context)




@login_required(login_url='login')
def updateStaff(request):

    if request.method == "POST":
        staffAdminId = request.POST.get('staffAdminId')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        joining_date = request.POST.get('joining_date')
        birth_certificate_no = request.POST.get('birth_certificate_no')
        blood_group = request.POST.get('blood_group')
        qualification = request.POST.get('Qualification')
        nid_no = request.POST.get('nid_no')
        fathers_name = request.POST.get('fathers_name')
        mothers_name = request.POST.get('mothers_name')
        permanent_address = request.POST.get('permanent_address')
        present_address = request.POST.get('present_address')
        religion = request.POST.get('religion')
        mobile_number = request.POST.get('mobile_number')
        staff_type = request.POST.get('staff_type')
        gender = request.POST.get('gender')
        profile_pic = request.FILES.get('profile_pic')
        username = str(first_name + "_staff")
        password = request.POST.get('password')

        staff_type = Stafftype.objects.get(id=staff_type)
        
        user = CustomUser.objects.get(id=staffAdminId)

        if staff_type == None and date_of_birth == None and joining_date==None:
            messages.error(request, "Please Select Staff Type, Date of Birth and Joining Date")
            return redirect('edit_staff')
        else:
            if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic
            if password != None and password != "":
                user.set_password(password)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            staff = Staff.objects.get(admin=staffAdminId)
            staff = Staff.objects.get(admin=staffAdminId)
            staff.gender = gender
            staff.date_of_birth= date_of_birth
            staff.birth_certificate = birth_certificate_no
            staff.religion = religion
            staff.joining_date = joining_date
            staff.mobile_number = mobile_number
            staff.present_address = present_address
            staff.permanent_address = permanent_address
            staff.staff_type = staff_type
            staff.blood_group = blood_group
            staff.qualification = qualification
            staff.nid = nid_no
            
            staff.fathers_name = fathers_name
            staff.mothers_name = mothers_name
            staff.save()
            messages.success(request, f"{first_name} {last_name} Updated Successfully")

            return redirect('view_staff')

    return render(request, 'hod/edit_staff.html')




@login_required(login_url='login')
def deleteStaff(request, id):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            staff = CustomUser.objects.get(id=id)
            staff.delete()
            messages.success(request, f"{staff.first_name} {staff.last_name} Deleted Successfully")

        else:
            messages.error(request, "Please Type CONFIRM to Delete Staff")
            return redirect('view_staff')
    
    return redirect('view_staff')







# School Teacher start here ===========================================================================
@login_required(login_url='login')
def viewSchoolTeacher(request):
    school_teacher_obj = SchoolTeacher.objects.all()
    
    context = {
        "school_teacher_obj":school_teacher_obj,
    }
    return render(request, 'hod/view_school_teacher.html', context)




@login_required(login_url='login')
def addSchoolTeacher(request):
    section_obj = Section.objects.all()
    staff_type = Stafftype.objects.all()
    course_obj = Course.objects.all()
    
    context = {
        "section_obj":section_obj,
        'staff_type':staff_type,
        'course_obj':course_obj,
    }
    return render(request, 'hod/add_school_teacher.html', context)


@login_required(login_url='login')
def saveSchoolTeacher(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        birth_certificate_no = request.POST.get('birth_certificate_no')
        blood_group = request.POST.get('blood_group')
        Qualification = request.POST.get('Qualification')
        nid_no = request.POST.get('nid_no')
        permanent_address = request.POST.get('permanent_address')
        present_address = request.POST.get('present_address')
        gender = request.POST.get('gender')
        joining_date = request.POST.get('joining_date')
        religion = request.POST.get('religion')
        mobile_number = request.POST.get('mobile_number')
        staff_type_id = request.POST.get('staff_type')
        fathers_name = request.POST.get('fathers_name')
        mothers_name = request.POST.get('mothers_name')
        course_id = request.POST.get('course_id')
        short_name = request.POST.get('short_name')
        sallery = request.POST.get('sallery')

        profile_pic = request.FILES.get('profile_pic')
        username = str(first_name + " ( School Teacher )")
        password = "schoolteacher"

        staff_type = Stafftype.objects.get(id=staff_type_id)
        course = Course.objects.get(id=course_id)
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f"{email} - Email Already Exists")
            return redirect('add_school_teacher')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, f"{first_name}_staff - Username Already Exists.")
            return redirect('add_school_teacher')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=2
            )
            user.set_password(password)
            user.save()

            school_teacher = SchoolTeacher(
                admin=user,
                gender=gender,
                date_of_birth = date_of_birth,
                birth_certificate = birth_certificate_no,
                religion = religion,
                joining_date = joining_date,
                mobile_number = mobile_number,
                present_address = present_address,
                permanent_address = permanent_address,
                staff_type = staff_type,
                blood_group = blood_group,
                qualification = Qualification,
                nid = nid_no,
                fathers_name = fathers_name,
                mothers_name = mothers_name,
                short_name = short_name,
                sallery = sallery,
                course=course,
                
            )
            school_teacher.save()
            messages.success(request, f"{first_name} {last_name} Added Successfully")
            return redirect('add_staff')
    

@login_required(login_url='login')
def editSchoolTeacher(request, id):
    school_teacher = SchoolTeacher.objects.filter(id=id)
    section_obj = Section.objects.all()
    staff_type = Stafftype.objects.all()
    course_obj = Course.objects.all()


    get_date_of_birth = None
    get_joining_date = None
    get_gender = None
    get_teacher_type = None
    get_teacher_type_id = None

    for i in school_teacher:
        get_date_of_birth = i.date_of_birth
        get_joining_date = i.joining_date
        get_gender = i.gender
        get_teacher_type = i.staff_type
        get_teacher_type_id = i.staff_type.id
        
        # print(f"get_date_of_birth : {get_date_of_birth} \nget joining date = {get_joining_date} \nget gender = {get_gender} \nget teacher type = {get_teacher_type}")
        
    
    context = {
        "school_teacher":school_teacher,
        "section_obj":section_obj,
        'staff_type':staff_type,
        'course_obj':course_obj,
        'get_date_of_birth':get_date_of_birth,
        'get_joining_date':get_joining_date,
        'get_gender' : get_gender,
        'get_teacher_type' : get_teacher_type,
        'get_teacher_type_id' : get_teacher_type_id,
    }
    return render(request, 'hod/edit_school_teacher.html', context)




@login_required(login_url='login')
def updateSchoolTeacher(request):


    if request.method == "POST":
        teacherAdminId = request.POST.get('teacherAdminId')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        birth_certificate_no = request.POST.get('birth_certificate_no')
        blood_group = request.POST.get('blood_group')
        qualification = request.POST.get('qualification')
        nid_no = request.POST.get('nid_no')
        permanent_address = request.POST.get('permanent_address')
        present_address = request.POST.get('present_address')
        gender = request.POST.get('gender')
        joining_date = request.POST.get('joining_date')
        religion = request.POST.get('religion')
        mobile_number = request.POST.get('mobile_number')
        staff_type_id = request.POST.get('staff_type')
        fathers_name = request.POST.get('fathers_name')
        mothers_name = request.POST.get('mothers_name')
        course_id = request.POST.get('course_id')
        short_name = request.POST.get('short_name')
        sallery = request.POST.get('sallery')
        password = request.POST.get('password')

        profile_pic = request.FILES.get('profile_pic')
        username = str(first_name + " ( School Teacher )")
        password = password

        staff_type = Stafftype.objects.get(id=staff_type_id)
        course = Course.objects.get(id=course_id)
        user = CustomUser.objects.get(id=teacherAdminId)

        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        if password != None and password != "":
            user.set_password(password)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        school_teacher = SchoolTeacher.objects.get(admin=teacherAdminId)
        school_teacher.gender = gender
        school_teacher.date_of_birth= date_of_birth
        school_teacher.birth_certificate = birth_certificate_no
        school_teacher.religion = religion
        school_teacher.joining_date = joining_date
        school_teacher.mobile_number = mobile_number
        school_teacher.present_address = present_address
        school_teacher.permanent_address = permanent_address
        school_teacher.staff_type = staff_type
        school_teacher.blood_group = blood_group
        school_teacher.qualification = qualification
        school_teacher.nid = nid_no
        
        school_teacher.fathers_name = fathers_name
        school_teacher.mothers_name = mothers_name
        
        school_teacher.course = course
        school_teacher.short_name = short_name
        school_teacher.sallery = sallery
        school_teacher.save()
        messages.success(request, f"{first_name} {last_name} Updated Successfully")

        return redirect('view_school_teacher')

    return render(request, 'hod/edit_staff.html')




from django.core.exceptions import ObjectDoesNotExist
@login_required(login_url='login')
def deleteSchoolTeacher(request, admin):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        school_teacher = CustomUser.objects.get(id=admin)
        if confirm == "CONFIRM":
            school_teacher.delete()
            messages.success(request, f"{school_teacher.first_name} {school_teacher.last_name} Deleted Successfully")

        else:
            messages.error(request, "Please Type CONFIRM to Delete Staff")
            return redirect('view_school_teacher')
    
    return redirect('view_school_teacher')



@login_required(login_url='login')
def downloadSchoolTeacherCsv(request):
    # Replace 'queryset' with the actual queryset you want to export as CSV (e.g., Student.objects.all())
    teacher_obj = SchoolTeacher.objects.all()
    data = []
    
    for i in teacher_obj:
        Date_of_Birth = str(i.date_of_birth)
        Joining = str(i.joining_date)
        Create = str(i.created_at)
        Update = str(i.updated_at)
        
        data.append({

            'name' : i.admin.first_name + i.admin.last_name,
            
            'email' : i.admin.email,
            'Sallery' : i.sallery,
            'Gender': i.gender,
            "Date of Birth" : Date_of_Birth,
            'Birth Certificate' : i.birth_certificate,
            'Religion' : Joining,
            'Mobile Number' : i.mobile_number,
            'Present Address' : i.present_address,
            'Permanent Address' :i.permanent_address,
            'Staff Type' : i.staff_type,
            'Blood Group' : i.blood_group,
            'Qualification' : i.qualification,
            'NID' : i.nid,
            'Fathers Name' : i.fathers_name,
            'Mothers Name' : i.mothers_name,
            'Course' : i.course,
            'Short Name' : i.short_name,
            'Sallery' : i.sallery,
            
        })
        
        # Define the folder path where you want to save the file
    folder_path = os.path.join(os.path.expanduser("~"), "Downloads")  # For PC
    # For Android, you may need to specify a different path

    # Ensure the folder exists, create it if it doesn't
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    excel_file_path = os.path.join(folder_path, 'teacher.xlsx')
        
    pd.DataFrame(data).to_excel(excel_file_path)
    messages.success(request, "Teachers Data Downloaded Successfully")
    return redirect('view_school_teacher')

    
    
    
    
    
    
    



# School Teacher start here ===========================================================================

@login_required(login_url='login')
def addClass(request):
    if request.method == "POST":
        class_name = request.POST.get('class_name')
        class_name = class_name.upper()
        classes = Classes(
            name=class_name,
        )
        classes.save()
        messages.success(request, f"{class_name} Added Successfully")
        return redirect('add_class')

    return render(request, 'hod/add_class.html')



@login_required(login_url='login')
def viewClass(request):
    class_obj = Classes.objects.all()

    context = {
        "class_obj":class_obj,
    }

    return render(request, 'hod/view_class.html', context)





@login_required(login_url='login')
def editClass(request, id):
    class_name = Classes.objects.all()

    context = {
        'class_name' : class_name,
    }

    return render(request, 'hod/edit_class.html', context)



@login_required(login_url='login')
def updateClass(request):
    if request.method == "POST":
        class_id = request.POST.get('class_id')
        class_name = request.POST.get('class_name')

   
        classes = Classes.objects.get(id=class_id)
        classes.name = class_name
        classes.save()
        messages.success(request, f"{class_name} Updated Successfully")
        return redirect('view_class')

    return render(request, 'hod/edit_class.html')




@login_required(login_url='login')
def deleteClass(request, id):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            classes = Classes.objects.get(id=id)
            classes.delete()
            messages.success(request, f"{classes.name} Deleted Successfully")

        else:
            messages.error(request, "Please Type CONFIRM to Delete Class")
            return redirect('view_class')
    
    return redirect('view_class')



@login_required(login_url='login')
def addStaffType(request):
    if request.method == "POST":
        staff_type = request.POST.get('staff_type')

        stafftype = Stafftype(
            name = staff_type,
        )
        stafftype.save()
        messages.success(request, f"{staff_type} Added Successfully")
        return redirect('add_staff_type')


    return render(request, 'hod/add_staff_type.html')





@login_required(login_url='login')
def viewStaffType(request):
    staff_type_obj = Stafftype.objects.all()

    context = {
        "staff_type_obj":staff_type_obj,
    }

    return render(request, 'hod/view_staf_type.html', context)




@login_required(login_url='login')
def editStaffType(request, id):
    staff_type = Stafftype.objects.filter(id=id)

    context = {
        "staff_type":staff_type,
    }

    return render(request, 'hod/edit_staff_type.html', context)



@login_required(login_url='login')
def updateStaffType(request):
    if request.method == "POST":
        staff_type_id = request.POST.get('staff_type_id')
        staff_type = request.POST.get('staff_type')

        stafftype = Stafftype.objects.get(id=staff_type_id)
        stafftype.name = staff_type
        stafftype.save()

        messages.success(request, f"{staff_type} Updated Successfully")

        return redirect('view_staff_type')

    return render(request, 'hod/edit_staff_type.html')



@login_required(login_url='login')
def deleteStaffType(request, id):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            staff_type = Stafftype.objects.get(id=id)
            staff_type.delete()
            messages.success(request, f"{staff_type.name} Deleted Successfully")

        else:
            messages.error(request, "Please Type CONFIRM to Delete Staff")
            return redirect('view_staff_type')
    
    return redirect('view_staff_type')



#===================================    STAFF END HERE    =====================================



#===================================    SUBJECT START HERE    =====================================

@login_required(login_url='login')
def addSubject(request):
    course_obj = Course.objects.all()
    teacher_obj = SchoolTeacher.objects.all()
    class_obj = Classes.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        teacher_id = request.POST.get('teacher_id')
        class_id = request.POST.get('class_name')

        subject_name = str(name+' - '+class_id)
        course = Course.objects.get(id=course_id)
        teacher = SchoolTeacher.objects.get(id=teacher_id)
        classes = Classes.objects.get(id=class_id)

        subject = SchoolSubjects(
            name = subject_name,
            class_name=classes,
            course_id = course,
            teacher = teacher,
        )
        subject.save()
        messages.success(request, f"{name} Added Successfully")

    
    context = {
        "course_obj":course_obj,
        "teacher_obj":teacher_obj,
        'class_obj' : class_obj,
    }

    return render(request, 'hod/add_subject.html', context)


@login_required(login_url='login')
def viewSubject(request):
    subject_obj = SchoolSubjects.objects.all()


    context = {
        "subject_obj":subject_obj,
    }
    return render(request, 'hod/view_subject.html', context)



@login_required(login_url='login')
def editSubject(request, id):
    subject = SchoolSubjects.objects.filter(id=id)
    course_obj = Course.objects.all()
    teacher_obj = SchoolTeacher.objects.all()
    class_obj = Classes.objects.all()

    context = {
        "subject":subject,
        "course_obj":course_obj,
        "teacher_obj":teacher_obj,
        'class_obj' : class_obj,
    }

    return render(request, 'hod/edit_subject.html', context)


@login_required(login_url='login')
def updateSubject(request):
    if request.method=='POST':
        subjectId = request.POST.get('subjectId')
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        teacher_id = request.POST.get('teacher_id')
        class_name = request.POST.get('class_name')

        subject_name = str(name+' - '+class_name)
        course = Course.objects.get(id=course_id)
        teacher = SchoolTeacher.objects.get(id=teacher_id)
        class_id = Classes.objects.get(id=class_name)
        
        subject = SchoolSubjects.objects.get(id=subjectId)
        subject.name = subject_name
        subject.course_id = course
        subject.teacher = teacher
        subject.class_name = class_id
        subject.save()
# name
# class_name
# teacher
# course_id
        messages.success(request, f"{name} Updated Successfully")

        return redirect('view_subject')


@login_required(login_url='login')
def deleteSubject(request, id):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            subject = SchoolSubjects.objects.get(id=id)
            subject.delete()
            messages.success(request, f"{subject.name} Deleted Successfully")

        else:
            messages.error(request, "Please Type CONFIRM to Delete Subject")
            return redirect('view_subject')
    
    return redirect('view_subject')




@login_required(login_url='login')
def deleteStaff(request, id):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            staff = CustomUser.objects.get(id=id)
            staff.delete()
            messages.success(request, f"{staff.first_name} {staff.last_name} Deleted Successfully")

        else:
            messages.error(request, "Please Type CONFIRM to Delete Staff")
            return redirect('view_staff')
    
    return redirect('view_staff')



#===================================    SUBJECT END HERE    =====================================




#===================================    SESSION START HERE    =====================================

@login_required(login_url='login')
def addSession(request):
    session_obj = Session_Year.objects.all()

    if request.method == "POST":
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')

        session = Session_Year(
            session_start = session_start,
            session_end = session_end,
        )

        session.save()
        messages.success(request, f"{session_start} - {session_end} Added Successfully")
        return redirect('add_session')
    

    context = {
        "session_obj":session_obj,
    }
    
    return render(request, 'hod/add_session.html', context)






@login_required(login_url='login')
def viewSession(request):
    session_obj = Session_Year.objects.all()

    context = {
        "session_obj":session_obj,
    }

    return render(request, 'hod/view_session.html', context)




@login_required(login_url='login')
def editSession(request, id):
    session = Session_Year.objects.filter(id=id)
    
    context = {
        "session":session,
    }

    return render(request, 'hod/edit_session.html', context)




@login_required(login_url='login')
def updateSession(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')

        session = Session_Year.objects.get(id=session_id)
        session.session_start = session_start
        session.session_end = session_end
        session.save()

        messages.success(request, f"{session_start} - {session_end} Updated Successfully")
        return redirect('view_session')


    return render(request, 'hod/edit_session.html')




# def deleteSession(request, id):
#     if request.method == 'post':
#         confirm = request.POST.get('confirm')
#         if confirm == "CONFIRM":
#             session = Session_Year.objects.get(id=id)
#             session.delete()
#             messages.success(request, f"{session.session_start} - {session.session_end} Deleted Successfully")
#             return redirect('view_session')

#         else:
#             messages.error(request, "Please Type CONFIRM to Delete Session")
#             return redirect('view_session')
        
#     return render(request, 'hod/view_session.html')

    

@login_required(login_url='login')
def deleteSession(request, id):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            session = Session_Year.objects.get(id=id)
            session.delete()
            messages.success(request, f"{session.session_start} - {session.session_end} Deleted Successfully")

        else:
            messages.error(request, "Please Type CONFIRM to Delete Session")
            return redirect('view_session')
    
    return redirect('view_session')

        
    



# staff start here
@login_required(login_url='login')
def staffNotification(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by("-id")[0:5]

    context = {
        "staff":staff,
        "see_notification":see_notification,
    }

    return render(request, 'hod/staff_notification.html', context)




@login_required(login_url='login')
def saveStaffNotification(request):

    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin=staff_id)
        notification = Staff_Notification(
            staff_id = staff,
            message = message,
        )
        notification.save()
        messages.success(request, f"Notification Sent Successfully")
        return redirect('add_staff_notification')

    return None


@login_required(login_url='login')
def staffLeave(request):
    staff_leave = Staff_Leave.objects.all()

    context = {
        "staff_leave":staff_leave,
    }
    
    return render(request, 'hod/staff_leave.html', context)



@login_required(login_url='login')
def staffApproveLeave(request, id):
    leave = Staff_Leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect("staff_leave")
    



@login_required(login_url='login')
def staffDisapproveLeave(request, id):
    
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            leave = Staff_Leave.objects.get(id=id)
            leave.status = 2
            leave.save()
            return redirect("staff_leave")
    
        else:
            messages.error(request, "Please Type CONFIRM to Disapprove Leave Applications")
            return redirect('staff_leave')
    
    


@login_required(login_url='login')
def staffFeedback(request):
    feedback = Staff_Feedback.objects.all()
    
    context = {
        "feedback":feedback,
    }
    
    return render(request, 'hod/staff_feedback.html', context)



@login_required(login_url='login')
def staffFeedbackSave(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Staff_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        
        messages.success(request, f"Feedback Sent Successfully")
        return redirect('staff_feedback_reply')
    
    
    
@login_required(login_url='login')
def studentNotifications(request):
    student = Student.objects.all()
    student_notification = Student_Notification.objects.all().order_by("-id")[0:5]

    context = {
        "student":student,
        "student_notification":student_notification,
    }

    return render(request, 'hod/student_notification.html', context)



@login_required(login_url='login')
def saveStudentNotification(request):

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')
        

        student = Student.objects.get(admin=student_id)
        notification = Student_Notification(
            student_id = student,
            message = message,
        )
        notification.save()
        messages.success(request, f"Notification Sent Successfully")
        return redirect('student_notifications')

    return render(request, 'hod/student_notification.html')




@login_required(login_url='login')
def studentFeedback(request):
    feedback = Student_Feedback.objects.all()
    
    context = {
        "feedback":feedback,
    }
    
    return render(request, 'hod/student_feedback.html', context)



@login_required(login_url='login')
def studentFeedbackSave(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Student_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        
        messages.success(request, f"Feedback Sent Successfully")
        return redirect('student_feedback_reply')
    
    


@login_required(login_url='login')
def studentLeave(request):
    student_leave = Student_Leave.objects.all()

    context = {
        "student_leave":student_leave,
    }
    
    return render(request, 'hod/student_leave.html', context)




@login_required(login_url='login')
def studentApproveLeave(request, id):

    leave = Student_Leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect("student_leave")



@login_required(login_url='login')
def studentDisapproveLeave(request,id):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            leave = Student_Leave.objects.get(id=id)
            leave.status = 2
            leave.save()
            return redirect("student_leave")
    
        else:
            messages.error(request, "Please Type CONFIRM to Delete Student")
            return redirect('student_leave')
    return render(request, 'hod/student_leave.html')





@login_required(login_url='login')
def viewStudentAttendance(request):
    session_year = Session_Year.objects.all()
    section = Section.objects.all()
    
    action = request.GET.get('action')
    
    get_section=None
    get_date = None
    get_session_year = None
    attendance_report=None
    if action is not None:
        if request.method == 'POST':
            session_year_id = request.POST.get('session_year_id')
            section_id = request.POST.get('section_id')
            date = request.POST.get('date')
            
            get_section = Section.objects.get(id=section_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            get_date = date
            
            attendence = Attendence.objects.filter(section_id=section_id, session_year_id=session_year_id, attendence_date=date)
            for i in attendence:
                attendence = i.id
                attendance_report = Attendence_Report.objects.filter(attendence_id=attendence)

    
    context = {
        'session_year': session_year,
        'section': section,
        'action': action,
        'get_section': get_section,
        'get_session_year': get_session_year,
        'get_date': get_date,
        'attendance_report': attendance_report,
    }
    
    
    return render(request, 'hod/view_student_attendance.html', context)




# Section start here ================================================


@login_required(login_url='login')
def addSection(request):
    class_obj = Classes.objects.all()
    course_obj = Course.objects.all()
    teacher_obj = SchoolTeacher.objects.all()
    
    context = {
        'class_obj' : class_obj,
        'course_obj' : course_obj,
        'teacher_obj' : teacher_obj,
    }
    return render(request, "hod/add_section.html", context)




@login_required(login_url='login')
def saveSection(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        class_obj = request.POST.get('class_obj')
        course_obj = request.POST.get('course_id')
        teacher_obj = request.POST.get('teacher_id')
        
        class_id = Classes.objects.get(id=class_obj)
        course_id = Course.objects.get(id = course_obj)
        teacher_id = SchoolTeacher.objects.get(id=teacher_obj)

        section = Section(
            section_name = name,
            class_id = class_id,
            course = course_id,
            teacher_id = teacher_id,
        )
        section.save()
        messages.success(request, f"{section.section_name}Section added Successfully")
        return redirect('add_section')
    
    return render(request, "hod/add_section.html")




@login_required(login_url='login')
def viewSection(request):
    section_obj = Section.objects.all()
    
    context = {
        'section_obj' : section_obj
    }
    return render(request, 'hod/view_section.html', context)



@login_required(login_url='login')
def deleteSection(request, id):

    section = Section.objects.get(id=id)
    section.delete()
    messages.success(request, f"{section.section_name}  Deleted Successfully")
    return redirect('view_section')
    


@login_required(login_url='login')
def editSection(request, id):
    section = Section.objects.filter(id=id)
    class_obj = Classes.objects.all()
    course_obj = Course.objects.all()
    teacher_obj = SchoolTeacher.objects.all()
    
    context = {
        'section' : section,
        'class_obj' : class_obj,
        'course_obj' : course_obj,
        'teacher_obj' : teacher_obj,
    }
    
    return render(request, "hod/edit_section.html", context)




@login_required(login_url='login')
def updateSection(request):
    name=request.POST.get('name')
    section_id=request.POST.get('section_id')
    class_obj=request.POST.get('class_obj')
    course_id=request.POST.get('course_id')
    teacher_id=request.POST.get('teacher_id')
    
    section = Section.objects.get(id=section_id)
    classes = Classes.objects.get(id=class_obj)
    coursees = Course.objects.get(id=course_id)
    teacheres = SchoolTeacher.objects.get(id=teacher_id)
    
    section.section_name = name
    section.class_id = classes
    section.course = coursees
    section.teacher_id = teacheres
    section.save()
    messages.success(request, f"{section.section_name}  Updated Successfully")
    
    return redirect('view_section')



# Section end here ================================================




@login_required(login_url='login')
def addRoutine(request):
    section = Section.objects.all()
    subject = SchoolSubjects.objects.all()
    teacher = SchoolTeacher.objects.all()
    session_year = Session_Year.objects.all()
    class_routine = RoutineSubjects.objects.all()
    period = Period.objects.all()
    
    
    
    context = {
        'section' : section,
        'subject' : subject,
        'teacher' : teacher,
        'class_routine' : class_routine,
        'session_year' : session_year,
        'period' : period,
        
    }
    return render(request, 'hod/add_class_routine.html', context)


@login_required(login_url='login')
def saveRoutine(request):
    if request.method == 'POST':
        # period = request.POST.get('period')
        section_id = request.POST.get('section_id')
        session_id = request.POST.get('session_id')
        class_day = request.POST.get('class_day')
        
        section = Section.objects.get(id=section_id)
        session = Session_Year.objects.get(id=session_id)
        class_id = class_day
        
        first_subject_id = request.POST.get('first_subject_id')
        first_subject_teacher = request.POST.get('first_subject_teacher')
        first_class_time = request.POST.get('first_class_time')
        
        fist_subject = SchoolSubjects.objects.get(id=first_subject_id)
        first_teacher = SchoolTeacher.objects.get(id=first_subject_teacher)
        first_period = Period.objects.get(id=first_class_time)

        
        
        second_subject_id = request.POST.get('second_subject_id')
        second_subject_teacher = request.POST.get('second_subject_teacher')
        second_class_time = request.POST.get('second_class_time')
        
        second_subject = SchoolSubjects.objects.get(id=second_subject_id)
        second_teacher = SchoolTeacher.objects.get(id=second_subject_teacher)
        second_period = Period.objects.get(id=second_class_time)
        
        
        
        third_subject_id = request.POST.get('third_subject')
        third_subject_teacher_id = request.POST.get('third_subject_teacher')
        third_class_time = request.POST.get('third_class_time')
        
        third_subject = SchoolSubjects.objects.get(id=third_subject_id)
        third_teacher = SchoolTeacher.objects.get(id=third_subject_teacher_id)
        third_period = Period.objects.get(id=third_class_time)
        
        
        
        fourth_subject_id = request.POST.get('fourth_subject_id')
        fourth_subject_teacher = request.POST.get('fourth_subject_teacher')
        fourth_class_time = request.POST.get('fourth_class_time')
        
        fourth_subject = SchoolSubjects.objects.get(id=fourth_subject_id)
        fourth_teacher = SchoolTeacher.objects.get(id=fourth_subject_teacher)
        fourth_period = Period.objects.get(id=fourth_class_time)
        
        
        
        fifth_subject_id = request.POST.get('fifth_subject_id')
        fifth_subject_teacher = request.POST.get('fifth_subject_teacher')
        fifth_class_time = request.POST.get('fifth_class_time')
        
        fifth_subject = SchoolSubjects.objects.get(id=fifth_subject_id)
        fifth_teacher = SchoolTeacher.objects.get(id=fifth_subject_teacher)
        fifth_period = Period.objects.get(id=fifth_class_time)
        
        
        
        sixth_subject_id = request.POST.get('sixth_subject_id')
        sixth_subject_teacher = request.POST.get('sixth_subject_teacher')
        sixth_class_time = request.POST.get('sixth_class_time')
        
        sixth_subject = SchoolSubjects.objects.get(id=sixth_subject_id)
        sixth_teacher = SchoolTeacher.objects.get(id=sixth_subject_teacher)
        sixth_period = Period.objects.get(id=sixth_class_time)
        
        
        
        seventh_subject_id = request.POST.get('seventh_subject_id')
        seventh_subject_teacher = request.POST.get('seventh_subject_teacher')
        seventh_subject_id = request.POST.get('seventh_subject_id')
        
        seventh_subject = SchoolSubjects.objects.get(id=seventh_subject_id)
        seventh_teacher = SchoolTeacher.objects.get(id=seventh_subject_teacher)
        seventh_period = Period.objects.get(id=seventh_subject_id)
        
        
        
        


        
        routine = RoutineSubjects(
            section_id = section,
            session_year_id = session,
            class_day = class_id,
            
            first_subject = fist_subject,
            fitst_subject_teacher = first_teacher,
            first_period = first_period,
            
            
            second_subject = second_subject,
            second_subject_teacher = second_teacher,
            second_period = second_period,
            
            third_subject = third_subject,
            third_subject_teacher = third_teacher,
            third_period = third_period,
            
            fourth_subject = fourth_subject,
            fourth_subject_teacher = fourth_teacher,
            fourth_period = fourth_period,
            
            fifth_subject = fifth_subject,
            fifth_subject_teacher = fifth_teacher,
            fifth_period = fifth_period,
            
            sixth_subject = sixth_subject,
            sixth_subject_teacher = sixth_teacher,
            sixth_period = sixth_period,
            
            seventh_subject = seventh_subject,
            seventh_subject_teacher = seventh_teacher,
            seventh_period  = seventh_period,
            
            
            
        )
        routine.save()
        
        
        
        

        messages.success(request, f"Routine Added Successfully")
        return redirect('add_routine')
    
    return render(request, 'hod/add_class_routine.html')

    
    
@login_required(login_url='login')
def viewRoutine(request):
    section = Section.objects.all()
    session_year = Session_Year.objects.all()
    
    action = request.GET.get('action')
    
    
    get_section = None
    get_session_year = None
    routine_report = None
    sunday = None
    monday = None
    saturday = None
    tuesday = None
    wednesday = None
    thursday= None
    if action is not None:
        if request.method == 'POST':
            session_year_id = request.POST.get('session_year_id')
            section_id = request.POST.get('section_id')
            
            
            get_section = Section.objects.get(id=section_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            
            routine = RoutineSubjects.objects.filter(section_id=section_id, session_year_id=session_year_id)
            for i in routine:
                routine = i.id
                routine_report = RoutineSubjects.objects.filter(id=routine)
                
                if i.class_day == 'Saturday':
                    saturday = RoutineSubjects.objects.filter(id=routine, class_day='Saturday')
                    
                elif i.class_day == 'Sunday':
                    sunday = RoutineSubjects.objects.filter(id=routine, class_day='Sunday')
                    
                elif i.class_day == 'Monday ':
                    monday = RoutineSubjects.objects.filter(id=routine, class_day='Monday ')
                    
                elif i.class_day == 'Tuesday':
                    tuesday = RoutineSubjects.objects.filter(id=routine, class_day='Tuesday')
                    
                elif i.class_day == 'Wednesday':
                    wednesday = RoutineSubjects.objects.filter(id=routine, class_day='Wednesday')
                
                elif i.class_day == 'Thursday':
                    thursday = RoutineSubjects.objects.filter(id=routine, class_day='Thursday')
                
                
                
    context = {
        'action' : action,
        'section' : section,
        'session_year' : session_year,
        'routine_report' : routine_report,
        'get_section' : get_section,
        'get_session_year' : get_session_year,
        'sunday' : sunday,
        'monday' : monday,
        'tuesday' : tuesday,
        'wednesday' : wednesday,
        'thursday' : thursday,
        'saturday' : saturday,
       
    }

    return render(request, 'hod/view_routine.html', context)



@login_required(login_url='login')
def editRoutine(request, id):
    
    section = Section.objects.all()
    subject = SchoolSubjects.objects.all()
    teacher = SchoolTeacher.objects.all()
    session_year = Session_Year.objects.all()
    class_routine = RoutineSubjects.objects.all()
    period = Period.objects.all()
    
    routine = RoutineSubjects.objects.filter(id=id)
    
    
    
    context = {
        'section' : section,
        'subject' : subject,
        'teacher' : teacher,
        'class_routine' : class_routine,
        'session_year' : session_year,
        'period' : period,
        'routine' : routine,
        
    }
    
    return render(request, 'hod/edit_routine.html', context)


@login_required(login_url='login')
def updateRoutine(request):
    if request.method == 'POST':
        # period = request.POST.get('period')
        section_id = request.POST.get('section_id')
        session_id = request.POST.get('session_id')
        class_day = request.POST.get('class_day')
        routineId = request.POST.get('routineId')
        
        section = Section.objects.get(id=section_id)
        session = Session_Year.objects.get(id=session_id)
        class_id = class_day
        
        first_subject_id = request.POST.get('first_subject_id')
        first_subject_teacher = request.POST.get('first_subject_teacher')
        first_class_time = request.POST.get('first_class_time')
        
        fist_subject = SchoolSubjects.objects.get(id=first_subject_id)
        first_teacher = SchoolTeacher.objects.get(id=first_subject_teacher)
        first_period = Period.objects.get(id=first_class_time)

        
        
        second_subject_id = request.POST.get('second_subject_id')
        second_subject_teacher = request.POST.get('second_subject_teacher')
        second_class_time = request.POST.get('second_class_time')
        
        second_subject = SchoolSubjects.objects.get(id=second_subject_id)
        second_teacher = SchoolTeacher.objects.get(id=second_subject_teacher)
        second_period = Period.objects.get(id=second_class_time)
        
        
        
        third_subject_id = request.POST.get('third_subject')
        third_subject_teacher_id = request.POST.get('third_subject_teacher')
        third_class_time = request.POST.get('third_class_time')
        
        third_subject = SchoolSubjects.objects.get(id=third_subject_id)
        third_teacher = SchoolTeacher.objects.get(id=third_subject_teacher_id)
        third_period = Period.objects.get(id=third_class_time)
        
        
        
        fourth_subject_id = request.POST.get('fourth_subject_id')
        fourth_subject_teacher = request.POST.get('fourth_subject_teacher')
        fourth_class_time = request.POST.get('fourth_class_time')
        
        fourth_subject = SchoolSubjects.objects.get(id=fourth_subject_id)
        fourth_teacher = SchoolTeacher.objects.get(id=fourth_subject_teacher)
        fourth_period = Period.objects.get(id=fourth_class_time)
        
        
        
        fifth_subject_id = request.POST.get('fifth_subject_id')
        fifth_subject_teacher = request.POST.get('fifth_subject_teacher')
        fifth_class_time = request.POST.get('fifth_class_time')
        
        fifth_subject = SchoolSubjects.objects.get(id=fifth_subject_id)
        fifth_teacher = SchoolTeacher.objects.get(id=fifth_subject_teacher)
        fifth_period = Period.objects.get(id=fifth_class_time)
        
        
        
        sixth_subject_id = request.POST.get('sixth_subject_id')
        sixth_subject_teacher = request.POST.get('sixth_subject_teacher')
        sixth_class_time = request.POST.get('sixth_class_time')
        
        sixth_subject = SchoolSubjects.objects.get(id=sixth_subject_id)
        sixth_teacher = SchoolTeacher.objects.get(id=sixth_subject_teacher)
        sixth_period = Period.objects.get(id=sixth_class_time)
        
        
        
        seventh_subject_id = request.POST.get('seventh_subject_id')
        seventh_subject_teacher = request.POST.get('seventh_subject_teacher')
        seventh_period = request.POST.get('seventh_class_time')
        
        seventh_subject = SchoolSubjects.objects.get(id=seventh_subject_id)
        seventh_teacher = SchoolTeacher.objects.get(id=seventh_subject_teacher)
        seventh_period = Period.objects.get(id=seventh_period)
        
        
        routine = RoutineSubjects.objects.get(id=routineId)
        routine.section_id = section
        routine.session_year_id = session
        routine.class_day = class_id
        
        routine.first_subject = fist_subject
        routine.fitst_subject_teacher = first_teacher
        routine.first_period = first_period
        
        routine.second_subject = second_subject
        routine.second_subject_teacher = second_teacher
        routine.second_period = second_period
        
        routine.third_subject = third_subject
        routine.third_subject_teacher = third_teacher
        routine.third_period = third_period
        
        routine.fourth_subject = fourth_subject
        routine.fourth_subject_teacher = fourth_teacher
        routine.fourth_period = fourth_period
        
        routine.fifth_subject = fifth_subject
        routine.fifth_subject_teacher = fifth_teacher
        routine.fifth_period = fifth_period
        
        routine.sixth_subject = sixth_subject
        routine.sixth_subject_teacher = sixth_teacher
        routine.sixth_period = sixth_period
        
        routine.seventh_subject = seventh_subject
        routine.seventh_subject_teacher = seventh_teacher
        routine.seventh_period  = seventh_period
        
        routine.save()
        
        messages.success(request, f" {routine.session_year_id} -  section: {routine.section_id}     Routine Updated Successfully")
        
        return redirect('view_routine')


@login_required(login_url='login')
def deleteRoutine(request, id):
    routine = RoutineSubjects.objects.get(id=id)
    routine.delete()
    messages.success(request, f" {routine.session_year_id} -  section: {routine.section_id}     Routine Deleted Successfully")
    return redirect('view_routine')
    


@login_required(login_url='login')
def AddNotice(request):
    try:
        if request.method=="POST":
            title = request.POST.get('title')
            desc = request.POST.get('desc')

            notice = Notice(
                headline = title,
                notice  = desc
            )
            notice.save()
            messages.success(request, f"{notice.headline} Notice Added Successfully")
    
    except:
        return redirect('oops')

    return render(request, 'hod/add_notice.html')



@login_required(login_url='login')
def viewNotice(request):
    notice_obj = Notice.objects.all()

    context = {
        'notice_obj' : notice_obj,
    }
    return render(request, 'hod/view_notice.html', context)





@login_required(login_url='login')
def editNotice(request, id):
    notice_obj = Notice.objects.filter(id = id)

    context = {
        'notice_obj' : notice_obj,
    }
    return render(request, 'hod/edit_notice.html', context)


@login_required(login_url='login')
def updateNotice(request):
    if request.method == "POST":
        title = request.POST.get('title')
        notice_id = request.POST.get('notice_id')
        desc = request.POST.get('desc')

        notice = Notice.objects.get(id = notice_id)
        notice.headline = title
        notice.notice = desc
        notice.save()
        messages.success(request, f"{notice.headline}Notice updated Successfully")
        return redirect('view_notice')




@login_required(login_url='login')
def deleteNotice(request, id):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            notice = Notice.objects.get(id=id)
            notice.delete()
            return redirect("view_notice")
            messages.success(request, f"{notice.headline} Notice deleted Successfully")
    
        else:
            messages.error(request, "Please Type CONFIRM to Delete Notice")
            return redirect('view_notice')
    return render(request, 'hod/view_notice.html')







@login_required(login_url='login')
def addResultPlan(request):
    subject_obj = SchoolSubjects.objects.all()

    context = {
        'subject_obj' : subject_obj,
    }
    return render(request, 'hod/result_plan.html', context)	




@login_required(login_url='login')
def saveResultPlan(request):
    if request.method == 'POST':
        subject = request.POST.get('subject_id')
        pi_no = request.POST.get('pi_no')
        pi_desc = request.POST.get('pi_desc')
        bi_desc = request.POST.get('bi_desc')

        subject_id = SchoolSubjects.objects.get(id=subject)

        result_plan = ResultPlan(
            subject = subject_id,
            pi_no = pi_no,
            pi_name = pi_desc,
            bi_name = bi_desc,
        )

        result_plan.save()
        messages.success(request, f"Result Plan Added Successfully")

        return redirect('result_plan')

    else:
        return redirect('oops')



@login_required(login_url='login')
def viewResultPlan(request):
    result_plan = ResultPlan.objects.all()
    subject_obj = SchoolSubjects.objects.all()

    context = {
        'result_plan' : result_plan,
        'subject_obj' : subject_obj,
    }
    return render(request, 'hod/view_result_plan.html', context)




@login_required(login_url='login')
def editResultPlan(request, id):
    result_plan = ResultPlan.objects.filter(id=id)

    context = {
        'result_plan' : result_plan,
    }
    return render(request, 'hod/edit_result_plan.html', context)




@login_required(login_url='login')
def updateResultPlan(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        pi_no = request.POST.get('pi_no')
        pi_desc = request.POST.get('pi_desc')
        bi_desc = request.POST.get('bi_desc')

        result_plan = ResultPlan.objects.get(id=plan_id)
        result_plan.pi_no = pi_no,
        result_plan.pi_name = pi_desc,
        result_plan.bi_name = bi_desc,
        result_plan.save()

        messages.success(request, f"Result Plan Updated Successfully")

        return redirect('result_plan')

    else:
        return redirect('oops')





@login_required(login_url='login')
def deleteResultPlan(request, id):
    if request.method == "POST":
        confirm = request.POST.get('confirm')
        if confirm == "CONFIRM":
            result_plan = ResultPlan.objects.get(id=id)
            result_plan.delete()
            return redirect("view_result_plan")
            messages.success(request, f"Result Plan deleted Successfully")
    
        else:
            messages.error(request, "Please Type CONFIRM to Delete Result Plan")
            return redirect('view_result_plan')
    return render(request, 'hod/view_result_plan.html')




@login_required(login_url='login')
def adminViewResult(request):
    try:
        class_obj = Classes.objects.all()
        subject_obj = SchoolSubjects.objects.all()
        student_obj = Student.objects.all()
        
        action = request.GET.get('action')

        student_name = None
        student_id = None
        roll = None
        class_name = None
        section_name = None
        teacher_name = None
        subject = None
        pi_no = None
        grade = None
        result = None
        pi_name = None
        bi_name = None
        pi_bi_name = None
        get_student = None
        get_subject  = None

        if action is not None:
            if request.method == 'POST':
                subject = request.POST.get('subject')
                student = request.POST.get('student')

                subject_obj = SchoolSubjects.objects.filter(id = subject)
                subject_id = SchoolSubjects.objects.get(id=subject)

                result = StudentResult.objects.filter(student_id=student, subject_id=subject)
                get_subject = subject_id

                get_student = Student.objects.get(id=student)
                get_subject = subject_id


                for i in result:
                    pi_no = i.pi_no
                    grade = i.grade
                    student_name = i.student_id.first_name + ' ' + i.student_id.last_name
                    student_id = i.student_id.id
                    roll = i.student_id.roll
                    class_name = i.student_id.class_name.name
                    section_name = i.student_id.section.section_name
                    teacher_name = i.subject_id.teacher.admin.first_name + ' ' + i.subject_id.teacher.admin.last_name
                    subject = i.subject_id.name
                    
                # print(f'\n\n student_name: {student_name}\n student_id: {student_id} \n roll: {roll}\n class_name: {class_name}\n section_name: {section_name}\n s teacher_name: {teacher_name}\n subject: {subject}\n pi_no: {pi_no}\n grade: {grade}\n result: {result}\n\n'	)

    except:
        messages.error(request, "Please Select Subject and Student")
        return redirect('admin_view_result')


    context = {
        'result': result,
        'subject_obj' : subject_obj,
        'student_obj' : student_obj,
        'get_student' : get_student,
        'get_subject' : get_subject,
        'student_name' : student_name,
        'class_name' : class_name,
        'section_name' : section_name,
        'teacher_name' : teacher_name,
        'roll' : roll,
        'student_id' : student_id,
        'subject' : subject,
        'pi_no' : pi_no,
        'grade' : grade,
        'subject_obj' : subject_obj,
        'class_obj' : class_obj,
        'action' : action,
    }
    

    return render(request, 'hod/view_result.html', context)