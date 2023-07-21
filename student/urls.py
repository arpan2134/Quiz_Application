from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

app_name="student"

urlpatterns = [
path('studentclick/', views.studentclick_view),
path('studentlogin/', LoginView.as_view(template_name='studentlogin.html'),name='studentlogin'),
path('signup/', views.student_signup_view,name='studentsignup'),

path('student-dashboard/', views.student_dashboard_view, name='student-dashboard'),

path('student-exam/', views.student_exam_view,name='student-exam'),
path('take-exam/<int:pk>/', views.take_exam_view,name='take-exam'),
path('start-exam/<int:pk>/', views.start_exam_view, name='start-exam'),


path('calculate-marks/', views.calculate_marks_view, name='calculate_marks'),
 path('view-result/', views.view_result_view, name='view_result'), 
path('check-marks/<int:pk>/', views.check_marks_view, name='check-marks'),
path('student-marks/', views.student_marks_view,name='student-marks'),
]       