# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import User, Profile

class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove default help_text
        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

class AdminUserUpdateForm(UserChangeForm):
    password = None  # Hide the password field/hash

    class Meta:
        model = User
        fields = ('username', 'role', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show ALL roles for updating, so a user can be promoted/demoted
        self.fields['role'].choices = User.Roles.choices

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Roles.CUSTOMER
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'phone_number']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write something about yourself...',
                'rows': 3
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number'
            }),
        }