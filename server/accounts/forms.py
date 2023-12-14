from django import forms
from .models import User


class UserCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput, strip=False)
    password2 = forms.CharField(widget=forms.PasswordInput, strip=False)

    class Meta:
        model = User
        fields = ['username', 'cpf', 'email']

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
        user.first_name = self.cleaned_data.get("name")
        user.set_password(self.cleaned_data.get("password1"))

        if commit:
            user.save()
        return user