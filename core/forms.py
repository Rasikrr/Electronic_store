from django.forms import ModelForm, PasswordInput
from .models import CustomUser
from django.contrib.auth.hashers import make_password, check_password
from django import forms


class SignupForm(ModelForm):
    policy = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "password_2")

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            if key in ("password", "password_2"):
                self.fields[key].widget = PasswordInput()
            if key == "password_2":
                self.fields[key].widget.attrs["placeholder"] = f"Confirm password"
            else:
                self.fields[key].widget.attrs["placeholder"] = f"enter your {key}"

    def clean(self):
        clean_data = super().clean()
        unique_email = CustomUser.objects.filter(email=clean_data.get("email")).exists()
        unique_username = CustomUser.objects.filter(username=clean_data.get("username")).exists()
        policy = clean_data.get("policy")
        password_1 = clean_data.get("password")
        password_2 = clean_data.get("password_2")
        if password_1 != password_2:
            self.add_error("password_2", "Passwords are not similar")
        if not policy:
            self.add_error("policy", "Please accept policy")
        if unique_email:
            self.add_error("email", "User with this email is exists")
        if unique_username:
            self.add_error("username", "User with this username is exists")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        user.password_2 = make_password(self.cleaned_data["password_2"])
        if commit:
            user.save()
        return user