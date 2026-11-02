from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo_barras', 
            'nombre', 
            'categoria', 
            'precio', 
            'stock_bodega', 
            'stock_sala', 
            'fecha_vencimiento', 
            'en_oferta'
        ]
        widgets = {
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 7801234567890'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_bodega': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_sala': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'en_oferta': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
        self.fields['categoria'].empty_label = "Selecciona una categoría..."

    # Validación personalizada para la fecha
    def clean_fecha_vencimiento(self):
        fecha = self.cleaned_data.get('fecha_vencimiento')
        
        if fecha:
            # Calculamos la fecha de hoy + 15 días
            fecha_minima = date.today() + timedelta(days=15)
            
            if fecha < fecha_minima:
                raise ValidationError(f"El producto está muy próximo a vencer. La fecha debe ser igual o posterior al {fecha_minima.strftime('%d/%m/%Y')}.")
        
        return fecha