from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput
from django import forms
from .models import AlgoUser, Profile
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = AlgoUser
        fields = UserCreationForm.Meta.fields + ('email', 'user_level')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

        self.fields['username'].widget.attrs.update({
            'class': 'border rounded-lg p-1 transition-shadow shadow-md hover:shadow-lg',
            'placeholder': 'e.g. tourist'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'border rounded-lg p-1 transition-shadow shadow-md hover:shadow-lg',
            'placeholder': 'e.g. user@gmail.com'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'border rounded-lg p-1 transition-shadow shadow-md hover:shadow-lg'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'border rounded-lg p-1 transition-shadow shadow-md hover:shadow-lg'
        })

        for field in self.fields.values():
            field.help_text = None

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = AlgoUser
        fields = ['username', 'email', 'github_username', 'codeforces_username', 'leetcode_username']

        labels = {
            'github_username': 'Github Username',
            'codeforces_username': 'Codeforces Username',
            'leetcode_username': 'LeetCode Username'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'bg-yellow-100 border-2 border-yellow-300 pl-2 mt-1'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'bg-yellow-100 border-2 border-yellow-300 pl-2 mt-1'
        })
        
        self.fields['github_username'].widget.attrs.update({
            'class': 'bg-yellow-100 border-2 border-yellow-300 pl-2 mt-1'
        })

        self.fields['codeforces_username'].widget.attrs.update({
            'class': 'bg-yellow-100 border-2 border-yellow-300 pl-2 mt-1'
        })

        self.fields['leetcode_username'].widget.attrs.update({
            'class': 'bg-yellow-100 border-2 border-yellow-300 pl-2 mt-1'
        })

        for field in self.fields.values():
            field.help_text = None


class ProfilePicStyling(ClearableFileInput):
    initial_text = mark_safe('<span class="text-gray-500 font-semibold">Current</span>')
    input_text = mark_safe('<span class="text-gray-500 font-semibold">Change</span>')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']

        labels = {'profile_pic': 'Profile Picture'}
        widgets = {'profile_pic': ProfilePicStyling()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['bio'].widget.attrs.update({
            'class': 'bg-yellow-100 border-2 border-yellow-300 pl-2 mt-1'
        })

        self.fields['profile_pic'].widget.attrs.update({
            'class': (
                'mt-5 text-cyan-600 file:bg-blue-200 file:rounded-full file:py-1 file:px-3 '
                'file:font-semibold file:mr-3 file:cursor-pointer file:border-2 file:border-sky-400 '
                'file:transition file:hover:bg-sky-200 file:hover:text-cyan-700 '
            )
        })

        
    