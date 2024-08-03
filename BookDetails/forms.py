from django import forms
from .models import BedField,BookData
from django.forms.widgets import DateInput
from datetime import datetime, timedelta

class BookingForm(forms.ModelForm):
    checkin = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    checkout = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    class Meta:
        model = BookData
        fields = [
            'checkin', 'checkout','adults','children','bedtype'
        ]
        widgets = {
            'adults': forms.NumberInput(attrs={'class': 'form-control'}),
            'children': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'adults': 'Number of Adults',
            'children': 'Number of Children',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['checkin'].initial = datetime.now().date()
        self.fields['checkout'].initial = datetime.now().date() + timedelta(days=1)


        
# class BedType(forms.ModelForm):  

        
class BedFieldForm(forms.ModelForm):
    class Meta:
        model = BedField
        fields = ['bed']

   