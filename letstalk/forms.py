from django  import forms

def daterange(r=1970, e=2023):
    years = [r for r in range(r, e+1)]
    return years

GENDER = (('MALE', 'Male'), ('FEMALE', 'Female'))
class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="Surname", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Surname or FirstName'}))
    last_name = forms.CharField(max_length=30, label="Last Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    phone_number = forms.CharField(max_length=30, label="Phone Number", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Password")
    confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Confirm Password")
    gender = forms.ChoiceField(choices=GENDER, widget=forms.RadioSelect(attrs={'class':'form-check-inline p-0'}), label="Gender")
    dob = forms.DateField(label="DOB",required=False, widget=forms.SelectDateWidget(attrs={'class':'form-control-inline p-2 ml-2'},  years=daterange()))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class':'form-control'}), label="Password")