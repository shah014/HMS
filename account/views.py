from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filters import *
# for register
from django.contrib.auth.forms import UserCreationForm
# for flash message
from django.contrib import messages   # now adding the message to our template
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'P':
                group = Group.objects.get(name='patient')
                user.groups.add(group)
                Patient.objects.create(
                    user=user
                )
            if user_type == 'D':
                group = Group.objects.get(name='doctor')
                user.groups.add(group)
                Doctor.objects.create(
                    user=user
                )
            messages.success(request, 'Account Created Successfully for ' + username)
            return redirect('login')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
                print(msg)
    context = {'form': form}
    return render(request, 'accounts/RegLogin/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password invalid !!')

    context = {}
    return render(request, 'accounts/RegLogin/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    appointment = Appointment.objects.all()

    total_patient = patient.count()
    total_doctor = doctor.count()
    appointment_pending = appointment.filter(status="pending").count()

    context = {'patient': patient, 'doctor': doctor, 'appointment': appointment,
               'total_patient': total_patient, 'total_doctor': total_doctor,
               'appointment_pending': appointment_pending}
    return render(request, 'accounts/dashboard.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'patient', 'doctor'])
def about_us(request):
    context = {}
    return render(request, 'accounts/about.html', context)


def team(request):
    context = {}
    return render(request, 'accounts/team.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient', 'doctor'])
def userPage(request):
    group = None
    group = request.user.groups.all()[0].name
    if group == 'doctor':
        appointment = request.user.doctor.appointment_set.all()
        total_appointment = appointment.count()
        context = {'total_appointment': total_appointment, 'appointment': appointment}
        return render(request, 'accounts/doctor/DoctorProfile/user.html', context)
    if group == 'patient':
        patient = request.user.patient
        appointment = patient.appointment_set.all()
        context = {'appointment': appointment}
        return render(request, 'accounts/patient/PatientProfile/user.html', context)


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin', 'patient', 'doctor'])
def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        message = request.POST.get('message')

        sub = f'Message from {name}[{email}]'
        from_email = 'anilshah65156@gmail.com'
        to = ['anilshah98600@gmail.com']
        message = message

        send_mail(subject=sub, message=message, from_email=from_email, recipient_list=to, fail_silently=True)
        return redirect('home')
    return render(request, 'accounts/contact.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def patient_dash(request):
    patient = Patient.objects.all()
    appointment = Appointment.objects.all()

    total_patient = patient.count()
    active_patient = appointment.filter(status="Active").count()
    appointment_pending = appointment.filter(status="Pending").count()

    myFilter = PatientFiter(request.GET, queryset=patient)
    patient = myFilter.qs

    context = {'patient': patient, 'appointment': appointment,
               'total_patient': total_patient, 'active_patient': active_patient,
               'appointment_pending': appointment_pending, 'myFilter': myFilter}

    return render(request, 'accounts/patient/patientDash/patient-dash.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def doctor_dash(request):
    doctor = Doctor.objects.all()
    total_doctor = doctor.count()
    myFilter = Doctorfilter(request.GET, queryset=doctor)
    doctor = myFilter.qs

    context = {'doctor': doctor, 'total_doctor': total_doctor, 'myFilter': myFilter}
    return render(request, 'accounts/doctor/doctorDash/doctor-dash.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'patient'])
def patient_view(request, pk):
    patient = Patient.objects.get(id=pk)
    appointment = patient.appointment_set.all()
    # myFilter = AppointmentFilter(request.GET, queryset=appointment)
    # appointment = myFilter.qs
    # appointment = Appointment.objects.all()
    # appointment = Appointment.objects.get(appointDate=patient.appointDate)
    # context = {'patient': patient, 'appointment': appointment}
    context = {'patient': patient, 'appointment': appointment}

    return render(request, 'accounts/patient/patientView/patient-view.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'doctor'])
def doctor_view(request, pk):
    doctor = Doctor.objects.get(id=pk)
    context = {'doctor': doctor}
    return render(request, 'accounts/doctor/doctorView/doctor-view.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'patient'])
def createPatient(request):
    form = PatientForm()

    if request.method == "POST":
        form = PatientForm(request.POST)
        form.is_valid()
        form.save()
        return redirect('user_page')
    context = {'form': form}
    return render(request, 'accounts/createform/createPatient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'doctor'])
def createDoctor(request):
    form = DoctorForm()

    if request.method == "POST":
        form = DoctorForm(request.POST)
        form.is_valid()
        form.save()
        return redirect('user_page')
    context = {'form': form}
    return render(request, 'accounts/createform/createDoctor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updatePatient(request, pk):
    patient = Patient.objects.get(id=pk)
    form = PatientForm(instance=patient)

    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        form.is_valid()
        form.save()
        return redirect('patient_dash')
    context = {'form': form}
    return render(request, 'accounts/createform/createPatient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateDoctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    form = DoctorForm(instance=doctor)

    if request.method == "POST":
        form = DoctorForm(request.POST, instance=doctor)
        form.is_valid()
        form.save()
        return redirect('doctor_dash')
    context = {'form': form}
    return render(request, 'accounts/createform/createDoctor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delPatient(request, pk):
    patient = Patient.objects.get(id=pk)

    if request.method == "POST":
        patient.delete()
        return redirect('patient_dash')
    context = {'patient': patient}
    return render(request, 'accounts/deleteForm/deletePatient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delDoctor(request, pk):
    doctor = Doctor.objects.get(id=pk)

    if request.method == "POST":
        doctor.delete()
        return redirect('doctor_dash')
    context = {'doctor': doctor}
    return render(request, 'accounts/deleteForm/deleteDoctor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'patient'])
def updatePatientView(request, pk):
    patient = Patient.objects.get(id=pk)
    form = PatientViewForm(instance=patient)

    if request.method == "POST":
        form = PatientViewForm(request.POST, instance=patient)
        form.is_valid()
        form.save()
        return redirect('patient_dash')
    context = {'form': form}
    return render(request, 'accounts/createform/update_patient_view.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'doctor'])
def updateDoctorView(request, pk):
    doctor = Doctor.objects.get(id=pk)
    form = DoctorViewForm(instance=doctor)

    if request.method == "POST":
        form = DoctorViewForm(request.POST, instance=doctor)
        form.is_valid()
        form.save()
        return redirect('doctor_dash')
    context = {'form': form}
    return render(request, 'accounts/createform/update_doctor_view.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def appointPatient(request, pk):
    AppointFormSet = inlineformset_factory(Patient, Appointment, fields=('appointDate', 'doctor', 'status'), extra=1)
    patient = Patient.objects.get(id=pk)
    formset = AppointFormSet(queryset=Appointment.objects.none(), instance=patient)

    if request.method == 'POST':
        formset = AppointFormSet(request.POST, instance=patient)
        formset.is_valid()
        formset.save()
        return redirect('patient_dash')
    context = {'formset': formset}
    return render(request, 'accounts/appointForm/appointPatient.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def accountSettings(request):
    patient = request.user.patient
    form = PatientForm(instance=patient)
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES, instance=patient)
        form.is_valid()
        form.save()

    content = {'form': form}
    return render(request, 'accounts/patient/PatientProfile/account_settings.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def doctorSettings(request):
    doctor = request.user.doctor
    form = DoctorForm(instance=doctor)
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        form.is_valid()
        form.save()

    content = {'form': form}
    return render(request, 'accounts/doctor/DoctorProfile/account_settings.html', content)


@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def prescribeMe(request, pk):
    appointment = Appointment.objects.get(id=pk)
    context = {'appointment': appointment}
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        to = request.POST.get('to_email')
        message = request.POST.get('message')
        sub = f'Message from {name}[{email}]'
        from_email = 'anilshah65156@gmail.com'
        to = [to]
        message = message
        send_mail(subject=sub, message=message, from_email=from_email, recipient_list=to, fail_silently=True)
        return redirect('home')
    return render(request, 'accounts/doctor/prescribeForm/prescribe.html', context)
