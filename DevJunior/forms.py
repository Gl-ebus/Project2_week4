from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from DevJunior.models import Application, Company, Vacancy


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        TextAttrib = {'class': 'form-control', 'type': 'text'}
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        labels = {
            'written_username': 'Вас зовут',
            'written_phone': 'Ваш телефон',
            'written_cover_letter': 'Сопроводительное письмо',
        }
        widgets = {
            'written_cover_letter': forms.Textarea(attrs=TextAttrib),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_class = 'col-lg-8'
        self.helper.label_class = 'col-lg-10 pl-3'
        self.helper.add_input(Submit('submit', 'Отправить отлик'))


class EditCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        TextAttrib = {'class': 'form-control', 'type': 'text'}
        fields = ('name', 'logo', 'location', 'description', 'employee_count')
        widgets = {
            'name': forms.TextInput(attrs=TextAttrib),
            'logo': forms.ClearableFileInput(),
            'location': forms.TextInput(attrs=TextAttrib),
            'description': forms.Textarea(attrs=TextAttrib),
            'employee_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Название компании'),
            'logo': _('Логотип'),
            'location': _('География'),
            'description': _('Информация о компании'),
            'employee_count': _('Количество человек в компании'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_class = 'col-lg-8'
        self.helper.label_class = 'col-lg-10 pl-3'
        self.helper.form_class = 'form-group mb-2'
        self.helper.add_input(Submit('submit', 'Сохранить'))


class EditVacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        TextAttrib = {'class': 'form-control', 'type': 'text'}
        fields = ('title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max')
        widgets = {
            'title': forms.TextInput(attrs=TextAttrib),
            'specialty': forms.Select(attrs=TextAttrib),
            'skills': forms.TextInput(attrs=TextAttrib),
            'description': forms.Textarea(attrs=TextAttrib),
            'salary_min': forms.NumberInput(attrs=TextAttrib),
            'salary_max': forms.NumberInput(attrs=TextAttrib),
        }
        labels = {
            'title': _('Название вакансии'),
            'specialty': _('Специализация'),
            'skills': _('Навыки'),
            'description': _('Описание'),
            'salary_min': _('Зарплата от'),
            'salary_max': _('Зарплата до'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_class = 'col-lg-8'
        self.helper.label_class = 'col-lg-10 pl-3'
        self.helper.form_class = 'form-group mb-2'
        self.helper.add_input(Submit('submit', 'Сохранить'))


# Forms by REGISTRATION and LOGIN
class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label=_('Ваше имя'),
        widget=(forms.TextInput(attrs={'class': 'form-control'}))
    )
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=(forms.PasswordInput(attrs={'class': 'form-control'}))
    )
    password2 = forms.CharField(
        label=_('Подтвердите пароль'),
        widget=(forms.PasswordInput(attrs={'class': 'form-control'}))
    )

    class Meta:
        model = User
        TextAttrib = {'class': 'form-control', 'type': 'text'}
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Создать аккаунт'))
        self.helper.label_class = 'col-lg-10'
        self.helper.field_class = 'col-lg-15'
        self.helper.form_class = 'form-group mb-3'


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Ваше имя'),
        widget=(forms.TextInput(attrs={'class': 'form-control'}))
    )
    password = forms.CharField(
        label=_('Пароль'),
        widget=(forms.PasswordInput(attrs={'class': 'form-control'}))
    )

    class Meta:
        model = User
        TextAttrib = {'class': 'form-control', 'type': 'text'}
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-lg-12 text-center'
        self.helper.field_class = 'col-lg-15'
