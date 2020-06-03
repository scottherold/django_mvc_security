"""
This file is specific to generating Django user forms for the basic_app
application.
"""
from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo


class UserForm(forms.ModelForm):
    """
        ModelForm for the User model.

        Attributes:
            password (str): The password for the User (to be hashed and stored)
    """
    password = forms.Charfield(widget=forms.PasswordInput())

    class Meta():
        """
            UserForm settings (Meta).

            Model to be linked to the form is User.

            Fields used by the form to be linked to the User model are
            username, email and password.
        """
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        """
            UserProfileInfoForm settings (Meta).

            Model to be linked to the form is UserProfileInfo

            Fields used by the form to be linked to the UserProfileInfo model
            are portfolio_site and profile_pic
        """
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')