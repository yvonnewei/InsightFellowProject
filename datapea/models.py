
from django.db import models


class Patient(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    insurance = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    ssn = models.CharField(max_length=100, default="", blank=True, null=True)
    provider = models.ForeignKey('auth.User', related_name='patients', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Patient, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created']

# /////////////////////////////////////////////////////////////

#
# class Role(models.Model):
#     PROVIDER = 1
#     PATIENT = 2
#     ADMIN = 3
#     ROLE_CHOICES = (
#         (PROVIDER, 'Provider'),
#         (PATIENT, 'Patient'),
#         (ADMIN, 'admin'),
#     )
#
#     id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
#
#     def __str__(self):
#         return self.get_id_display()
#
#
# class User(AbstractUser):
#     roles = models.ManyToManyField(Role)
#     description = models.TextField(max_length=500, default="", blank=True, null=True)

#
# class Provider(models.Model):
#     """
#     national_provider_identifier: npi
#     last_name
#     first_name
#     city
#     state
#     specialty_description
#     source_of_provider_specialty
#
#     """
#     # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     # patients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='providers')
#
#     national_provider_identifier = models.CharField(max_length=100, default="", blank=True, null=True)
#     last_name = models.CharField(max_length=100, blank=True, null=True)
#     first_name = models.CharField(max_length=100, blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     state = models.CharField(max_length=100, blank=True, null=True)
#     specialty_description = models.CharField(max_length=100, blank=True, null=True)
#     source_of_provider_specialty = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.national_provider_identifier
#
#     class Meta:
#         db_table = 'provider_table'
#

# class Patient(models.Model):
#     """
#     last_name
#     first_name
#     insurance
#     address
#     date_of_birth
#     gender
#     phone
#     ssn
#
#     """
#     # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     # provider = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='provider_patients')
#
#     last_name = models.CharField(max_length=100, blank=True, null=True)
#     first_name = models.CharField(max_length=100, blank=True, null=True)
#     insurance = models.CharField(max_length=100, blank=True, null=True)
#     address = models.CharField(max_length=100, blank=True, null=True)
#     date_of_birth = models.CharField(max_length=100, blank=True, null=True)
#     gender = models.CharField(max_length=100, blank=True, null=True)
#     phone = models.CharField(max_length=100, blank=True, null=True)
#     ssn = models.CharField(max_length=100, default="", blank=True, null=True)
#
#     provider = models.ForeignKey('auth.User', related_name='patients', on_delete=models.CASCADE)
#
#     def save(self, *args, **kwargs):
#         super(Patient, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return self.ssn
#
#     class Meta:
#         db_table = 'patient_table'

#
# class Drug(models.Model):
#     """
#     drug_name
#     generic_name
#
#     """
#     drug_name = models.CharField(max_length=100, default="", blank=True, null=True)
#     generic_name = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.drug_name
#
#     class Meta:
#         db_table = 'drug_table'

# class ProviderPatient(models.Model):
#     provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.pk
#
#     class Meta:
#         db_table = 'provider_patient_table'
