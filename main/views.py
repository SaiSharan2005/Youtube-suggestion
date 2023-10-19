from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Sub_course,UserSelectedCourse,Category,Sub_Topic,UserSelected_Sub
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    if request.user.is_authenticated :
        name = request.user
        course = UserSelectedCourse.objects.filter(host = name)
        courses = []

        for i in course:
            dam=Category.objects.get(name = i.course)
            courses.append(dam)
            print(dam.thumbnail.url)
        allCourses = Category.objects.all()
        
        context = {"courses":courses,"allCourses":allCourses}
        return render(request,'main/home.html',context )


    else :
        return redirect("non-login-home")


def sign_up(request):
    form = UserCreationForm()


    if request.method == 'POST':
        print(form)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    context = {"form":form}
    return render(request, "main/signup.html",context)


def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            pass
    return render(request, 'main/login.html')


def log_out(request):
    logout(request)
    return redirect('home')


def nonLogInUser(request):

    return render(request,"main/non-login.html")


def learner(request):
    name = request.user
    courses = UserSelectedCourse.objects.filter(host = name)
    if courses:
        Category_data= []
        for course in courses:
            Category_data += Category.objects.filter(name = course.course)
           
    return render(request,'main/learner.html',{"Category_data":Category_data})

# @login_required
def lecture(request,Topic,SubTopic):
    if UserSelectedCourse.objects.filter(host = request.user).count()>0:

        main = Category.objects.get(name = Topic)
        subTopic = Sub_course.objects.filter(main = main)
        sub_topic = []
        tut = Sub_Topic.objects.get(topic_name = SubTopic)
        

        bool,done = False,False
        back,next = None,None
        for topic in subTopic:
            tem= []
            tem.append(topic)
            tem.append(Sub_Topic.objects.filter(main = topic))
            if not done:
                for top in Sub_Topic.objects.filter(main = topic):
                    if bool :
                        next = top
                        done = True
                        break
                    if top == tut:
                        bool = True
                        continue
                    back = top
            sub_topic.append(tem)
        
        # bool = False
        # back,next = None,None
        # for i in subTopic:
        #     if bool :
        #         next = i 
        #         break
        #     if i == tut:
        #         bool = True
        #         continue
        #     back = i
        print(back,next)
        if back:
            back = Sub_Topic.objects.get(topic_name = back )
        if next:
            next = Sub_Topic.objects.get(topic_name = next)
        
        context = {"main":main,"sub_topic":sub_topic,"tut":tut,"back":back,"next":next}

        return render(request, 'main/learner.html',context)
    else:
        return redirect("topic",Topic=Topic)

    #     sub_topic = []
    #     for topic in subTopic:
    #         if  UserSelected_Sub.objects.filter(host = request.user,main = topic).count()==1:
    #             tem= []
    #             tem.append(topic)
    #             tem.append(Sub_Topic.objects.filter(main = topic))
    #             sub_topic.append(tem)
        
    #     tut = Sub_Topic.objects.get(topic_name = SubTopic)
    #     bool = False
    #     back,next = None,None
    #     for i in subTopic:
    #         if bool :
    #             next = i 
    #             break
    #         if i == tut:
    #             bool = True
    #             continue
    #         back = i
    #     if back:
    #         back = Sub_course.objects.get(topic_name = back , main = main)
    #     if next:
    #         next = Sub_course.objects.get(topic_name = next)
        
    #     context = {"main":main,"sub_topic":sub_topic,"tut":tut,"back":back,"next":next}

    #     return render(request, 'main/learner.html',context)
    # else:
    #     return redirect("topic",Topic=Topic)

@login_required(login_url = "/log_in")  
def topic(request ,Topic):
    course = Category.objects.get(name = Topic)
    if request.method == "POST":
            if request.POST.get("enroll"):
                b = UserSelectedCourse(host = request.user,course = course)
                b.save()
    sub_course = Sub_course.objects.filter(main = course)
    # if UserSelectedCourse.objects.filter(host = request.user,course = course).count()==1:
    #     sub_topic = []
    #     for topic in sub_course:
    #         if  UserSelected_Sub.objects.filter(host = request.user,main = topic).count()==1:
    #             tem= []
    #             tem.append(topic)
    #             tem.append(Sub_Topic.objects.filter(main = topic))
    #             sub_topic.append(tem)
    #     enroll  = UserSelectedCourse.objects.filter(host = request.user,course = course)
        
    #     context = {"course":course,"sub_topic":sub_topic,"enroll":enroll ,"next":sub_topic[0]}

    #     return render(request,"main/topic.html",context )
    # else:
    sub_topic = []
    for topic in sub_course:
        tem= []
        tem.append(topic)
        tem.append(Sub_Topic.objects.filter(main = topic))
        sub_topic.append(tem)
    enroll  = UserSelectedCourse.objects.filter(host = request.user,course = course)
    
    context = {"course":course,"sub_topic":sub_topic,"enroll":enroll ,"next":sub_topic[0]}

    return render(request,"main/topic.html",context )






def courses(request):
    courses = Category.objects.all()
    context = {"courses":courses}
    return render(request,"main/courses.html",context)

 

