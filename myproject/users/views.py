from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, OtpToken
from django.utils import timezone
from .signals import create_otp
def logout_view(request):
    logout(request)
    redirect("/")


def login_view(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password = password)
        if user is not None:
            login(req,user)
            return redirect("student_list")
        else:
            messages.error(req,"Invalid credential")
    return render(req, "login.html")


def resend_otp(request, username):
    user = get_object_or_404(User, username=username)
    create_or_refresh_otp(user)
    messages.success(request, "A new OTP has been sent to your email.")
    return redirect("verify_otp", username=user.username)

def verify_otp_view(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == "POST":
        otp_input = request.POST.get("otp")

        try:
            otp_record = OtpToken.objects.filter(user=user).last()
        except OtpToken.DoesNotExist:
            messages.error(request, "No OTP found. Please request a new one.")
            return redirect("resend_otp", username=user.username)

        if timezone.now() > otp_record.expires_at:
            messages.error(request, "Your OTP has expired. Please request a new one.")
            return redirect("resend_otp", username=user.username)

        if otp_record.otp == otp_input:
            user.is_active = True
            user.save()
            otp_record.delete()  # clean up after successful verification
            messages.success(request, "Your account has been verified. You can now log in.")
            return redirect("login")  # redirect to login page
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "verify_otp.html", {"username": username})



@login_required
def delete_student(request, student_id):
    try:
        student = UserProfile.objects.get(id=student_id)
        student.user.delete()  # deletes UserProfile automatically
    except UserProfile.DoesNotExist:
        pass  # ignore if not found

    return redirect('student_list')

@login_required
def edit_student(request, student_id):
    try:
        student = UserProfile.objects.get(id=student_id)
    except UserProfile.DoesNotExist:
        messages.error(request, "Student not found!")
        return redirect('student_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')

        if not username or not email:
            messages.error(request, "Username and Email are required!")
            return render(request, 'student_form.html', {'student': student})

        # Update user
        student.user.username = username
        student.user.email = email
        student.user.save()

        # Update profile
        student.bio = bio
        student.location = location
        student.save()

        messages.success(request, "Student updated successfully!")
        return redirect('student_list')

    return render(request, 'student_form.html', {'student': student})



def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        bio = request.POST.get('bio', '')
        location = request.POST.get('location', '')

        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required!")
            return render(request, 'student_form.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'student_form.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'student_form.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'student_form.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, bio=bio, location=location)

        messages.success(request, "User created successfully!")
        return redirect('home')

    return render(request, 'student_form.html')

def student_list(request):
    students = UserProfile.objects.select_related('user').all()
    return render(request, 'student_list.html', {'students': students})
