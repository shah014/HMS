from django.urls import path
from . import views
# from django.conf.urls.static import static
# from django.conf import settings
from django.contrib.auth  import views as auth_views

urlpatterns = [

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('user/', views.userPage, name='user_page'),

    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('team/', views.team, name='team'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('prescribe/<str:pk>/', views.prescribeMe, name='prescribe'),

    path('patient_dash/', views.patient_dash, name="patient_dash"),
    path('doctor_dash/', views.doctor_dash, name="doctor_dash"),


    path('patient_view/<str:pk>/', views.patient_view, name="patient_view"),
    path('doctor_dash/<str:pk>/', views.doctor_view, name="doctor_view"),

    path('createPatient/', views.createPatient, name="createPatient"),
    path('createDoctor/', views.createDoctor, name="createDoctor"),


    path('updatePatient/<str:pk>/', views.updatePatient, name="updatePatient"),
    path('updateDoctor/<str:pk>/', views.updateDoctor, name="updateDoctor"),

    path('delPatient/<str:pk>/', views.delPatient, name="delPatient"),
    path('delDoctor/<str:pk>/', views.delDoctor, name="delDoctor"),

    path('updatePatientView/<str:pk>/', views.updatePatientView, name="updatePatientView"),
    path('updateDoctorView/<str:pk>/', views.updateDoctorView, name="updateDoctorView"),

    path('appointPatient/<str:pk>/', views.appointPatient, name="appointPatient"),

    path('account/', views.accountSettings, name='account'),
    path('doctor_account/', views.doctorSettings, name='doctor_account'),


    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/ResetPassword/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/ResetPassword/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/ResetPassword/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/ResetPassword/password_reset_done.html"),
         name="password_reset_complete"),
]
