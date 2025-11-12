from django import forms
from .models import Content, Archive, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# 1. Formulário principal para os dados de texto
class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'text']
        
        # Adiciona widgets para aplicar classes CSS e atributos HTML
        widgets = {
            # Aplicando a classe Bootstrap e o placeholder
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': "O que você está pensando?"
            }),
            # Se 'title' não for visível, é bom escondê-lo.
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título',
            }),
        }

# 2. Formulário para o upload de arquivos. 
# Embora você possa ter vários arquivos, usaremos este form para processar cada upload.
class ArchiveForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ['file']
        # Não precisa de widget, o FileField já gera o input type="file"

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  # mantém o email obrigatório

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esse e-mail já está em uso.")
        return email
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'bio', 'phone', 'location']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }