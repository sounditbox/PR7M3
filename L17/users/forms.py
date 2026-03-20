from django import forms
from django.contrib.auth import get_user_model


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        self.fields['username'].disabled = True
