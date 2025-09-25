from django.forms import ModelForm
from church_app.models import *

from django.contrib.auth.forms import UserCreationForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "profile_icon", "born_date", "login"]

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "profile_icon", "born_date", "login")