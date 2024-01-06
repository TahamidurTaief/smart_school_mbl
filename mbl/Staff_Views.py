from django.shortcuts import render,redirect
from app.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
def staff_home(request):
    return render(request, 'staff/home.html')



@login_required(login_url='login')
def staffNotifications(request):
    schoolteacher = SchoolTeacher.objects.filter(admin=request.user.id)

    notifications = None
    for i in schoolteacher:
        notifications = Staff_Notification.objects.filter(school_teacehr_id=i.id)

    context = {
        'notifications': notifications,
    }

    return render(request, 'staff/staff_admin_notifications.html', context)
    


@login_required(login_url='login')
def staffNotificationsSeen(request, status):
    notification = Staff_Notification.objects.get(id=status)
    notification.status = True
    notification.save()
    return redirect('staff_notifications')



@login_required(login_url='login')
def staffApplyLeave(request):
    school_teacher_id = SchoolTeacher.objects.get(admin = request.user.id)
    staff_leave_history = Staff_Leave.objects.filter(school_teacher_id=school_teacher_id)
    
    context = {
        'staff_leave_history': staff_leave_history
    }
    return render(request, 'staff/staff_apply_leave.html', context)




@login_required(login_url='login')
def staffApplyLeaveSave(request):
    if request.method == 'POST':
        leaveDate = request.POST.get('leave_date')
        leaveMessage = request.POST.get('leave_message')
        schoolteacher = SchoolTeacher.objects.get(admin=request.user.id)
        
        
        leaveReport = Staff_Leave(school_teacher_id=schoolteacher, data=leaveDate, message=leaveMessage)
        leaveReport.save()
        messages.success(request, 'Leave Applied Successfully')
        return redirect('staff_apply_leave')

    
    return render(request, 'staff/staff_apply_leave.html')



@login_required(login_url='login')
def staffFeedback(request):
    school_teacher_id = SchoolTeacher.objects.get(admin = request.user.id)
    feedback_history = Staff_Feedback.objects.filter(school_teacher_id=school_teacher_id)
    
    context = {
        'feedback_history': feedback_history
    }
    
    
    return render(request, 'staff/staff_feedback.html', context)




@login_required(login_url='login')
def staffFeedbackSave(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback_message')
        schoolteacher = SchoolTeacher.objects.get(admin=request.user.id)
        
        feedback = Staff_Feedback(school_teacher_id=schoolteacher, feedback=feedback, feedback_reply='')
        feedback.save()
        messages.success(request, 'Feedback Sent Successfully')
        return redirect('staff_feedback')
    
    return render(request, 'staff/staff_feedback.html')




@login_required(login_url='login')
def SchoolTeacherAttendance(request):
    school_teacher = SchoolTeacher.objects.get(admin=request.user.id)
    section = Section.objects.filter(teacher_id=school_teacher)
    session_year = Session_Year.objects.all()
    
    action = request.GET.get('action')
    get_section=None
    session_year_obj=None
    attendance=None
    students = None
    
    if action is not None:
        if request.method == 'POST':
            section_id = request.POST.get('section_id')
            session_year_id = request.POST.get('session_year_id')
            
            get_section = Section.objects.get(id=section_id)
            session_year_obj = Session_Year.objects.get(id=session_year_id)
            
            section = Section.objects.filter(teacher_id=school_teacher)
            students = Student.objects.filter(section = section_id, session_year_id=session_year_obj)
            
            
            # for i in section:
            #     student_id = i.course.id
            #     students = Student.objects.filter(course_id=student_id)
                
                 
            # attendance = Attendence.objects.filter(section_id=section_id, session_year_id=session_year_obj, date=date)
            # attendance_report = Attendence_Report.objects.filter(attendence_id=attendance[0].id)
            # students = []
            # for student in attendance_report:
            #     students.append(student.student_id)
            # print(students)

    
    context = {
        'session_year': session_year,
        'section': section,
        # 'attendance': attendance,
        # 'session_year': session_year,
        # 'section': section,
        # 'students': students,
        # 'date': date,
        # 'section_id': section_id,
        # 'session_year_id': session_year_id,
        'students': students,
        'action': action,
        'get_section': get_section,
        'session_year_obj': session_year_obj,
    }
    return render(request, 'staff/st_attendance.html', context)





@login_required(login_url='login')
def saveSchoolTeacherAttendance(request):
    if request.method == "POST":
        attendance_date = request.POST.get('date')
        session_year_id = request.POST.get('session_year')
        section_id = request.POST.get('section_id')
        student_id = request.POST.getlist('student_id')
        
        get_section = Section.objects.get(id=section_id)
        session_year_obj = Session_Year.objects.get(id=session_year_id)
        
        attendance = Attendence(
            section_id=get_section,
            session_year_id = session_year_obj,
            attendence_date = attendance_date
        )
        attendance.save()
        
        
        
        
        for i in student_id:
            stud_id= i
            int_stud_id = int(stud_id)
            present_student = Student.objects.get(id=int_stud_id)
            
            attendance_report = Attendence_Report(
                student_id=present_student,
                attendence_id=attendance,
            )
            attendance_report.save()
            
            sudent_attendence = Student.objects.get(id = int_stud_id)
            sudent_attendence.attendence_status = 1
            sudent_attendence.attendence_date = attendance_date
            sudent_attendence.save()
        
            messages.success(request, 'Attendance Taken Successfully')
    
    return redirect('school_teacher_attendance')




@login_required(login_url='login')
def viewSchoolTeacherAttendance(request):
    teacher_id = SchoolTeacher.objects.get(admin=request.user.id)
    session_year = Session_Year.objects.all()
    section = Section.objects.filter(teacher_id=teacher_id)
    student = Student.objects.all()
    
    action = request.GET.get('action')
    
    get_section=None
    get_date = None
    get_session_year = None
    attendance_report=None
    all_student=None
    
    if action is not None:
        if request.method == 'POST':
            session_year_id = request.POST.get('session_year_id')
            section_id = request.POST.get('section_id')
            date = request.POST.get('date')
            
            get_section = Section.objects.get(id=section_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            get_date = date
            
            
            if get_date != "":
                attendence_date = Attendence.objects.filter(attendence_date=date)
                attendence = Attendence.objects.filter(section_id=section_id, session_year_id=session_year_id, attendence_date=date)
                for i in attendence:
                    attendence = i.id
                    attendance_report = Attendence_Report.objects.filter(attendence_id=attendence)

            if get_date == "":
                all_student = Student.objects.filter(section=section_id, session_year_id=session_year_id)
                # print(all_student)
                    
    
    context = {
        'session_year': session_year,
        'section': section,
        'action': action,
        'get_section': get_section,
        'get_session_year': get_session_year,
        'get_date': get_date,
        'attendance_report': attendance_report,
        'all_student': all_student,
    }
    
    return render(request, 'staff/view_st_attendance.html', context)
        




# Result start here ========================================================

@login_required(login_url='login')
def staffViewResult(request):

    # try:
    class_obj = Classes.objects.all()
    session_year = Session_Year.objects.all()
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
    result = None
    get_session = None
    get_class = None

    if action is not None:
        if request.method == 'POST':
            class_id = request.POST.get('class_id')
            session_year_id = request.POST.get('session_year_id')

            class_obj = Classes.objects.filter(id = class_id)
            session_year_obj = Session_Year.objects.get(id=session_year_id)


            get_session = Session_Year.objects.get(id=session_year_id)
            get_class = Classes.objects.get(id=class_id)

            
            result = StudentResult.objects.filter(class_id=class_id, session_year_id=session_year_id)

            for i in result:
                student_name = i.student_id.first_name + ' ' + i.student_id.last_name
                student_id = i.student_id.id
                roll = i.student_id.roll
                class_name = i.student_id.class_name.name
                section_name = i.student_id.section.section_name
                # teacher_name = i.subject_id.teacher.admin.first_name + ' ' + i.subject_id.teacher.admin.last_name
                # subject = i.subject_id.name
                    
                # print(f'\n\n student_name: {student_name}\n student_id: {student_id} \n roll: {roll}\n class_name: {class_name}\n section_name: {section_name}\n s teacher_name: {teacher_name}\n subject: {subject}\n pi_no: {pi_no}\n grade: {grade}\n result: {result}\n\n'	)

    # except:
    #     messages.error(request, "Please Select Subject and Student")
    #     return redirect('admin_view_result')


    context = {
        'result': result,
        'subject_obj' : subject_obj,
        'student_obj' : student_obj,
        'student_name' : student_name,
        'class_name' : class_name,
        'section_name' : section_name,
        'teacher_name' : teacher_name,
        'roll' : roll,
        'student_id' : student_id,
        'subject' : subject,
        'subject_obj' : subject_obj,
        'class_obj' : class_obj,
        'session_year' : session_year,
        'action' : action,
        'get_session' : get_session,
        'get_class' : get_class,
    }
    
    return render(request, 'staff/view_result.html', context)



@login_required(login_url='login')
def viewRoutine(request):
    section = Section.objects.all()
    subject = SchoolSubjects.objects.all()
    teacher = SchoolTeacher.objects.all()
    session_year = Session_Year.objects.all()
    class_routine = RoutineSubjects.objects.all()
    
    
    
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
        
        'section' : section,
        'subject' : subject,
        'teacher' : teacher,
        'class_routine' : class_routine,
        'session_year' : session_year,
       
    }
    
    
    return render(request, 'staff/view_routine.html', context)




@login_required(login_url='login')
def viewNotice(request):
    notice_obj = Notice.objects.all()

    context = {
        'notice_obj' : notice_obj,
    }
    return render(request, 'staff/view_notice.html', context)




@login_required(login_url='login')
def myProfile(request):
    school_teacher_obj = SchoolTeacher.objects.filter(admin=request.user.id)

    name = None
    student_id = None
    email = None
    staff_type = None
    gender = None
    date_of_birth = None
    class_name = None
    joining_date = None
    mobile_number = None
    qualification = None
    course = None

    for i in school_teacher_obj:
        JoiningDate = str(i.joining_date)
        DateOfBirth = str(i.date_of_birth)

        name = i.admin.first_name + " " + i.admin.last_name
        email = i.admin.email
        staff_type = i.staff_type
        gender = i.gender
        date_of_birth = DateOfBirth
        joining_date = JoiningDate
        mobile_number = i.mobile_number
        religion = i.religion
        fname = i.fathers_name
        mname = i.mothers_name
        address = i.present_address
        profile_pic = i.admin.profile_pic.url
        qualification = i.qualification
        course = i.course

        

        
    
    context = {
        'school_teacher_obj' : school_teacher_obj,
        'name': name,
        'student_id': student_id,
        'email': email,
        'staff_type' : staff_type,
        'gender' : gender,
        'date_of_birth' : date_of_birth,
        'class_name' : class_name,
        'joining_date' : joining_date,
        'mobile_number' : mobile_number,
        'fname' : fname,
        'mname' : mname,
        'religion' : religion,
        'address' : address,
        'profile_pic' : profile_pic,
        'qualification' : qualification,
        'course' : course,
    }


    return render(request, 'staff/my_profile.html', context)