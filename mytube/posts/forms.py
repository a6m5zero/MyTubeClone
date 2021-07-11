from django import forms
from django.forms import ModelForm, fields , Form
from django.http import request
from .models import Post


# class PostForm(ModelForm):
#     class Meta:
#         model = Post
#         fields = ['pub_date', 'text', ]

class ContactForm(Form):
    subject = forms.CharField(label='Тема обращения:',max_length=100)
    message = forms.CharField(label='Сообщение:', widget=forms.Textarea)
    sender = forms.EmailField(label='E-mail для обратной связи:')
    # cc_myself = forms.BooleanField(required=False)
    
    #Method to validate subject field in form 
    def clean_subject(self):
        data = self.cleaned_data['subject']
        # If user do not say "Spasibo" to admin - raise ValidationError
        if "спасибо" not in data.lower():
            raise forms.ValidationError("Вы должны написать \'спасибо' в тексте перед обращением.")
        return data


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['groups', 'text', ]
        
    def __init__(self , *args, **kwargs):
        self.author = kwargs.pop('author')
        super(AddPostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AddPostForm, self).save(commit=False)
        instance.author = self.author
        if commit:
            instance.save()
            self.save_m2m()
        return instance


