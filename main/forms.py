from django import forms
from django.forms.widgets import NumberInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAddressBook
GENDER_CHOICE=(
    ("Male",'Laki-Laki'),
    ("Female",'Perempuan')
)

class SignUpForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'type':'text','placeholder':'Iqbal'}),max_length=50,required=True)
    last_name=forms.CharField(widget=forms.TextInput(attrs={'type':'text','placeholder':'Anniswa'}),max_length=50,required=True)
    phone_number=forms.CharField(widget=forms.TextInput(attrs={'type':'number','placeholder':'62xxxxxxx11'}))
    email=forms.EmailField(max_length=50)
    gender=forms.ChoiceField(choices=GENDER_CHOICE)
    birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model=User
        fields=('first_name','last_name','username','phone_number','email','birth_date','gender','password1','password2')
class AddressBookForm(forms.ModelForm):   
    class Meta:
        model=UserAddressBook
        fields=('city','street','status')