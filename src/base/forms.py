from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text="Required. Provide a valid email address.",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email',
            'type': 'email',
            'id': 'form3Example3cg',
            'class': 'form-control form-control-lg'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'type': 'text',
                'id': 'form3Example1cg',
                'class': 'form-control form-control-lg'
            })
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'type': 'password',
            'id': 'form3Example4cg',
            'class': 'form-control form-control-lg'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Re-enter Your Password',
            'type': 'password',
            'id': 'form3Example4cdg',
            'class': 'form-control form-control-lg'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control form-control-lg', 'type': 'text', 'id': 'form3Example1cg'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control form-control-lg', 'type': 'password', 'id': 'form3Example4cg'}))


class PassResetForm(PasswordResetForm):
    email = forms.EmailField(
        required=True, 
        help_text="Required. Provide a valid email address.",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email',
            'type': 'email',
            'id': 'form3Example3cg',
            'class': 'form-control form-control-lg'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("The email address you entered is not registered. Please enter registered email id")
        return email
    
    def get_user(self):
        email = self.cleaned_data.get('email')
        return User.objects.get(email=email, is_active=True)
    

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New password',
            'type': 'password',
            'id': 'form3Example4cg',
            'class': 'form-control form-control-lg pt-1 mt-3'
        }),
    )
    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm new password',
            'type': 'password',
            'id': 'form3Example4cg',
            'class': 'form-control form-control-lg pt-1 mt-3'
        }),
    )