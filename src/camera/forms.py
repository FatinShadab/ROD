from django import forms
from .models import Camera


class CameraRegForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ('cname', 'cip', 'cport')
        widgets = {
            'cname': forms.TextInput(attrs={
                "placeholder": "CAMERA NAME",
                "id": "inlineFormInputGroup",
                "class": "form-control"
            }),
            'cip': forms.TextInput(attrs={
                "placeholder": "IP (1xx.1xx.x.1xx)",
                "id": "inlineFormInput",
                "class": "form-control mb-2"
            }),
            'cport': forms.NumberInput(attrs={
                "placeholder": "PORT (xxxx)",
                "id": "inlineFormInput1",
                "class": "form-control mb-2"
            })
        }
