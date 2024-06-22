from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),  # Ensure password is not shown in plain text
        }