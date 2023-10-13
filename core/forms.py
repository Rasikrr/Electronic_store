from django.forms import ModelForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")

    def __init__(self,*args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs['placeholder'] = "enter your username"
        self.fields["email"].widget.attrs['placeholder'] = "enter your email"
        self.fields["password"].widget.attrs['placeholder'] = "enter your password"


