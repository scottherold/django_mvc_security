from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm


# Create your views here.
def index(request):
    """Returns basic_app/index.html for the root route"""
    return render(request, 'basic_app/index.html')


def register(request):
    """
        Creates a variable for registration status.

        Determines if the request method is POST. If true, the ModelForm data
        is populated for both UserForm and UserProfileInformForm.If both
        forms' data is valid, the UserForm data is mapped to a User Model and
        saved. The password is hashed, using the set_password() method, which
        uses the hiearchy of hashing algorithms provived in the
        PASSWORD_HASHERS list in the settings.py file. The User model is then
        saved.

        The UserProfileInfoForm is then mapped to a UserProfileInfo model and
        saved, but not committed to the DB (this is to prevent collision errors
        for User model overwrites). The one-to-one relationship is then
        established between the UserProfileInformForm instance and the
        generated User instance.

        If a profile_pic was provided with the registration, the profile_pic
        attribute of the instantiated UserProfileInfo model is populated with
        the buffer provided. The instance of UserProfileInfo is then committed
        to the DB, and the registered variable is set to True.

        If either form is invalid, the errors are printed to the server
        console. (***CHANGE WHEN SENT TO TEMPLATE***)

        If the request is not a POST request, then a blank UserForm and a
        blank UserProfileInfoForm are instantiated, and along with the
        registered variable are returned with basic_app/register.html as
        context.
    """
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # hashes the password using the PASSWORD_HASHERS list in
            # settings.py
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            # sets the one-to-one relationship with the User model generated
            # above
            profile.user = user

            if 'profile_pic' in request.FILES:
                # all files are accessed as a dictionary with the key provided
                # from the form
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,
                  'basic_app/registration.html',
                    {
                        'user_form': user_form,
                        'profile_form': profile_form,
                        'registered': registered
                    })

