from django import forms
from django.contrib.auth.models import User, Group

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
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'})
    )

class EditarUsuarioForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(), 
        required=False, 
        empty_label="Sin grupo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sueldo_base = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }