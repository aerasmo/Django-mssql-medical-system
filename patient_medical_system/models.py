from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateField
# Create your models here.
sex = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]
blood_types = [
    ('O+', 'O+'), ('O-', 'O-'),
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
]
vision_levels = [
    ('20/10', '20/10'), # outstanding
    ('20/12', '20/12'), # outstanding 
    ('20/15', '20/15'), # normal
    ('20/20', '20/20'), # normal 
    ('20/25', '20/25'), # normal
    ('20/30', '20/30'), # near-normal
    ('20/40', '20/40'), # near-normal
    ('20/50', '20/50'), # near-normal
    ('20/70', '20/70'), # moderate low vision
    ('20/100', '20/100'), # moderate-low vision
    ('20/200', '20/200'), # severe low vision
    ('20/500', '20/500'), # severe low vision
    ('20/1000', '20/1000'), # profound low vision
    ('Less than 20/1000', 'Less than 20/1000'), # profound low vision
]

eye_conditions = [
    ('None', 'None'),
    ('Nearsightedness', 'Nearsightedness'),
    ('Farsightedness', 'Farsightedness'),
    ('Astigmatism', 'Nearsightedness'),
]

status = [
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
    ('Rejected', 'Rejected'),
    ('Approved', 'Approved'),
    ('Ongoing', 'Ongoing'),
    ('Discharged', 'Discharged'),
]

appointment_types = [
    ('Eye Checkup', 'Eye Checkup'),
    ('Eye Examination', 'Eye Examination'),
    ('Eye Surgery', 'Eye Surgery'),
    ('Eye Massage', 'Eye Massage'),
]

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to ='uploads/patient_profiles/',null=True,blank=True)
    phone_number = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=7, choices=sex)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    blood_type = models.CharField(max_length=3, choices=blood_types, default='O+')
    vision_level = models.CharField(max_length=30, choices=vision_levels, default='unclassified')
    eye_condition = models.CharField(max_length=30, choices=eye_conditions, default='None')
    has_glasses = models.BooleanField(default=False)
    notes = models.TextField()

    @property
    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_id(self):
        return self.user.id

    @property
    def vision_classification(self):
        vision = 'unclassified'
        if self.vision_level in {'20/10', '20/12'}:
            vision = 'outstanding'
        elif self.vision_level in {'20/15', '20/20', '20/25'}:
            vision = 'normal'
        elif self.vision_level in {'20/30', '20/40', '20/50'}:
            vision = 'near-normal'
        elif self.vision_level in {'20/70', '20/100'}:
            vision = 'moderate low'
        elif self.vision_level in {'20/200', '20/500'}:
            vision = 'severe low'
        elif self.vision_level in {'20/1000', '20/1000'}:
            vision = 'profound low'
        elif self.vision_level in {'Less than 20/1000'}:
            vision = 'near-total low'
        return vision


    def __str__(self):
        return self.user.first_name

    def save(self, *args, **kwargs):
        # saving to 2 decimal form
        self.weight = round(self.weight, 2)
        self.height = round(self.height, 2)

        super(Patient, self).save(*args, **kwargs)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField(null=True)
    appointment_time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=status, default='Pending')
    appointment_type = models.CharField(max_length=30, choices=appointment_types, default='Eye Checkup')

    def __str__(self):
        return self.patient.user.username
     
class Discharge(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    admit_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    consultation_fee = models.FloatField(default=0)
    room_fee = models.FloatField(default=0)
    medicine_fees = models.FloatField(default=0)
    other_fees = models.FloatField(default=0)

    @property
    def total_fees(self):
        return self.consultation_fee + self.room_fee + self.medicine_fees + self.other_fees


# class MedicalRecord()

