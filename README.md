# Django-mssql-medical-system

# Project Information:
 - Project/System Name: Philippine Optimum General Hospital
 - Description: Hospital catered to optical concerns and operations. Our motto is -theres more to us than meets the Eye (optimus prime edited quote). The following are the main features and function of the system:
	 1. Appointment management system - allows user to register for an appointment at the hospital. The staff would be able to see the users and their appointments and are able to approve their appointments. 
	 2. Medical Information System - Users who came for an appointment allows the staff to add and modify their medical information. The patient and staff are able to see their medical information.
	 3. Invoice receipts - Users and staff are able to see the bills once discharged from an appointment and the bills history. and are allowed to download the invoice.
 - Objectives: 
	 - The main goal is to have a patient appointment system that can be managed by the hospital staff and allow users and staff to track their appointments and receipts
	 - allow users to have an appointment with the hospital and check their medical records and history
	 - allow hospital staff to manage their appointments and patients 
- Platform: Web
- Programming Languages:
	- Front-end: Jinja2, Javascript, CSS, SASS, Semantic UI
	- Back-end: Python-Django, SQLite | MSQL
- Tools: VScode, Github, Figma
- Deployment: undecided 
	
## Timeline
- Week1 - BrainStorming, Planning, Documentation, Routes, Wireframing
- Week2 and 3 - Coding
- 2-3 days before presentation - Testing

## Roles
- Documentation and Wireframing: Nocon, Bayquen, Erasmo
- Frontend: San Andres, Nocon, Bayquen
- Backend: Castro, Erasmo, Versoza
- Tester: Versoza, Castro, San Andres

---
# Database Entities
- Users / Patient
	- __id__
	- username
	- first_name
	- last_name
	- email_address
	- password
- Users / Staff:
	- __id__
	- username
	- first_name
	- last_name
	- email_address
	- password
- Patient Information:
	- __id__
	- _user_id_ (Users.id)
	- profile_picture
	- phone_number
	- address
	- age
	- weight
	- height
	- blood_type
	- _vision_level_ - mild: (6/12), moderate ()
	- _eye_condition_ - (glaucoma, neatsightedness etc)
	- _has_glasses_ (boolean)
- Appointment
	- __id__
	- _user_id_ (Users.id)
	- appointment_date
	- type  ( eye checkup, eye surgery etc.)
	- status (pending, ongoing, discharged, cancelled)
- Discharge
	- __id__
	- _patient_id_
	- _appintment_id_
	- consultation_fee
	- admit_date
	- release_date
	- findings (comments / diagnosis)
	- room_fees
	- medicine_fees
	- other_fees
	- total_fees

---
# Routes
## User Routes
| URL                    | METHOD | NAME               | DESCRIPTION                                    |
| ---------------------- | ------ | ------------------ | ---------------------------------------------- |
| /login                 | GET    | login view         | renders the login form                         |
| /login                 | POST   | login auth         | login authentication                           |
| /signup                | GET    | signup view        | renders the signup form                        |
| /signup                | POST   | signup auth        | signup authentication -> adds to database      |
| /home                  | GET    | home               | shows company information and services         |
| /add_appointment       | GET    | add appointment    | show the add appointment form                  |
| /add_appointment       | POST   | post appointment   | adds to apopintments and database              |
| /appointments          | GET    | view appointments  | view history of previous appointments          |
| /profile               | GET    | patient profile    | view patient profile                           |
| /edit_profile          | GET    | edit profile       | view edit profile form                         |
| /profile               | POST   | save profile       | save edited profile                            |
| /invoice/{id}          | GET    | view invoice       | view invoice for the appointment               |
| /invoice/{id}/download | POST   | download invoice   | download invoice as pdf                        |
| /medical_information   | GET    | view medical info  | allows user to check their medical information |
| /logout                | POST   | logout             | logout from the system                         |
| /cancel_appointment    | POST   | cancel appointment | cancel current appointment                     |
|                        |        |                    |                                                |
	

## Staff Routes
| URL                                    | METHOD | NAME                  | DESCRIPTION                                                                       |
| -------------------------------------- | ------ | --------------------- | --------------------------------------------------------------------------------- |
| /staff_login                           | GET    | login view            | renders the login form                                                            |
| /staff_login                           | POST   | login auth            | login authentication                                                              |
| /dashboard                             | GET    | view dashboard        | shows an overview for information such as patients admitted, pending appointments |
| /appointments                          | GET    | view appointments     | shows all appointments                                                            |
| /approve/{appointment_id}              | POST   | approve appointment   | approve appointment                                                               |
| /admit/{appointment_id}                | POST   | admit appointment     | admit an approved appointment                                                     |
| /discharge/{appointment_id}            | GET    | discharge form        | view discharge appointment form                                                   |
| /discharge/{appointment_id}            | POST   | discharge appointment | discharge a patient -> saves into database                                        |
| /medical_information/{patient_id}/edit | GET    | medical info form     | edit form for patient medical info                                                |
| /medical_information/{patient_id}/edit | POST   | save medical info     | update patient medical information                                                |
| /patient/{patient_id}                  | GET    | view patient          | view patient information                                                          |
| /patients                              | GET    | view patients         | view all patients                                                                 |
| /staff_logout                          | POST   | logout                | logout from the system                                                            |
| /invoice/{id}                          | GET    | view invoice          | view invoice for the appointment                                                  |
| /invoice/{id}/download                 | POST   | download invoice      | download invoice as pdf                                                           |

---


