from django import forms

from .models.post import Archive, Content
from .models import Profile
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
    avatar_upload = forms.FileField(required=False)

    class Meta:
        model = Profile
        fields = ["bio", "phone", "location", "birth_date"]

    def save(self, commit=True):
        profile = super().save(commit=False)

        avatar_file = self.cleaned_data.get("avatar_upload")
        if avatar_file:
            archive = Archive.objects.create(file=avatar_file)
            profile.avatar = archive

        if commit:
            profile.save()

        return profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

from django import forms
from church_app.models.bible.book import Book, Chapter
from .models import PlanTask

class PlanTaskForm(forms.ModelForm):
    # Campos extras para definir o intervalo de capítulos
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label="Livro", widget=forms.Select(attrs={'class': 'form-select'}))
    start_chapter = forms.IntegerField(label="Capítulo Inicial", widget=forms.NumberInput(attrs={'class': 'form-select'}))
    end_chapter = forms.IntegerField(label="Capítulo Final", widget=forms.NumberInput(attrs={'class': 'form-select'}))

    start_verse = forms.IntegerField(
        label="Versículo Inicial",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    end_verse = forms.IntegerField(
        label="Versículo Final",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PlanTask
        fields = ['week_number', 'day_number']
        widgets = {
            'week_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1'}),
            'day_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1'}),
        }
    
    def clean(self):
        cleaned = super().clean()

        sc = cleaned.get('start_chapter')
        ec = cleaned.get('end_chapter')
        sv = cleaned.get('start_verse')
        ev = cleaned.get('end_verse')

        # Versículos só podem existir em um único capítulo
        if sv or ev:
            if ec and ec != sc:
                raise forms.ValidationError(
                    "Versículos só podem ser definidos para um único capítulo."
                )

            if not sv or not ev:
                raise forms.ValidationError(
                    "Informe o versículo inicial e final."
                )

            if sv > ev:
                raise forms.ValidationError(
                    "Versículo inicial não pode ser maior que o final."
                )

        # Se não informou capítulo final
        if not ec:
            cleaned['end_chapter'] = sc

        return cleaned


from .models.bible.plantask import ReadingPlan
class ReadingPlanForm(forms.ModelForm):
    class Meta:
        model = ReadingPlan
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 21 Dias com os Salmos'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }