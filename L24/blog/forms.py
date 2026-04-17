from django.core.exceptions import ValidationError
from django.forms import forms, BooleanField, Textarea, PasswordInput, \
    RadioSelect, DateInput, CheckboxInput, TextInput, CheckboxSelectMultiple
from django.forms.fields import EmailField, CharField, ChoiceField, DateField
from django.forms.models import ModelForm

from .models import Post, Comment


class FeedbackForm(forms.Form):
    email = EmailField(label='Your E-mail', error_messages={'invalid': 'Input an actual e-mail!'})
    feedback = CharField(label='Your Message', max_length=500)

    def clean_feedback(self):
        feedback = self.cleaned_data.get('feedback')
        if any(word in feedback.split() for word in ['shit', 'fuuuu']):
            raise ValidationError('No curse words allowed!')
        return feedback


class PostForm(ModelForm):
    terms_of_service = BooleanField(
        label='Agree to publication terms',
        help_text='By submitting, you allow this content to be published.',
        error_messages={'required': 'You must accept the publication terms.'}
    )

    class Meta:
        model = Post
        exclude = ['views', 'author']
        widgets = {
            'content': Textarea(attrs={'rows': 10, 'class': 'content-editor'}),
            'title': TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'content': 'Post content',
            'published': 'Publish?'
        }
        help_texts = {
            'published': 'If disabled, the post will be saved as a draft.',
            'tags': 'Use Ctrl/Cmd to select multiple tags.'
        }
        error_messages = {
            'content': {'required': 'Post content is required.'},
            'title': {'required': 'Post title is required.', 'max_length': 'Title is too long.'},
        }

    def clean_terms_of_service(self):
        if not self.cleaned_data['terms_of_service']:
            raise ValidationError
        return self.cleaned_data['terms_of_service']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class ExampleForm(forms.Form):
    description = CharField(widget=Textarea)
    password = CharField(widget=PasswordInput)
    COLOR_CHOICES = [('R', 'Red'), ('G', 'Green'), ('B', 'Blue')]
    color = ChoiceField(choices=COLOR_CHOICES, widget=RadioSelect)
    event_date = DateField(widget=DateInput(attrs={'type': 'date', 'style': 'background-color:red'}))


class StyledForm(forms.Form):
    name = CharField(
        label="Name",
        widget=TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your full name'
        })
    )
    message = CharField(
        label="Message",
        widget=Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'cols': 40
        })
    )
    agree = BooleanField(
        label="I agree to the terms",
        widget=CheckboxInput(attrs={'class': 'form-check-input'})
    )


for _field in StyledForm.base_fields.values():
    css_class = _field.widget.attrs.get('class', '')
    if 'form-check-input' not in css_class:
        _field.widget.attrs['class'] = f"{css_class} form-control".strip()
