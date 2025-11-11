from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Author

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published', "comments", "image"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Write your post...'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Add comments...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            # 'author': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'published': 'Draft',
        }
    
    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if len(title) < 5:
    #         raise forms.ValidationError("Title must be at least 5 characters.")
    #     return title

    # def clean_content(self):
    #     content = self.cleaned_data.get('content')
    #     if len(content.split()) < 5:
    #         raise forms.ValidationError("Content must be at least 20 words.")
    #     return content

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Author
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

