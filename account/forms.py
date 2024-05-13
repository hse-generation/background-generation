from account.models import Users
from django.forms import ModelForm, TextInput, Textarea, PasswordInput, DateInput, DateTimeInput, EmailInput, \
    ImageField, forms, FileInput, NumberInput


class AccountForm(ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'client_id',  'email', 'profile_picture', 'api_key']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя',
                'name': 'name',
            }),
            'client_id': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ID клиента',
                'name': 'client_id'
            }),
            'api_key': TextInput(attrs={
                'class': 'form-control',
                'name': 'api_key',
                'placeholder': 'Введите ключ',
                'type': "password"
            }),

            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите почту',
                'name': 'email',
            }),
            'profile_picture': FileInput(attrs={
                'class': 'form-control',
            })
        }
