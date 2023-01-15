import re
from random import randint
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .utils import EmailThread


# Create your views here.
def register_user(request):
    try:
        if request.method == 'GET':
            return render(request, "app/register.html")

        if request.method == 'POST':
            if all(i for i in request.POST.values()):
                print("Request values : ", [i for i in request.POST.values()])
                print("All values : ", all(i for i in request.POST.values()))
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                dob = request.POST['dob']
                gender = request.POST['gender']
                type_of_user = request.POST['type']
                email = request.POST['email']
                contact = request.POST['contact']
                password = request.POST['password']
                conf_password = request.POST['confirm_password']
                if password == conf_password:

                    user = User.objects.filter(email=email)
                    contact = User.objects.filter(contact=contact)

                    if len(user) == 0:
                        if len(contact) == 0:

                            c_user = User.objects.create(
                                firstname=firstname,
                                lastname=lastname,
                                dob=dob,
                                gender=gender,
                                type=type_of_user,
                                email=email,
                                contact=contact,
                                password=make_password(password))
                            c_user.save()
                            recipient_list = c_user.email
                            EmailThread(f'This is your username-{c_user.email} and  password-{password}  please login to continue.',
                                        recipient_list=[recipient_list]).start()
                            messages.success(request, "User Created,Please login to continue !!")
                            return redirect('login')
                        else:
                            messages.error(request, "Contact already exists")
                            return redirect('users')

                    else:
                        messages.error(request, "Email already exists")
                        return redirect('users')
                else:
                    messages.error(request, "Password Doesn't Match")
                    return redirect('register')
            else:
                messages.error(request, "Please fill all the mandatory fields")
                return redirect('users')

    except Exception as e:
        messages.error(request, "Something went wrong !!")
        return redirect("users")


def login_user(request):
    if request.method == 'GET':
        return render(request, "app/login.html")

    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect('users')
        else:
            logout(request)
            return render(request,"app/login.html")


def login_data(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            get_user = User.objects.get(email=email)
            if get_user:
                return redirect('users')
            else:
                messages.error(request, "User Doesn't Exist")
                return redirect("/")
        else:
            messages.error(request, "Incorrect credentials")
            return redirect("/")

    else:
        messages.error(request,"Session Expired")
        return redirect("login")

@login_required
def users(request):
    try:
        if request.method == "GET":
            user = User.objects.all()
            return render(request,"app/users.html",{'user': user})
        else:
            messages.error(request, "Please Login to continue !!")
            return redirect("/")

    except Exception as ep:
        print(ep)
        messages.error(request, "Something went wrong !!")
        return redirect("/")


def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')


def forgot(request):
    return render(request,"app/fp-email.html")


def fpOTPPage(request):
    if 'otp' in request.session:
        return render(request, "app/fp-otp.html")
    else:
        messages.error(request, "Session Expired")
        return redirect("/")


def fpOTP(request):
    if 'otp' in request.session:
        if request.method == 'POST':
            t1 = request.POST['t1']
            t2 = request.POST['t2']
            t3 = request.POST['t3']
            t4 = request.POST['t4']
            total_otp = t1+t2+t3+t4

            if total_otp.rstrip(' ') == "":
                messages.error(request,"Please fill all the mandatory fields")
                return redirect('forgototppage')
            else:
                try:
                    if request.session['otp'] ==  int(total_otp):
                        print(int(total_otp))
                        print(request.session['otp'])
                        del request.session['otp']
                        return redirect('forgotpasswordpage')
                    else:
                        messages.error(request, "Invalid OTP! Please try again.")
                        return redirect('forgototppage')
                except Exception as ep:
                    print("Error--->",ep)
                    request.user.flush()
                    return render(request,"app/badrequest.html")
        else:
            return render(request,"app/badrequest.html")
    else:
        return redirect('/')

def femail(request):
    return render(request, "app/fp-email.html")

def fpPasswordPage(request):
    if 'email' in request.session:
        messages.error(request,"Minimum 8 characters required! ( One Upper Case & One Special Character mandatory)")
        return render(request, "app/fp-password.html")
    else:
        messages.error(request, "Session Expired")
        return redirect("/")


def fpPasswordData(request):
    if 'email' in request.session:
        if request.method =='POST':
            password = request.POST['password']
            cpassword = request.POST['cpassword']
            special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if password.rstrip(' ') == "" or cpassword.rstrip(' ') == "":
                messages.error(request,"Please fill all the mandatory fields")
                return redirect('forgotpasswordpage')
            else:
                user = User.objects.get(email=request.session['email'])
                if password == cpassword:
                    if len(password) >= 8 and special_char.search(password) != None:
                        user.password = make_password(password)
                        user.save()
                        messages.success(request, "Password changed successfully. Login to continue")
                        return redirect("login")
                    else:
                        messages.error(request,"Invalid Password Format")
                        return redirect('forgotpasswordpage')
                else:
                    messages.error(request,"Password and Confirm Password doesn't match")
                    return redirect('forgotpasswordpage')
        else:
            return render(request,"app/badrequest.html")
    else:
            messages.error(request,"Session Expired")
            return redirect("badrequest")


def fpEmailPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        if email.rstrip(' ') == "":
            messages.error(request, "Please Enter Your Email")
            return redirect('forgotemail')
        else:
            try:
                get_user = User.objects.filter(email=email).first()
                print(get_user)
                if get_user:
                    otp_verify = randint(1000, 9999)
                    print(get_user.email)
                    request.session['otp'] = otp_verify
                    request.session['email'] = email
                    subject = f'Your Forgot Password OTP is {otp_verify}'
                    recipient_list = get_user.email
                    EmailThread(message=subject, recipient_list=[recipient_list]).start()
                    return redirect('forgototppage')
                else:
                    messages.error(request, "User doesn't exist")
                    return redirect('forgotemail')

            except Exception as ep:
                request.user.flush()
                return render(request,"app/badrequest.html")
    else:
        messages.error(request,"Session Expired")
        return redirect("/")


def bad_Request(request):
    request.user.flush()
    return render(request,"app/badrequest.html")


@login_required
def profile(request):
    try:
        if request.method == "GET":
            pk = request.user.id
            profile = User.objects.filter(id=pk)
            return render(request, "app/profile.html", {'profile': profile})
        else:
            messages.error(request, "Something went wrong !!")
            return redirect("users")

    except Exception as ep:
        print(ep)
        messages.error(request, "Something went wrong !!")
        return redirect("/")


@login_required
def update_user(request):
    try:
        if request.method == "POST":
            if all(i for i in request.POST.values()):
                user_id = request.POST.get("user_id", None)
                firstname = request.POST.get("firstname")
                lastname = request.POST.get("lastname")
                email = request.POST.get("email")
                contact = request.POST.get("contact")
                gender = request.POST.get("gender")
                dob = request.POST.get("dob")

                User.objects.filter(id=user_id).update(
                    email=email,
                    firstname=firstname,
                    lastname=lastname,
                    contact=contact,
                    dob=dob,
                    gender=gender
                )
                messages.success(request, "User updated Successfully")
                return redirect("profile")
            else:
                messages.error(request, "Please fill all the mandatory fields")
                return redirect('profile')

    except Exception as ep:

        messages.error(request, str(ep))
        return redirect("profile")


def show_user(request, pk):
    try:
        if request.method == "GET":
            user = User.objects.get(id=pk)
            return JsonResponse(
                {
                    "id": user.id,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "email": user.email,
                    "contact": user.contact,
                    "gender": user.gender,
                    "dob": user.dob,

                }
            )

    except Exception as ep:
        return JsonResponse({"error": str(ep)})


@login_required
def change_password(request):
    try:
        if request.method == "GET":
            user = User.objects.all()
            return render(request,"app/password.html",{'user':user})

        if request.method == "POST":
            pk = request.user.id
            password = request.POST['password']
            conf_password = request.POST['confirm_password']
            if all(i for i in request.POST.values()):
                if password == conf_password:
                    User.objects.filter(id=pk).update(
                        password=make_password(password)
                    )
                    messages.success(request, "Password changed successfully, Login to Continue !!")
                    return redirect("login")
                else:
                    messages.error(request, "confirm password doesn't match to your new password !!")
                    return redirect('change-password')
            else:
                messages.error(request, "Please fill all the mandatory fields")
                return redirect('change-password')

    except Exception as ep:
        print(ep)
        messages.error(request, "Something went wrong !!")
        return redirect("/")
