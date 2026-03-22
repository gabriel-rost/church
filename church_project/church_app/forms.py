from django import forms

from .models.post import Archive, Post
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

# 1. Formulário principal para os dados de texto
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
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

        def clean(self):
            cleaned_data = super().clean()
            text = cleaned_data.get("text")
            title = cleaned_data.get("title")

            # Aqui você pega os arquivos do request
            files = self.files.getlist("attachments")

            if not text and not title and not files:
                raise ValidationError("O post não pode estar vazio.")

            return cleaned_data

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
    
class UserProfileForm(forms.ModelForm):
    # Campo para upload manual (não está no banco de dados)
    avatar_upload = forms.ImageField(required=False, label="Alterar Foto de Perfil")

    class Meta:
        model = User # Agora aponta para o seu Custom User
        fields = ["first_name", "last_name", "email", "bio", "phone", "location", "birth_date"]

    def save(self, commit=True):
        # O 'profile' aqui é, na verdade, a instância do seu Usuário
        user_instance = super().save(commit=False)

        avatar_file = self.cleaned_data.get("avatar_upload")
        if avatar_file:
            # 1. Cria o objeto Archive
            # Supondo que seu model Archive tenha um campo 'file' ou 'archive'
            from .models import Archive 
            archive = Archive.objects.create(file=avatar_file)
            
            # 2. Associa à instância do usuário (não à Classe User)
            user_instance.avatar = archive

        if commit:
            user_instance.save()

        return user_instance


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
    # Campo extra que não vai pro banco, mas controla a lógica do Signal/Service
    send_notification = forms.BooleanField(
        required=False, 
        initial=True,
        label="Notificar igreja ao publicar?",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = ReadingPlan
        # Note que mudei 'draft' para 'is_published' se você seguiu a lógica anterior, 
        # ou mantenha 'draft' se for seu booleano original.
        fields = ['title', 'description', 'is_published', 'send_notification']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control rounded-pill px-4', 
                'placeholder': 'Ex: 21 Dias com os Salmos'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control rounded-4', 
                'rows': 3,
                'placeholder': 'Uma breve introdução sobre esta jornada...'
            }),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }