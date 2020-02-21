from django.db import models
# these are the two classes need to modify default Django user/admin login
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        #make the email letter case insensitive a method from BaseUserManager
        email = self.normalize_email(email)
        # create user model object without the password by using .model attribute from BaseuserManager class https://stackoverflow.com/questions/51163088/self-model-in-django-custom-usermanager
        user = self.model(email=email, name=name)
        # store the password not as string but an encripted to hash
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Crate and save a new superuser with given details"""
        user = self.create_user(email, name, password)
        # We did not specify is_superuser because is automatically created by PermissionMixin
        user.is_superuser = True
        # this method is specified in the UserProfile model
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users authentication in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Creates a user profile manager
    objects = UserProfileManager()

    # Overwriting the default Django username and replace it with USERNAEM_FIELD
    # by taking user's email instead a user's name
    USERNAME_FIELD = 'email'
    # making the name as a requirement field
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of the user"""
        return f'{self.email} is {self.name}'
        #return self.email
