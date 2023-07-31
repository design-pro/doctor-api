from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        # Add other user types here
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=450)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    # Add other common fields for all user types

    def __str__(self):
        return f"{self.user.username} - {self.first_name} {self.last_name}"


class DoctorProfile(models.Model):
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, parent_link=True)
    medical_license_code = models.CharField(max_length=20)
    # Add other specific fields for doctors

    def __str__(self):
        return f"Doctor: {self.user_profile.user.username} - {self.user_profile.first_name} {self.user_profile.last_name}"


class PatientProfile(models.Model):
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, parent_link=True)
    national_id = models.CharField(max_length=10)
    # Add other specific fields for patients

    def __str__(self):
        return f"Patient: {self.user_profile.user.username} - {self.user_profile.first_name} {self.user_profile.last_name}"

# TODO: change model
class Location(models.Model):
    KIND_LIST = (
        ("office", "office"),
        ("clinic", "clinic"),
        ("policlinic", "policlinic"),
        ("hospital", "hospital")
    )
    kind = models.CharField(choices=KIND_LIST, max_length=100)
    title = models.CharField(null=True, blank=True, max_length=500)
    position = models.JSONField(default={})
    address = models.TextField()


# TODO: change model
class LocationDoctor(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="user_location")
    location = models.ForeignKey(Location,on_delete=models.DO_NOTHING,related_name="location_rel")


