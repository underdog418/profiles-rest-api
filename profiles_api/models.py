from django.db import models
# these are the two classes need to modify default Django user/admin login
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        #make the email letter case insensitive a method from BaseUserManager
        #email = self.normalize_email(email)
        # .normalize_email is a BaseuserManager class method
        """create user model object without the password by using .model attribute from BaseUserManager class https://stackoverflow.com/questions/51163088/self-model-in-django-custom-usermanager
        https://docs.djangoproject.com/en/3.0/topics/auth/customizing/ """
        #user = self.model(email=email, name=name)
        user = self.model(email=self.normalize_email(email), name=name)
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

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        """Return the model as a string"""
        return self.created_on
        #return f'created on {self.created_on}.  Content: {self.status_text} '
