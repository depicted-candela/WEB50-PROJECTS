from django.forms import ModelForm, ValidationError
from .models import Post

MAX_LENGTH_TWEET = 240

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['text', 'image']
        labels = {
            'text': '',
            'image': ''
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['rows'] = 8
    
    def validate(self):
        text = self.cleaned_data.get('text')
        if len(text) > MAX_LENGTH_TWEET:
            raise ValidationError("You must resume your ideas in 240 characters")
        else:
            return text
