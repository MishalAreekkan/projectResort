from django import forms
from .models import User,StayPics,DinePics

class RegisterationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']
        help_texts = {
            'username': None,
        }
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=100)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    

class StayPicsForm(forms.ModelForm):
    class Meta:
        model = StayPics
        fields = ['room','description','image']
        
class DinePicsForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    
    class Meta:
        model = DinePics
        fields = ['meal_time', 'meal_type','name', 'description', 'image', 'start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError('End time must be after start time.')
        return cleaned_data
# class BookingDateForm(forms.ModelForm):
#     class Meta:
#         model = bookingdate
#         fields = ['time', 'day', 'month', 'year', 'availabe_data', 'filled_data']

# class BookingField(forms.ModelForm):
#     members = forms.CharField( max_length=10, required=True)
#     # beds = forms.