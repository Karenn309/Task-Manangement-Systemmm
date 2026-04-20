from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from django.forms import TextInput

class NewUserForm(UserCreationForm):
    email= forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username","email","password1","password2")
        
        def save(self, commit=True):
            user=super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            
            if commit:
                user.save()
            return user
            


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields=['username','password1','password2']
        widgets = {
            'username': TextInput(attrs={'class':'form-control'}),
        }