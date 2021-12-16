from django.urls import path
from . import views
from .views import GeneratePdf
from django.contrib.auth.views import LoginView,LogoutView
from .wrappers import logged_in_switch_view, user_switch_view

# url conf - patterns used in browser 
# ie. http://127.0.0.1:8000/appointment_system/staff-login/
urlpatterns = [
	path('', logged_in_switch_view(views.user_home, views.home), name="home"),
	
	# Test / middleware
	path('test/', views.test, name="test"),
    path('_handle_user/', views.handle_user,  name='handle user'),

	# User
	# path('logins/', views.user_login, name="user login"),
    path('login/', LoginView.as_view(template_name='patient/login.jinja'),  name='user login'),
    # path('login/', views.user_login,  name='user login'),
    path('signup/', views.user_signup,  name='user signup'),
    path('dashboard/', user_switch_view(views.patient_dashboard, views.staff_dashboard),  name='dashboard'),

    path('cancel_appointment/<int:id>', user_switch_view(views.cancel_appointment, views.reject_appointment),  name='cancel appointment'),
    path('approve_appointment/<int:id>', views.approve_appointment,  name='approve appointment'),
    path('admit_appointment/<int:id>', views.admit_appointment,  name='admit appointment'),
    path('discharge/<int:discharge_id>', views.discharge_patient,  name='discharge'),

	path('add_appointment/', views.add_appointment, name="add appointment"),
	# path('appointments/', views.appointments, name="appointments"),
	path('patients/', views.patients, name="patients"),
	path('admitted_patients/', views.admitted, name="admitted"),
	path('invoice/', views.user_invoice, name="user invoice"),

    path('logout/', views.user_logout,  name='logout'),
	# Staff
    path('staff_login/', LoginView.as_view(template_name='staff/login.jinja'),  name='staff login'),
    path('staff_signup/', views.staff_signup,  name='staff signup'),
	# path('staff_home/', views.staff_home, name="staff home"),
	# User and Staff
	# path('pdf/', GeneratePdf.as_view()), 
]	
