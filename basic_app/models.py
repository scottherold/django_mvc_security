from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfileInfo(models.Model):
    """
        Creates a one-to-one relationship with the defaut User class, and links
        additional attributes.

        Attributes:
            portfolio_site (str): The URL for a User's portfolio website. Must
            in URL format. Optional field.
            profile_pic (buffer): A image file that is saved as a buffer onto
            the web server in the media/profile_pics directory.

        Methods:
            __str__(): String representation of the additional data in the
            new DB table.
    """
    # NOTE: Do no directly inherit from the User class. This may screw up your
    # DB into think that it has multiple instances of a single user.

    # NOTE: on_delete argument required on relationships in Django3
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional fiels to add onto the default Django User model
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username