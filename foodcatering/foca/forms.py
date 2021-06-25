from django import forms
from foca.models import UserData 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 


class UserForm(UserCreationForm): 
    class Meta: 
        model = User 
        fields = ('username','first_name', 'last_name', 'email','password1','password2') 

 
 
         
class RegForm(forms.ModelForm): 
    dob=forms.DateField(label='Date of Birth') 
    choices=[('male','Male'), 
         ('female','Female')] 
 
    gender = forms.ChoiceField(choices=choices, widget=forms.RadioSelect) 
     
    class Meta: 
        model=UserData 
        fields=('bio','gender','dob','location') 