from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django import forms
from .models import CustomUser
import re
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs= { 
                'class':'form-control',
                'patter':'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                'placeholder':'Ingrese su contraseña',
                'title' : 'Formato no valido',  
                }
        )
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs= { 
                'class':'form-control',
                'patter':'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                'placeholder':'Confirme su contraseña',
                'title' : 'Formato no valido'
                
                }
        )
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'name',
            'surname',
            'control_number',
            'age',
            'tel',
            'password1',
            'password2'
            ]
        


        widgets = {
            
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico',
                'required': True,
                'minlength': '20',
                'maxlength': '30',
                'title' : 'Ingresa un correo con dominio de la Utez',

               'pattern': '^[a-zA-Z0-9]+@utez\.edu\.mx$',
            }),
            
            'name': forms.TextInput(attrs={  
                'class': 'form-control',
                'placeholder': 'Nombre',
                'required': True,
                'minlength': '2',
                'maxlength': '50',
                'title' : 'Solo letras',  

                'pattern': '^[a-zA-Z]+$'
            }),

            'surname': forms.TextInput(attrs={  
                'class': 'form-control',
                'placeholder': 'Apellido',
                'required': True,
                'minlength': '2',
                'maxlength': '50',
                'title' : 'Solo letras',  

                'pattern': '^[a-zA-Z]+$'
            }),

            'age': forms.NumberInput(attrs={ 
                'class': 'form-control',
                'placeholder': 'Edad',
                'required': True,
                'minlength': '18',
                'maxlength': '100',
                'title' : 'Edad invalida',  

               'pattern': '^\d{10}$', 
            }),

            'tel': forms.NumberInput(attrs={ 
                'class': 'form-control',
                'placeholder': 'Teléfono',
                'required': True,
                'title' : 'Debe contener 10 didjitos',  
                'pattern': '^\d{10}$', 
            }),
            
            'control_number': forms.TextInput(attrs={ 
                'class': 'form-control',
                'placeholder': 'Edad',
                'required': True,
                'min': '10',
                'max': '10',
                'title' : 'Formato no valido',  
               'pattern':'^\d{5}[a-zA-Z]{2}\d{3}$'
            }),
        
        }
        
    def clean(self):
    
        email= self.cleaned_data.get('email')
        email_regex=r'^[a-zA-Z0-9]+@utez\.edu\.mx$'
        if not re.match(email_regex, email):
            raise forms.ValidationError('Ingresa un correo del domino de la UTZEM')
        
        name= self.cleaned_data.get('name')
        name_regex = r'^[a-zA-Z]+$' 
        if not re.match(name_regex, name):
            raise forms.ValidationError('Formato invalido ingresa solo letras')
        if len(name) < 3 or len(name) > 50:
            raise forms.ValidationError('Exediste el limite de caracteres')

        surname=self.cleaned_data.get('surname')
        surname_regex = r'^[a-zA-Z]+$' 

        if not re.match(surname_regex,surname):
            raise forms.ValidationError('Formato invalido ingresa solo letras')
        if len(surname)>100 or len(surname)<3:
            raise forms.ValidationError('Exediste el limite de caracteres')
        
        control_number=self.cleaned_data.get('control_number')
        control_number_regex=r'^\d{5}[a-zA-Z]{2}\d{3}$'
        if not re.match(control_number_regex,control_number):
            raise forms.ValidationError('Formato invalido del dato ingresado')
    
        age=self.cleaned_data.get('age')
        age_regex=r'^\d{2}$'
        if not re.match(age_regex,str(age)):
            raise forms.ValidationError('Edad invalida')
        
        tel=self.cleaned_data.get('tel')
        tel_regex=r'^\d{10}$'
        if not re.match(tel_regex,tel):
            raise forms.ValidationError('Exediste el numero de caracteres')
        
        password1=self.cleaned_data.get('password1')
        password_regex=r'^(?=.*\d)(?=.*[A-Z])(?=.*[!#$%&?]).{8,}$'
        if not re.match(password_regex, password1):
            raise forms.ValidationError('La contraseña debe tener al menos una letra mayuscula, un número y un caracter especial y 8 digitos')
        
        password2=self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Las contraseñas deben coincidir')
     
        return self.cleaned_data

        
     

class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico',
            'required': True,
            'minlength': '20',
            'maxlength': '30',
            'title': 'El correo no pertenece al dominio de la UTEZ',
            'pattern': '^[a-zA-Z0-9]+@utez\.edu\.mx$',
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'pattern': '^(?=.*\d)(?=.*[A-Z])(?=.*[!#$%&?]).{8,}$',
            'required': True,
            'minlength': '8',
             'title': 'Contraseña no valida',
            'maxlength': '50',
        })
    )
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if not user:
                raise forms.ValidationError("Usuario o contraseña incorrectos.")

        return self.cleaned_data
