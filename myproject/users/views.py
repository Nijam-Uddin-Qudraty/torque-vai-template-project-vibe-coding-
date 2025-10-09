from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

def delete_student(request, student_id):
    try:
        student = UserProfile.objects.get(id=student_id)
        student.user.delete()  # deletes UserProfile automatically
    except UserProfile.DoesNotExist:
        pass  # ignore if not found

    return redirect('student_list')

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
