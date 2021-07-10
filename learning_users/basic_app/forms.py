from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from basic_app.models import UserProfileInfo, Object

class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        fields = ('username', 'email', 'password1','password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["username"].label = "Display name"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm password"

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')

class ObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('category','colour','description','price', 'image', 'size')

# Old code

# from django import forms
# from django.contrib.auth.models import User
# from basic_app.models import UserProfileInfo
#
# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#
#     class Meta():
#         model = User
#         fields = ('username', 'email', 'password')
#
#
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')
