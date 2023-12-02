import uuid

from django.db import models

from api.models.definitions import ACCOUNT_TYPE_CHOICES


class AbstractUser(models.Model):
    id = models.CharField(
        max_length=150, unique=True, primary_key=True, null=False, editable=False
    )
    username = models.CharField(max_length=25)
    email = models.EmailField(
        verbose_name="Email", max_length=255, unique=True, null=False
    )
    fname = models.CharField(max_length=255, null=False)
    lname = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    dob = models.DateField(null=True)
    phone = models.CharField(max_length=15, null=True)
    image = models.ImageField(
        upload_to="images/users/",
        default="images/users/defaultUserImage.png",
        null=True,
    )
    is_active = models.BooleanField(default=False)
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        default="Regular",
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.email

    @property
    def get_is_admin(self):
        if self.account_type == "admin":
            return True
        else:
            return False

    @property
    def get_is_seller(self):
        if self.account_type == "seller":
            return True
        else:
            return False

    @property
    def get_is_regular(self):
        if self.account_type == "regular":
            return True
        else:
            return False

    @property
    def get_phone(self):
        """Fetch registered Phone Number of the user"""
        if self.phone:
            return self.phone

    @property
    def get_full_name(self):
        """Fethch registered Phone Number of the user"""
        if self.fname and self.lname:
            return f"{self.fname} {self.lname}"
        else:
            return None

    @property
    def get_is_active(self):
        return self.is_active

    @property
    def get_username(self):
        if self.username:
            return self.username

    def save(self, *args, **kwargs):
        self.id = uuid.uuid4()
        super().save(*args, **kwargs)
