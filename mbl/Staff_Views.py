from django.shortcuts import render,redirect
from app.models import *
from django.contrib import messages



def staff_home(request):
    return render(request, 'staff/home.html')


def staffNotifications(request):
    staaf = Staff.objects.filter(admin=request.user.id)
    for i in staaf:
        notifications = Staff_Notification.objects.filter(staff_id=i.id)

        context = {
            'notifications': notifications
        }

        return render(request, 'Staff/staff_admin_notifications.html', context)
    

def staffNotificationsSeen(request, status):
    notification = Staff_Notification.objects.get(id=status)
    notification.status = True
    notification.save()
    return redirect('staff_notifications')


def staffApplyLeave(request):
    staaf = Staff.objects.get(admin=request.user.id)
    staff_leave_history = Staff_Leave.objects.filter(staff_id=staaf)
    
    context = {
        'staff_leave_history': staff_leave_history
    }
    return render(request, 'staff/staff_apply_leave.html', context)



def staffApplyLeaveSave(request):
    if request.method == 'POST':
        leaveDate = request.POST.get('leave_date')
        leaveMessage = request.POST.get('leave_message')
        staff = Staff.objects.get(admin=request.user.id)
        
        
        leaveReport = Staff_Leave(staff_id=staff, data=leaveDate, message=leaveMessage)
        leaveReport.save()
        messages.success(request, 'Leave Applied Successfully')
        return redirect('staff_apply_leave')

    
    return render(request, 'staff/staff_apply_leave.html')



def staffFeedback(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    feedback_history = Staff_Feedback.objects.filter(staff_id=staff_id)
    
    context = {
        'feedback_history': feedback_history
    }
    
    
    return render(request, 'staff/staff_feedback.html', context)



def staffFeedbackSave(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback_message')
        staff = Staff.objects.get(admin=request.user.id)
        
        feedback = Staff_Feedback(staff_id=staff, feedback=feedback, feedback_reply='')
        feedback.save()
        messages.success(request, 'Feedback Sent Successfully')
        return redirect('staff_feedback')
    
    return render(request, 'staff/staff_feedback.html')



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
                attendence_date = Attendence.objects.get(attendence_date=date)
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


def addResult(request):
    school_teacher = SchoolTeacher.objects.get(admin=request.user.id)
    session_year = Session_Year.objects.all()
    subjects = SchoolSubjects.objects.filter(teacher=school_teacher)
    result = StudentResult.objects.all()
    result_plan = ResultPlan.objects.all()
    
    action = request.GET.get('action')
    
    get_subject=None
    get_session=None
    students=None
    
    if action is not None:
        if request.method == 'POST':
            session_year_id = request.POST.get('session_year_id')
            subject_id = request.POST.get('subject_id')
            student_id = request.POST.get('student_id')
            
            session_year_obj = Session_Year.objects.get(id=session_year_id)
            subject_obj = SchoolSubjects.objects.get(id=subject_id)
            
        
            get_subject = SchoolSubjects.objects.get(id=subject_id)
            get_session = Session_Year.objects.get(id=session_year_id)

            
    
            subjects = SchoolSubjects.objects.filter(id = subject_id)
            for i in subjects:
                subject_id = i.course_id.id
                students = Student.objects.filter(course_id=subject_id)
    
    
    context = {
        'session_year': session_year,
        'subjects': subjects,
        'action' : action,
        'get_subject' : get_subject,
        'get_session' : get_session,
        'students' : students,
        'result' : result,
        'result_plan' : result_plan,
    }
    return render(request, 'staff/add_result.html', context)



def saveResult(request):
    if request.method == "POST":
        session_year_id = request.POST.get('session_year_id')
        subject_id = request.POST.get('subject_id')
        student_id = request.POST.get('student_id')
        pi_bi_no = request.POST.get('pi_bi_no')
        grade_no = request.POST.get('grade_no')

        print(f'session_year_id: {session_year_id}\nsubject_id: {subject_id}\nstudent_id: {student_id}\npi_bi_no: {pi_bi_no}\ngrade_no: {grade_no}\n')
        
        

        student_obj = Student.objects.get(admin=student_id)
        session_year_obj = Session_Year.objects.get(id=session_year_id)
        subject_obj = SchoolSubjects.objects.get(id=subject_id)
        
        check_exist = StudentResult.objects.filter(student_id=student_obj, subject_id=subject_obj).exists()



        result = StudentResult(
            subject_id=subject_obj,
            student_id=student_obj,
            pi_no=pi_bi_no,
            grade=grade_no,
        )
        result.save()
        messages.success(request, 'Result Added Successfully')
        return redirect('add_result')

    
    return render(request, 'staff/add_result.html')



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





def viewNotice(request):
    notice_obj = Notice.objects.all()

    context = {
        'notice_obj' : notice_obj,
    }
    return render(request, 'staff/view_notice.html', context)