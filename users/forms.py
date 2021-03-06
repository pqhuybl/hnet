from django import forms
from users.models import UserProfile

from django.utils.translation import ugettext, ugettext_lazy as _

class UserProfileForm(forms.ModelForm):

	
    class Meta:
        model = UserProfile
        exclude = ('user',)

'''
	class Meta:
		model = UserProfile
		fields = '__all__'



	user = models.OneToOneField(User)
	dOB = models.DateField(null=True)
	sSN = models.CharField(max_length=11,default='000-00-0000',blank=True)
	phoneNumber = models.CharField(max_length=15,default='xxx-xxx-xxxx',null=True)
	streetAddress = models.CharField(max_length=100,blank=True)
	city = models.CharField(max_length=30,blank=True)
	state = models.CharField(max_length=2,blank=True)
	zipcode = models.CharField(max_length=5,default='xxxxx',blank=True)
	email = models.EmailField(max_length=75, blank=True)


from __future__ import unicode_literals

import warnings

from django import forms
from django.forms.util import flatatt
from django.template import loader
from django.utils.datastructures import SortedDict
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.text import capfirst

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site




#
from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile

import datetime


class UserCreationForm(forms.ModelForm):

    error_css_class = 'alert alert-danger'

    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")},
        widget=forms.TextInput(attrs={'class':'form-control'}),

        )

    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            userprofile = UserProfile.create(user)
            userprofile.save()
        return user
'''