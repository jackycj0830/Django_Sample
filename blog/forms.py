from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """評論表單"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '請輸入您的評論...',
                'required': True,
            }),
        }
        labels = {
            'content': '評論內容',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'rows': 4,
            'placeholder': '請輸入您的評論...',
        })
