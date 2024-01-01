
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views, Hod_Views, Staff_Views, Student_Views

urlpatterns = [
    path('', views.home, name='home'),


    path('oops', Hod_Views.oops, name='oops'),
    path('superadmin/', admin.site.urls),
    path('base/', views.base, name='base'),
    path('login/', views.custom_login, name='login'),
    path('dologin/', views.doLogin, name='doLogin'),
    path('doLogout/', views.doLogout, name='logout'),

    # profile url
    path('profile/', views.profile, name='profile'),
    path('profile/update', views.profileUpdate, name='profileUpdate'),

    # HOD Path:
    path('admin/', Hod_Views.admin_home, name='admin_home'),
    # path('admin/my_profile/', Hod_Views.myProfile, name='admin_my_profile'),
    path('admin/add_student/', Hod_Views.addStudent, name='add_student'),
    path('admin/view_student/', Hod_Views.viewStudent, name='view_student'),
    path('admin/student/<str:id>/edit', Hod_Views.editStudent, name='edit_student'),
    path('admin/student/update', Hod_Views.updateStudent, name='update_student'),
    path('admin/student/<str:admin>/delete', Hod_Views.deleteStudent, name='delete_student'),
    path('admin/student/download-csv', Hod_Views.downloadStudentCsv, name='download_csv_student'),

    path('admin/student/<str:id>/approve', Hod_Views.approveStudent, name='approve_student'),

    # course
    path('admin/Course/add', Hod_Views.addCourse, name="add_course"),
    path('admin/Course/view', Hod_Views.viewCourse, name="view_Course"),
    path('admin/Course/<str:id>/edit', Hod_Views.editCourse, name="edit_Course"),
    path('admin/Course/update', Hod_Views.updateCourse, name="update_Course"),
    path('admin/Course/<str:id>/delete', Hod_Views.deleteCourse, name="delete_Course"),


    # Staff
    path('admin/staff/add', Hod_Views.addStaff, name="add_staff"),
    path('admin/staff/view', Hod_Views.staffView, name="view_staff"),
    path('admin/staff/<str:id>/edit', Hod_Views.editStaff, name="edit_staff"),
    path('admin/staff/update', Hod_Views.updateStaff, name="update_staff"),
    path('admin/staff/<str:id>/delete', Hod_Views.deleteStaff, name="delete_staff"),
    path('admin/staff/downloads', Hod_Views.downloadStaffxlsx, name="download_staff_data"),
    
    path('admin/staff_type/add', Hod_Views.addStaffType, name="add_staff_type"),
    path('admin/staff_type/view', Hod_Views.viewStaffType, name="view_staff_type"),
    path('admin/staff_type/<str:id>/edit', Hod_Views.editStaffType, name="edit_staff_type"),
    path('admin/staff_type/update', Hod_Views.updateStaffType, name="update_staff_type"),
    path('admin/staff_type/<str:id>/delete', Hod_Views.deleteStaffType, name="delete_staff_type"),

    path('admin/add/school/teacher', Hod_Views.addSchoolTeacher, name="add_school_teacher"),
    path('admin/save/school/teacher', Hod_Views.saveSchoolTeacher, name="save_school_teacher"),
    path('admin/view/school/teacher', Hod_Views.viewSchoolTeacher, name="view_school_teacher"),
    path('admin/school/teacher/<str:id>edit', Hod_Views.editSchoolTeacher, name="edit_school_teacher"),
    path('admin/school/teacher/update', Hod_Views.updateSchoolTeacher, name="update_school_teacher"),
    path('admin/school/teacher/<str:admin>/delete', Hod_Views.deleteSchoolTeacher, name="delete_school_teacher"),
    path('admin/school/teacher/download_csv', Hod_Views.downloadSchoolTeacherCsv, name="download_csv_school_teacher"),
    # Subject
    path('admin/subject/add', Hod_Views.addSubject, name="add_subject"),
    path('admin/subject/view', Hod_Views.viewSubject, name="view_subject"),
    path('admin/subject/<str:id>/edit', Hod_Views.editSubject, name="edit_subject"),
    path('admin/subject/update', Hod_Views.updateSubject, name="update_subject"),
    path('admin/subject/<str:id>/delete', Hod_Views.deleteSubject, name="delete_subject"),


    path('admin/class/assign', Hod_Views.addClass, name="add_class"),
    path('admin/class/<str:id>/edit', Hod_Views.editClass, name="edit_class"),
    path('admin/class/view', Hod_Views.viewClass, name="view_class"),
    path('admin/class/update', Hod_Views.updateClass, name="update_class"),
    path('admin/class/<str:id>/delete', Hod_Views.deleteClass, name="delete_class"),
    # Session
    path('admin/session/add', Hod_Views.addSession, name="add_session"),
    path('admin/session/view', Hod_Views.viewSession, name="view_session"),
    path('admin/session/<str:id>/edit', Hod_Views.editSession, name="edit_session"),
    path('admin/session/update', Hod_Views.updateSession, name="update_session"),
    path('admin/session/<str:id>/delete', Hod_Views.deleteSession, name="delete_session"),

    # staaf Notifications
    path('admin/staff_notification/add', Hod_Views.staffNotification, name="add_staff_notification"),
    path('admin/staff_notification/save', Hod_Views.saveStaffNotification, name="save_staff_notification"),

    # staff leave see from admin
    path('admin/staff/leave', Hod_Views.staffLeave, name="staff_leave"),
    path('admin/staff/approve/leave/<str:id>', Hod_Views.staffApproveLeave, name="staff_approve_leave"),
    path('admin/staff/disapprove/leave/<str:id>', Hod_Views.staffDisapproveLeave, name="staff_disapprove_leave"),

    # Student leave see from admin
    path('admin/student/leave', Hod_Views.studentLeave, name="student_leave"),
    path('admin/student/approve/leave/<str:id>', Hod_Views.studentApproveLeave, name="student_approve_leave"),
    path('admin/student/disapprove/leave/<str:id>', Hod_Views.studentDisapproveLeave, name="student_disapprove_leave"),

    # staff feedback reply see from admin
    path('admin/student/feedback', Hod_Views.studentFeedback, name="student_feedback_reply"),
    path('admin/student/feedback/save', Hod_Views.studentFeedbackSave, name="student_feedback_reply_save"),
    
    # Student feedback reply see from admin
    path('admin/staff/feedback', Hod_Views.staffFeedback, name="staff_feedback_reply"),
    path('admin/staff/feedback/save', Hod_Views.staffFeedbackSave, name="staff_feedback_reply_save"),

    path('admin/student/notifications', Hod_Views.studentNotifications, name="admin_student_notifications"),
    path('admin/student/notifications/save', Hod_Views.saveStudentNotification, name="save_student_notifications"),
    
    path('admin/view/student/attendance', Hod_Views.viewStudentAttendance, name="view_student_attendance"),

    path('admin/section/add', Hod_Views.addSection, name="add_section"),
    path('admin/section/save', Hod_Views.saveSection, name="save_section"),
    path('admin/section/view', Hod_Views.viewSection, name="view_section"),
    path('admin/section/<str:id>delete', Hod_Views.deleteSection, name="delete_section"),
    path('admin/section/<str:id>edit', Hod_Views.editSection, name="edit_section"),
    path('admin/section/update', Hod_Views.updateSection, name="update_section"),



    path('admin/routine/view', Hod_Views.viewRoutine, name="view_routine"),
    path('admin/routine/add', Hod_Views.addRoutine, name="add_routine"),
    path('admin/routine/save', Hod_Views.saveRoutine, name="save_routine"),
    path('admin/routine/<str:id>edit', Hod_Views.editRoutine, name="edit_routine"),
    path('admin/routine/update', Hod_Views.updateRoutine, name="update_routine"),
    path('admin/routine/<str:id>delete', Hod_Views.deleteRoutine, name="delete_routine"),


    path('admin/notice/add', Hod_Views.AddNotice, name="add_notice"),
    path('admin/notice/view', Hod_Views.viewNotice, name="view_notice"),
    path('admin/notice/<str:id>/edit', Hod_Views.editNotice, name="edit_notice"),
    path('admin/notice/update', Hod_Views.updateNotice, name="update_notice"),
    path('admin/notice/<str:id>/delete', Hod_Views.deleteNotice, name="delete_notice"),

    path('admin/result/plan/add', Hod_Views.addResultPlan, name='result_plan'),
    path('admin/result/plan/save', Hod_Views.saveResultPlan, name='save_result_plan'),
    path('admin/result/plan/view', Hod_Views.viewResultPlan, name='view_result_plan'),
    path('admin/result/plan/<str:id>/edit', Hod_Views.editResultPlan, name='edit_result_plan'),
    path('admin/result/plan/update', Hod_Views.updateResultPlan, name='update_result_plan'),
    path('admin/result/plan/<str:id>/delete', Hod_Views.deleteResultPlan, name='delete_result_plan'),

    path('admin/result/view', Hod_Views.adminViewResult, name='admin_view_result'),


    # This is Staff Panel URL
    path('teacher/school', Staff_Views.staff_home, name='staff_home'),
    path('teacher/school/notifications', Staff_Views.staffNotifications, name='staff_notifications'),
    path('teacher/school/notifications/<str:status>/seen', Staff_Views.staffNotificationsSeen, name='staff_notifications_seen'),

    path('teacher/school/leave', Staff_Views.staffApplyLeave, name='staff_apply_leave'),
    path('teacher/school/Apply_leave_save', Staff_Views.staffApplyLeaveSave, name='staff_apply_leave_save'),


    path('teacher/school/feedback', Staff_Views.staffFeedback, name='staff_feedback'),
    path('teacher/school/feedback/save', Staff_Views.staffFeedbackSave, name='staff_feedback_save'),
    
    path('teacher/school/attendance', Staff_Views.SchoolTeacherAttendance, name='school_teacher_attendance'),
    path('teacher/school/attendance/save', Staff_Views.saveSchoolTeacherAttendance, name='save_school_teacher_attendance'),
    path('teacher/school/attendance/view', Staff_Views.viewSchoolTeacherAttendance, name='view_school_teacher_attendance'),
    
    path('teacher/result/add', Staff_Views.addResult, name='add_result'),
    path('teacher/result/save', Staff_Views.saveResult, name='save_result'),
    
    path('teacher/routine/view', Staff_Views.viewRoutine, name='staff_view_routine'),
    path('teacher/notice/view', Staff_Views.viewNotice, name='staff_view_notice'),
    
    path('teacher/my_profile', Staff_Views.myProfile, name='teacher_my_profile'),

    
    
    
    
    # student panel ================
    path('student', Student_Views.studentHome, name='student_home'),
    path('student/notifications', Student_Views.studentNotifications, name='student_notifications'),
    path('student/notifications/<str:status>/seen', Student_Views.studentNotificationsSeen, name='student_notifications_seen'),
    
    path('student/feedback', Student_Views.studentFeedback, name='student_feedback'),
    path('student/feedback/save', Student_Views.saveStudentFeedback, name='save_student_feedback'),
    
    path('student/apply_leave', Student_Views.studentApplyLeave, name='student_apply_leave'),
    path('student/apply_leave/save', Student_Views.studentApplyLeaveSave, name='student_apply_leave_save'),
    
    path('student/attendance/view', Student_Views.studentViewAttendance, name='student_view_attendance'),
    
    path('student/result/view', Student_Views.studentViewResult, name='student_view_result'),
    path('student/routine/view', Student_Views.studentViewRoutine, name='student_view_routine'),

    path('student/my_profile', Student_Views.myProfile, name='student_my_profile'),


    # path('html/pdf', Hod_Views.GeneratePdf.as_view(), name='generate_pdf')

    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)