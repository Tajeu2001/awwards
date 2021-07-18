from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Project,Rating



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic','bio','contact']

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name',]

class PostProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user','design_rating','content_rating','usability_rating']
        widgets = {
            'project_categories': forms.CheckboxSelectMultiple()
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ['overall_score','project','user']

