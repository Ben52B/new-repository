from django.shortcuts import render
from appfour.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.




def index(request):
    context_dic={'text':"Please go to login"}
    return render(request,'appfour/index.html', context=context_dic)

def register(request):

    registered=False

    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.my_user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request,'appfour/registration.html',
                        {'user_form':user_form,
                          'profile_form':profile_form,
                          'registered':registered})

def user_login(request):
    print("im in")
    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return render(request,'appfour/my_profile.html')
            else:
                return HttpResponse("account not active")
        else:
            print("faild log in accure")
            print("user name: {} and password {}".format(username,password))
            return HttpResponse ("user name or password are not maching")
    else:
        print("im in else")
        return render(request,'appfour/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def my_profile(request):
    return render(request,'appfour/my_profile.html')
