from django import forms
from .models import Post

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



