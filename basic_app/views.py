from django.shortcuts import render
from django.urls import reverse
# decorater that can be used with a view to require authentication for access
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, UserProfileInfoForm


# Create your views here.
def index(request):
    """Returns basic_app/index.html for the root route"""
    return render(request, 'basic_app/index.html')


@login_required # ensures user is currently logged in
def user_logout(request):
    """
    Logs a user out and redirects them to the index view, only if the user is
    currently logged in.
    """
    logout(request)
    return HttpResponseRedirect(reverse('basic_app:index'))


@login_required # ensure user is currently logged in
def special(request):
    """Dummy view to demonstrate login_required decorator"""
    return HttpResponse("You are logged in, Nice!")


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


def user_login(request):
    """
    User authentication.

    If the request method is POST, attempts to log the user in. The Django
    authenticate function is used with the username/password provided by
    the form.

    If the user is authenticated, the credentials are checked for active
    status. If the user is active, they are then logged in using the Django
    login function and redirected to the index view. If the user
    is inactive, a response is returned notating that the user is not
    active.

    If the credentials provided are not authenticated, the failed
    credentials are printed to the web server for logging and a message is
    returned to the client notating a failed login.

    If the request method is not POST then basic_app/login.html is
    rendered to the client.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('basic_app:index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse('INVALID LOGIN DETAILS SUPPLIED')
    else:
        return render(request, 'basic_app/login.html', {})