from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Query
from django.utils.html import escape
from django.core.mail import send_mail
import re


# we can create a bug here...
@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')


def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if len(username) > 20 or username == "" or email == "" or pass1 == "" or pass2 == "":
            msg = "Input all the fields"
            return render(request, 'signup.html', {'msg': msg})
        if User.objects.filter(username=username).exists():
            msg = "UserName already exist"
            return render(request, 'signup.html', {'msg': msg})

        # Create the new user
        try:
            if pass1 == pass2:
                my_user = User.objects.create_user(username=username, email=email, password=pass1)
                my_user.save()
                return redirect('login')
            else:
                msg = "Your password is incorrect."
                return render(request, 'signup.html', {'msg': msg})
        except:
            msg = "Your password is incorrect."
            return render(request, 'signup.html', {'msg': msg})
    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        if not re.match("^[a-zA-Z0-9]+$", username):
            msg = "Username should only contain letters and numbers."
            return render(request, 'login.html', {'msg': msg})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            msg = "Your UserName and password doesn't match"
            return render(request, 'login.html', {'msg': msg})
    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


def PlacementPage(request):
    return render(request, 'placement_info.html')


def query(request):
    return render(request, 'query.html')


def submitedQuery(request):
    if request.method == 'POST':
        useremail = request.POST.get('Email')
        username = request.POST.get('Name')
        userquery = request.POST.get('Query')
        if not re.match("^[a-zA-Z0-9]+$", username):
            msg = "Username should only contain letters and numbers."
            return render(request, 'query.html', {'msg': msg})
        if not re.match("^[a-zA-Z0-9]+$", userquery):
            msg = "Userquery should only contain letters and numbers."
            return render(request, 'query.html', {'msg': msg})
        q = Query(useremail=useremail, username=username, userquery=userquery)
        q.save()
        # it is used for the admin
        subject = f'New Query from {username}'
        message = f'Name: {username}\nEmail: {useremail}\nQuery: {userquery}'
        from_email = 'gurupruthvi61@gmail.com'
        recipient_list = ['20ise0059@vvce.ac.in', '20cse0133@vvce.ac.in', '20cse0123@vvce.ac.in',
                          '20cse0094@vvce.ac.in', '20aiml0072@vvce.ac.in']
        # send_mail(subject, message, from_email, recipient_list)

        # it is used for the user
        subject = f'Query is Accepted'
        message = f'Name: {username}\nEmail: {useremail}\nQuery: {userquery}'
        from_email = 'gurupruthvi61@gmail.com'
        recipient_list = [{useremail}]
        # try:
        #     send_mail(subject, message, from_email, recipient_list)
        # except:
        #     msg = "Your email is not valid"
        #     return render(request, 'query.html', {'msg': msg})
        # msg = "Query submitted successfully"
        # return render(request, 'query.html', {'msg': msg})
    else:
        return render(request, 'query.html')


class HomePageView(TemplateView):
    template_name = 'basic.html'


class ContactPage(TemplateView):
    template_name = 'contact.html'
