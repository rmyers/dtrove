
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from dtrove.models import Datastore


class KeystoneForm(AuthenticationForm):
    """Custom Keystone Authentication form.

    Basically all we need to do is add the request to the authenticate
    method in order to login the user.
    """

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(request=self.request,
                                           username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class ClusterForm(forms.Form):
    name = forms.CharField(max_length=100)
    datastore = forms.ModelChoiceField(
        queryset=Datastore.objects.all(), empty_label='Choose a Datastore')
    key = forms.CharField()
