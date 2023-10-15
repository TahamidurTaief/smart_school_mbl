from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from django.contrib import messages




@login_required(login_url='login')
def studentHome(request):
    return render(request, 'student/home.html')


@login_required(login_url='login')
def studentNotifications(request):
    student = Student.objects.filter(admin=request.user.id)
    
    for i in student:
        notifications = Student_Notification.objects.filter(student_id=i.id)

        context = {
            'notifications': notifications
        }
        
        return render(request, 'student/student_admin_notifications.html', context)
    

@login_required(login_url='login')
def studentNotificationsSeen(request, status):
    notification = Student_Notification.objects.get(id=status)
    notification.status = True
    notification.save()
    return render(request, 'student/student_admin_notifications.html')




@login_required(login_url='login')
def studentFeedback(request):
    student = Student.objects.get(admin=request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id=student)
    
    context = {
        'feedback_history': feedback_history
    }
    return render(request, 'student/student_feedback.html', context)




@login_required(login_url='login')
def saveStudentFeedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback_message')
        student = Student.objects.get(admin=request.user.id)
        
        feedback_report = Student_Feedback(student_id=student, feedback=feedback, feedback_reply='')
        feedback_report.save()
        messages.success(request, 'Feedback Submitted Successfully')
        return redirect('student_feedback')
    
    return render(request, 'student/student_feedback.html')





@login_required(login_url='login')
def studentApplyLeave(request):
    student = Student.objects.get(admin=request.user.id)
    student_leave_history = Student_Leave.objects.filter(student_id=student)
    
    context = {
        'student_leave_history': student_leave_history
    }
    return render(request, 'student/student_appy_leave.html', context)



@login_required(login_url='login')
def studentApplyLeaveSave(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        student = Student.objects.get(admin=request.user.id)
        
        try:
            leave_report = Student_Leave(student_id=student, data=leave_date, message=leave_message, status=0)
            leave_report.save()
            messages.success(request, 'Leave Applied Successfully')
            return redirect('student_apply_leave')
        except:
            messages.error(request, 'Failed to Apply Leave')
            return redirect('student_apply_leave')
        
    return render(request, 'student/student_appy_leave.html')






@login_required(login_url='login')
def studentViewAttendance(request):
    student = Student.objects.get(admin=request.user.id)
    section = Section.objects.filter(class_id=student.class_name)
    
    action = request.GET.get('action')
    
    get_section = None
    attendance_report=None
    if action is not None:
        if request.method == 'POST':
            section_id = request.POST.get('section_id')
            get_section = Section.objects.get(id=section_id)
            
            # attendance = Attendence.objects.get(section_id=get_section)
            attendance_report = Attendence_Report.objects.filter(student_id = student, attendence_id__section_id=section_id)
    
    context = {
        'section': section,
        'action': action,
        'attendance_report': attendance_report,
    }
    
    return render(request, 'student/view_attendence/view_attendence.html', context)




@login_required(login_url='login')
def studentViewResult(request):
    student = Student.objects.get(admin=request.user.id)
    stu_class_name = Classes.objects.get(id=student.class_name.id)
    subject_obj = SchoolSubjects.objects.filter(class_name=stu_class_name)
    class_obj = Classes.objects.all()
    # result = StudentResult.objects.filter(student_id=student)
    
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

    if action is not None:
        if request.method == 'POST':
            subject = request.POST.get('subject')
            subject_id = SchoolSubjects.objects.get(id=subject)

            result = StudentResult.objects.filter(student_id=student, subject_id=subject)
            get_subject = subject_id


            for i in result:
                pi_no = i.pi_no
                # pi_name = i.result.pi_name
                # bi_name = i.result.bi_name
                grade = i.grade
                student_name = i.student_id.first_name + ' ' + i.student_id.last_name
                student_id = i.student_id.id
                roll = i.student_id.roll
                class_name = i.student_id.class_name.name
                section_name = i.student_id.section.section_name
                # session_year = i.student_id.session_year.session_year
                teacher_name = i.subject_id.teacher.admin.first_name + ' ' + i.subject_id.teacher.admin.last_name
                subject = i.subject_id.name
                
            print(f'\n\n student_name: {student_name}\n student_id: {student_id} \n roll: {roll}\n class_name: {class_name}\n section_name: {section_name}\n s teacher_name: {teacher_name}\n subject: {subject}\n pi_no: {pi_no}\n grade: {grade}\n result: {result}\n\n'	)
            
            # pi_bi_name = ResultPlan.objects.filter(subject=subject_id, pi_no=pi_no)
            # print(f'\n\n pi_bi_name: {pi_bi_name}\n\n')

            # pi_bi_name = ResultPlan.objects.filter(pi_no=pi_no)
            # print(f'\n\n pi_bi_name: {pi_bi_name}\n\n')

            # for i in pi_bi_name:
            #     pi_name = i.pi_name
            #     bi_name = i.bi_name
            #     print(f'\n pi_name: {pi_name}\nbi_name : {bi_name}\n')


    context = {
        'result': result,
        'student_name' : student_name,
        'class_name' : class_name,
        'section_name' : section_name,
        # 'session_year' : session_year,
        'teacher_name' : teacher_name,
        'roll' : roll,
        'student_id' : student_id,
        'subject' : subject,
        'pi_no' : pi_no,
        'grade' : grade,
        'subject_obj' : subject_obj,
        'class_obj' : class_obj,
        # 'pi_name' : pi_name,
        # 'bi_name' : bi_name,
        # 'pi_bi_name' : pi_bi_name,
        'action' : action,
    }
    

    return render(request, 'student/student_view_result.html', context)






@login_required(login_url='login')
def studentViewRoutine(request):
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
    
    
    return render(request, 'student/view_routine.html', context)




@login_required(login_url='login')
def viewNotice(request):
    notice_obj = Notice.objects.all()

    context = {
        'notice_obj' : notice_obj,
    }
    return render(request, 'student/view_notice.html', context)



@login_required(login_url='login')
def myProfile(request):
    student_obj = Student.objects.filter(admin=request.user.id)
        
        
    name = None
    student_id = None
    email = None
    session = None
    roll = None
    course_id = None
    gender = None
    date_of_birth = None
    class_name = None
    joining_date = None
    mobile_number = None

    for i in student_obj:
        JoiningDate = str(i.joining_date)
        DateOfBirth = str(i.date_of_birth)

        name = i.admin.first_name + " " + i.admin.last_name
        student_id = i.student_id
        email = i.admin.email
        session = i.session_year_id
        roll = i.roll
        course_id = i.course_id
        gender = i.gender
        date_of_birth = DateOfBirth
        class_name = i.class_name
        joining_date = JoiningDate
        mobile_number = i.mobile_number
        section = i.section
        religion = i.religion
        fname = i.fathers_name
        mname = i.mothers_name
        fnum = i.fathers_mobile
        mnum = i.mothers_mobile
        address = i.present_address
        profile_pic = i.admin.profile_pic.url

        

        
    
    context = {
        'student_obj' : student_obj,
        'name': name,
        'student_id': student_id,
        'email': email,
        'session': session,
        'roll': roll,
        'course_id' : course_id,
        'gender' : gender,
        'date_of_birth' : date_of_birth,
        'class_name' : class_name,
        'joining_date' : joining_date,
        'mobile_number' : mobile_number,
        'section' : section,
        'fname' : fname,
        'mname' : mname,
        'fnum' : fnum,
        'mnum' : mnum,
        'religion' : religion,
        'address' : address,
        'profile_pic' : profile_pic,
    }
    
    return render(request, 'student/my_profile.html', context)