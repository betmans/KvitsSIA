# kvitsapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User # Import the standard User model
# Import your models needed for forms
from .models import Profile, Order

class UserRegistrationForm(UserCreationForm):
    """
    Form for registering new users. Inherits from Django's UserCreationForm
    and adds an email field.
    """
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Lietotājs ar šādu e-pasta adresi jau pastāv.")
        return email

class UserUpdateForm(forms.ModelForm):
    """
    Form for updating basic user information (e.g., email, name).
    Does NOT handle password changes.
    """
    email = forms.EmailField(required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cits lietotājs jau izmanto šo e-pasta adresi.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating the custom profile information stored in the Profile model.
    """
    class Meta:
        model = Profile
        exclude = ['user']
        # Or explicitly list fields:
        # fields = ['company_name', 'registration_number', 'vat_number', 'address', 'phone_number']

# ++++++++++ MOVED ORDER CREATE FORM HERE ++++++++++
class OrderCreateForm(forms.ModelForm):
    """
    Form for collecting customer details during checkout.
    """
    class Meta:
        model = Order # Use the Order model
        # Fields to display in the checkout form
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'company_name', 'address']
        # Add Bootstrap classes via widgets for styling
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vārds'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uzvārds'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-pasts'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefona numurs (nav obligāts)'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uzņēmuma nosaukums (nav obligāts)'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Iela, māja/dzīvoklis, pilsēta, pasta indekss'}),
        }
        # Optional: Add labels if needed (Bootstrap often uses placeholders)
        # labels = {
        #     'first_name': 'Vārds',
        #     'last_name': 'Uzvārds',
        #     # ...
        # }
# ++++++++++ END MOVED ORDER CREATE FORM ++++++++++

