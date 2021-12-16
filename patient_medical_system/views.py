from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf 
from . import forms,models
from django.db.models import Q

# --- TESTING ---
def test(request):
    return render(request, 'demodemo.html', {'account': 'user'})


# --- USER ---
# test/
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def is_staff(user):
    return user.groups.filter(name='STAFF').exists()

def handle_user(request):
    if is_staff(request.user):
        print("ITS AN STAFF")
        request.session['type'] = 'STAFF'
        return redirect('dashboard')
    elif is_patient(request.user):
        print("It Is a User")
        request.session['type'] = 'PATIENT'
        return redirect('dashboard')

# /
def home(request):
    # print("BRUH")
    # return render(request, 'front-updated/index.html')
    # if request.user.is_authenticated:
        # return redirect('handle user')
    return render(request, 'home.jinja', {'account': None})

# /user_home
def user_home(request):
    return render(request, 'user_home.html', {'account': 'user'})

# /signup
def user_signup(request):
    user_form = forms.UserForm()
    patient_form = forms.PatientForm()
    if request.method=='POST':
        user_form = forms.UserForm(request.POST, request.FILES)
        patient_form = forms.PatientForm(request.POST, request.FILES)
        if user_form.is_valid():
            # user = user_form.save()
            print("Type:", "Patient")
            print("Username:", user_form.cleaned_data['username'])
            print("Email:", user_form.cleaned_data['email'])
            print("Password:", user_form.cleaned_data['password'])
            print("RE Password:", user_form.cleaned_data['re_password'])
            print(patient_form.is_valid())
            if patient_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                patient = patient_form.save(commit=False)
                patient.user = user
                patient.save()

                patient_group = Group.objects.get_or_create(name='PATIENT')
                patient_group[0].user_set.add(user)
                return redirect('user login')
            else:
                print(patient_form.errors)

    ctx = {'user_form': user_form, 'patient_form': patient_form}
    return render(request, 'patient/signup.jinja', context=ctx)

# /signup
def staff_signup(request):
    user_form = forms.UserForm()
    if request.method=='POST':
        user_form = forms.UserForm(request.POST, request.FILES)
        if user_form.is_valid():
            print("Type:", "staff")
            print("Username:", user_form.cleaned_data['username'])
            print("Email:", user_form.cleaned_data['email'])
            print("Password:", user_form.cleaned_data['password'])
            print("RE Password:", user_form.cleaned_data['re_password'])
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            staff_group = Group.objects.get_or_create(name='STAFF')
            staff_group[0].user_set.add(user)
            return redirect('staff login')
        else:
            print(user_form.errors)

    ctx = {'user_form': user_form}
    return render(request, 'staff/signup.jinja', context=ctx)

# /login
def user_login(request):
    user_form = forms.UserForm
    if request.method == "POST":
        # user_form = forms.UserForm(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Type:", "Patient")
        print("Username:", username)
        print("Password:", password)

        user = authenticate(username=username, password=password)
        if user:
            print("here")
            login(request, user)
            return redirect("dashboard")

    ctx = {'form': user_form}       
    return render(request, 'patient/login.jinja', context=ctx)

# render: user_login.jinja
# /logout
def user_logout(request):
    logout(request)
    return redirect("home")



# /dashboard
@login_required
def patient_dashboard(request):
    ctx = {"user": request.user}
    user_type= request.session['type']
    user = request.user.id
        # query = models.Appointment.objects.filter(pk=user, status='Pending')
    pending = models.Appointment.objects.filter(patient__user_id=user, status="Pending")
    approved = models.Appointment.objects.filter(patient__user_id=user, status="Approved")
        # for appointment in query:

    
    # assert len(query) > 1:
        # print("THIS IS WRONG")
    # else:
    # if len(query) == 1:
        # appointment = query[0]
    ctx['pending'] = pending
    ctx['approved'] = approved

    return render(request, "patient/dashboard.jinja", context=ctx)
 
@login_required
def staff_dashboard(request):
    ctx = {"user": request.user}
    user_type= request.session['type']
    print(user_type)
    print(request.user.id)
    user = request.user.id
    # query = models.Appointment.objects.filter(pk=user, status='Pending')
    # query = models.Appointment.objects.all().exclude(status__in=("Cancelled", "Rejected"))
    query = models.Appointment.objects.all()
        # for appointment in query:
    ctx['appointments'] = query
    return render(request, "staff/dashboard.jinja", context=ctx)

# /add_appointment
@login_required
def add_appointment(request):
    appointment_form = forms.AppointmentForm()
    if request.method == "POST":
        appointment_form = forms.AppointmentForm(request.POST)
        appointment_date = request.POST["appointment_date"]
        appointment_time = request.POST["appointment_time"]

        # print(request.POST["appointment_date"])
        print(request.POST["appointment_type"])
        print(appointment_date)
        print(appointment_time)

        if appointment_form.is_valid():
            patient = models.Patient.objects.get(user__id=request.user.id)
            # query = models.Appointment.objects.filter(user_id=request.user.id, status="Pending")
            # if len(query) >= 1:
            #     # message.something
            #     print("You already have a pending query. Wait for confirmation or cancel this")
            #     return redirect("dashboard")
            appointment = appointment_form.save(commit=False)
            appointment.appointment_date = appointment_date
            appointment.appointment_time = appointment_time
            appointment.patient = patient
            appointment.save()
            return redirect("dashboard")
        else:
            print(appointment_form.errors)
        
    ctx ={'form': appointment_form}
    return render(request, 'patient/add_appointment.jinja', context=ctx)


# user reject appointment
@login_required
def cancel_appointment(request, id):
    if request.method == "POST":
        # get appointment by id
        apnt = models.Appointment.objects.get(id=id)
        user = request.user.id
        # check if the user who created appointment is the one who will cancel
        if apnt.user.id == user and apnt.status == "Pending":
            apnt.status = "Cancelled"
            apnt.save()
        return redirect("dashboard")
    else: 
        return redirect("home")

@login_required
def reject_appointment(request, id):
    if request.method == "POST":
        apnt = models.Appointment.objects.get(id=id)
        if request.session.get("type") == "STAFF" and apnt.status == "Pending":
            apnt.status = "Rejected"
            apnt.save()
        return redirect("dashboard")
    else: 
        return redirect("home")

@login_required
def approve_appointment(request, id):
    if request.method == "POST":
        apnt = models.Appointment.objects.get(id=id)
        if request.session.get("type") == "STAFF" and apnt.status == "Pending":
            apnt.status = "Approved"
            apnt.save()
        return redirect("dashboard")
    else: 
        return redirect("home")

@login_required
def admit_appointment(request, id):
    if request.method == "POST":
        apnt = models.Appointment.objects.get(id=id)
        if request.session.get("type") == "STAFF" and apnt.status == "Approved":

            # save discharge date
            patient = models.Patient.objects.get(user__id=apnt.patient.user.id)
            discharge = models.Discharge(patient=patient, appointment=apnt)
            discharge.save()

            apnt.status = "Ongoing"
            apnt.save()
        return redirect("dashboard")
    else: 
        return redirect("home")

@login_required
def discharge_patient(request, discharge_id):
    discharge = models.Discharge.objects.get(id=discharge_id)
    ctx = {'discharge': discharge}
    if request.session.get("type") == "STAFF" and discharge.appointment.status == "Ongoing":
        if request.method == "POST":
            # if request.session.get("type") == "STAFF" and apnt.status == "Approved":
            pass
                # save discharge date
                # patient = models.Patient.objects.get(user__id=apnt.patient.user.id)
                # discharge = models.Discharge(patient=patient, appointment=apnt)
                # discharge.save()

                # apnt.status = "Ongoing"
                # apnt.save()
            # return redirect("dashboard")
        else: 
            return render(request, "/staff/discharge.jinja", context = ctx)
    else:
        return redirect("admitted")
# /appointments
def appointments(request):
    # account = None
    # if (request.cookie(type) == 'user') {
    #     account = 'user'
    #     get appointments for user
    # } else {
    #     account = 'staff'
    #     get appointments for staf
    # }
    return render(request, 'appointments.html', {'account': 'user'})

# /patients
@login_required
def patients(request):
    if request.session.get("type") == "STAFF":
        patients = models.Patient.objects.filter(user__groups__name__in=['PATIENT'])

        ctx = {'patients': patients}
        return render(request, 'staff/patients.jinja', context = ctx)
    else:
        return redirect("dashboard")

# /admitted_patients
@login_required
def admitted(request):
    # discharge = models.Appointment.objects.filter(patient__user__groups__name__in=['PATIENT'], status="Ongoing")
    if request.session.get("type") == "STAFF":
        discharges = models.Discharge.objects.all()
        ctx = {'discharges': discharges}
        return render(request, 'staff/admitted_patients.jinja', context = ctx)
    else:
        return redirect("dashboard")
# /invoice/
def user_invoice(request):
    return render(request, 'invoice.html')

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        #getting the template
        pdf = render_to_pdf('invoice.html')
            
        #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

# --- STAFF ---
# # /staff_home
# def staff_home(request):
#     return render(request, 'staff_home.html', {'account': 'staff'})

# # /staff_login
# def staff_login(request):
#     return render(request, 'login.html', {'account': 'staff'})

