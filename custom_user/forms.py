from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from .models import Participant


class ParticipantLoginForm(AuthenticationForm):
    '''
    A form that fetches the data needed to authentic
    and login a participant
    '''

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    error_messages = {
        'email_unknown': 'The email credential is unknown.',
        'invalid_pass': 'Invalid password or PIN',
        'inactive': 'This account is inactive',
    }

    def clean(self):
        email = self.cleaned_data.get('username')  # because this is in settings
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)

            if self.user_cache is None:
                try:
                    participant = Participant.objects.get(email=email)
                except Participant.DoesNotExist:
                    raise forms.ValidationError(
                        self.error_messages['email_unknown'],
                        code='email_unknown',
                        params={'email': self.username_field}
                    )

                if participant.password != password:
                    raise forms.ValidationError(
                        self.error_messages['invalid_pass'],
                        code='invalid_pass',
                    )

                assert False, 'Here Be Dragons'

            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )

        return self.cleaned_data


class ParticipantCreationForm(forms.ModelForm):
    """
    A form that creates a participant, with no privileges, from the given email and
    password.
    """

    ## Largely copied from django.contrib.auth.forms.UserCreationForm

    error_messages = {
        'duplicate_email': "A participant with that email address already exists.",
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = Participant
        fields = ("email", "email_backup")

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            Participant.objects.get(email=email).exists()
        except Participant.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
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
        user = super(ParticipantCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user