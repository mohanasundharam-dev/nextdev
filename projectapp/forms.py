from django import forms
from django.forms import ModelForm
from .models import Movie, Tag

class ProjectForm(ModelForm):
    custom_technology = forms.CharField(
        required=False,
        label='Add another technology',
        help_text='Enter one or more technologies separated by commas.',
        widget=forms.TextInput(attrs={
            'placeholder': 'For example: React Native, FastAPI'
        })
    )

    class Meta:
        model = Movie
        fields = ('title', 'desc', 'technology', 'custom_technology', 'demo_link', 'source_link', 'image_path')
        labels = {
            'title': 'Project title',
            'desc': 'Description',
            'technology': 'Technologies',
            'demo_link': 'Live demo URL',
            'source_link': 'Source code URL',
            'image_path': 'Project image',
        }
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 6}),
            'technology': forms.SelectMultiple(attrs={'size': 6}),
            'demo_link': forms.URLInput(),
            'source_link': forms.URLInput(),
        }

    def save(self, commit=True):
        project = super().save(commit=commit)
        if commit:
            names = {
                name.strip() for name in self.cleaned_data.get('custom_technology', '').split(',')
                if name.strip()
            }
            if names:
                project.technology.add(*[Tag.objects.get_or_create(name=name)[0] for name in names])
        return project