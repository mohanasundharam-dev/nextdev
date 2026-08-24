from django.forms import ModelForm
from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields=['first_name','email','username','password1','password2']
        labels={
            'first_name':'Name',
        }

class ProfileForm(ModelForm):

    username = forms.CharField(max_length=150)
    skills = forms.MultipleChoiceField(
        required=False,
        choices=(
            ('Python', 'Python'),
            ('JavaScript', 'JavaScript'),
            ('TypeScript', 'TypeScript'),
            ('React', 'React'),
            ('Django', 'Django'),
            ('Node.js', 'Node.js'),
            ('Java', 'Java'),
            ('Spring Boot', 'Spring Boot'),
            ('.NET', '.NET'),
            ('C#', 'C#'),
            ('PHP', 'PHP'),
            ('Laravel', 'Laravel'),
            ('SQL', 'SQL'),
            ('PostgreSQL', 'PostgreSQL'),
            ('Docker', 'Docker'),
            ('Git', 'Git'),
        ),
        widget=forms.SelectMultiple(attrs={'size': 8}),
        help_text='Hold Ctrl or Command to select multiple skills.',
    )
    location = forms.CharField(
        required=False,
        max_length=200,
        label='Location',
        widget=forms.TextInput(attrs={
            'list': 'location-suggestions',
            'placeholder': 'Choose or type your city / region',
            'autocomplete': 'address-level2',
        }),
        help_text='Start typing to choose a suggestion, or enter your own location.',
    )

    class Meta:
        model = Profile
        exclude = ['user','id','created']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['skills'].initial = list(
                Skill.objects.filter(owner=self.instance).values_list('name', flat=True)
            )

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if commit:
            selected_skills = {
                name.strip() for name in self.cleaned_data.get('skills', []) if name.strip()
            }
            Skill.objects.filter(owner=profile).exclude(name__in=selected_skills).delete()
            existing_names = set(
                Skill.objects.filter(owner=profile, name__in=selected_skills)
                .values_list('name', flat=True)
            )
            Skill.objects.bulk_create([
                Skill(owner=profile, name=name)
                for name in selected_skills - existing_names
            ])
        return profile

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exclude(id=self.instance.user.id).exists():
            raise forms.ValidationError("Username already taken")

        return username

class UsernameOrEmailPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        max_length=254,
        label="Username or Email"
    )

    def clean_email(self):
        value = self.cleaned_data["email"]

        # If input is username, convert it to actual email
        try:
            user = User.objects.get(username__iexact=value)
            return user.email
        except User.DoesNotExist:
            return value
        
class UsernameOrEmailAuthenticationForm(AuthenticationForm):

    def clean_username(self):
        username = self.cleaned_data.get("username")

        # If input looks like email
        if "@" in username:
            try:
                user = User.objects.get(email__iexact=username)
                return user.username
            except User.DoesNotExist:
                return username

        return username