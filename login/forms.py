from django.db import models
from django import forms
from django.contrib.auth import authenticate


import warnings


from django.template import loader

from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

UNMASKED_DIGITS_TO_SHOW = 6

mask_password = lambda p: "%s%s" % (p[:UNMASKED_DIGITS_TO_SHOW], "*" * max(len(p) - UNMASKED_DIGITS_TO_SHOW, 0))



# Creates a new login form 
class loginForm(forms.Form):
    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    #error_css_class = 'alert alert-danger'
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	
    # Redefines the clean method to include error raising
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            #raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
            raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login'
            )

        return self.cleaned_data

    # Redefines the login method
    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

'''
class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data

    def check_for_test_cookie(self):
        warnings.warn("check_for_test_cookie is deprecated; ensure your login "
                "view is CSRF-protected.", DeprecationWarning)

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
'''
