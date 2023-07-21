from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz_app.models import Course, Question, Result


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    
    return render(request,'studentclick.html')


def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect(reverse('student:studentlogin'))
    
    return render(request,'studentsignup.html',context=mydict)





def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

##student dashboard

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    total_course = Course.objects.all().count()
    total_question = Question.objects.all().count()
    courses = Course.objects.all()
    student = models.Student.objects.get(user_id=request.user.id)
    results = Result.objects.filter(student=student)

    context = {
        'total_course': total_course,
        'total_question': total_question,
        'courses': courses,
        'results': results
    }
    return render(request, 'student_dashboard.html', context)





@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=Course.objects.all()
    return render(request,'student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, pk):
    course = Course.objects.get(id=pk)
    questions = Question.objects.all().filter(course=course)
    total_questions = questions.count()
    total_marks = questions.aggregate(Sum('marks'))['marks__sum']
    
    context = {
        'course': course,
        'total_questions': total_questions,
        'total_marks': total_marks,
    }
    
    return render(request, 'take_exam.html', context)


###start exam 
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=Course.objects.get(id=pk)
    questions=Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'start_exam.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = Course.objects.get(id=course_id)

        total_marks = 0
        questions = Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            selected_ans = request.COOKIES.get(str(i + 1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = Result()
        result.marks = total_marks
        result.exam = course
        result.student = student
        result.save()

        return HttpResponseRedirect(reverse('student:view_result'))



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses = Course.objects.all()
    return render(request, 'view_result.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=Course.objects.all()
    return render(request,'student_marks.html',{'courses':courses})


  