from django.core.exceptions import ValidationError
from django.forms import forms, BooleanField, Textarea, PasswordInput, \
    RadioSelect, DateInput, CheckboxInput, TextInput, CheckboxSelectMultiple
from django.forms.fields import EmailField, CharField, ChoiceField, DateField
from django.forms.models import ModelForm

from .models import Post, Comment


class FeedbackForm(forms.Form):  # Оболочка над html-form
    email = EmailField(label='Your E-mail', error_messages={'invalid': 'Input an actual e-mail!'})
    feedback = CharField(label='Your Message', max_length=500)

    def clean_feedback(self):
        feedback = self.cleaned_data.get('feedback')
        if any(word in feedback.split() for word in ['блин', 'ё-моё', 'shit', 'fuuuu']):
            raise ValidationError('No curse words allowed!')
        return feedback


class PostForm(ModelForm):
    terms_of_service = BooleanField(label='Согласен с условиями публикации',
                                    help_text='Нажимая, я даю право свободно распространять данные',
                                    error_messages={'required': 'Для публикации нужно согласиться с условиями обслуживания'})


    class Meta:
        model = Post
        exclude = ['views', 'author']
        widgets = {
            # Использовать большое текстовое поле для content
            'content': Textarea(attrs={'rows': 10, 'class': 'content-editor'}),
            # Использовать радио-кнопки для поля status
            'status': RadioSelect,
            # Использовать чекбоксы для выбора тегов (ManyToMany)
            # 'tags': CheckboxSelectMultiple,
            # Добавить CSS класс к полю title
            'title': TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Текст поста',
            'published': 'Опубликовать?'
        }
        help_texts = {
            'published': 'Если отключено, то пост будет сохранён, как черновик',
            'tags': 'Зажмите Ctrl(Cmd), для выделения нескольких тэгов'
        }
        error_messages = {
            'content': {'required': 'Нельзя создать пустой пост'},
            'title': {'required': 'Укажите название поста', 'max_length': 'Название слишком длинное'},
        }

    def clean_terms_of_service(self):
        if not self.cleaned_data['terms_of_service']:
            raise ValidationError
        del self.cleaned_data['terms_of_service']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

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


# Bootstrap-friendly widgets for generic include rendering
for _field in StyledForm.base_fields.values():
    css_class = _field.widget.attrs.get('class', '')
    if 'form-check-input' not in css_class:
        _field.widget.attrs['class'] = f"{css_class} form-control".strip()
