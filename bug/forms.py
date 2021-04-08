from django import forms
from .models import Project, Profile, Ticket,Team
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap_modal_forms.forms import BSModalModelForm



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                'email', 'password1', 'password2',)
        

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',            
        }

    ))
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password again',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','email')

    def clean_password2(self):
        cd = self.cleaned_data
        if (cd['password'] != cd['password2']):
            raise forms.ValidationError("Passwords are not the same")
        return cd['password2']

class DateInput(forms.DateInput):
    input_type = 'date'

class AddProjectForm(BSModalModelForm):
    
    class Meta:
        model = Project
        fields = ['name','description','team','manager','project_deadline']
        widgets = {
            'project_deadline': DateInput(attrs={'type': 'date'})
        }





class AddTicketForm(BSModalModelForm):
    class Meta:
        model = Ticket
        fields = ['name','description','project','assigned_team','assigned_member','ticket_deadline']
        widgets = {
            'ticket_deadline': DateInput(attrs={'type': 'date'})
        }

class AddTeamForm(BSModalModelForm):

    class Meta:
        model = Team
        fields = ['name','members','team_manager']



