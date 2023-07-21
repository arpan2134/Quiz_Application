from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz_app.models import Course, Question
from student.models import Student
from quiz_app import forms as QFORM

#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('afterlogin'))

    return render(request,'teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect(reverse('teacher:teacherlogin'))

    return render(request, 'teachersignup.html', context=mydict)




def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    dict={
    
    'total_course':Course.objects.all().count(),
    'total_question':Question.objects.all().count(),
    'total_student':Student.objects.all().count()
    }
    return render(request,'teacher_dashboard.html',context=dict)




@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher_exam.html')





@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request,'teacher_add_exam.html',{'courseForm':courseForm})




@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = Course.objects.all()
    return render(request,'teacher_view_exam.html',{'courses':courses})




@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')




@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request,'teacher_question.html')




@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request,'teacher_add_question.html',{'questionForm':questionForm})




@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    courses= Course.objects.all()
    return render(request,'teacher_view_question.html',{'courses':courses})




@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=Question.objects.all().filter(course_id=pk)
    return render(request,'see_question.html',{'questions':questions})




@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')