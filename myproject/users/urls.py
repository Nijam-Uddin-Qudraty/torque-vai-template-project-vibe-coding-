from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('students/', views.student_list, name='student_list'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path("login/", views.login_view, name="login"),
    path("verify-otp/<str:username>/", views.verify_otp_view, name="verify_otp"),
    path("resend-otp/<str:username>/", views.resend_otp, name="resend_otp"),
]
