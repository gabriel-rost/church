from django.forms import ModelForm
from church_app.models import *

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "profile_icon", "born_date", "login"]