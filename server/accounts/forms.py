from django.core.validators import MaxLengthValidator
from django import forms

from .models import User, OrganizerRequest


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, strip=False, label="Senha")
    password2 = forms.CharField(
        widget=forms.PasswordInput, strip=False, label="Repita sua senha"
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "cpf", "email"]
        labels = {"first_name": "Nome", "last_name": "Sobrenome"}
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "col-lg-6"}),
            "last_name": forms.TextInput(attrs={"class": "col-lg-6"}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            self.add_error("password2", "As senhas devem ser iguais")

    def save(self, commit=True):
        cpf = self.cleaned_data.get("cpf")

        try:
            user = User.objects.get(cpf=cpf)
        except:
            user = User(cpf=cpf)
        user.username = self.cleaned_data.get("username")
        user.email = self.cleaned_data.get("email")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.set_password(self.cleaned_data.get("password1"))

        if commit:
            user.save()
        return user

class OrganizerRequestForm(forms.ModelForm):
    reason = forms.CharField(
        max_length=1000,
        label='Conte-nos por que você deve ser um organizador.',
        widget=forms.Textarea(attrs={'rows': 5}),
        validators=[MaxLengthValidator(limit_value=1000, message='Exceeds maximum length of 1000 characters.')]
    )

    class Meta:
        model = OrganizerRequest
        fields = ['reason']