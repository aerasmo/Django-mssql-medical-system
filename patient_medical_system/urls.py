from django.urls import path
from . import views
from .views import GeneratePdf
from django.contrib.auth.views import LoginView,LogoutView
from .wrappers import logged_in_switch_view, user_switch_view, triple_switch_view

urlpatterns = [
	# all users
	path('', views.home, name="home"),	
    path('_handle_user/', views.handle_user,  name='handle user'),
	path('invoice/<int:id>', views.invoice, name="invoice"),
    path('dashboard/', user_switch_view(views.patient_dashboard, views.staff_dashboard),  name='dashboard'),
    path('patient/<int:id>', views.patient,  name='patient'),
    path('cancel_appointment/<int:id>', user_switch_view(views.cancel_appointment, views.reject_appointment),  name='cancel appointment'),
    path('logout/', views.user_logout,  name='logout'),

	# patients view
    path('signup/', views.user_signup,  name='user signup'),
    path('login/', LoginView.as_view(template_name='patient/login.jinja'),  name='user login'),
	path('add_appointment/', views.add_appointment, name="add appointment"),
    path('history/', views.history,  name='history'),
    path('patient/', views.patient,  name='patient'),
    path('profile/', views.profile,  name='profile'),

	# staff view
    path('staff_login/', LoginView.as_view(template_name='staff/login.jinja'),  name='staff login'),
    path('staff_signup/', views.staff_signup,  name='staff signup'),
    path('approve_appointment/<int:id>', views.approve_appointment,  name='approve appointment'),
    path('admit_appointment/<int:id>', views.admit_appointment,  name='admit appointment'),
	path('patients/', views.patients, name="patients"),
	path('admitted_patients/', views.admitted, name="admitted"),
    path('discharge/<int:discharge_id>', views.discharge_patient,  name='discharge'),

	path('pdf/', GeneratePdf.as_view()),
	path('download_pdf/<int:id>', views.download_pdf, name="pdf")

]	
