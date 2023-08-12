from django.db import models
from django.contrib.auth.models import User
from users.common import CommonModel
from users.managers import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class DjangoUsers(AbstractBaseUser, PermissionsMixin):
    """
    Class  Base User
    """
    USER_LEVEL = (
        (1, "doctor"),
        (2, "patient"),
        (3, "superuser")
    )
    LEVEL_USER = 1
    LEVEL_SPECIAL_USER = 2
    LEVEL_SUPERUSER = 3
    GENDER = (
        (1, "Male"),
        (2, "Female"),
        (3, "None")
    )
    # username = models.CharField(unique=True, max_length=25, blank=True, null=True)
    cellphone_number = models.BigIntegerField(unique=True, null=False)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(
        max_length=126, null=True, blank=True, unique=True)
    password = models.CharField(max_length=512)  # hash
    register_date = models.DateTimeField(auto_now_add=True)
    gender = models.IntegerField(choices=GENDER)
    is_blocking = models.BooleanField(
        verbose_name="مسدود کردن کاربر", default=False)
    blocking_end = models.DateTimeField(
        verbose_name="تاریخ پایان مسدودی کاربر", null=True, blank=True)
    # authorization = models.JSONField(default=DEFAULT_AUTHORIZATION, null=True, blank=True)
    last_login = models.DateTimeField(
        verbose_name="آخرین ورود", null=True, blank=True)
    a2fa = models.BooleanField(default=False, verbose_name="2FA")
    first_name = models.CharField(
        max_length=250, verbose_name="نام", null=True, blank=True)
    last_name = models.CharField(
        max_length=750, verbose_name="نام خانوادگی", null=True, blank=True)
    user_level = models.PositiveIntegerField(
        choices=USER_LEVEL, default=LEVEL_USER)
    block_detail = models.CharField(max_length=2000, null=True, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    objects = UserManager()

    USERNAME_FIELD = 'cellphone_number'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(cellphone_number__isnull=False) | Q(
                    email__isnull=False),
                name='not_both_null'
            ),
            models.UniqueConstraint(fields=['cellphone_number', 'email'],
                                    name='unique_field_cellphone_number_field_email')
        ]

    def __str__(self):
        return f'{self.cellphone_number}'


class Degree(CommonModel):
    """
        fa: درجه (نوع مدرک)
    """
    icon = models.ImageField(
        _("Icon"), upload_to="degree/", null=True, blank=True)


class Awards(CommonModel):
    """
        fa: جوایز
    """
    pass


class Scientific(CommonModel):
    """
        fa: علمی
    """
    pass


class Symptomes(CommonModel):
    """
        fa: نشانه علامت بیماری
    """
    pass


class Feedbacks(CommonModel):
    pass


class Insurances(CommonModel):
    """
        Insurances of that can use in canters
    """
    pass


class Provinces(CommonModel):
    provinces_en_slug = models.CharField()


class Cities(CommonModel):
    province = models.ForeignKey(
        Provinces, on_delete=models.SET_NULL, null=True, blank=True)
    city_en_slug = models.CharField()


class CenterTypes(CommonModel):
    slug = models.SlugField(_(""))


class Expertise(CommonModel):
    """
        fa: تجربه و تخصص
    """
    icon = models.ImageField(
        upload_to='expertise/', blank=True, null=True)
    en_slug = models.SlugField()
    degrees = models.ManyToManyField(Degree, null=True, blank=True)


class GroupExpertises(CommonModel):
    icon = models.ImageField(
        upload_to='expertise/', blank=True, null=True)
    en_slug = models.SlugField()


class RelationGroupExpertise(CommonModel):
    group_id = models.ForeignKey(
        GroupExpertises, on_delete=models.SET_NULL, null=True, blank=True)
    expertise_id = models.ForeignKey(
        Expertise, on_delete=models.SET_NULL, null=True)
    en_slug = models.SlugField()


class DoctorProfile(CommonModel):
    """
        fa:پروفایل دکتر
    """
    user_profile = models.OneToOneField(
        DjangoUsers, on_delete=models.CASCADE, parent_link=True)
    medical_license_code = models.CharField(max_length=20)
    awards = models.ManyToManyField(Awards, blank=True, null=True)
    biography = models.TextField(null=True, blank=True)
    medical_code = models.CharField(max_length=1024)
    number_of_visits = models.IntegerField(default=0)
    scientific = models.ManyToManyField(Scientific, blank=True, null=True)
    score = models.IntegerField()
    should_recommend_other_doctors = models.BooleanField()
    slug = models.SlugField()
    symptomes = models.ManyToManyField(Symptomes, blank=True, null=True)
    experience = models.IntegerField(
        null=True, blank=True, default=0)  # experience years
    # Add other specific fields for doctors

    def __str__(self):
        return "دکتر: {}{}".format(self.user_profile.first_name, self.user_profile.last_name)


class PatientProfile(CommonModel):
    user_profile = models.OneToOneField(
        DjangoUsers, on_delete=models.CASCADE, parent_link=True)
    national_id = models.CharField(max_length=10)
    # Add other specific fields for patients

    def __str__(self):
        return f"Patient: {self.user_profile.user.username} - {self.user_profile.first_name} {self.user_profile.last_name}"


class Centers(CommonModel):
    STATUS = (
        (1, "active"),
        (2, "deactive")
    )
    center_type = models.ForeignKey(
        CenterTypes, on_delete=models.DO_NOTHING, related_name="centers_type")
    map = models.JSONField(default={})
    address = models.TextField()
    doctors = models.ManyToManyField(DoctorProfile)
    insurances = models.ManyToManyField(Insurances)
    status = models.IntegerField(choices=STATUS, default=1)
    city = models.ForeignKey(Cities, null=True, blank=True)
    province = models.ForeignKey(Provinces)
