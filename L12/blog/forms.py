from django.core.exceptions import ValidationError
from django.forms import forms, BooleanField, Textarea, PasswordInput, \
    RadioSelect, DateInput, CheckboxInput, TextInput
from django.forms.fields import EmailField, CharField, ChoiceField, DateField


class FeedbackForm(forms.Form):  # Оболочка над html-form
    email = EmailField(label='Your E-mail', error_messages={'invalid': 'Input an actual e-mail!'})
    feedback = CharField(label='Your Message', max_length=500)

    def clean_feedback(self):
        feedback = self.cleaned_data.get('feedback')
        if any(word in feedback.split() for word in ['блин', 'ё-моё', 'shit', 'fuuuu']):
            raise ValidationError('No curse words allowed!')
        return feedback


class PostForm(forms.Form):
    title = CharField(label='Title of your post', max_length=255)
    content = CharField(label='Your post content')
    published = BooleanField(label='Publish post', initial=True, help_text='If not checked, the post goes to drafts')
    # tags = ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=CheckboxSelectMultiple,  # Or forms.SelectMultiple
    #     required=False,
    # )


class ExampleForm(forms.Form):
    # Использовать многострочное поле вместо однострочного
    description = CharField(widget=Textarea)
    # Использовать поле для пароля (скрывает ввод)
    password = CharField(widget=PasswordInput)
    # Использовать радио-кнопки вместо выпадающего списка
    COLOR_CHOICES = [('R', 'Red'), ('G', 'Green'), ('B', 'Blue')]
    color = ChoiceField(choices=COLOR_CHOICES, widget=RadioSelect)
    # Использовать поле для даты с HTML5 виджетом
    event_date = DateField(widget=DateInput(attrs={'type': 'date', 'style': 'background-color:red'}))


class StyledForm(forms.Form):
    name = CharField(
        label="Имя",
        widget=TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Введите ваше полное имя'
        })
    )
    message = CharField(
        label="Сообщение",
        widget=Textarea(attrs={
            'class': 'form-control',
            'rows': 5,  # Устанавливаем количество строк
            'cols': 40  # Устанавливаем количество колонок
        })
    )
    agree = BooleanField(
        label="Согласен с условиями",
        widget=CheckboxInput(attrs={'class': 'form-check-input'})
    )
