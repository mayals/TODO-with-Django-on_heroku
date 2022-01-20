from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from . models import Profile
from django.views.generic import DetailView


# https: // docs.djangoproject.com/en/3.2/topics/auth/customizing/
class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        label='Username', max_length=15, help_text='space not allowed in username')
    first_name = forms.CharField(label='First Name',required=True)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput(), min_length=8)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2',)



    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('ops! there is another user took this username.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    def save(self,commit=True,user=None):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user





# --------------UserUpdateForm----------------------
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name',required=False )
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')



# --------------ProfileUpdateForm----------------------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('P_image',)





# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/
# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     disabled password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name',
#                   'email', 'password')
