from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

class CrearUsuarioForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'})
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'})
    )
    grupo = forms.ModelChoiceField(
        label="Rol / Perfil (Grupo)",
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'})
    )
    sueldo = forms.IntegerField(
        label="Sueldo Base ($)",
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'min': '0'})
    )

    # Validación para que el sueldo no sea negativo al crear
    def clean_sueldo(self):
        sueldo = self.cleaned_data.get('sueldo')
        if sueldo is not None and sueldo < 0:
            raise ValidationError("El sueldo no puede ser un valor negativo.")
        return sueldo


class EditarUsuarioForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(), 
        required=False, 
        empty_label="Sin grupo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sueldo_base = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    # Validación para que el sueldo base no sea negativo al editar
    def clean_sueldo_base(self):
        sueldo_base = self.cleaned_data.get('sueldo_base')
        if sueldo_base is not None and sueldo_base < 0:
            raise ValidationError("El sueldo base no puede ser un valor negativo.")
        return sueldo_base