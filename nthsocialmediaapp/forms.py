from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'body'
        )

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'body'
        )

class UserLoginForm(forms.Form):
    username = forms.CharField( label = '')
    password = forms.CharField( label= '', widget = forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                    'placeholder': 'password'
            }
        )
    )
    confirm_password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                    'placeholder': 'confirm password'
            }
        )

    )
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords Not Matched")
        else:
            return confirm_password



