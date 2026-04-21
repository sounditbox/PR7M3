from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['username'].disabled = True

class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

